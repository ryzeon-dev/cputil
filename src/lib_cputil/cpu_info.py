from .util import readFile, grep, terminal
from .static_const import GENERAL_DRIVER, CPUFREQ_DIR

import os
import sys
import platform
import re

def getModelName():
    procCpuinfo = readFile('/proc/cpuinfo').split('\n')
    modelName = grep(procCpuinfo, 'model name')

    if isinstance(modelName, list):
        modelName = modelName[0]

    if modelName is None:
        return ''

    name = modelName.split(':')[1].strip()

    return name

def getByteOrder():
    order = sys.byteorder

    if order == 'little':
        return 'Little Endian', 'LSB'

    elif order == 'big':
        return 'Big Endian', 'MSB'

    else:
        return '', ''

def getArchitecture():
    arch = platform.machine()

    if arch == 'x86_64':
        arch = 'amd64 / x86_64'

    elif arch == 'i386':
        arch = 'i386 / i686'

    elif arch == 'aarch64':
        arch = 'arm64 / aarch64'

    elif not arch:
        arch = 'amd64 / x86_64 ' if sys.maxsize == (2 ** 63 - 1) else 'i386 / i686'

    busSize = platform.architecture()[0]

    if not busSize:
        busSize = '64bit' if sys.maxsize == (2 ** 63 - 1) else '32bit'

    return f'{arch} ({busSize})'

def getCoreCount():
    global GENERAL_DRIVER
    coreIds = set()

    for cpu in os.listdir(GENERAL_DRIVER):
        if not re.fullmatch('^cpu[0-9]{1,3}$', cpu):
            continue

        coreId = readFile(f'{GENERAL_DRIVER}/{cpu}/topology/core_id').strip()

        if coreId:
            coreIds.add(coreId)

    return cores if (cores := len(coreIds)) else None

def getThreadCount():
    return threads if (threads := grep(readFile('/proc/cpuinfo'), 'processor', count=True)) else None

def getClockBoost():
    global CPUFREQ_DIR

    try:
        if 'boost' in os.listdir(CPUFREQ_DIR):
            with open(f'{CPUFREQ_DIR}/boost', 'r') as file:
                return 'active' if '1' in file.read() else 'not active'

    except:
        pass

    return 'not available'

def getMinimumClock():
    return round(min(
        int(freq) for freq in terminal(f'cat {CPUFREQ_DIR}/policy*/cpuinfo_min_freq').strip().split('\n')
    ) / 1000000, 2)

def getMaximumClock():
    return round(max(
        int(freq) for freq in terminal(f'cat {CPUFREQ_DIR}/policy*/cpuinfo_max_freq').strip().split('\n')
    ) / 1000000, 2)

def getAmdPState():
    global GENERAL_DRIVER

    pStateDir = os.path.join(GENERAL_DRIVER, 'amd_pstate')
    status = None
    prefcore = None

    if (pStateStatus := os.path.join(pStateDir, 'status')) and os.path.exists(pStateStatus):
        with open(pStateStatus, 'r') as file:
            status = file.read().strip()

    if (pStatePrefcore := os.path.join(pStateDir, 'prefcore')) and os.path.exists(pStatePrefcore):
        with open(pStatePrefcore, 'r') as file:
            prefcore = file.read().strip()

    return status, prefcore

def getBogoMips():
    values = grep(readFile('/proc/cpuinfo'), 'bogomips', ignoreCase=True)
    try:
        return sum(float(v.split(':')[1].strip()) for v in values) / len(values)

    except:
        return None

def getVirtualizationEnabled():
    return True if (grep(readFile('/proc/cpuinfo'), 'svm', True)
        or grep(readFile('/proc/cpuinfo'), 'vmx', True)) else False

def getFlags():
    flags = grep(readFile('/proc/cpuinfo'), 'flags', returnFirstMatch=True)

    if flags and ':' in flags:
        return flags.split(':')[1].strip()

    return None