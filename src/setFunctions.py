from lib_cputil import *

def set(argParser):
    cpu = True

    if os.getuid():
        print('Setting requires root privilegies', file=sys.stderr)
        sys.exit(0)

    if argParser.setGovernor:
        if argParser.cpu:
            cpu = int(argParser.cpu)

        if not setScalingGovernor(argParser.setGovernor, cpu):
            print('Error setting governor')
            sys.exit(1)

    elif argParser.setFrequency:
        if argParser.cpu:
            cpu = int(argParser.cpu)

        if (freq := argParser.setFrequencyMaximum):
            if not setMaximumScalingFrequency(freq, cpu):
                print('Error setting maximum scaling frequency')
                sys.exit(1)

        elif (freq := argParser.setFrequencyMinimum):
            if not setMinimumScalingFrequency(freq, cpu):
                print('Error setting minimum scaling frequency')
                sys.exit(1)

    elif argParser.setEnergyPerformancePreference:
        if argParser.cpu:
            cpu = int(argParser.cpu)

        if not setEnergyPerformancePreference(argParser.setEnergyPerformancePreference, cpu):
            print('Error setting energy performance preference')
            sys.exit(1)

    elif argParser.setClocksource:
        if not setClockSource(argParser.setClocksource):
            print('Error setting clocksource')
            sys.exit(1)

    elif argParser.setIdleState:
        setCpuCstateEnabled(argParser.setIdleState, argParser.setIdleStateEnabled)

def loadConf(argParser):
    if os.path.isabs(argParser.loadFileName):
        filePath = argParser.loadFileName

    else:
        if not argParser.loadFileName.endswith('.conf'):
            argParser.loadFileName += '.conf'

        filePath = os.path.join("/etc/cputild/templates", argParser.loadFileName)

    if not os.path.exists(filePath):
        print(f'Error: no such file `{filePath}`')
        sys.exit(1)

    governor, scalingMinFreq, scalingMaxFreq, energyPerformancePreference, _, clocksource = parseConf(filePath)

    if governor and governor != "auto":
        if not setScalingGovernor(governor, True):
            print('Error setting governor')
            sys.exit(1)

    if scalingMinFreq and scalingMinFreq != "auto":
        if not setMinimumScalingFrequency(scalingMinFreq, True):
            print('Error setting minimum scaling frequency')
            sys.exit(1)

    if scalingMaxFreq and scalingMaxFreq != "auto":
        if not setMaximumScalingFrequency(scalingMaxFreq, True):
            print('Error setting maximum scaling frequency')
            sys.exit(1)

    if energyPerformancePreference and energyPerformancePreference != "auto":
        if not setEnergyPerformancePreference(energyPerformancePreference, True):
            print('Error setting energy performance preference')
            sys.exit(1)

    if clocksource and clocksource != "auto":
        if not setClockSource(clocksource):
            print('Error setting clocksource')
            sys.exit(1)
