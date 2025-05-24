from lib_cputil import *
import json

VERSION = '4.1.0'

if __name__ == '__main__':
    args = sys.argv[1:]
    cpu = True

    if not args:
        print('Available governors:')

        for governor in GOVERNORS:
            print(f'\t{governor}')

        if FREQUENCIES is not None:
            print('\nAvailable scaling frequencies:')

            for frequency in FREQUENCIES:
                print(f'\t{frequency}')

        print("\nCurrent status:")
        try:
            freqs = getCurrentScalingFrequencies()

        except:
            pass

        else:
            for index, governor in getCurrentGovernors().items():
                print(
                    f'Processor {index.replace("policy", "")}: \t"{governor}" governor\tfrequency max = {freqs[index]["max"]}, min = {freqs[index]["min"]}')

    elif '-h' in args or '--help' in args:
        print(f'cputil: cpu utils CLI v{VERSION}')
        print('usage: cputil [OPTIONS]')
        print('\nOptions:')
        print('    -sg  --set-governor          GOVERNOR     Set governor (root)')
        print('    -sfm --set-minimum-frequency FREQUENCY    Set minimum frequency (root)')
        print('    -sfM --set-maximum-frequency FREQUENCY    Set maximum frequency (root)')
        print('    --maximum-performance                     Set "performace" governor and set both minimum')
        print('                                              and maximum scaling frequency to the max allowed value (root)')
        print('    -cpu CPU                                  Select which processor to affect with action,')
        print('                                              if omitted the action will affect all processors,')
        print('                                              to be used with -sg, -sfm, -sfM, -u')
        print('    -i   --info                               Show info about CPU')
        print('    -g                                        Show general info only, to be used only with -i')
        print('    -u   --usage                              Show CPU usage')
        print('    -avg                                      If specified, only average usage is shown,')
        print('                                              to be used only with -u')
        print('    -j   --json                               Output all the available information in json format')
        print('    -V   --version                            Show cputil version')
        print('    -h   --help                               Show this message and exit')

    elif '-j' in args or '--json' in args:
        print(json.dumps(jsonFormat()))

    elif '-i' in args or '--info' in args:
        model = getModelName()
        if model:
            print(f'Model name:\t{model}')

        print(f'Architecture:\t{getArchitecture()}')

        byteOrder, firstBit = getByteOrder()
        if byteOrder:
            print(f'Byte order:\t{byteOrder} (first bit is {firstBit})')

        coreCount = getCoreCount()
        if coreCount:
            print(f'Cores count:\t{coreCount}')

        threadCount = getThreadCount()
        if threadCount:
            print(f'Threads count:\t{threadCount}')

        print(f'Clock boost:\t{getClockBoost()}')

        try:
            print(f'Minimum clock:\t{getMinimumClock()} GHz')
        except:
            pass

        try:
            print(f'Maximum clock:\t{getMaximumClock()} GHz')
        except:
            pass

        if '-g' in args:
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

        for index, processor in enumerate(processorSort(cache.keys())):
            print(f'\nProcessor {index}:')

            for cacheLevel in cache[processor]:
                sharing = processorsFromRange(cache[processor][cacheLevel]["shared"])

                if len(sharing) == int(threadCount):
                    sharing = ['all']

                else:
                    try:
                        sharing.remove(index)

                    except:
                        pass

                    if not sharing:
                        sharing = ['none']

                amount = cache[processor][cacheLevel]["amount"]

                print(
                    f'    L{cacheLevel} cache: {amount} KB\tshared with processor(s): {", ".join(str(processor) for processor in sharing)}')

            if threadDistribution is not None:
                print(f'    Physical core: {threadDistribution[index]}')

            if dieDistribution is not None:
                print(f'    Physical die: {dieDistribution[index]}')

    elif '-u' in args or '--usage' in args:
        try:
            usages = cpuUsage()
            averageFrequency, frequencies = cpuFrequency()


        except KeyboardInterrupt:
            sys.exit(0)

        if '-cpu' in args:
            cpuIndex = args[args.index('-cpu') + 1]

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

            if '-avg' not in args:
                for index, thread in enumerate(usages[1:]):
                    print(f'\nProcessor: {index}')

                    for label, percent in thread.items():
                        indent = '\t'

                        if len(label) <= 9:
                            indent += '\t'

                        print(f'    {label}:{indent}{percent} %')

                    if frequencies and index < len(frequencies):
                        print(f'    Frequency: \t\t{frequencies[index]} MHz')

    elif '-sg' in args or '--set-governor' in args:
        if os.getuid():
            print('Governor setting requires root privilegies', file=sys.stderr)
            sys.exit(0)

        try:
            governor = args[args.index('-sg') + 1]
        except:
            governor = args[args.index('--set-governor') + 1]

        if '-cpu' in args:
            cpu = int(args[args.index('-cpu') + 1])

        if not setGovernor(governor, cpu):
            print('Error setting governor')

    elif '-sfm' in args or '--set-min-frequency' in args:
        if os.getuid():
            print('Scaling frequency setting requires root privilegies', file=sys.stderr)
            sys.exit(0)

        try:
            frequency = args[args.index('-sfm') + 1]
        except:
            frequency = args[args.index('--set-min-frequency') + 1]

        if '-cpu' in args:
            cpu = int(args[args.index('-cpu') + 1])

        if not setMinimumScalingFrequency(frequency, cpu):
            print('Error setting min frequency', file=sys.stderr)

    elif '-sfM' in args or '--set-max-frequency' in args:
        if os.getuid():
            print('Scaling frequency setting requires root privilegies', file=sys.stderr)
            sys.exit(0)

        try:
            frequency = args[args.index('-sfM') + 1]
        except:
            frequency = args[args.index('--set-max-frequency') + 1]

        if '-cpu' in args:
            cpu = int(args[args.index('-cpu') + 1])

        if not setMaximumScalingFrequency(frequency, cpu):
            print('Error setting max frequency', file=sys.stderr)

    elif '--maximum-performance' in args:
        if os.getuid():
            print('Setting cpu to max performance requires root privilegies', file=sys.stderr)
            sys.exit(0)

        try:
            maxAll()

        except Exception as e:
            print(f'Error setting cpu to max performance because of: {e}')
            sys.exit(1)

    elif '-V' in args or '--version' in args:
        print(f'cputil v{VERSION}')

    else:
        arg = args[0]

        if arg[0] == '-':
            print(f'Error: unrecognised option "{arg}"')

        else:
            print(f'Error: unrecognised argument "{arg}"')