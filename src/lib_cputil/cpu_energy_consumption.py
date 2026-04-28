import os
import time

from .static_const import POWERCAP_DRIVER

class EnergyConsumption:
    def __init__(self, intelRaplEnabled: bool):
        self.intelRaplEnabled: bool = intelRaplEnabled
        self.sensors: list[EnergyConsumptionSensor] = []

    def toJson(self):
        return {
            'intel_rapl_enabled': self.intelRaplEnabled,
            'sensors': [sensor.toJson() for sensor in self.sensors]
        }

class EnergyConsumptionSensor:
    def __init__(self, name: str, energyJ: float):
        self.name = name
        self.energyJ = energyJ

    def toJson(self):
        return {
            'name': self.name,
            'energy_J': self.energyJ
        }

def getCpuEnergyConsumption() -> EnergyConsumption | None:
    intelRapl = os.path.join(POWERCAP_DRIVER, 'intel-rapl')
    if not os.path.exists(intelRapl):
        return None

    enabledFile = os.path.join(intelRapl, 'enabled')
    if not os.path.exists(enabledFile):
        return EnergyConsumption(False)

    with open(enabledFile, 'r') as file:
        enabledContent = file.read()

    if enabledContent.strip() != '1':
        return EnergyConsumption(False)

    energyConsumption = EnergyConsumption(True)

    for entry in os.listdir(POWERCAP_DRIVER):
        entryPath = os.path.join(POWERCAP_DRIVER, entry)

        if not os.path.isdir(entryPath):
            continue

        entryNameFile = os.path.join(entryPath, 'name')
        entryValueFile = os.path.join(entryPath, 'energy_uj')

        if not os.path.exists(entryValueFile) or not os.path.exists(entryNameFile):
            continue

        with open(entryNameFile, 'r') as file:
            entryName = file.read().strip()

        with open(entryValueFile, 'r') as file:
            beforeValue = file.read().strip()

        time.sleep(0.25)

        with open(entryValueFile, 'r') as file:
            afterValue = file.read().strip()

        deltaUj = float(afterValue) - float(beforeValue)
        deltaJ = deltaUj / 1000000 / 0.25

        energyConsumption.sensors.append(
            EnergyConsumptionSensor(entryName, deltaJ)
        )

    return energyConsumption

if __name__ == '__main__':
    print(getCpuEnergyConsumption())