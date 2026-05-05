from .util import readFile, grep
from .static_const import GENERAL_DRIVER

import os
import string

def getThreadDistribution():
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

    cpuDirs = grep(os.listdir(GENERAL_DRIVER), 'cpu', ignoreCase=True)
    if not isinstance(cpuDirs, list):
        return {}

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
                linearRange.append(int(addition))
            return linearRange

        else:
            end = int(splittedRange[1])

            return list(range(start, end + 1))
    return list(int(element) for element in processorRange.split(','))

def processorSort(processors):
    return sorted(processors, key=lambda processor: int(''.join([chr for chr in processor if chr in '0123456789'])))