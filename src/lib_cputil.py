import os
import sys
import time
import platform
from subprocess import getstatusoutput
import string
import re
from conf import confFilePath, editConf

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
    global _CPUFREQ_DIR

    try:
        policies = grep(os.listdir(_CPUFREQ_DIR), 'policy')
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
    global _CPUFREQ_DIR

    try:
        with open(os.path.join(_CPUFREQ_DIR, policy, file), 'w') as file:
            file.write(content)

    except:
        print('Error: cannot write to cpufreq\'s sysfs')
        return False

    return True

### SYSFS CONST READER ###

def readScalingFrequencies():
    global _CPUFREQ_CONTENT, _CPUFREQ_DIR

    frequencies = set()
    frequencyFiles = ['scaling_max_freq', 'scaling_min_freq', 'scaling_available_frequencies',
                      'amd_pstate_lowest_nonlinear_freq', 'amd_pstate_max_freq', 'cpuinfo_max_freq', 'cpuinfo_min_freq']

    for e in _CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(_CPUFREQ_DIR, e)

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
    global _CPUFREQ_CONTENT, _CPUFREQ_DIR

    governors = set()
    governorFiles = ['scaling_available_governors']

    for e in _CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(_CPUFREQ_DIR, e)

        for file in governorFiles:
            filePath = os.path.join(policyPath, file)
            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for governor in file.read().strip().split(' '):
                    governors.add(governor)

    return list(governors)

def getEnergyPerformancePreferences():
    global _CPUFREQ_CONTENT, _CPUFREQ_DIR

    preferences = set()
    preferenceFiles = ['energy_performance_available_preferences', 'energy_performance_preference']

    for policy in _CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', policy):
            continue

        for preferenceFile in preferenceFiles:
            filePath = os.path.join(_CPUFREQ_DIR, policy, preferenceFile)

            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for chunk in file.read().strip().split(' '):
                    preferences.add(chunk)

    return list(preferences)

### CONST ###

_CPUFREQ_DIR = '/sys/devices/system/cpu/cpufreq'

try:
    _CPUFREQ_CONTENT = os.listdir(_CPUFREQ_DIR)

except:
    print('Error: cannot access cpufreq\'s sysfs')
    exit(1)

_GLOBAL_VARIABLES_TO_INIT = True

_GENERAL_DRIVER = '/sys/devices/system/cpu/'

_POLICIES = None
_FREQUENCIES = None
_GOVERNORS = None
_ENERGY_PERFORMANCE_PREFERENCES = None

def initGlobalVariables():
    global _POLICIES, _FREQUENCIES, _GOVERNORS, _ENERGY_PERFORMANCE_PREFERENCES, _GLOBAL_VARIABLES_TO_INIT
    try:
        _POLICIES = getPolicies()
        _FREQUENCIES = readScalingFrequencies()
        _GOVERNORS = findAvailableGovernors()
        _ENERGY_PERFORMANCE_PREFERENCES = getEnergyPerformancePreferences()

    except:
        print('Error: cannot read scaling information')
        sys.exit(1)

    _GLOBAL_VARIABLES_TO_INIT = False

### CONST GETTERS ###

def getAllPolicies():
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    return _POLICIES


def getAllGovernors():
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    return _GOVERNORS


def getAllFrequencies():
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    return _FREQUENCIES


def getAllEnergyPerformancePreferences():
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    return _ENERGY_PERFORMANCE_PREFERENCES

### SETTERS ###

def setScalingGovernor(governor, cpu=True, updateConf=True):
    global _GOVERNORS, _CPUFREQ_DIR, _POLICIES, _GLOBAL_VARIABLES_TO_INIT
    
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()
        
    if governor not in _GOVERNORS:
        print(f'Error: `{governor}` is not an available governor')
        return False

    if cpu is True:
        print('Setting governor for all processors to ' + governor)

        for policy in _POLICIES:
            if not writePolicyFile(policy, 'scaling_governor', governor):
                return False

        if os.path.exists(confFilePath) and updateConf:
            editConf(confFilePath, governor=governor)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in _POLICIES:
            print('Setting governor for processor ' + str(cpu) + ' to ' + governor)

            if not writePolicyFile(policy, 'scaling_governor', governor):
                return False

            return True
        return False

def setMinimumScalingFrequency(frequency, cpu, updateConf=True):
    global _FREQUENCIES, _CPUFREQ_DIR, _POLICIES, _GLOBAL_VARIABLES_TO_INIT
    
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()
        
    if _FREQUENCIES is None:
        print(f'Error: cputil is unable to detect allowed scaling frequencies')
        return False

    if frequency not in _FREQUENCIES:
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    if cpu is True:
        print('Setting for all processors minimum frequency to ' + str(round(int(frequency) / 1000000, 1)) + ' GHz')

        for policy in _POLICIES:
            if not writePolicyFile(policy, 'scaling_min_freq', frequency):
                return False

        if updateConf and os.path.exists(confFilePath):
            editConf(confFilePath, scalingMinFreq=frequency)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in _POLICIES:
            print('Setting for processor ' + str(cpu) + ' minimum frequency to ' + str(
                round(int(frequency) / 1000000, 1)) + ' GHz')

            if not writePolicyFile(policy, 'scaling_min_freq', frequency):
                return False

            return True

        return False

def setMaximumScalingFrequency(frequency, cpu, updateConf=True):
    global _FREQUENCIES, _POLICIES, _CPUFREQ_DIR, _GLOBAL_VARIABLES_TO_INIT
    
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    if _FREQUENCIES is None:
        print(f'Error: cputil.py is unable to detect allowed scaling frequencies')
        return False

    if frequency not in _FREQUENCIES:
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    if cpu is True:
        print('Setting for all processors maximum frequency to ' + str(round(int(frequency) / 1000000, 1)) + ' GHz')

        for policy in _POLICIES:
            if not writePolicyFile(policy, 'scaling_max_freq', frequency):
                return False

        if updateConf and os.path.exists(confFilePath):
            editConf(confFilePath, scalingMaxFreq=frequency)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in _POLICIES:
            print('Setting for processor ' + str(cpu) + ' maximum frequency to ' + str(
                round(int(frequency) / 1000000, 1)) + ' GHz')

            if not writePolicyFile(policy, 'scaling_max_freq', frequency):
                return False
            return True
        return False

def setEnergyPerformancePreference(preference, cpu, updateConf=True):
    global _ENERGY_PERFORMANCE_PREFERENCES, _GLOBAL_VARIABLES_TO_INIT
    
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    # changing governor requires reaload of energy performance preferences
    _ENERGY_PERFORMANCE_PREFERENCES = getEnergyPerformancePreferences()

    if _ENERGY_PERFORMANCE_PREFERENCES is None:
        print(f'Error: cputil is unable to detect allowed energy performance preferences')
        return False

    if preference not in _ENERGY_PERFORMANCE_PREFERENCES:
        print(f'Error: `{preference}` is not one of the allowed energy performance preferences')
        return False

    if cpu is True:
        print('Setting for all processors energy performance preference to ' + preference)

        for policy in _POLICIES:
            if not writePolicyFile(policy, 'energy_performance_preference', preference):
                return False

        if updateConf and os.path.exists(confFilePath):
            editConf(confFilePath, energyPerformancePreference=preference)

        return True

    else:
        policy = f'policy{cpu}'

        if policy in _POLICIES:
            print('Setting for processor ' + str(cpu) + ' energy performance preference to ' + preference)

            if not writePolicyFile(policy, 'energy_performance_preference', preference):
                return False

            return True
        return False

def maxAll():
    global _GLOBAL_VARIABLES_TO_INIT, _FREQUENCIES
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()
        
    maxScalingFrequency = str(max(int(freq) for freq in _FREQUENCIES))
    setScalingGovernor('performance', True)

    setMinimumScalingFrequency(maxScalingFrequency, True)
    setMaximumScalingFrequency(maxScalingFrequency, True)

    setEnergyPerformancePreference('performance', True)

def minAll():
    global _GLOBAL_VARIABLES_TO_INIT, _FREQUENCIES
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()
        
    minScalingFrequency = str(min(int(freq) for freq in _FREQUENCIES))

    for governor in ['powersave', 'schedutil']:
        if governor in _GOVERNORS:
            setScalingGovernor(governor, True)
            break

    setMinimumScalingFrequency(minScalingFrequency, True)
    setMaximumScalingFrequency(minScalingFrequency, True)

    setEnergyPerformancePreference('power', True)

### CURRENT STATUS GETTERS ###

def getCurrentScalingDriver():
    global _GLOBAL_VARIABLES_TO_INIT, _POLICIES, _CPUFREQ_DIR
    
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()
    
    drivers = set()

    for policy in _POLICIES:
        path = os.path.join(_CPUFREQ_DIR, policy)
        driver = readFile(os.path.join(path, 'scaling_driver'))

        if driver:
            drivers.add(driver)

    return ','.join(drivers)

def getCurrentScalingGovernors():
    global _CPUFREQ_DIR, _POLICIES, _GLOBAL_VARIABLES_TO_INIT
    
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    governors = {}
    for policy in _POLICIES:
        governors[policy] = readFile(f'{_CPUFREQ_DIR}/{policy}/scaling_governor').strip()

    return governors

def getCurrentScalingFrequencies():
    global _CPUFREQ_DIR, _POLICIES, _GLOBAL_VARIABLES_TO_INIT

    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    frequencies = {}

    for policy in _POLICIES:
        try:
            frequencies[policy] = {
                'min': readFile(f'{_CPUFREQ_DIR}/{policy}/scaling_min_freq').strip() if 'scaling_min_freq' in os.listdir(
                    f'{_CPUFREQ_DIR}/{policy}') else '',
                'max': readFile(f'{_CPUFREQ_DIR}/{policy}/scaling_max_freq').strip() if 'scaling_max_freq' in os.listdir(
                    f'{_CPUFREQ_DIR}/{policy}') else ''
            }
        except:
            print('Error: cannot read cpufreq\'s sysfs')
            sys.exit(1)

    return frequencies

def getCurrentEnergyPerformancePreferences():
    global _CPUFREQ_DIR, _CPUFREQ_CONTENT, _GLOBAL_VARIABLES_TO_INIT

    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    currentEnergyPreferences = {}

    for policy in _CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', policy):
            continue

        filePath = os.path.join(_CPUFREQ_DIR, policy, 'energy_performance_preference')
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
        arch = 'amd64 / x86_64 ' if sys.maxsize == (2 ** 63 - 1) else 'i386 / i686'

    busSize = platform.architecture()[0]

    if not busSize:
        busSize = '64bit' if sys.maxsize == (2 ** 63 - 1) else '32bit'

    return f'{arch} ({busSize})'

def getCoreCount():
    global _GENERAL_DRIVER
    coreIds = set()

    for cpu in os.listdir(_GENERAL_DRIVER):
        if not re.fullmatch('^cpu[0-9]{1,3}$', cpu):
            continue

        coreId = readFile(f'{_GENERAL_DRIVER}/{cpu}/topology/core_id').strip()

        if coreId:
            coreIds.add(coreId)

    return cores if (cores := len(coreIds)) else None

def getThreadCount():
    return threads if (threads := grep(readFile('/proc/cpuinfo'), 'processor', count=True)) else None

def getClockBoost():
    global _CPUFREQ_DIR

    try:
        if 'boost' in os.listdir(_CPUFREQ_DIR):
            with open(f'{_CPUFREQ_DIR}/boost', 'r') as file:
                return 'active' if '1' in file.read() else 'not active'

    except:
        pass

    return 'not available'

def getMinimumClock():
    global _CPUFREQ_DIR, _GLOBAL_VARIABLES_TO_INIT

    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    return round(min(
        int(freq) for freq in terminal(f'cat {_CPUFREQ_DIR}/policy*/cpuinfo_min_freq').strip().split('\n')
    ) / 1000000, 2)

def getMaximumClock():
    global _CPUFREQ_DIR, _GLOBAL_VARIABLES_TO_INIT

    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    return round(max(
        int(freq) for freq in terminal(f'cat {_CPUFREQ_DIR}/policy*/cpuinfo_max_freq').strip().split('\n')
    ) / 1000000, 2)

def getAmdPState():
    global _GENERAL_DRIVER

    pStateDir = os.path.join(_GENERAL_DRIVER, 'amd_pstate')
    status = None
    prefcore = None

    if (pStateStatus := os.path.join(pStateDir, 'status')) and os.path.exists(pStateStatus):
        with open(pStateStatus, 'r') as file:
            status = file.read().strip()

    if (pStatePrefcore := os.path.join(pStateDir, 'prefcore')) and os.path.exists(pStatePrefcore):
        with open(pStatePrefcore, 'r') as file:
            prefcore = file.read().strip()

    return status, prefcore

def getBogoMips():
    values = grep(readFile('/proc/cpuinfo'), 'bogomips', ignoreCase=True)
    try:
        return sum(float(v.split(':')[1].strip()) for v in values) / len(values)

    except:
        return None

def getVirtualizationEnabled():
    return True if grep(readFile('/proc/cpuinfo'), 'svm', True) or grep(readFile('/proc/cpuinfo'), 'vmx', True) else False

def getFlags():
    flags = grep(readFile('/proc/cpuinfo'), 'flags', returnFirstMatch=True)

    if flags and ':' in flags:
        return flags.split(':')[1].strip()

    return None

def makeListStructure(stat):
    for index, line in enumerate(stat):
        splitted = line.split(' ')

        while '' in splitted:
            splitted.remove('')

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
    usage = {'total': 0}

    deltas = [
        beforeStat[i] - afterStat[i] for i in range(len(beforeStat))
    ]
    total = sum(deltas)

    for index, param in enumerate(deltas):
        usage[usageContexts[index]] = abs(round(param * 100 / total, 2))

    usage['total'] = round(100 - usage['idle'], 2)

    return usage

def getUsageStats():
    fileLines = grep(readFile('/proc/stat'), 'cpu', ignoreCase=True)
    lines = []

    for line in fileLines:
        prefixIndexes = re.match('cpu\\d*', line).span()
        prefix = line[prefixIndexes[0]:prefixIndexes[1]]
        lines.append(line.replace(prefix, ''))

    return lines

def cpuUsage():
    global usageContexts
    beforeStat = getUsageStats()
    time.sleep(0.25)
    afterStat = getUsageStats()

    try:
        beforeStat = makeListStructure(beforeStat)
        afterStat = makeListStructure(afterStat)
    except:
        return []

    if len(beforeStat) != usageContexts:
        usageContexts.extend([
            'steal', 'guest', 'guest_nice'
        ])

    usages = []
    for i in range(len(beforeStat)):
        usages.append(getParameterUsage(beforeStat[i], afterStat[i]))

    return usages

def cpuFrequency():
    global _CPUFREQ_DIR
    lines = grep(readFile('/proc/cpuinfo'), 'cpu MHz')
    frequencies = []

    if lines is not None:
        for line in lines:
            frequencies.append(line.split(':')[1].strip())

    if not frequencies or frequencies == ['']:
        frequencies = []

        for policy in _POLICIES:
            try:
                freq = readFile(f'{_CPUFREQ_DIR}/{policy}/cpuinfo_cur_freq')

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
    global _GENERAL_DRIVER
    processors = {}

    for dir in os.listdir(_GENERAL_DRIVER):
        if dir.replace('cpu', '') and dir.replace('cpu', '')[0] not in string.ascii_letters:

            if 'topology' not in os.listdir(os.path.join(_GENERAL_DRIVER, dir)) or \
                    'core_id' not in os.listdir(os.path.join(_GENERAL_DRIVER, dir, 'topology')):
                return []
            processors[dir] = readFile(os.path.join(_GENERAL_DRIVER, dir, 'topology', 'core_id')).strip()

    res = []
    for processor in processorSort(processors.keys()):
        res.append(processors[processor])

    return res

def processorDieDistribution():
    global _GENERAL_DRIVER
    processors = {}

    for dir in os.listdir(_GENERAL_DRIVER):
        if dir.replace('cpu', '') and dir.replace('cpu', '')[0] not in string.ascii_letters:

            if 'topology' not in os.listdir(os.path.join(_GENERAL_DRIVER, dir)) or \
                    'die_id' not in os.listdir(os.path.join(_GENERAL_DRIVER, dir, 'topology')):
                return None

            with open(os.path.join(_GENERAL_DRIVER, dir, 'topology', 'die_id'), 'r') as file:
                processors[dir] = file.read().strip()

    res = []
    for processor in processorSort(processors.keys()):
        res.append(processors[processor])

    return res

def cpuCache():
    global _GENERAL_DRIVER

    cpuDirs = grep(os.listdir(_GENERAL_DRIVER), 'cpu', ignoreCase=True)  # terminal('ls /sys/devices/system/cpu | grep -i cpu').split('\n')

    if 'cpufreq' in cpuDirs:
        cpuDirs.remove('cpufreq')

    if 'cpuidle' in cpuDirs:
        cpuDirs.remove('cpuidle')

    cpuCache = {}
    for cpu in cpuDirs:
        cpuCache[cpu] = {}

        for cacheIndex in grep(os.listdir(f'{_GENERAL_DRIVER}/{cpu}/cache'), 'index', ignoreCase=True):
            try:
                size = readFile(f'{_GENERAL_DRIVER}/{cpu}/cache/{cacheIndex}/size').strip()
            except:
                size = 'unknown'

            level = readFile(f'{_GENERAL_DRIVER}/{cpu}/cache/{cacheIndex}/level')
            sharing = readFile(f'{_GENERAL_DRIVER}/{cpu}/cache/{cacheIndex}/shared_cpu_list')

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
    global _GLOBAL_VARIABLES_TO_INIT
    if _GLOBAL_VARIABLES_TO_INIT:
        initGlobalVariables()

    dict = {}

    dict["model name"] = getModelName()
    dict['architecture'] = getArchitecture()
    dict['byte order'] = getByteOrder()[0]

    dict['core count'] = int(getCoreCount())
    dict['thread count'] = int(getThreadCount())

    dict['clock boost'] = getClockBoost()
    dict['bogomips'] = getBogoMips()

    dict['minimum frequency'] = int(float(getMinimumClock()) * 1000)
    dict['maximum frequency'] = int(float(getMaximumClock()) * 1000)

    dict['governors'] = [governor for governor in _GOVERNORS]
    dict['scaling frequencies'] = [int(frequency) for frequency in _FREQUENCIES]
    dict['energy performance preferences'] = [epp for epp in _ENERGY_PERFORMANCE_PREFERENCES]

    status, prefcore = getAmdPState()

    dict['amd-p-state-status'] = status
    dict['amd-p-state-prefcore'] = prefcore

    scalingFrequencies = getCurrentScalingFrequencies()
    governors = getCurrentScalingGovernors()

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

if __name__ == '__main__':
    print(cpuUsage())