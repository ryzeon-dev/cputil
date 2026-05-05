from .conf import confFilePath, editConf
from .sysfs_const import *

def writePolicyProperty(propertyName, propertyDescription, propertyFile, value, cpu, updateConf):
    if cpu is True:
        print(f'Setting {propertyDescription} for all processors to {value}')

        for policy in getAllPolicies():
            if not writePolicyFile(policy, propertyFile, value):
                return False

        if os.path.exists(confFilePath) and updateConf:
            editConf(confFilePath, **{propertyName: value})

        return True
    else:
        policy = f'policy{cpu}'

        if policy not in getAllPolicies():
            return False

        print(f'Setting {propertyName} for processor {cpu} to {value}')

        if not writePolicyFile(policy, propertyFile, value):
            return False

        return True

def setScalingGovernor(governor, cpu=True, updateConf=True):
    if governor not in getAllGovernors():
        print(f'Error: `{governor}` is not an available governor')
        return False

    return writePolicyProperty(
        propertyName='governor',
        propertyDescription='governor',
        propertyFile='scaling_governor',
        value=governor,
        cpu=cpu,
        updateConf=updateConf
    )

def setMinimumScalingFrequency(frequency, cpu, updateConf=True):
    if getAllFrequencies() is None:
        print(f'Error: cputil is unable to detect allowed scaling frequencies')
        return False

    if frequency not in getAllFrequencies():
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    return writePolicyProperty(
        propertyName='scalingMinFreq',
        propertyDescription='minimum scaling frequency',
        propertyFile='scaling_min_freq',
        value=frequency,
        cpu=cpu,
        updateConf=updateConf
    )

def setMaximumScalingFrequency(frequency, cpu, updateConf=True):
    if getAllFrequencies() is None:
        print(f'Error: cputil is unable to detect allowed scaling frequencies')
        return False

    if frequency not in getAllFrequencies():
        print(f'Error: `{frequency}` is not one of the allowed scaling frequencies')
        return False

    return writePolicyProperty(
        propertyName='scalingMaxFreq',
        propertyDescription='maximum scaling frequency',
        propertyFile='scaling_max_freq',
        value=frequency,
        cpu=cpu,
        updateConf=updateConf
    )

def setEnergyPerformancePreference(preference, cpu, updateConf=True):
    # changing governor requires reaload of energy performance preferences
    reloadEnergyPerformancePreferences()

    if getAllEnergyPerformancePreferences() is None:
        print(f'Error: cputil is unable to detect allowed energy performance preferences')
        return False

    if preference not in getAllEnergyPerformancePreferences():
        print(f'Error: `{preference}` is not one of the allowed energy performance preferences')
        return False

    return writePolicyProperty(
        propertyName='energyPerformancePreference',
        propertyDescription='energy performance preference',
        propertyFile='energy_performance_preference',
        value=preference,
        cpu=cpu,
        updateConf=updateConf
    )

def setClockSource(clocksource):
    global CLOCKSOURCE_DIR
    if getAllClocksources() is None:
        print(f'Error: cputil is unable to detect available clocksources')
        return False

    if clocksource not in getAllClocksources():
        print(f'Error: `{clocksource}` is not one of the allowed clocksources')
        return False

    print(f'Setting {clocksource} clock source')

    try:
        with open(os.path.join(CLOCKSOURCE_DIR, 'current_clocksource'), 'w') as file:
            file.write(clocksource)
    except:
        return False

    return True

def maxAll():
    maxScalingFrequency = str(max(int(freq) for freq in getAllFrequencies()))
    setScalingGovernor('performance', True)

    setMinimumScalingFrequency(maxScalingFrequency, True)
    setMaximumScalingFrequency(maxScalingFrequency, True)

    setEnergyPerformancePreference('performance', True)

def minAll():
    minScalingFrequency = str(min(int(freq) for freq in getAllFrequencies()))

    for governor in ['powersave', 'schedutil']:
        if governor in getAllGovernors():
            setScalingGovernor(governor, True)
            break

    setMinimumScalingFrequency(minScalingFrequency, True)
    setMaximumScalingFrequency(minScalingFrequency, True)

    setEnergyPerformancePreference('power', True)

def getCurrentScalingDriver() -> str:
    drivers = set()

    for policy in getAllPolicies():
        path = os.path.join(CPUFREQ_DIR, policy)
        driver = readFile(os.path.join(path, 'scaling_driver'))

        if driver:
            drivers.add(driver)

    return ','.join(drivers)

def getCurrentScalingGovernors() -> dict[str]:
    governors = {}
    for policy in getAllPolicies():
        governors[policy] = readFile(f'{CPUFREQ_DIR}/{policy}/scaling_governor').strip()

    return governors

def getCurrentScalingFrequencies() -> dict[str, dict[str, float]]:
    frequencies = {}

    for policy in getAllPolicies():
        try:
            frequencies[policy] = {
                'min': readFile(
                    f'{CPUFREQ_DIR}/{policy}/scaling_min_freq').strip() if 'scaling_min_freq' in os.listdir(
                    f'{CPUFREQ_DIR}/{policy}') else '',
                'max': readFile(
                    f'{CPUFREQ_DIR}/{policy}/scaling_max_freq').strip() if 'scaling_max_freq' in os.listdir(
                    f'{CPUFREQ_DIR}/{policy}') else ''
            }
        except:
            print('Error: cannot read cpufreq\'s sysfs')
            sys.exit(1)

    return frequencies

def getCurrentEnergyPerformancePreferences() -> dict[str, str]:
    global CPUFREQ_CONTENT
    currentEnergyPreferences = {}

    for policy in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', policy):
            continue

        filePath = os.path.join(CPUFREQ_DIR, policy, 'energy_performance_preference')
        if os.path.exists(filePath):
            with open(filePath, 'r') as file:
                currentEnergyPreferences[policy] = file.read().strip()

    return currentEnergyPreferences

def getCurrentClocksource() -> str:
    global CLOCKSOURCE_DIR

    with open(os.path.join(CLOCKSOURCE_DIR, 'current_clocksource'), 'r') as file:
        clocksource = file.read().strip()

    return clocksource