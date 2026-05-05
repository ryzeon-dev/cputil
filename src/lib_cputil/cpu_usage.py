import time
from .util import grep, readFile
from .sysfs_const import getAllPolicies
from .static_const import *

import re

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
        usage[usageContexts[index]] = 0 if total == 0 else abs(round(param * 100 / total, 2))

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

    if len(beforeStat[0]) != len(usageContexts):
        usageContexts.extend([
            'steal', 'guest', 'guest_nice'
        ])

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

        for policy in getAllPolicies():
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

        avg = 0 if len(nonZeroFreqs) == 0 else round(sum(nonZeroFreqs) / len(nonZeroFreqs), 2)
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
