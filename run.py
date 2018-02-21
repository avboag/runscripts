#!/usr/bin/env python3

import argparse
import glob
import os
import shutil
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description = 'Run planned runs.')
parser.add_argument('--sleep_time', type=float, default = 1.)
parser.add_argument('--max_num_active_processes', type=int, default = 1)
parser.add_argument('--executor', default = 'nohup')
parser.add_argument('--preamble')
parser.add_argument('executable')
args = parser.parse_args()

sleep_time = args.sleep_time
max_num_active_processes = args.max_num_active_processes
executor = args.executor
executable = args.executable

executable = executable.split()
executable[0] = os.path.abspath(executable[0])
executable = ' '.join(executable)

if args.preamble is None:
    preamble = ''
else:
    with open(args.preamble, 'r') as f:
        preamble = f.read()

def count_running():
    return len(glob.glob('**/queued', recursive = True)) + len(glob.glob('**/running', recursive = True))

script = """\
#!/usr/bin/env bash

{preamble}

mv queued running

{executable} > out 2> error

rm running
""".format(**globals())

with open('script', 'w') as f:
    f.write(script)

os.chmod('script', 0o700)

script_abspath = os.path.abspath('script')

for plan_indicator in sorted(glob.iglob('**/planned', recursive = True)):
    d = os.path.dirname(plan_indicator)
    print(d)
    while count_running() >= max_num_active_processes:
        print('{} jobs running, sleeping for {} seconds'.format(count_running(), sleep_time))
        time.sleep(sleep_time)

    os.rename(plan_indicator, d + '/queued')

    subprocess.Popen('cd {d}; {executor} {script_abspath}'.format(**globals()), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
