DEFAULT_MAPLE_PATH ='/Library/Frameworks/Maple.framework/Versions/17/bin/maple'

import sys
import subprocess
import random
import time
import threading
import Queue

###
# Adapted from by:
# http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading
#####

class AsynchronousFileReader(threading.Thread):
  '''
  Helper class to implement asynchronous reading of a file
  in a separate thread. Pushes read lines on a queue to
  be consumed in another thread.
  '''
  
  def __init__(self, fd, queue, callback = None):
    assert isinstance(queue, Queue.Queue)
    assert callable(fd.readline)
    threading.Thread.__init__(self)
    self._fd = fd
    self._queue = queue
    self._callback = callback
  
  def run(self):
    '''The body of the tread: read lines and put them on the queue.'''
    for line in iter(self._fd.readline, ''):
      self._queue.put(line)
      if self._callback:
        self._callback(line)
  
  def eof(self):
    '''Check whether there is no more content to expect.'''
    return not self.is_alive() and self._queue.empty()


class ShellSession(object):
  
  def __init__(self, cmd, lines = None, continue_read = None, no_wait = False):
    self.continue_read = continue_read
    if not continue_read:
      self.continue_read = self.__default_continue_read
      
    self.no_wait = no_wait

    # initialize process
    self.process = subprocess.Popen(cmd,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE,
                                    stdin  = subprocess.PIPE)
    
    self.stdout_queue = Queue.Queue()
    self.stdout_reader = AsynchronousFileReader(self.process.stdout,
                                                self.stdout_queue)
    self.stdout_reader.start()
    
    self.stderr_queue = Queue.Queue()
    self.stderr_reader = AsynchronousFileReader(self.process.stderr,
                                                self.stderr_queue,
                                                callback = self.__default_stderr)
    self.stderr_reader.start()
    
    if lines:
      if type(lines) is str or type(lines) is unicode:
        lines = lines.strip().split()
      
      for line in lines:
        self.writeline(lines)
        
  def __enter__(self):
    return self
  
  def __exit__(self, type, value, tb):
    self.__del__()
    
  def __del__(self):
    try:
      self.close()
    except:
      pass
  
  def __default_stderr(self, line):
    raise Exception("stderr: %s" % line)
  
  def writeline(self, cmd):
    self.process.stdin.write(cmd)
    self.process.stdin.write("\n")
    self.process.stdin.flush()
    
  def __default_continue_read(self, buff, line):
    if line and line.strip() != "":
      newbuff = buff[:]
      newbuff.append(line)
      return (False, newbuff, line)
    
    return (True, buff, line)
    
  def readlines(self, timeout = -1):
    self.result = []
    start = time.time()
    
    while not self.stdout_reader.eof() and (
        timeout == -1 or (time.time() - start < timeout)):
      while not self.stdout_queue.empty():
        line = self.stdout_queue.get()

        # if not handling function, simply return the line
        if not self.continue_read:
          self.result = [line]
          return self.result
        
        (stop, self.result, line) = self.continue_read(self.result, line)
        if stop:
          return self.result
        
      # wait to look for more line
      if not self.no_wait:
        time.sleep(.1)
      
    return self.result
  
  def run(self, cmd, timeout = -1):
    '''Run a command in the shell, then wait and return result as a buffer of
    lines.

    '''
    self.writeline(cmd)
    return self.readlines(timeout = timeout)
  
  def close(self):
    '''Close the shell session.'''
    self.process.kill()
    
    # Let's be tidy and join the threads we've started.
    self.stdout_reader.join()
    self.stderr_reader.join()
 
    # Close subprocess' file descriptors.
    self.process.stdout.close()
    self.process.stderr.close()


class MapleSession(ShellSession):
  
  def __init__(self, lines = [], maple_path = None):
    '''Initialize a Maple session; lines may contain initialization commands.

    '''
    self.maple_path = maple_path
    if not self.maple_path:
      self.maple_path = DEFAULT_MAPLE_PATH

    # option -q : for quiet
    # option -c <cmd> : to run <cmd> on startup
    # 'interface(prettyprint=0)' : set maple's output to 1-D math
    
    super(MapleSession, self).__init__(cmd = [self.maple_path, "-q", "-c",
                                              "'interface(prettyprint=0)'"],
                                       lines = None,
                                       continue_read = self.__maple_continue_read,
                                       no_wait = True)

    # double-check that 1-D math is set
    self.run("interface(prettyprint=0);")
    
    # run the initialization lines here (rather than in the parent)
    # only after the pretty printing has been set to 1-D math
    if lines:
      if type(lines) is str or type(lines) is unicode:
        lines = lines.strip().split()
      
      for line in lines:
        self.run(line)
  
  def close(self):
    '''Close the Maple session.'''
    self.writeline("quit();")
    time.sleep(.2)
    super(MapleSession, self).close()
    
  def run(self, cmd, timeout = -1):
    '''Run Maple command in the current session, and return the resulting
    output in 1-D math notation, or None.

    '''
    # Try to see if this command should have output;
    # if it doesn't then force to a non-infinity time-out
    if timeout == -1:
      if cmd.strip()[-1] != ";":
        timeout = 5
      
    # results are one line only in 1-D math
    lines = super(MapleSession, self).run(cmd, timeout = timeout)
    if len(lines) == 0:
      return None
    assert(len(lines) == 1)
    return lines[0]
    
  def __maple_continue_read(self, buff, line):
    # return (stop, newbuff, newline)
    # - buff is the lines read up until now
    # - line is the new line
    #
    newline = line.strip()
    
    # code to handle errors (that span several lines)
    # FIXME: make more robust
    if newline.find("syntax error") != -1 or (
        len(buff) > 0 and buff[0].find("syntax error") != -1):
      newbuff = buff[:]
      newbuff.append(line)
      if newline != '^':
        return (False, newbuff, line)
      else:
        # end of error
        # FIXME: we don't know how to recover from these
        # (i.e., the subprocess is unresponsive)
        try:
          self.close()
        except:
          pass
        raise Exception("Error with Maple: %s" % "".join(newbuff))
        
        # return (True, [ "".join(newbuff) ], line)
      
    # default case
    return (True, [newline], newline)


def test_maple_session():
  with MapleSession() as m:
    assert(m.run("4+5;") == "9")
    assert(m.run("x^3;") == "x^3")
    assert(m.run("4+5:") == None)
  print "Test for MapleSession successful!"
