#!/usr/bin/python3

from sh import git
import subprocess
import time
from datetime import datetime

def check_git_has_update(verbose = False):
    try:
        p = git('fetch', 'origin', 'master')
    except:
        return False

    if (verbose):
      print('Fetch complete')
      print(p)

    status = git("status")
    if verbose:
        print(status)

    return 'branch is up to date' not in status

def start_worker():
    f = open('log.txt', 'w')
    proc = subprocess.Popen(['node', 'main.js'], stdout=f, stderr=subprocess.PIPE)
    return f, proc

def check_worker(proc):
    proc.poll()
    if proc.returncode is not None:
        _, errs = proc.communicate()
        if len(errs) != 0:
            print('The bot has crashed!')
            with open('logerr.txt', 'wb') as f:
                dt = datetime.now()
                outstr = 'Crash at time {}\n'.format(dt.strftime('%b %d, %H:%M:%S'))
                f.write(outstr.encode('utf-8'))
                f.write(errs)
        return True
    return False


if __name__ == '__main__':
    check_period = 5
    crash_count = 0

    print('Entering manager script. Checking git status every {} s.'.format(check_period))
    f, proc = start_worker()

    while True:
        time.sleep(check_period)

        if crash_count < 3:
            finish = check_worker(proc)
            if finish:
                print('Worker has crashed. See logerr.txt for details.')
                f, proc = start_worker()
                crash_count += 1
                continue

        if check_git_has_update():
            print('Update detected. Pulling.')
            if not finish: proc.terminate()
            #check_worker(proc)
            git('pull')
            f, proc = start_worker()
            crash_count = 0


