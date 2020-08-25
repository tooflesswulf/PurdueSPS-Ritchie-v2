#!/usr/bin/python3

from sh import git
import time

def check_git_update(verbose = False):
    p = git('fetch', 'origin', 'master')

    if (verbose):
      print('Fetch complete')
      print(p)
    
    status = git("status")
    if verbose:
        print(status)

    return 'branch is up to date' in status


if __name__ == '__main__':
    check_period = 5

    print('Entering manager script. Checking git status every %d s.'.format(check_period))

    while True:
        if check_git_update():
            time.sleep(check_period)
        else:
            print('Update detected. Pulling.')
            git('pull')

