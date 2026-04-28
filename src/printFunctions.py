import signal
import time

from lib_cputil import *

def printHelp(version):
    print(f'cputil: cpu utils CLI v{version}')
    print('usage: cputil [COMMAND arg [OPTION]]')
    print('\nCommands:')
    print('    set governor (sg) GOVERNOR               Set scaling governor (root)')
    print('    set frequency minimum (sfm) FREQUENCY    Set minimum scaling frequency (root)')
    print('    set frequency maximum (sfM) FREQUENCY    Set maximum scaling frequency (root)')
    print('    set energy preference (sep) PREFERENCE   Set energy performance preference (root)')
    print('    set clocksource (sc) CLOCKSOURCE         Set clocksource (root)')
    print('    set cstate (sC) STATE (enabled|disabled) Set idle C-State enabled/disabled (root)')
    print('    max                                      Set "performance" governor, set both minimum')
    print('                                             and maximum scaling frequency to highest allowed value')
    print('                                             and set energy performance preference to "performance" (root)')
    print('    min                                      Set "powersave" governor, set both minimum')
    print('                                             and maximum scaling frequency to lowest allowed value')
    print('                                             and set energy performance preference to "power" (root)')
    print('    load (l) CONF_FILE                       Loads template file configuration; CONF_FILE can either be')
    print('                                             a filepath or the name of a file located in the templates')
    print('                                             directory at /etc/cputild/templates/ (root)')
    print()

    print('    all          (a)                         Show all available information')
    print('    info         (i)                         Show CPU info (default)')
    print('    scaling      (s)                         Show scaling settings')
    print('    topology     (t)                         Show CPU topology')
    print('    temperature  (T)                         Show CPU temperature sensors')
    print('    usage        (u)                         Show CPU usage')
    print('    energy       (e)                         Show CPU energy consumption')
    print('    prefcore     (p)                         Show CPU prefcore ranking')
    print('    cstate       (c)                         Show CPU C-State usage')
    print('    vuln         (v)                         Show CPU vulnerabilities and if the processor is affected')
    print('    watch        (w)                         Show continuous cpu usage reading')
    print()

    print('    dump         (d)                         Show currently loaded cputild configuration')
    print('    json         (j)                         Output all available information in JSON format')
    print('    yaml         (y)                         Output all available information in YAML format')
    print()

    print('    version      (V)                         Show version')
    print('    help         (h)                         Show this message and exit')
    print('\nOptions:')
    print('    -cpu CPU                            Select which logical processor to affect with setting action')
    print('                                        Works only with "set governor", "set frequency minimum" ')
    print('                                        and "set frequency maximum"')
    print('    -avg                                Show only average usage, to be used with "usage"')

def printScaling():
    print('Available scaling governors:')

    for governor in getAllGovernors():
        print(f'\t{governor}')

    if getAllFrequencies() is not None:
        print('\nAvailable scaling frequencies:')

        for frequency in getAllFrequencies():
            print(f'\t{frequency}')

    if getAllEnergyPerformancePreferences():
        print('\nEnergy performance preferences:')

        for preference in getAllEnergyPerformancePreferences():
            print(f'\t{preference}')

    if getAllClocksources() is not None:
        print('\nClocksources:')

        for clocksource in getAllClocksources():
            print(f'\t{clocksource}')

    scalingDriver = getCurrentScalingDriver()
    print(f'\nCurrent scaling driver: {scalingDriver}')

    try:
        currentClocksource = getCurrentClocksource()
        print(f'\nCurrent clocksource: {currentClocksource}')
    except:
        pass

    print("\nCurrent status:")

    try:
        freqs = getCurrentScalingFrequencies()

    except:
        freqs = {}

    try:
        energyPerformance = getCurrentEnergyPerformancePreferences()

    except:
        energyPerformance = {}

    for policy, governor in getCurrentScalingGovernors().items():
        line = f'Processor {policy.replace("policy", ""):>2}:\t{governor} governor'

        if (policyFreqs := freqs.get(policy)) is not None:
            line += f'    frequency max = {policyFreqs["max"]}, min = {policyFreqs["min"]}'

        if (energyPreference := energyPerformance.get(policy)) is not None:
            line += f'    energy preference = {energyPreference}'

        print(line)

def printInfo():
    model = getModelName()
    prefixSize = 24

    if model:
        print(f'Model name:'.ljust(prefixSize) + model)

    print(f'Architecture:'.ljust(prefixSize) + getArchitecture())

    byteOrder, firstBit = getByteOrder()
    if byteOrder:
        print(f'Byte order:'.ljust(prefixSize) + f'{byteOrder} (first bit is {firstBit})')

    coreCount = getCoreCount()
    if coreCount:
        print(f'Cores count:'.ljust(prefixSize) + f'{coreCount}')

    threadCount = getThreadCount()
    if threadCount:
        print(f'Threads count:'.ljust(prefixSize) + f'{threadCount}')

    print(f'Clock boost:'.ljust(prefixSize) + getClockBoost())

    try:
        print(f'Minimum clock:'.ljust(prefixSize) + f'{getMinimumClock()} GHz')
    except:
        pass

    try:
        print(f'Maximum clock:'.ljust(prefixSize) + f'{getMaximumClock()} GHz')
    except:
        pass

    if (bogomips := getBogoMips()):
        print(f'BogoMIPS:'.ljust(prefixSize) + str(round(bogomips, 2)))

    print(f'Virtualization:'.ljust(prefixSize) + ('not ' if not getVirtualizationEnabled() else '') + 'enabled')

    amdPStateStatus, amdPStatePrefcore = getAmdPState()

    if amdPStateStatus is not None:
        print(f'AMD P-State status:'.ljust(prefixSize) + amdPStateStatus)

    if amdPStatePrefcore is not None:
        print(f'AMD P-State prefcore:'.ljust(prefixSize) + amdPStatePrefcore)

    if (flags := getFlags()):
        print(f'Flags:'.ljust(prefixSize) + flags)

def printTopology():
    threadCount = getThreadCount()

    try:
        cache = cpuCache()
    except:
        sys.exit(0)

    try:
        threadDistribution = getThreadDistribution()
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

def printUsage(argParser):
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
            print(f'    {(label + ":").ljust(20)}{percent} %')

        if frequencies:
            print(f'    Frequency:\t\t{frequency} MHz')

    else:
        print('Average:')

        for label, percent in usages[0].items():
            print(f'    {(label + ":").ljust(20)}{percent} %')

        if averageFrequency:
            print(f'    Frequency:\t\t{averageFrequency} MHz')

        if not argParser.avg:
            for policy, thread in enumerate(usages[1:]):
                print(f'\nProcessor: {policy}')

                for label, percent in thread.items():
                    print(f'    {(label + ":").ljust(20)}{percent} %')

                if frequencies and policy < len(frequencies):
                    print(f'    Frequency: \t\t{frequencies[policy]} MHz')

def printTemperature():
    try:
        temperatureReadings = getCpuTemperature()

    except:
        print('Error getting cpu temperature')
        sys.exit(1)

    for sensorName, value in temperatureReadings.items():
        print(f'{sensorName}: {value} C')

def printWatchUsage():
    def sigint_handler(*_):
        global run_watch
        run_watch = False

    signal.signal(signal.SIGINT, sigint_handler)

    # try:
    while run_watch:
        before = time.time()

        usages = cpuUsage()
        averageFrequency, frequencies = cpuFrequency()

        try:
            temperatureReadings = getCpuTemperature()
        except:
            temperatureReadings = None

        lines = ['Average Usage:']
        longestLine = -1

        for label, percent in usages[0].items():
            line = f'    {(label + ":").ljust(20)}{percent} %'
            longestLine = max(longestLine, len(line))
            lines.append(line)

        if averageFrequency:
            line = f'    Frequency:\t\t{averageFrequency} MHz'
            longestLine = max(longestLine, len(line))
            lines.append(line)

        if temperatureReadings is not None:
            lines.append('Average Temperature:')
            for sensor, value in temperatureReadings.items():
                line = f'    {sensor}:\t\t{value} C'
                longestLine = max(longestLine, len(line))
                lines.append(line)

        lineCount = len(lines)
        for line in lines:
            print(line.ljust(longestLine))

        print(f'\r\x1b[{lineCount + 1}A\x1b[999C')

        after = time.time()
        time.sleep(1 - (after - before))

    print()

def printConfigDump():
    try:
        with open('/etc/cputild/cputild.conf', 'r') as file:
            conf = file.read()
    except:
        print('Error reading currently loaded configuration')
        sys.exit(1)

    print('Currently loaded configuration:\n')
    print(conf)

def printEnergy():
    try:
        energyConsumption = getCpuEnergyConsumption()
    except PermissionError:
        print('Error: permission denied. Retry as root')
        sys.exit(1)

    except:
        print('Error getting energy consumption')
        sys.exit(1)

    print(f'Intel RAPL: {"enabled" if energyConsumption.intelRaplEnabled else "disabled"}')
    if not energyConsumption.sensors:
        sys.exit(0)

    print('Sensors:')
    for entry in energyConsumption.sensors:
        print(f'    {entry.name}: {entry.energyJ} J/s')

def printPrefcore():
    try:
        prefcoreInfo = getCpuPrefcores()

    except:
        print('Error getting CPU prefcore')
        sys.exit(1)

    if not prefcoreInfo:
        print('Error: prefcore info not available in this system')
        sys.exit(1)

    maxPrefcore = max(prefcore.ranking for prefcore in prefcoreInfo)

    for prefcore in sorted(prefcoreInfo, key=lambda p: p.coreId):
        print(f'Core {prefcore.coreId:>2} [CCD{prefcore.dieId}]: {prefcore.ranking}' + (
            "  [preferred]" if prefcore.ranking == maxPrefcore else ""))

def printCstate():
    try:
        cstates, coreCstates = getCpuCstates()
    except Exception as e:
        print('Error getting CPU C-State info')
        sys.exit(1)

    print('States:')
    for state in sorted(cstates, key=lambda c: c.name):
        print(f'  {state.name:<4} -> {state.desc} [latency: {state.latency}]')

    print()
    print('Percent values since boot\n')
    for coreCstate in sorted(coreCstates, key=lambda c: c.coreId):
        print(
            f'Core {coreCstate.coreId:>2}    ' + '    '.join(
                f'{state.name} [{"enabled" if state.enabled else "disabled"}]: '
                f'{(f"{(state.time * 100 / coreCstate.total):.2f}").rjust(6)} %' for state in
                sorted(coreCstate.coreCstates, key=lambda c: c.name)
            )
        )

def printVulnerabilities():
    try:
        vulnInfo = getCpuVulnerabilities()

    except:
        print('Error getting CPU vulnerabilities')
        sys.exit(1)

    maxVulnLength = len(max([vuln.name for vuln in vulnInfo], key=len))

    for vuln in vulnInfo:
        print(f'{vuln.name.ljust(maxVulnLength)} -> {vuln.status}')