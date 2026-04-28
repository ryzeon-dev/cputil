import os.path

from .static_const import GENERAL_DRIVER

class CpuVulnerability:
    def __init__(self, name: str, status: str):
        self.name = name
        self.status = status

    def toJson(self):
        return {
            'name': self.name,
            'status': self.status,
        }

def getCpuVulnerabilities() -> list[CpuVulnerability]:
    vulnerabilitiesPath = os.path.join(GENERAL_DRIVER, 'vulnerabilities')
    if not os.path.exists(vulnerabilitiesPath):
        return []

    vulnerabilities = []
    for entry in os.listdir(vulnerabilitiesPath):
        entryPath = os.path.join(vulnerabilitiesPath, entry)

        if not os.path.exists(entryPath) or not os.path.isfile(entryPath):
            continue

        name = entry
        with open(entryPath, 'r') as file:
            status = file.read().strip()

        vulnerabilities.append(CpuVulnerability(name, status))

    return vulnerabilities