##############################################################################
#
# Copyright (c) 2011 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
import os
import psutil
import re
import subprocess
import threading
import signal
import sys
import time
from . import logger

MAX_TIMEOUT = 3600 * 4

class SubprocessError(EnvironmentError):
  def __init__(self, status_dict):
    self.status_dict = status_dict
  def __getattr__(self, name):
    return self.status_dict[name]
  def __str__(self):
    return 'Error %i' % self.status_code

class TimeoutError(EnvironmentError):
  def __init__(self):
    pass
  def __str__(self):
    return 'Timeout expired. Process killed'

class CancellationError(EnvironmentError):
  pass

_format_command_search = re.compile("[[\\s $({?*\\`#~';<>&|]").search
_format_command_escape = lambda s: "'%s'" % r"'\''".join(s.split("'"))

def format_command(*args, **kw):
  cmdline = []
  for k, v in sorted(kw.items()):
    if _format_command_search(v):
      v = _format_command_escape(v)
    cmdline.append('%s=%s' % (k, v))
  for v in args:
    if _format_command_search(v):
      v = _format_command_escape(v)
    cmdline.append(v)
  return ' '.join(cmdline)

def subprocess_capture(p, log_prefix, get_output=True):
  log = logger.info
  if log_prefix:
    log_prefix += ': '
  def readerthread(input, buffer):
    while True:
      data = input.readline()
      if not data:
        break
      if get_output:
        buffer.append(data)
      log(log_prefix + data.rstrip('\n'))
  if p.stdout:
    stdout = []
    stdout_thread = threading.Thread(target=readerthread,
                                     args=(p.stdout, stdout))
    stdout_thread.daemon = True
    stdout_thread.start()
  if p.stderr:
    stderr = []
    stderr_thread = threading.Thread(target=readerthread,
                                     args=(p.stderr, stderr))
    stderr_thread.daemon = True
    stderr_thread.start()
  p.wait()
  if p.stdout:
    stdout_thread.join()
  if p.stderr:
    stderr_thread.join()
  return (p.stdout and ''.join(stdout),
          p.stderr and ''.join(stderr))

def killCommand(pid):
  """
  To prevent processes from reacting to the KILL of other processes,
  we STOP them all first, and we repeat until the list of children does not
  change anymore. Only then, we KILL them all.
  """
  try:
    process = psutil.Process(pid)
    process.suspend()
  except psutil.Error, e:
    return
  process_list = [process]
  new_list = process.children(recursive=True)
  while new_list:
    process_list += new_list
    for child in new_list:
      try:
        child.suspend()
      except psutil.Error, e:
        logger.debug("killCommand/suspend: %s", e)
    time.sleep(1)
    new_list = set(process.children(recursive=True)).difference(process_list)
  for process in process_list:
    try:
      process.kill()
    except psutil.Error, e:
      logger.debug("killCommand/kill: %s", e)

class ProcessManager(object):

  stdin = file(os.devnull)

  def __init__(self, max_timeout=MAX_TIMEOUT):
    self.process_pid_set = set()
    signal.signal(signal.SIGTERM, self.sigterm_handler)
    self.under_cancellation = False
    self.p = None
    self.result = None
    self.max_timeout = max_timeout
    self.timer_set = set()

  def spawn(self, *args, **kw):
    def timeoutExpired(p):
      if p.poll() is None:
        logger.warning('PROCESS TOO LONG OR DEAD, GOING TO BE TERMINATED')
        killCommand(p.pid)
        raise SubprocessError('Dead or too long process killed')

    if self.under_cancellation:
      raise CancellationError("Test Result was cancelled")
    get_output = kw.pop('get_output', True)
    log_prefix = kw.pop('log_prefix', '')
    new_session = kw.pop('new_session', True)
    subprocess_kw = {}
    cwd = kw.pop('cwd', None)
    if cwd:
      subprocess_kw['cwd'] = cwd
    if new_session:
      subprocess_kw['preexec_fn'] = os.setsid
    raise_error_if_fail = kw.pop('raise_error_if_fail', True)
    env = dict(os.environ, **kw) if kw else None
    command = format_command(*args, **kw)
    logger.info('subprocess_kw : %r', subprocess_kw)
    logger.info('$ %s', command)
    sys.stdout.flush()
    p = subprocess.Popen(args, stdin=self.stdin, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=env, **subprocess_kw)
    self.process_pid_set.add(p.pid)
    timer = threading.Timer(self.max_timeout, timeoutExpired, args=(p,))
    self.timer_set.add(timer)
    timer.start()
    stdout, stderr = subprocess_capture(p, log_prefix, get_output=get_output)
    timer.cancel()
    self.timer_set.discard(timer)
    result = dict(status_code=p.returncode, command=command,
                  stdout=stdout, stderr=stderr)
    self.process_pid_set.discard(p.pid)
    if self.under_cancellation:
      raise CancellationError("Test Result was cancelled")
    if raise_error_if_fail and p.returncode:
      raise SubprocessError(result)
    return result

  def getSupportedParameterList(self, program_path):
    return re.findall(r'^  (--\w+)',
      self.spawn(program_path, '--help')['stdout'], re.M)

  def killall(self, name):
    """
    Kill processes of given name, only if they're orphan or subprocesses of
    the testnode.
    """
    to_kill_list = []
    pid = os.getpid()
    for process in psutil.process_iter():
      try:
        if process.name() != name:
          continue
        p = process.parent()
        if p is not None:
          while p is not None:
            if p.pid == pid:
              break
            p = p.parent()
          else:
            continue
      except (psutil.AccessDenied, psutil.NoSuchProcess):
        continue
      logger.debug('ProcesssManager, killall on %s having pid %s',
               name, process.pid)
      to_kill_list.append(process.pid)
    for pid in to_kill_list:
      killCommand(pid)

  def killPreviousRun(self, cancellation=False):
    logger.debug('ProcessManager killPreviousRun, going to kill %r',
             self.process_pid_set)
    if cancellation:
      self.under_cancellation = True
    for timer in self.timer_set:
      timer.cancel()
    for pgpid in self.process_pid_set:
      killCommand(pgpid)
    try:
      pid_file = self.supervisord_pid_file
    except AttributeError:
      pass
    else:
      del self.supervisord_pid_file
      try:
        if os.path.exists(pid_file):
          with open(pid_file) as f:
            pid = int(f.read().strip())
          logger.debug('ProcessManager killPreviousRun,'
                       ' going to kill supervisor with pid %r', pid)
          os.kill(pid, signal.SIGTERM)
      except Exception:
        logger.exception(
          'ProcessManager killPreviousRun, exception when killing supervisor')
    self.process_pid_set.clear()

  def sigterm_handler(self, signal, frame):
    logger.debug('SIGTERM_HANDLER')
    sys.exit(1)