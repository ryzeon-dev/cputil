import sys

class ArgParse:
    def __init__(self):
        self.set = False
        self.setGovernor = None
        self.setFrequency = False
        self.setFrequencyMinimum = None
        self.setFrequencyMaximum = None
        self.setEnergyPerformancePreference = None
        self.max = False
        self.min = False
        self.load = False
        self.loadFileName = None
        self.scaling = False
        self.info = False
        self.topology = False
        self.usage = False
        self.json = False
        self.yaml = False
        self.help = False
        self.version = False
        self.cpu = None
        self.avg = False
        self.noArg = False

    def parse(self, args):
        if not args:
            self.noArg = True
            return

        index = 0

        while index < len(args):
            arg = args[index]

            if arg == 'set':
                self.set = True

                index += 1
                if index >= len(args) or (arg := args[index]) not in ('governor', 'frequency', 'energy') :
                    print('Error: exptecting either `governor`, `frequency` or `energy` after verb `set`')
                    sys.exit(1)

                if arg == 'governor':
                    index += 1

                    if index >= len(args):
                        print('Error: expecting a governor after `set governor` command')
                        sys.exit(1)

                    self.setGovernor = args[index]

                elif arg == 'frequency':
                     self.setFrequency = True
                     index += 1

                     if index >= len(args) or (arg := args[index]) not in ('minimum', 'maximum'):
                         print('Error: exptecting either `minimum` or `maximum` after command `frequency`')
                         sys.exit(1)

                     if arg == 'minimum':
                         index += 1

                         if index >= len(args):
                             print('Error: expecting a frequency after `set frequency minimum` command')
                             sys.exit(1)

                         self.setFrequencyMinimum = args[index]

                     elif arg == 'maximum':
                         index += 1

                         if index >= len(args):
                             print('Error: expecting a frequency after `set frequency maximum` command')
                             sys.exit(1)

                         self.setFrequencyMaximum = args[index]

                elif arg == 'energy':
                    index += 1

                    if index >= len(args) or (arg := args[index]) != 'preference':
                        print('Error: expecting a `preference` after `set energy` command')
                        sys.exit(1)
                    index += 1

                    if index >= len(args):
                        print('Error: expecting a `preference` after `set energy preference` command')
                        sys.exit(1)

                    self.setEnergyPerformancePreference = args[index]

            elif arg == 'sg':
                index += 1

                if index >= len(args):
                    print('Error: exptecting scaling governor after abbreviated command `sg`')
                    sys.exit(1)

                self.set = True
                self.setGovernor = args[index]

            elif arg == 'sfM':
                index += 1

                if index >= len(args):
                    print('Error: exptecting scaling frequency after abbreviated command `sfM`')
                    sys.exit(1)

                self.set = True
                self.setFrequency = True
                self.setFrequencyMaximum = args[index]

            elif arg == 'sfm':
                index += 1

                if index >= len(args):
                    print('Error: exptecting scaling frequency after abbreviated command `sfm`')
                    sys.exit(1)

                self.set = True
                self.setFrequency = True
                self.setFrequencyMinimum = args[index]

            elif arg == 'sep':
                index += 1

                if index >= len(args):
                    print('Error: exptecting energy performance preference after abbreviated command `sep`')
                    sys.exit(1)

                self.set = True
                self.setEnergyPerformancePreference = args[index]

            elif arg == 'min':
                self.min = True

            elif arg == 'max':
                self.max = True

            elif arg == 'load':
                self.load = True

                index += 1
                if index >= len(args):
                    print('Error: expecting configuration file name after `load` verb')
                    sys.exit(1)

                self.loadFileName = args[index]

            elif arg == 'scaling' or arg == 's':
                self.scaling = True

            elif arg == 'info' or arg == 'i':
                self.info = True

            elif arg == 'usage' or arg == 'u':
                self.usage = True

            elif arg == 'topology' or arg == 't':
                self.topology = True

            elif arg == 'json' or arg == 'j':
                self.json = True

            elif arg == 'yaml' or arg == 'y':
                self.yaml = True

            elif arg == 'version' or arg == 'v':
                self.version = True

            elif arg == 'help' or arg == 'h':
                self.help = True

            elif arg == '-cpu':
                index += 1

                if index >= len(args):
                    print('Error: expecting a processor number after `-cpu` flag')
                    sys.exit(1)

                self.cpu = args[index]

            elif arg == '-avg':
                self.avg = True

            else:
                print(f'Error: unrecognised argument `{arg}`, run `cputil help` to get help')
                sys.exit(1)

            index += 1