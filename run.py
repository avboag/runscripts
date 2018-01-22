#!/usr/bin/env python3

import glob
import os
import shutil
import subprocess
import sys
import time
import yaml

with open(sys.argv[1], 'r') as f:
    params = yaml.safe_load(f)

executioner = params['executioner']

try:
    sleep_time = int(params['sleep_time'])
except KeyError:
    sleep_time = 1

def count_running():
    return len(glob.iglob('**/queued')) + len(glob.iglob('**/running'))

max_num_active_processes = int(params['max_num_active_processes'])

script = """\
#!/usr/bin/env bash

{preamble}

mv queued running

(cd ..; {executable} > out 2> error)

rm running
""".format(params)

with open('script', 'w') as f:
    f.write(script)

os.chmod('script', 0o700)

for plan_indicator in glob.iglob('**/planned'):
    d = os.path.dirname(plan_indicator)
    print(d)
    while count_running() >= max_num_active_processes:
        print('{} jobs running, sleeping'.format(count_running()))
        time.sleep(sleep_time)

    os.rename(plan_indicator, d + '/queued')

    subprocess.Popen("cd {d}; {executioner} ../script".format(**globals()), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
