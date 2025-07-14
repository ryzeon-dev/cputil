import os
import sys
import time
import platform
from subprocess import getstatusoutput
import string
from conf import confFilePath, editConf
import re

### UTILS ###

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
    global CPUFREQ_DIR

    try:
        policies = grep(os.listdir(CPUFREQ_DIR), 'policy')
    except:
        print('Error: cannot read cpufreq\'s sysfs')
        sys.exit(1)

    if isinstance(policies, str):
        return [policies]
    return sorted(policies, key=lambda x: int(x.replace('policy', '')))

def readFile(path):
    with open(path, 'r') as file:
        content = file.read()
    return content.strip()

def writePolicyFile(policy, file, content):
    global CPUFREQ_DIR

    try:
        with open(os.path.join(CPUFREQ_DIR, policy, file), 'w') as file:
            file.write(content)

    except:
        print('Error: cannot write to cpufreq\'s sysfs')
        return False

    return True

### SYSFS CONST READER ###

def readScalingFrequencies():
    global CPUFREQ_CONTENT, CPUFREQ_DIR

    frequencies = set()
    frequencyFiles = ['scaling_max_freq', 'scaling_min_freq', 'scaling_available_frequencies',
                      'amd_pstate_lowest_nonlinear_freq', 'amd_pstate_max_freq', 'cpuinfo_max_freq', 'cpuinfo_min_freq']

    for e in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(CPUFREQ_DIR, e)

        for file in frequencyFiles:
            filePath = os.path.join(policyPath, file)
            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for chunk in file.read().strip().split(' '):
                    frequencies.add(chunk)

    frequencies = list(frequencies)
    frequencies.sort(key=lambda x: int(x))
    return frequencies

def findAvailableGovernors():
    global CPUFREQ_CONTENT, CPUFREQ_DIR

    governors = set()
    governorFiles = ['scaling_available_governors']

    for e in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(CPUFREQ_DIR, e)

        for file in governorFiles:
            filePath = os.path.join(policyPath, file)
            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for governor in file.read().strip().split(' '):
                    governors.add(governor)

    return list(governors)

def getEnergyPerformancePreferences():
    global CPUFREQ_CONTENT, CPUFREQ_DIR

    preferences = set()
    preferenceFiles = ['energy_performance_available_preferences', 'energy_performance_preference']

    for policy in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', policy):
            continue

        for preferenceFile in preferenceFiles:
            filePath = os.path.join(CPUFREQ_DIR, policy, preferenceFile)

            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for chunk in file.read().strip().split(' '):
                    preferences.add(chunk)

    return list(preferences)

### CONST ###

CPUFREQ_DIR = '/sys/devices/system/cpu/cpufreq'

try:
    CPUFREQ_CONTENT = os.listdir(CPUFREQ_DIR)

except:
    print('Error: cannot access cpufreq\'s sysfs')
    exit(1)

POLICIES = getPolicies()
GENERAL_DRIVER = '/sys/devices/system/cpu/'

FREQUENCIES = readScalingFrequencies()
GOVERNORS = findAvailableGovernors()
ENERGY_PERFORMANCE_PREFERENCES = getEnergyPerformancePreferences()

### SETTERS ###

def setGovernor(governor, cpu=True, updateConf=True):
    global GOVERNORS, CPUFREQ_DIR, POLICIES

    if governor not in GOVERNORS:
        print(f'Error: `{governor}` is not an available governor')
        return False

    if cpu is True:
        print('Setting governor for all processors to ' + governor)

        for policy in POLICIES:
            if not writePolicyFile(policy, 'scaling_governor', governor):
                return False

        if os.path.exists(confFilePath) and updateConf:
            editConf(confFilePath, governor=governor)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting governor for processor ' + str(cpu) + ' to ' + governor)

            if not writePolicyFile(policy, 'scaling_governor', governor):
                return False

            return True
        return False

def setMinimumScalingFrequency(frequency, cpu, updateConf=True):
    global FREQUENCIES, CPUFREQ_DIR, POLICIES
    if FREQUENCIES is None:
        print(f'Error: cputil is unable to detect allowed scaling frequencies')
        return False

    if frequency not in FREQUENCIES:
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    if cpu is True:
        print('Setting for all processors minimum frequency to ' + str(round(int(frequency) / 1000000, 1)) + ' GHz')

        for policy in POLICIES:
            if not writePolicyFile(policy, 'scaling_min_freq', frequency):
                return False

        if updateConf and os.path.exists(confFilePath):
            editConf(confFilePath, scalingMinFreq=frequency)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting for processor ' + str(cpu) + ' minimum frequency to ' + str(
                round(int(frequency) / 1000000, 1)) + ' GHz')

            if not writePolicyFile(policy, 'scaling_min_freq', frequency):
                return False

            return True

        return False

def setMaximumScalingFrequency(frequency, cpu, updateConf=True):
    global FREQUENCIES, POLICIES, CPUFREQ_DIR

    if FREQUENCIES is None:
        print(f'Error: cputil.py is unable to detect allowed scaling frequencies')
        return False

    if frequency not in FREQUENCIES:
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    if cpu is True:
        print('Setting for all processors maximum frequency to ' + str(round(int(frequency) / 1000000, 1)) + ' GHz')

        for policy in POLICIES:
            if not writePolicyFile(policy, 'scaling_max_freq', frequency):
                return False

        if updateConf and os.path.exists(confFilePath):
            editConf(confFilePath, scalingMaxFreq=frequency)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting for processor ' + str(cpu) + ' maximum frequency to ' + str(
                round(int(frequency) / 1000000, 1)) + ' GHz')

            if not writePolicyFile(policy, 'scaling_max_freq', frequency):
                return False
            return True
        return False

def setEnergyPerformancePreference(preference, cpu, updateConf=True):
    global ENERGY_PERFORMANCE_PREFERENCES

    # changing governor requires reaload of energy performance preferences
    ENERGY_PERFORMANCE_PREFERENCES = getEnergyPerformancePreferences()

    if ENERGY_PERFORMANCE_PREFERENCES is None:
        print(f'Error: cputil is unable to detect allowed energy performance preferences')
        return False

    if preference not in ENERGY_PERFORMANCE_PREFERENCES:
        print(f'Error: `{preference}` is not one of the allowed energy performance preferences')
        return False

    if cpu is True:
        print('Setting for all processors energy performance preference to ' + preference)

        for policy in POLICIES:
            if not writePolicyFile(policy, 'energy_performance_preference', preference):
                return False

        if updateConf and os.path.exists(confFilePath):
            editConf(confFilePath, energyPerformancePreference=preference)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in POLICIES:
            print('Setting for processor ' + str(cpu) + ' energy performance preference to ' + preference)

            if not writePolicyFile(policy, 'energy_performance_preference', preference):
                return False

            return True
        return False

def maxAll():
    maxScalingFrequency = str(max(int(freq) for freq in FREQUENCIES))
    setGovernor('performance', True)

    setMinimumScalingFrequency(maxScalingFrequency, True)
    setMaximumScalingFrequency(maxScalingFrequency, True)

    setEnergyPerformancePreference('performance', True)

def minAll():
    minScalingFrequency = str(min(int(freq) for freq in FREQUENCIES))

    for governor in ['powersave', 'schedutil']:
        if governor in GOVERNORS:
            setGovernor(governor, True)
            break

    setMinimumScalingFrequency(minScalingFrequency, True)
    setMaximumScalingFrequency(minScalingFrequency, True)

    setEnergyPerformancePreference('power', True)

### CURRENT STATUS GETTERS ###

def getCurrentGovernors():
    global CPUFREQ_DIR, POLICIES

    governors = {}
    for policy in POLICIES:
        governors[policy] = readFile(f'{CPUFREQ_DIR}/{policy}/scaling_governor').strip()

    return governors

def getCurrentScalingFrequencies():
    global CPUFREQ_DIR, POLICIES
    frequencies = {}

    for policy in POLICIES:
        try:
            frequencies[policy] = {
                'min': readFile(f'{CPUFREQ_DIR}/{policy}/scaling_min_freq').strip() if 'scaling_min_freq' in os.listdir(
                    f'{CPUFREQ_DIR}/{policy}') else '',
                'max': readFile(f'{CPUFREQ_DIR}/{policy}/scaling_max_freq').strip() if 'scaling_max_freq' in os.listdir(
                    f'{CPUFREQ_DIR}/{policy}') else ''
            }
        except:
            print('Error: cannot read cpufreq\'s sysfs')
            sys.exit(1)

    return frequencies

def getCurrentEnergyPerformancePreferences():
    global CPUFREQ_DIR, CPUFREQ_CONTENT
    currentEnergyPreferences = {}

    for policy in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', policy):
            continue

        filePath = os.path.join(CPUFREQ_DIR, policy, 'energy_performance_preference')
        if os.path.exists(filePath):
            with open(filePath, 'r') as file:
                currentEnergyPreferences[policy] = file.read().strip()

    return currentEnergyPreferences

### INFO && USAGE READERS ###

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
    global GENERAL_DRIVER
    try:
        cores = terminal(f'cat {GENERAL_DRIVER}/cpu*/topology/core_id').strip().split('\n')
    except:
        return ''

    return str(len(getDistinct(cores)))

def getThreadCount():
    return grep(readFile('/proc/cpuinfo'), 'processor', count=True)

def getClockBoost():
    global CPUFREQ_DIR
    try:
        if 'boost' in os.listdir(CPUFREQ_DIR):

            with open(f'{CPUFREQ_DIR}/boost', 'r') as file:
                return 'active' if '1' in file.read() else 'not active'

        else:
            return 'not available'

    except:
        return 'not available'

def getMinimumClock():
    global CPUFREQ_DIR
    return round(min(
        int(freq) for freq in terminal(f'cat {CPUFREQ_DIR}/policy*/cpuinfo_min_freq').strip().split('\n')
    ) / 1000000, 2)

def getMaximumClock():
    global CPUFREQ_DIR
    return round(max(
        int(freq) for freq in terminal(f'cat {CPUFREQ_DIR}/policy*/cpuinfo_max_freq').strip().split('\n')
    ) / 1000000, 2)

def getAmdPState():
    global GENERAL_DRIVER

    pStateDir = os.path.join(GENERAL_DRIVER, 'amd_pstate')
    status = None
    prefcore = None

    if (pStateStatus := os.path.join(pStateDir, 'status')) and os.path.exists(pStateStatus):
        with open(pStateStatus, 'r') as file:
            status = file.read().strip()

    if (pStatePrefcore := os.path.join(pStateDir, 'prefcore')) and os.path.exists(pStatePrefcore):
        with open(pStatePrefcore, 'r') as file:
            prefcore = file.read().strip()

    return status, prefcore

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
    global CPUFREQ_DIR
    lines = grep(readFile('/proc/cpuinfo'), 'cpu MHz')
    frequencies = []

    if lines is not None:
        for line in lines:
            frequencies.append(line.split(':')[1].strip())

    if not frequencies or frequencies == ['']:
        frequencies = []

        for policy in POLICIES:
            try:
                freq = readFile(f'{CPUFREQ_DIR}/{policy}/cpuinfo_cur_freq')

            except:
                frequencies.append(0)

            else:
                freq = round(float(freq) / 1000, 2)
                frequencies.append(freq)

        nonZeroFreqs = []
        for freq in frequencies:
            if freq:
                nonZeroFreqs.append(freq)

        avg = round(sum(nonZeroFreqs) / len(nonZeroFreqs), 2)
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
    global GENERAL_DRIVER
    processors = {}

    for dir in os.listdir(GENERAL_DRIVER):
        if dir.replace('cpu', '') and dir.replace('cpu', '')[0] not in string.ascii_letters:

            if 'topology' not in os.listdir(os.path.join(GENERAL_DRIVER, dir)) or \
                    'core_id' not in os.listdir(os.path.join(GENERAL_DRIVER, dir, 'topology')):
                return []
            processors[dir] = readFile(os.path.join(GENERAL_DRIVER, dir, 'topology', 'core_id')).strip()

    res = []
    for processor in processorSort(processors.keys()):
        res.append(processors[processor])

    return res

def processorDieDistribution():
    global GENERAL_DRIVER
    processors = {}

    for dir in os.listdir(GENERAL_DRIVER):
        if dir.replace('cpu', '') and dir.replace('cpu', '')[0] not in string.ascii_letters:

            if 'topology' not in os.listdir(os.path.join(GENERAL_DRIVER, dir)) or \
                    'die_id' not in os.listdir(os.path.join(GENERAL_DRIVER, dir, 'topology')):
                return None

            with open(os.path.join(GENERAL_DRIVER, dir, 'topology', 'die_id'), 'r') as file:
                processors[dir] = file.read().strip()

    res = []
    for processor in processorSort(processors.keys()):
        res.append(processors[processor])

    return res

def cpuCache():
    global GENERAL_DRIVER

    cpuDirs = grep(os.listdir(GENERAL_DRIVER), 'cpu', ignoreCase=True)  # terminal('ls /sys/devices/system/cpu | grep -i cpu').split('\n')

    if 'cpufreq' in cpuDirs:
        cpuDirs.remove('cpufreq')

    if 'cpuidle' in cpuDirs:
        cpuDirs.remove('cpuidle')

    cpuCache = {}
    for cpu in cpuDirs:
        cpuCache[cpu] = {}

        for cacheIndex in grep(os.listdir(f'{GENERAL_DRIVER}/{cpu}/cache'), 'index', ignoreCase=True):
            try:
                size = readFile(f'{GENERAL_DRIVER}/{cpu}/cache/{cacheIndex}/size').strip()
            except:
                size = 'unknown'

            level = readFile(f'{GENERAL_DRIVER}/{cpu}/cache/{cacheIndex}/level')
            sharing = readFile(f'{GENERAL_DRIVER}/{cpu}/cache/{cacheIndex}/shared_cpu_list')

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

def dictFormat():
    dict = {}

    dict["model name"] = getModelName()
    dict['architecture'] = getArchitecture()
    dict['byte order'] = getByteOrder()[0]

    dict['core count'] = int(getCoreCount())
    dict['thread count'] = int(getThreadCount())

    dict['clock boost'] = getClockBoost()
    dict['minimum frequency'] = int(float(getMinimumClock()) * 1000)
    dict['maximum frequency'] = int(float(getMaximumClock()) * 1000)

    dict['governors'] = [governor for governor in GOVERNORS]
    dict['scaling frequencies'] = [int(frequency) for frequency in FREQUENCIES]
    dict['energy performance preferences'] = [epp for epp in ENERGY_PERFORMANCE_PREFERENCES]

    status, prefcore = getAmdPState()

    dict['amd-p-state-status'] = status
    dict['amd-p-state-prefcore'] = prefcore

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
    energyPerformancePreferences = getCurrentEnergyPerformancePreferences()

    dict['average'] = {
        "usage": {}
    }

    for label, percent in usages.pop(0).items():
        dict['average']['usage'][label] = float(percent)

    dict['average']['frequency'] = int(averageFrequency) if averageFrequency else ''

    sortedCache = processorSort(cache.keys())

    for index, processor in enumerate(usages):
        processorId = 'processor' + str(index)
        dict[processorId] = {
            'usage': {},
            'frequency': '',
            'cache': {},
            'minimum scaling frequency': '',
            'maximum scaling frequency': '',
            'governor': '',
            'energy performance preference' : ''
        }

        try:
            scaling = scalingFrequencies[f'policy{index}']
            dict[processorId]['minimum scaling frequency'] = int(scaling['min'])
            dict[processorId]['maximum scaling frequency'] = int(scaling['max'])

        except:
            pass

        try:
            governor = governors[f'policy{index}']
            dict[processorId]['governor'] = str(governor)

        except:
            pass

        try:
            preference = energyPerformancePreferences[f'policy{index}']
            dict[processorId]['energy performance preference'] = str(preference)

        except:
            pass

        for label, percent in processor.items():
            dict[processorId]['usage'][label] = float(percent)

        dict[processorId]['frequency'] = int(frequencies[index]) if frequencies and index < len(frequencies) and frequencies[index] is not None else ''
        if threadDist:
            dict[processorId]['physical core'] = int(threadDist[index])

        if dieDist:
            dict[processorId]['physical die'] = int(dieDist[index]) if dieDist else ''

        if cache is not None:
            processorCacheKey = sortedCache[index]
            for cacheLevel in cache[processorCacheKey]:

                sharing = processorsFromRange(cache[processorCacheKey][cacheLevel]['shared'])
                if len(sharing) == int(getThreadCount()):
                    sharing = ['all']

                dict[processorId]['cache']['L' + str(cacheLevel)] = {
                    'sharing': [", ".join((str(processor)) for processor in sharing)],
                    "amount": int(level) if
                    isinstance((level := cache[processorCacheKey][cacheLevel]['amount']), str) and level.isdigit()
                    else level
                }

    return dict