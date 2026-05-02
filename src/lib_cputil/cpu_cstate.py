from .static_const import *
import os
import re

class Cstate:
    def __init__(self, name: str, desc: str, latency: int):
        self.name: str = name
        self.desc: str = desc
        self.latency: int = latency

    def toJson(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'latency': self.latency
        }

class CoreCstates:
    def __init__(self, coreId: int, total: int):
        self.coreId: int = coreId
        self.total: int = total

        self.coreCstates: list[CoreCstateStatus] = []

    def toJson(self):
        return {
            'core_id': self.coreId,
            'total': self.total,
            'states': [state.toJson() for state in self.coreCstates]
        }

class CoreCstateStatus:
    def __init__(self, name: str, time: int, enabled: bool):
        self.name: str = name
        self.time: int = time
        self.enabled: bool = enabled

    def toJson(self):
        return {
            'name': self.name,
            'time': self.time,
            'enabled': self.enabled
        }

def getCpuCstates() -> (list[Cstate], list[CoreCstates]):
    cstates = []
    cstateNames = set()

    coreIds = set()
    coresCstates = []

    for entry in os.listdir(GENERAL_DRIVER):
        if not re.fullmatch(r'^cpu[0-9]{1,3}$', entry):
            continue

        coreIdPath = os.path.join(GENERAL_DRIVER, entry, 'topology', 'core_id')
        statePath = os.path.join(GENERAL_DRIVER, entry, 'cpuidle')

        with open(coreIdPath, 'r') as file:
            coreId = int(file.read().strip())

        if coreId in coreIds:
            continue

        coreCstates = CoreCstates(coreId, 0)

        for state in os.listdir(statePath):
            statePath = os.path.join(GENERAL_DRIVER, entry, 'cpuidle', state)

            with open(os.path.join(statePath, 'name'), 'r') as file:
                stateName = file.read().strip()

            with open(os.path.join(statePath, 'time'), 'r') as file:
                stateTime = int(file.read().strip())

            with open(os.path.join(statePath, 'desc'), 'r') as file:
                stateDesc = file.read().strip()

            with open(os.path.join(statePath, 'disable'), 'r') as file:
                stateDisabled = file.read().strip()

            with open(os.path.join(statePath, 'latency'), 'r') as file:
                stateLatency = int(file.read().strip())

            coreCstates.total += stateTime
            coreCstates.coreCstates.append(CoreCstateStatus(stateName, stateTime, stateDisabled == '0'))

            if stateName not in cstateNames:
                cstates.append(Cstate(stateName, stateDesc, stateLatency))
                cstateNames.add(stateName)

        coresCstates.append(coreCstates)
        coreIds.add(coreId)

    return cstates, coresCstates

def setCpuCstateEnabled(selectedState: str, enabled: bool):
    for entry in os.listdir(GENERAL_DRIVER):
        if not re.fullmatch(r'^cpu[0-9]{1,3}$', entry):
            continue

        for state in os.listdir(os.path.join(GENERAL_DRIVER, entry, 'cpuidle')):
            statePath = os.path.join(GENERAL_DRIVER, entry, 'cpuidle', state)

            with open(os.path.join(statePath, 'name')) as file:
                stateName = file.read().strip()

            if stateName.lower() != selectedState.lower():
                continue

            with open(os.path.join(statePath, 'disable'), 'w') as file:
                file.write('0' if enabled else '1')