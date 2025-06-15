from argparser import ArgParse

from lib_cputil import *
import json

VERSION = '5.0.1'

if __name__ == '__main__':
    args = sys.argv[1:]
    cpu = True

    argParser = ArgParse()
    argParser.parse(args)

    if argParser.noArg:
        print('Available governors:')

        for governor in GOVERNORS:
            print(f'\t{governor}')

        if FREQUENCIES is not None:
            print('\nAvailable scaling frequencies:')

            for frequency in FREQUENCIES:
                print(f'\t{frequency}')

        if ENERGY_PERFORMANCE_PREFERENCES:
            print('\nEnergy performance preferences:')

            for preference in ENERGY_PERFORMANCE_PREFERENCES:
                print(f'\t{preference}')

        print("\nCurrent status:")

        try:
            freqs = getCurrentScalingFrequencies()

        except:
            freqs = {}

        try:
            energyPerformance = getCurrentEnergyPerformancePreferences()

        except:
            energyPerformance = {}

        for policy, governor in getCurrentGovernors().items():
            line = f'Processor {policy.replace("policy", "")}:\t{governor} governor'

            if (policyFreqs := freqs.get(policy)) is not None:
                line += f'    frequency max = {policyFreqs["max"]}, min = {policyFreqs["min"]}'

            if (energyPreference := energyPerformance.get(policy)) is not None:
                line += f'    energy preference = {energyPreference}'

            print(line)

    elif argParser.help:
        print(f'cputil: cpu utils CLI v{VERSION}')
        print('usage: cputil [COMMAND arg[OPTION]]')
        print('\nCommands:')
        print('    set governor (sg) GOVERNOR               Set scaling governor (root)')
        print('    set frequency minimum (sfm) FREQUENCY    Set minimum scaling frequency (root)')
        print('    set frequency maximum (sfM) FREQUENCY    Set maximum scaling frequency (root)')
        print('    set energy preference (sep) PREFERENCE   Set energy performance preference (root)')
        print('    max                                      Set "performance" governor, set both minimum')
        print('                                             and maximum scaling frequency to highest allowed value')
        print('                                             and set energy performance preference to "performance" (root)')
        print('    min                                      Set "powersave" governor, set both minimum')
        print('                                             and maximum scaling frequency to lowest allowed value')
        print('                                             and set energy performance preference to "power" (root)')
        print('    info                                     Show CPU info')
        print('    usage                                    Show CPU usage')
        print('    json                                     Output all available information in JSON format')
        print('    version                                  Show version')
        print('    help                                     Show this message and exit')
        print('\nOptions:')
        print('    -cpu CPU                            Select which logical processor to affect with setting action')
        print('                                        Works only with "set governor", "set frequency minimum" ')
        print('                                        and "set frequency maximum"')
        print('    -g                                  Show general info only, to be used with "info"')
        print('    -avg                                Show only average usage, to be used with "usage"')

    elif argParser.json:
        print(json.dumps(jsonFormat()))

    elif argParser.info:
        model = getModelName()
        if model:
            print(f'Model name:\t\t{model}')

        print(f'Architecture:\t\t{getArchitecture()}')

        byteOrder, firstBit = getByteOrder()
        if byteOrder:
            print(f'Byte order:\t\t{byteOrder} (first bit is {firstBit})')

        coreCount = getCoreCount()
        if coreCount:
            print(f'Cores count:\t\t{coreCount}')

        threadCount = getThreadCount()
        if threadCount:
            print(f'Threads count:\t\t{threadCount}')

        print(f'Clock boost:\t\t{getClockBoost()}')

        try:
            print(f'Minimum clock:\t\t{getMinimumClock()} GHz')
        except:
            pass

        try:
            print(f'Maximum clock:\t\t{getMaximumClock()} GHz')
        except:
            pass

        amdPStateStatus, amdPStatePrefcore = getAmdPState()

        if amdPStateStatus is not None:
            print(f'AMD P-State status:\t{amdPStateStatus}')

        if amdPStatePrefcore is not None:
            print(f'AMD P-State prefcore:\t{amdPStatePrefcore}')

        if argParser.general:
            sys.exit(0)

        try:
            cache = cpuCache()
        except:
            sys.exit(0)

        try:
            threadDistribution = threadDistribution()
        except:
            threadDistribution = None

        try:
            dieDistribution = processorDieDistribution()
        except:
            dieDistribution = None

        for policy, processor in enumerate(processorSort(cache.keys())):
            print(f'\nProcessor {policy}:')

            for cacheLevel in cache[processor]:
                sharing = processorsFromRange(cache[processor][cacheLevel]["shared"])

                if len(sharing) == int(threadCount):
                    sharing = ['all']

                else:
                    try:
                        sharing.remove(policy)

                    except:
                        pass

                    if not sharing:
                        sharing = ['none']

                amount = cache[processor][cacheLevel]["amount"]

                print(
                    f'    L{cacheLevel} cache: {amount} KB\tshared with processor(s): {", ".join(str(processor) for processor in sharing)}')

            if threadDistribution is not None:
                print(f'    Physical core: {threadDistribution[policy]}')

            if dieDistribution is not None:
                print(f'    Physical die: {dieDistribution[policy]}')

    elif argParser.usage:
        try:
            usages = cpuUsage()
            averageFrequency, frequencies = cpuFrequency()

        except:
            sys.exit(0)

        if argParser.cpu:
            cpuIndex = argParser.cpu

            usage = usages[int(cpuIndex) + 1]
            if frequencies:
                frequency = frequencies[int(cpuIndex)]

            print(f'Processor: {cpuIndex}')
            for label, percent in usage.items():
                indent = '\t'

                if len(label) <= 9:
                    indent += '\t'

                print(f'    {label}:{indent}{percent} %')

            if frequencies:
                print(f'    Frequency:\t\t{frequency} MHz')

        else:
            print('Average:')

            for label, percent in usages[0].items():
                indent = '\t'

                if len(label) <= 9:
                    indent += '\t'

                print(f'    {label}:{indent}{percent} %')

            if averageFrequency:
                print(f'    Frequency:\t\t{averageFrequency} MHz')

            if not argParser.avg:
                for policy, thread in enumerate(usages[1:]):
                    print(f'\nProcessor: {policy}')

                    for label, percent in thread.items():
                        indent = '\t'

                        if len(label) <= 9:
                            indent += '\t'

                        print(f'    {label}:{indent}{percent} %')

                    if frequencies and policy < len(frequencies):
                        print(f'    Frequency: \t\t{frequencies[policy]} MHz')

    elif argParser.set:
        if os.getuid():
            print('Governor setting requires root privilegies', file=sys.stderr)
            sys.exit(0)

        if argParser.setGovernor:
            if argParser.cpu:
                cpu = int(argParser.cpu)

            if not setGovernor(argParser.setGovernor, cpu):
                print('Error setting governor')

        elif argParser.setFrequency:
            frequency = None

            if argParser.cpu:
                cpu = int(argParser.cpu)

            if (freq := argParser.setFrequencyMaximum):
                setMaximumScalingFrequency(freq, cpu)

            elif (freq := argParser.setFrequencyMinimum):
                setMinimumScalingFrequency(freq, cpu)

        elif argParser.setEnergyPerformancePreference:
            if argParser.cpu:
                cpu = int(argParser.cpu)

            preference = setEnergyPerformancePreference(argParser.setEnergyPerformancePreference, cpu)

    elif argParser.version:
        print(f'cputil v{VERSION}')

    elif argParser.min:
        minAll()

    elif argParser.max:
        maxAll()