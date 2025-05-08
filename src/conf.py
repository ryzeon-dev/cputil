confFilePath = '/etc/cputild/cputild.conf'

def parseConf(path):
    with open(path, 'r') as file:
        content = file.read()

    governor = None
    scalingMinFreq = None
    scalingMaxFreq = None
    pollingInterval = None

    for line in content.split('\n'):
        if line.startswith('#'):
            continue

        if (prompt := 'governor:') in line:
            governor = line.replace(prompt, '').strip()

        elif (prompt := 'min_scaling_frequency:') in line:
            scalingMinFreq = line.replace(prompt, '').strip()

        elif (prompt := 'max_scaling_frequency:') in line:
            scalingMaxFreq = line.replace(prompt, '').strip()

        elif (prompt := 'polling_interval:') in line:
            try:
                pollingInterval = line.replace(prompt, '').strip()
            except:
                pass

    return governor, scalingMinFreq, scalingMaxFreq, pollingInterval

def editConf(path, governor, scalingMinFreq, scalingMaxFreq):
    with open(path, 'r') as file:
        content = file.read()

    splitted = content.split('\n')
    index = 0

    while index < len(splitted):
        line = splitted[index]

        if line.startswith('#'):
            index += 1
            continue

        if governor is not None:
            if line.startswith('governor:'):
                splitted[index] = f'governor: {governor}'

        if scalingMaxFreq is not None:
            if line.startswith('max_scaling_frequency:'):
                splitted[index] = f'max_scaling_frequency: {scalingMaxFreq}'

        if scalingMinFreq is not None:
            if line.startswith('min_scaling_frequency:'):
                splitted[index] = f'min_scaling_frequency: {scalingMinFreq}'

        index += 1

    with open(path, 'w') as file:
        file.write('\n'.join(splitted))