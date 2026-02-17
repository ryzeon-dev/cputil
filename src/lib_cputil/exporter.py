from .cpu_topology import cpuCache, getThreadDistribution, processorDieDistribution, processorSort, processorsFromRange

from .cpu_info import (
    getModelName, getArchitecture, getByteOrder, getCoreCount, getThreadCount, getClockBoost, getBogoMips, getMinimumClock, getMaximumClock, getAmdPState
)

from .scaling import (
    getAllGovernors, getAllFrequencies, getAllEnergyPerformancePreferences, getCurrentScalingFrequencies,
    getCurrentScalingGovernors, getCurrentEnergyPerformancePreferences
)

from .temperature import getCpuTemperature

from .cpu_usage import cpuUsage, cpuFrequency

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
    dict['bogomips'] = getBogoMips()

    dict['minimum frequency'] = int(float(getMinimumClock()) * 1000)
    dict['maximum frequency'] = int(float(getMaximumClock()) * 1000)

    dict['governors'] = [governor for governor in getAllGovernors()]
    dict['scaling frequencies'] = [int(frequency) for frequency in getAllFrequencies()]
    dict['energy performance preferences'] = [epp for epp in getAllEnergyPerformancePreferences()]

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

    threadDist = getThreadDistribution()
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
            'energy performance preference': ''
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

    try:
        temperatureReadings = getCpuTemperature()
    except:
        pass
    else:
        dict['temperature'] = temperatureReadings

    return dict

if __name__ == '__main__':
    print(getCpuTemperature())