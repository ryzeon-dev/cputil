import os
import sys
import time
import platform
from subprocess import getstatusoutput
import string
from conf import confFilePath, editConf
import re

def grep(target, pattern, returnFirstMatch=False, count=False, ignoreCase=False):
    res = []

    if isinstance(target, list):
        chunks = target

    elif isinstance(target, str):
        chunks = target.split('\n')

    for chunk in chunks:
        if ignoreCase:
            match = pattern.lower() in chunk.lower()

        else:
            match = pattern in chunk

        if match:
            if returnFirstMatch:
                return chunk

            res.append(chunk)

    if count:
        return len(res)

    return res if len(res) > 1 else (None if len(res) == 0 else res[0])

def terminal(cmd):
    statusCode, output = getstatusoutput(cmd)

    if statusCode != 0:
        raise Exception('Non 0 return code from console')

    return output

def getPolicies():
    global DRIVER_DIR

    policies = grep(os.listdir(DRIVER_DIR), 'policy')
    if isinstance(policies, str):
        return [policies]
    return sorted(policies, key=lambda x: int(x.replace('policy', '')))

def readFile(path):
    with open(path, 'r') as file:
        content = file.read()
    return content.strip()

DRIVER_DIR = '/sys/devices/system/cpu/cpufreq'
GOVERNORS = []

POLICIES = getPolicies()

GENERAL_DRIVER = '/sys/devices/system/cpu/'
FREQUENCIES = []

def readScalingFrequencies():
    frequencies = set()
    frequencyFiles = ['scaling_max_freq', 'scaling_min_freq', 'amd_pstate_lowest_nonlinear_freq', 'amd_pstate_max_freq', 'cpuinfo_max_freq', 'cpuinfo_min_freq']

    for e in os.listdir(DRIVER_DIR):
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(DRIVER_DIR, e)

        for file in frequencyFiles:
            filePath = os.path.join(policyPath, file)
            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                frequencies.add(file.read().strip())

    frequencies = list(frequencies)
    frequencies.sort(key= lambda x: int(x))
    return frequencies

def findAvailableGovernors():
    governors = set()
    governorFiles = ['scaling_available_governors']
    for e in os.listdir(DRIVER_DIR):
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(DRIVER_DIR, e)

        for file in governorFiles:
            filePath = os.path.join(policyPath, file)
            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for governor in file.read().strip().split(' '):
                    governors.add(governor)

    return list(governors)

FREQUENCIES = readScalingFrequencies()
GOVERNORS = findAvailableGovernors()

def setGovernor(governor, cpu):
    if governor not in GOVERNORS:
        print(f'Error: `{governor}` is not an available governor')
        return False

    if cpu is True:
        print('Setting governor for all processors to ' + governor)

        for policy in POLICIES:
            with open(f'{DRIVER_DIR}/{policy}/scaling_governor', 'w') as file:
                file.write(governor)

        if os.path.exists(confFilePath):
            editConf(confFilePath, governor, None, None)

        return True
    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting governor for processor ' + str(cpu) + ' to ' + governor)
            with open(f'{DRIVER_DIR}/{policy}/scaling_governor', 'w') as file:
                file.write(governor)

            return True
        return False

def getCurrentGovernors():
    governors = {}
    for policy in POLICIES:
        governors[policy] = readFile(f'{DRIVER_DIR}/{policy}/scaling_governor').strip()

    return governors

def getCurrentScalingFrequencies():
    frequencies = {}

    for policy in POLICIES:
        frequencies[policy] = {
            'min': readFile(f'{DRIVER_DIR}/{policy}/scaling_min_freq').strip() if 'scaling_min_freq' in os.listdir(
                f'{DRIVER_DIR}/{policy}') else '',
            'max': readFile(f'{DRIVER_DIR}/{policy}/scaling_max_freq').strip() if 'scaling_max_freq' in os.listdir(
                f'{DRIVER_DIR}/{policy}') else ''
        }

    return frequencies

def setMinimumScalingFrequency(frequency, cpu):
    if FREQUENCIES is None:
        print(f'Error: cputil is unable to detect allowed scaling frequencies')
        return False

    if frequency not in FREQUENCIES:
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    if cpu is True:
        print('Setting for all processors minimum frequency to ' + str(round(int(frequency) / 1000000, 1)) + ' GHz')
        for policy in POLICIES:
            with open(f'{DRIVER_DIR}/{policy}/scaling_min_freq', 'w') as file:
                file.write(frequency)

        if os.path.exists(confFilePath):
            editConf(confFilePath, None, frequency, None)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting for processor ' + str(cpu) + ' minimum frequency to ' + str(
                round(int(frequency) / 1000000, 1)) + ' GHz')

            with open(f'{DRIVER_DIR}/{policy}/scaling_min_freq', 'w') as file:
                file.write(frequency)

            return True
        return False

def setMaximumScalingFrequency(frequency, cpu):
    if FREQUENCIES is None:
        print(f'Error: cputil.py is unable to detect allowed scaling frequencies')
        return False

    if frequency not in FREQUENCIES:
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    if cpu is True:
        print('Setting for all processors maximum frequency to ' + str(round(int(frequency) / 1000000, 1)) + ' GHz')

        for policy in POLICIES:
            with open(f'{DRIVER_DIR}/{policy}/scaling_max_freq', 'w') as file:
                file.write(frequency)

        if os.path.exists(confFilePath):
            editConf(confFilePath, None, None, frequency)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting for processor ' + str(cpu) + ' maximum frequency to ' + str(
                round(int(frequency) / 1000000, 1)) + ' GHz')

            with open(f'{DRIVER_DIR}/{policy}/scaling_max_freq', 'w') as file:
                file.write(frequency)

            return True
        return False

def maxAll():
    maxScalingFrequency = str(max(int(freq) for freq in FREQUENCIES))
    setGovernor('performance', True)
    setMinimumScalingFrequency(maxScalingFrequency, True)
    setMaximumScalingFrequency(maxScalingFrequency, True)

def getModelName():
    procCpuinfo = readFile('/proc/cpuinfo').split('\n')
    modelName = grep(procCpuinfo, 'model name')

    if isinstance(modelName, list):
        modelName = modelName[0]

    if modelName is None:
        return ''

    name = modelName.split(':')[1].strip()

    return name

def getByteOrder():
    order = sys.byteorder

    if order == 'little':
        return 'Little Endian', 'LSB'

    elif order == 'big':
        return 'Big Endian', 'MSB'

    else:
        return '', ''

def getArchitecture():
    arch = platform.machine()

    if arch == 'x86_64':
        arch = 'amd64 / x86_64'

    elif arch == 'i386':
        arch = 'i386 / i686'

    elif arch == 'aarch64':
        arch = 'arm64 / aarch64'

    elif not arch:
        'amd64 / x86_64 ' if sys.maxsize == (2 ** 63 - 1) else 'i386 / i686'

    busSize = platform.architecture()[0]

    if not busSize:
        busSize = '64 bit' if sys.maxsize == (2 ** 63 - 1) else '32 bit'

    return f'{arch} ({busSize})'

def getDistinct(list):
    distinct = []

    for element in list:
        if element not in distinct:
            distinct.append(element)

    return distinct

def getCoreCount():
    try:
        cores = terminal(f'cat {GENERAL_DRIVER}/cpu*/topology/core_id').strip().split('\n')
    except:
        return ''

    return str(len(getDistinct(cores)))

def getThreadCount():
    return grep(readFile('/proc/cpuinfo'), 'processor', count=True)

def getClockBoost():
    try:
        if 'boost' in os.listdir(DRIVER_DIR):

            with open(f'{DRIVER_DIR}/boost', 'r') as file:
                return 'active' if '1' in file.read() else 'not active'

        else:
            return 'not available'

    except:
        return 'not available'

def getMinimumClock():
    return round(min(
        int(freq) for freq in terminal(f'cat {DRIVER_DIR}/policy*/cpuinfo_min_freq').strip().split('\n')
    ) / 1000000, 2)

def getMaximumClock():
    return round(max(
        int(freq) for freq in terminal(f'cat {DRIVER_DIR}/policy*/cpuinfo_max_freq').strip().split('\n')
    ) / 1000000, 2)

def makeListStructure(stat):
    for index, line in enumerate(stat):
        splitted = line.split(' ')

        for element in splitted:
            if element == '' or element == ' ':
                splitted.remove(element)

        stat[index] = list(int(element) for element in splitted)
    return stat

usageContexts = [
    'user',
    'nice',
    'system',
    'idle',
    'iowait',
    'interrupt',
    'soft-interrupt'
]

def getParameterUsage(beforeStat, afterStat):
    usage = {}
    beforeSum = sum(beforeStat)
    afterSum = sum(afterStat)

    beforeIdle = beforeStat[3]
    afterIdle = afterStat[3]

    total = afterSum - beforeSum
    totalUsagePercent = (total - (afterIdle - beforeIdle)) * 100 / total
    usage['total'] = round(totalUsagePercent, 2)

    for index, label in enumerate(usageContexts):
        usage[label] = round(
            100 - (total - (afterStat[index] - beforeStat[index])) * 100 / total, 2
        )

    return usage

def cpuUsage():
    beforeStat = terminal('grep cpu -i /proc/stat | awk \'{ $1="" ; print }\'').strip().split('\n')
    time.sleep(0.25)
    afterStat = terminal('grep cpu -i /proc/stat | awk \'{ $1="" ; print }\'').strip().split('\n')

    try:
        beforeStat = makeListStructure(beforeStat)
        afterStat = makeListStructure(afterStat)
    except:
        return []

    usages = []
    for i in range(len(beforeStat)):
        usages.append(getParameterUsage(beforeStat[i], afterStat[i]))

    return usages

def cpuFrequency():
    lines = grep(readFile('/proc/cpuinfo'), 'cpu MHz')
    frequencies = []

    if lines is None:
        return None, None

    for line in lines:
        frequencies.append(line.split(':')[1].strip())

    if not frequencies or frequencies == ['']:
        frequencies = []

        for policy in POLICIES:
            try:
                freq = readFile(f'{DRIVER_DIR}/{policy}/cpuinfo_cur_freq')

            except:
                return None, None

            else:
                freq = round(float(freq) / 1000, 2)
                frequencies.append(freq)

        avg = round(sum(frequencies) / len(frequencies), 2)
        return avg, frequencies

    else:
        frequencies = list(
            round(
                float(freq.replace(',', '.')),
                2
            ) for freq in frequencies
        )

        average = round(sum(frequencies) / len(frequencies), 2)
        return average, frequencies

def threadDistribution():
    driverDir = '/sys/devices/system/cpu'
    processors = {}

    for dir in os.listdir(driverDir):
        if dir.replace('cpu', '') and dir.replace('cpu', '')[0] not in string.ascii_letters:

            if 'topology' not in os.listdir(f'{driverDir}/{dir}') or \
                    'core_id' not in os.listdir(f'{driverDir}/{dir}/topology'):
                return []
            processors[dir] = readFile(f'{driverDir}/{dir}/topology/core_id').strip()

    res = []
    for processor in processorSort(processors.keys()):
        res.append(processors[processor])

    return res

def processorDieDistribution():
    driverDir = '/sys/devices/system/cpu'
    processors = {}

    for dir in os.listdir(driverDir):
        if dir.replace('cpu', '') and dir.replace('cpu', '')[0] not in string.ascii_letters:

            if 'topology' not in os.listdir(f'{driverDir}/{dir}') or \
                    'die_id' not in os.listdir(f'{driverDir}/{dir}/topology'):
                return None

            with open(f'{driverDir}/{dir}/topology/die_id', 'r') as file:
                processors[dir] = file.read().strip()

    res = []
    for processor in processorSort(processors.keys()):
        res.append(processors[processor])

    return res

def cpuCache():
    baseDir = '/sys/devices/system/cpu'
    cpuDirs = grep(os.listdir('/sys/devices/system/cpu'), 'cpu',
                   ignoreCase=True)  # terminal('ls /sys/devices/system/cpu | grep -i cpu').split('\n')

    if 'cpufreq' in cpuDirs:
        cpuDirs.remove('cpufreq')

    if 'cpuidle' in cpuDirs:
        cpuDirs.remove('cpuidle')

    cpuCache = {}
    for cpu in cpuDirs:
        cpuCache[cpu] = {}

        for cacheIndex in grep(os.listdir(f'{baseDir}/{cpu}/cache'), 'index', ignoreCase=True):
            try:
                size = readFile(f'{baseDir}/{cpu}/cache/{cacheIndex}/size').strip()
            except:
                size = 'unknown'

            level = readFile(f'{baseDir}/{cpu}/cache/{cacheIndex}/level')
            sharing = readFile(f'{baseDir}/{cpu}/cache/{cacheIndex}/shared_cpu_list')

            if cpuCache[cpu].get(level) is not None and size != 'unknown':
                cpuCache[cpu][level]['amount'] += int(size.replace('K', '').replace('k', ''))

            else:
                cpuCache[cpu][level] = {
                    'amount': int(size.replace('K', '').replace('k', ''))
                    if size != 'unknown' else size,
                    'shared': sharing
                }

    return cpuCache

def processorsFromRange(processorRange):
    if '-' in processorRange:
        splittedRange = processorRange.split('-')
        start = int(splittedRange[0])

        if ',' in splittedRange[1]:
            end = splittedRange[1]
            rangeEnd = int(end.split(',')[0])

            additional = end.split(',')[1:]
            linearRange = list(range(start, rangeEnd + 1))

            for addition in additional:
                linearRange.append(addition)
            return linearRange

        else:
            end = int(splittedRange[1])

            return list(range(start, end + 1))
    return list(int(element) for element in processorRange.split(','))

def processorSort(processors):
    sorted = [None] * len(processors)

    for processor in processors:
        processorName = list((chr if chr not in string.ascii_letters else '') for chr in processor)

        index = int(''.join(processorName))
        sorted[index] = processor

    return sorted

def wrap(string):
    return '"' + string + '"'

def jsonFormat():
    json = {}

    json["model name"] = getModelName()
    json['architecture'] = getArchitecture()
    json['byte order'] = getByteOrder()[0]

    json['core count'] = int(getCoreCount())
    json['thread count'] = int(getThreadCount())

    json['clock boost'] = getClockBoost()
    json['minimum frequency'] = int(float(getMinimumClock()) * 1000)
    json['maximum frequency'] = int(float(getMaximumClock()) * 1000)

    json['governors'] = [governor for governor in GOVERNORS]
    json['scaling frequencies'] = [int(frequency) for frequency in FREQUENCIES]

    scalingFrequencies = getCurrentScalingFrequencies()
    governors = getCurrentGovernors()

    usages = cpuUsage()
    averageFrequency, frequencies = cpuFrequency()

    try:
        cache = cpuCache()

    except:
        cache = None

    threadDist = threadDistribution()
    dieDist = processorDieDistribution()

    json['average'] = {
        "usage": {}
    }

    for label, percent in usages.pop(0).items():
        json['average']['usage'][label] = float(percent)

    json['average']['frequency'] = int(averageFrequency) if averageFrequency else ''

    sortedCache = processorSort(cache.keys())

    for index, processor in enumerate(usages):
        processorId = 'processor' + str(index)
        json[processorId] = {
            'usage': {},
            'frequency': '',
            'cache': {},
            'physical core': '',
            'physical die': '',
            'minimum scaling frequency': '',
            'maximum scaling frequency': '',
            'governor': ''
        }

        try:
            scaling = scalingFrequencies[f'policy{index}']
            json[processorId]['minimum scaling frequency'] = int(scaling['min'])
            json[processorId]['maximum scaling frequency'] = int(scaling['max'])

        except:
            pass

        try:
            governor = governors[f'policy{index}']
            json[processorId]['governor'] = str(governor)

        except:
            pass

        for label, percent in processor.items():
            json[processorId]['usage'][label] = float(percent)

        json[processorId]['frequency'] = int(frequencies[index]) if frequencies and index < len(frequencies) and \
                                                                    frequencies[index] is not None else ''
        json[processorId]['physical core'] = int(threadDist[index])
        json[processorId]['physical die'] = int(dieDist[index]) if dieDist else ''

        if cache is not None:
            processorCacheKey = sortedCache[index]
            for cacheLevel in cache[processorCacheKey]:

                sharing = processorsFromRange(cache[processorCacheKey][cacheLevel]['shared'])
                if len(sharing) == int(getThreadCount()):
                    sharing = ['all']

                json[processorId]['cache']['L' + str(cacheLevel)] = {
                    'sharing': [", ".join((str(processor)) for processor in sharing)],
                    "amount": int(level) if
                    isinstance((level := cache[processorCacheKey][cacheLevel]['amount']), str) and level.isdigit()
                    else level
                }

    return json