from .util import *
from .static_const import *

import os
import sys
import re


def getPolicies():
    global CPUFREQ_DIR

    try:
        policies = grep(os.listdir(CPUFREQ_DIR), 'policy')
    except:
        print('Error: cannot read cpufreq\'s sysfs')
        sys.exit(1)

    if isinstance(policies, str):
        return [policies]
    return sorted(policies, key=lambda x: int(x.replace('policy', '')))

def writePolicyFile(policy, file, content):
    global CPUFREQ_DIR

    try:
        with open(os.path.join(CPUFREQ_DIR, policy, file), 'w') as file:
            file.write(content)

    except:
        print('Error: cannot write to cpufreq\'s sysfs')
        return False

    return True

### SYSFS CONST READER ###

def _readScalingFrequencies():
    global CPUFREQ_CONTENT, CPUFREQ_DIR

    frequencies = set()
    frequencyFiles = ['scaling_max_freq', 'scaling_min_freq', 'scaling_available_frequencies',
                      'amd_pstate_lowest_nonlinear_freq', 'amd_pstate_max_freq', 'cpuinfo_max_freq', 'cpuinfo_min_freq']

    for e in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(CPUFREQ_DIR, e)

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

def _findAvailableGovernors():
    global CPUFREQ_CONTENT, CPUFREQ_DIR

    governors = set()
    governorFiles = ['scaling_available_governors']

    for e in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', e):
            continue

        policyPath = os.path.join(CPUFREQ_DIR, e)

        for file in governorFiles:
            filePath = os.path.join(policyPath, file)
            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for governor in file.read().strip().split(' '):
                    governors.add(governor)

    return list(governors)

def _getEnergyPerformancePreferences():
    global CPUFREQ_CONTENT, CPUFREQ_DIR

    preferences = set()
    preferenceFiles = ['energy_performance_available_preferences', 'energy_performance_preference']

    for policy in CPUFREQ_CONTENT:
        if not re.fullmatch('^policy[0-9]{1,3}$', policy):
            continue

        for preferenceFile in preferenceFiles:
            filePath = os.path.join(CPUFREQ_DIR, policy, preferenceFile)

            if not os.path.exists(filePath):
                continue

            with open(filePath, 'r') as file:
                for chunk in file.read().strip().split(' '):
                    preferences.add(chunk)

    return list(preferences)

def _getClocksources():
    global CLOCKSOURCE_DIR

    with open(os.path.join(CLOCKSOURCE_DIR, 'available_clocksource'), 'r') as file:
        sources = file.read()

    clocksources = set(sources.strip().split(' '))
    return list(clocksources)

### SYSFS CONST ###

try:
    CPUFREQ_CONTENT = os.listdir(CPUFREQ_DIR)

except Exception as e:
    print('Error: cannot access cpufreq\'s sysfs')
    exit(1)

_GLOBAL_VARIABLES_TO_INIT = True
_POLICIES = None
_FREQUENCIES = None
_GOVERNORS = None
_ENERGY_PERFORMANCE_PREFERENCES = None
_CLOCKSOURCES = None

def _initGlobalVariables():
    global _POLICIES, _FREQUENCIES, _GOVERNORS, _ENERGY_PERFORMANCE_PREFERENCES, _GLOBAL_VARIABLES_TO_INIT, _CLOCKSOURCES
    try:
        _POLICIES = getPolicies()
        _FREQUENCIES = _readScalingFrequencies()
        _GOVERNORS = _findAvailableGovernors()
        _ENERGY_PERFORMANCE_PREFERENCES = _getEnergyPerformancePreferences()
        _CLOCKSOURCES = _getClocksources()

    except:
        print('Error: cannot read scaling information')
        sys.exit(1)

### CONST GETTERS ###

def getAllPolicies():
    if _GLOBAL_VARIABLES_TO_INIT:
        _initGlobalVariables()

    return _POLICIES

def getAllGovernors():
    if _GLOBAL_VARIABLES_TO_INIT:
        _initGlobalVariables()

    return _GOVERNORS

def getAllFrequencies():
    if _GLOBAL_VARIABLES_TO_INIT:
        _initGlobalVariables()

    return _FREQUENCIES

def getAllEnergyPerformancePreferences():
    if _GLOBAL_VARIABLES_TO_INIT:
        _initGlobalVariables()

    return _ENERGY_PERFORMANCE_PREFERENCES

def reloadEnergyPerformancePreferences():
    global _ENERGY_PERFORMANCE_PREFERENCES

    _ENERGY_PERFORMANCE_PREFERENCES = _getEnergyPerformancePreferences()

def getAllClocksources():
    if _CLOCKSOURCES is None:
        _initGlobalVariables()

    return _CLOCKSOURCES