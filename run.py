#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import time
import yaml

with open(sys.argv[1], 'r') as f:
    params = yaml.load(f)

executioner = str(params['executioner'])
executable = str(params['executable'])
preamble = str(params['preamble'])
try:
    sleep_time = int(params['sleep_time'])
except KeyError:
    sleep_time = 1

def count_running():
    return len([None for d in os.listdir() if os.path.isfile(d + '/queued') or os.path.isfile(d + '/running')])

max_num_active_processes = int(params['max_num_active_processes'])

script = """\
#!/usr/bin/env bash

{preamble}

mv queued running

../{executable} > out 2> error

rm running
""".format(**globals())

with open('script', 'w') as f:
    f.write(script)

os.chmod('script', 0o700)

for d in os.listdir():
    if os.path.isfile(d + '/planned'):
        print(d)
        while count_running() >= max_num_active_processes:
            print('{} jobs running, sleeping'.format(count_running()))
            time.sleep(sleep_time)

        os.rename(d + '/planned', d + '/queued')

        subprocess.Popen("cd {d}; {executioner} ../script".format(**globals()), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
