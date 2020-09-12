#!/usr/bin/python3

from sh import git
import subprocess
import time
from datetime import datetime


class ScriptManager:
    def __init__(self):
        self.proc = None
        self.f = None
        self.num_crash = 0

    def start_worker(self, reset=False):
        if reset:
            self.num_crash = 0
        if self.num_crash > 3:
            print('Crashed too many times. Starting in debug mode.')
            self.proc = subprocess.Popen(['python3', 'bot.py', 'DEBUG'])
            return

        self.f = open('log.txt', 'w')
        # self.proc = subprocess.Popen(['node', 'main.js'], stdout=self.f, stderr=subprocess.PIPE)
        self.proc = subprocess.Popen(['python3', 'bot.py'],
                                     stdout=self.f, stderr=subprocess.PIPE)

    def check_worker_failed(self) -> bool:
        if self.proc is None:
            return True
        self.proc.poll()
        if self.proc.returncode is not None:
            _, errs = self.proc.communicate()
            if len(errs) != 0:
                print('The bot has crashed! See logerr.txt for more details.')
                self.num_crash += 1
                with open('logerr.txt', 'wb') as f:
                    dt = datetime.now()
                    outstr = 'Crash at time {}\n'.format(
                        dt.strftime('%b %d, %H:%M:%S')
                    )
                    f.write(outstr.encode('utf-8'))
                    f.write(errs)
            self.proc = None
            return True
        return False

    def kill_worker(self):
        if self.proc is not None:
            self.proc.terminate()
        self.proc = None


def check_git_has_update(verbose=False) -> bool:
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


if __name__ == '__main__':
    check_period = 5
    crash_count = 0
    sm = ScriptManager()

    print('Entering manager script. Checking git status every {} s.'.format(check_period))
    sm.start_worker()

    while True:
        time.sleep(check_period)

        if check_git_has_update():
            print('Update detected. Pulling.')
            sm.kill_worker()
            git('pull')
            sm.start_worker(reset=True)
            continue

        if sm.check_worker_failed():
            sm.start_worker()
            continue
