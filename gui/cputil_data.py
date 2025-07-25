import subprocess
import json

J_DATA = {}
PROCESSOR_KEYS = {}
TOPOLOGY = {}

def update():
    global J_DATA, PROCESSOR_KEYS
    output = subprocess.getoutput('/usr/local/bin/cputil json')
    J_DATA = json.loads(output)

    for key in J_DATA.keys():
        if key.startswith('processor'):
            n = int(key.replace('processor', ''))
            PROCESSOR_KEYS[n] = key

def makeTopology():
    global TOPOLOGY
    coresForDie = {}
    processorsForCore = {}

    for key in J_DATA.keys():
        if key.startswith('processor'):
            processorId = int(key.replace('processor', ''))

            physicalCore = int(coreId) if (coreId := J_DATA[key]['physical core']) is not None else None
            physicalDie = int(dieId) if (dieId := J_DATA[key]['physical die']) is not None else None

            if physicalDie is not None and physicalCore is not None:
                if physicalDie not in coresForDie:
                    coresForDie[physicalDie] = {physicalCore}

                else:
                    coresForDie[physicalDie].add(physicalCore)

            if physicalCore is not None:
                if physicalCore not in processorsForCore:
                    processorsForCore[physicalCore] = {processorId}

                else:
                    processorsForCore[physicalCore].add(processorId)

    if coresForDie and processorsForCore:
        topology = {}

        for die, cores in coresForDie.items():
            topology[die] = {}

            for core in cores:
                topology[die][core] = processorsForCore[core]

    else:
        topology = processorsForCore

    TOPOLOGY = topology

update()
makeTopology()