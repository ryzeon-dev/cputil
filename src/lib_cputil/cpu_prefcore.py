import os
from .static_const import GENERAL_DRIVER
import re

class Prefcore:
    def __init__(self, coreId: int, dieId: int, ranking: int):
        self.coreId: int = coreId
        self.dieId: int = dieId
        self.ranking: int = ranking

    def toJson(self):
        return {
            'core_id': self.coreId,
            'ranking': self.ranking,
            'die_id': self.dieId
        }

def getCpuPrefcores() -> list[Prefcore]:
    coreIds = set()
    prefcores = []

    for entry in os.listdir(os.path.join(GENERAL_DRIVER)):
        if not re.fullmatch(r'^cpu[0-9]{1,3}$', entry):
            continue

        entryPath = os.path.join(GENERAL_DRIVER, entry)
        coreIdPath = os.path.join(entryPath, 'topology', 'core_id')
        dieIdPath = os.path.join(entryPath, 'topology', 'die_id')
        rankingPath = os.path.join(entryPath, 'cpufreq', 'amd_pstate_prefcore_ranking')

        if not os.path.exists(rankingPath):
            continue

        with open(coreIdPath, 'r') as file:
            coreId = int(file.read().strip())

        if coreId in coreIds:
            continue

        with open(dieIdPath, 'r') as file:
            dieId = int(file.read().strip())

        with open(rankingPath, 'r') as file:
            ranking = int(file.read().strip())

        prefcores.append(
            Prefcore(
                coreId=coreId,
                ranking=ranking,
                dieId=dieId,
            )
        )
        coreIds.add(coreId)

    return prefcores