import os
import re
from .static_const import HWMON_DIR, HWMON_PROCESSOR_DRIVERS
from .util import readFile

def getCpuTemperature():
    try:
        hwmonEntries = os.listdir(HWMON_DIR)
    except:
        return {}

    readings = {}
    for entry in hwmonEntries:
        entryPath = os.path.join(HWMON_DIR, entry)
        entryName = readFile(os.path.join(entryPath, 'name'))

        if entryName not in HWMON_PROCESSOR_DRIVERS:
            continue

        hwmonFiles = os.listdir(entryPath)

        for file in hwmonFiles:
            if not re.fullmatch(r'^temp\d_(input|label)$', file):
                continue

            sensorName = file.split('_')[0]
            if sensorName not in readings:
                readings[sensorName] = {}

            if 'label' in file:
                readings[sensorName]['label'] = readFile(os.path.join(entryPath, file))

            elif 'input' in file:
                readings[sensorName]['input'] = readFile(os.path.join(entryPath, file))

        break

    outputReading = {}
    for sensorName, sensor in readings.items():
        sensorLabel = sensor.get('label', sensorName)
        value = sensor.get('input', 0)
        outputReading[sensorLabel] = int(value) / 1000

    return outputReading