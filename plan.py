import os

def simple_id(d, keys):
    return '_'.join([key + '_' + str(d[key]) for key in keys])

def plan(dirname, content, filename = 'param.yaml'):
    os.makedirs(dirname, exist_ok = True)
    with open(os.path.join(dirname, filename), 'w') as f:
        f.write(content)

    with open(dirname + '/planned', 'w') as f:
        pass
