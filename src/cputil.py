from argparser import ArgParse
from printFunctions import *
from setFunctions import *

import json
import yaml
import sys

VERSION = '8.0.1'

run_watch = True

def main():
    args = sys.argv[1:]

    argParser = ArgParse()
    argParser.parse(args)

    if argParser.noArg:
        argParser.info = True

    if argParser.help:
        printHelp(VERSION)

    elif argParser.scaling:
        printScaling()

    elif argParser.json:
        print(json.dumps(dictFormat()))

    elif argParser.yaml:
        yaml.dump(dictFormat(), stream=sys.stdout)

    elif argParser.info:
        printInfo()

    elif argParser.topology:
        printTopology()

    elif argParser.usage:
        printUsage(argParser)

    elif argParser.set:
        set(argParser)

    elif argParser.version:
        print(f'cputil v{VERSION}')

    elif argParser.min:
        minAll()

    elif argParser.max:
        maxAll()

    elif argParser.load:
        loadConf(argParser)

    elif argParser.temperature:
        printTemperature()

    elif argParser.watch:
        printWatchUsage()

    elif argParser.dump:
        printConfigDump()

    elif argParser.energy:
        printEnergy()

    elif argParser.prefcore:
        printPrefcore()

    elif argParser.cstate:
        printCstate()

    elif argParser.vuln:
        printVulnerabilities()

    elif argParser.all:
        print('[INFO]')
        printInfo()

        print('\n[SCALING]')
        printScaling()

        print('\n[TOPOLOGY]')
        printTopology()

        print('\n[ENERGY]')
        printEnergy()

        print('\n[PREFCORE]')
        printPrefcore()

        print('\n[C-STATE]')
        printCstate()

        print('\n[VULNERABILITIES]')
        printVulnerabilities()

        print('\n[TEMPERATURE]')
        printTemperature()

        print('\n[USAGE]')
        printUsage(argParser)

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        print(''.join(traceback.format_exception(e)))
        print(f'Fatal: unexpected error "{e}"')