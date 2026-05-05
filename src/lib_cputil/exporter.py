from .cpu_vulnerabilities import getCpuVulnerabilities
from .cpu_prefcore import getCpuPrefcores
from .cpu_energy_consumption import getCpuEnergyConsumption
from .cpu_cstate import getCpuCstates
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

    dict["model_name"] = getModelName()
    dict['architecture'] = getArchitecture()
    dict['byte_order'] = getByteOrder()[0]

    dict['core_count'] = int(getCoreCount())
    dict['thread_count'] = int(getThreadCount())

    dict['clock_boost'] = getClockBoost()
    dict['bogomips'] = getBogoMips()

    dict['minimum_frequency'] = int(float(getMinimumClock()) * 1000)
    dict['maximum_frequency'] = int(float(getMaximumClock()) * 1000)

    dict['governors'] = [governor for governor in getAllGovernors()]
    dict['scaling_frequencies'] = [int(frequency) for frequency in getAllFrequencies()]
    dict['energy_performance_preferences'] = [epp for epp in getAllEnergyPerformancePreferences()]

    status, prefcore = getAmdPState()

    dict['amd_p_state_status'] = status
    dict['amd_p_state_prefcore'] = prefcore

    scalingFrequencies = getCurrentScalingFrequencies()
    governors = getCurrentScalingGovernors()

    usages = cpuUsage()
    averageFrequency, frequencies = cpuFrequency()

    try:
        cache = cpuCache()

    except:
        cache = {}

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
            'minimum_scaling_frequency': '',
            'maximum_scaling_frequency': '',
            'governor': '',
            'energy_performance_preference': ''
        }

        try:
            scaling = scalingFrequencies[f'policy{index}']
            dict[processorId]['minimum_scaling_frequency'] = int(scaling['min'])
            dict[processorId]['maximum_scaling_frequency'] = int(scaling['max'])

        except:
            pass

        try:
            governor = governors[f'policy{index}']
            dict[processorId]['governor'] = str(governor)

        except:
            pass

        try:
            preference = energyPerformancePreferences[f'policy{index}']
            dict[processorId]['energy_performance_preference'] = str(preference)

        except:
            pass

        for label, percent in processor.items():
            dict[processorId]['usage'][label] = float(percent)

        dict[processorId]['frequency'] = int(frequencies[index]) if frequencies and index < len(frequencies) and frequencies[index] is not None else ''
        if threadDist:
            dict[processorId]['physical_core'] = int(threadDist[index])

        if dieDist:
            dict[processorId]['physical_die'] = int(dieDist[index]) if dieDist else ''

        if sortedCache:
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

    try:
        cstates, coreCstates = getCpuCstates()
    except:
        pass
    else:
        dict['cstates'] = [cstate.toJson() for cstate in cstates]
        dict['core_cstates'] = [coreCstate.toJson() for coreCstate in coreCstates]

    try:
        energyConsumption = getCpuEnergyConsumption()
    except:
        pass
    else:
        if energyConsumption is not None:
            dict['energy_consumption'] = energyConsumption.toJson()

    try:
        prefcores = getCpuPrefcores()
    except:
        pass
    else:
        dict['prefcores'] = [prefcore.toJson() for prefcore in prefcores]

    try:
        vulnerabilities = getCpuVulnerabilities()
    except:
        pass
    else:
        dict['vulnerabilities'] = [vulnerability.toJson() for vulnerability in vulnerabilities]

    return dict

if __name__ == '__main__':
    print(getCpuTemperature())