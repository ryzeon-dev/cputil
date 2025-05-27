# cputil
CPU performance utils and information tool CLI & daemon written in Python

# Install
- compilation requires `python3`, `python3-venv` and `python3-pip` to be installed
- use the `install.sh` script, executing it as root
  - run `sudo bash install.sh bin` to only install the utility program
  - run `sudo bash install.sh daemon` to only install the daemon
  - run `sudo bash install.sh all` to install both
- both options require the compilation of the source files (which is done automatically by the installation script) 

# Uninstall
- to uninstall use `uninstall.sh` script with root privilegies
  - run `sudo bash uninstall.sh bin` to uninstall binary executable
  - run `sudo bash uninstall.sh daemon` to uninstall the daemon
  - run `sudo bash uninstall.sh all` to uninstall both

# Usage
## Utility
- `cputil` allows to monitor cpu's usage, inspect its properties and set its governor and scaling frequencies

### Setting
- setting requires root privilegies
- to set the governor, use the `-sg` or `--set-governor` flag followed by the selected governor
  - run `cputil` with no argument to view the available governors
- to set minimum scaling frequency, use the `-sfm` or `--set-minimum-frequency` flag
  - run `cputil` with no argument to view the available scaling frequencies
- to set minimum scaling frequency, use the `-sfM` or `--set-maximum-frequency` flag
  - run `cputil` with no argument to view the available scaling frequencies
- if the flag `-cpu` is added, followed by a logical processor's number, any actions will only affect the specified processor
- when setting any parameter for the entire CPU, if `cputild` daemon is installed, the configuration file will be overwritten with the new parameters 

- to set the processor to its absolute max performace, run cputil with `-max` or `--maximum-performace` flag, which sets governor to "performace", sets both minimum and maximum scaling frequency to the max allowed value and sets energy performance preference to "performance"
- to set the processor to its absolute min performace, run cputil with `-min` or `--minimum-performace` flag, which sets governor to the weakest available, sets both minimum and maximum scaling frequency to the min allowed value and sets energy performance preference to "power"

### Inspecting 
- the inspection of CPU properties is done using the `-i` or `--info` flag
- it will show information like:
  - model name
  - architecture
  - byte order
  - cores count
  - threads count
  - clock parameters
  - logical processors' core distribution, die distribution and cache sharing  
  - if the `-g` flag is added, logical processor wise information is omitted

- the inspection of CPU performance level is done using `cputil` without any flag

### Usage
- cpu usage is monitored using `-u` or `--usage` flag
  - both average and logical processor wise usage is shown
  - if the `-avg` flag is used, only average usage will be shown

### Json
- the `-j` or `--json` flags prints all the available information in json format

### Version
- using `-V` or `--version` flag prints the current cputil's version

### Help
- use `-h` or `--help` to get help

## Daemon
- useful to set CPU parameters as default
- in the installation process, it is configured as service, and started
- once installed (refer to the Install section), the daemon will loop, executing its procedure every 60 seconds
  - it reads the configuration file, located at /etc/cputild/cputild.conf
  - parses the configuration, and applies it 
- the value assigned to configuration parameters must be allowed, check the available values in your system running `cputil` 
- if any parameter is set to `auto`, it will not be modified
- configuration parameters are:
  - governor
  - min_scaling_frequency
  - max_scaling_frequency
  - polling_interval (default value is 10 seconds)

## Example outputs

```
$ cputil
Available governors:
        powersave
        performance

Available scaling frequencies:
        600000
        2981000
        5752000

Energy performance preferences:
        performance
        power
        default
        balance_power
        balance_performance

Current status:
Processor 0:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 1:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 2:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 3:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 4:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 5:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 6:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 7:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 8:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 9:    powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 10:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 11:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 12:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 13:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 14:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 15:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 16:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 17:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 18:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 19:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 20:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 21:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 22:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 23:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 24:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 25:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 26:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 27:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 28:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 29:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 30:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 31:   powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
```

```
$ cputil -i
Model name:             AMD Ryzen 9 9950X 16-Core Processor
Architecture:           amd64 / x86_64 (64bit)
Byte order:             Little Endian (first bit is LSB)
Cores count:            16
Threads count:          32
Clock boost:            active
Minimum clock:          0.6 GHz
Maximum clock:          5.75 GHz
AMD P-State status:     active
AMD P-State prefcore:   enabled

Processor 0:
    L2 cache: 1024 KB   shared with processor(s): 16
    L1 cache: 80 KB     shared with processor(s): 16
    L3 cache: 32768 KB  shared with processor(s): 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 0
    Physical die: 0

Processor 1:
    L2 cache: 1024 KB   shared with processor(s): 17
    L1 cache: 80 KB     shared with processor(s): 17
    L3 cache: 32768 KB  shared with processor(s): 0, 2, 3, 4, 5, 6, 7, 16
    Physical core: 1
    Physical die: 0

Processor 2:
    L2 cache: 1024 KB   shared with processor(s): 18
    L1 cache: 80 KB     shared with processor(s): 18
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 3, 4, 5, 6, 7, 16
    Physical core: 2
    Physical die: 0

Processor 3:
    L2 cache: 1024 KB   shared with processor(s): 19
    L1 cache: 80 KB     shared with processor(s): 19
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 4, 5, 6, 7, 16
    Physical core: 3
    Physical die: 0

Processor 4:
    L2 cache: 1024 KB   shared with processor(s): 20
    L1 cache: 80 KB     shared with processor(s): 20
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 5, 6, 7, 16
    Physical core: 4
    Physical die: 0

Processor 5:
    L2 cache: 1024 KB   shared with processor(s): 21
    L1 cache: 80 KB     shared with processor(s): 21
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 6, 7, 16
    Physical core: 5
    Physical die: 0

Processor 6:
    L2 cache: 1024 KB   shared with processor(s): 22
    L1 cache: 80 KB     shared with processor(s): 22
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 7, 16
    Physical core: 6
    Physical die: 0

Processor 7:
    L2 cache: 1024 KB   shared with processor(s): 23
    L1 cache: 80 KB     shared with processor(s): 23
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 16
    Physical core: 7
    Physical die: 0

Processor 8:
    L2 cache: 1024 KB   shared with processor(s): 24
    L1 cache: 80 KB     shared with processor(s): 24
    L3 cache: 32768 KB  shared with processor(s): 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 8
    Physical die: 1

Processor 9:
    L2 cache: 1024 KB   shared with processor(s): 25
    L1 cache: 80 KB     shared with processor(s): 25
    L3 cache: 32768 KB  shared with processor(s): 8, 10, 11, 12, 13, 14, 15, 24
    Physical core: 9
    Physical die: 1

Processor 10:
    L2 cache: 1024 KB   shared with processor(s): 26
    L1 cache: 80 KB     shared with processor(s): 26
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 11, 12, 13, 14, 15, 24
    Physical core: 10
    Physical die: 1

Processor 11:
    L2 cache: 1024 KB   shared with processor(s): 27
    L1 cache: 80 KB     shared with processor(s): 27
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 12, 13, 14, 15, 24
    Physical core: 11
    Physical die: 1

Processor 12:
    L2 cache: 1024 KB   shared with processor(s): 28
    L1 cache: 80 KB     shared with processor(s): 28
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 13, 14, 15, 24
    Physical core: 12
    Physical die: 1

Processor 13:
    L2 cache: 1024 KB   shared with processor(s): 29
    L1 cache: 80 KB     shared with processor(s): 29
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 14, 15, 24
    Physical core: 13
    Physical die: 1

Processor 14:
    L2 cache: 1024 KB   shared with processor(s): 30
    L1 cache: 80 KB     shared with processor(s): 30
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 15, 24
    Physical core: 14
    Physical die: 1

Processor 15:
    L2 cache: 1024 KB   shared with processor(s): 31
    L1 cache: 80 KB     shared with processor(s): 31
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 24
    Physical core: 15
    Physical die: 1

Processor 16:
    L2 cache: 1024 KB   shared with processor(s): 0
    L1 cache: 80 KB     shared with processor(s): 0
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 0
    Physical die: 0

Processor 17:
    L2 cache: 1024 KB   shared with processor(s): 1
    L1 cache: 80 KB     shared with processor(s): 1
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 1
    Physical die: 0

Processor 18:
    L2 cache: 1024 KB   shared with processor(s): 2
    L1 cache: 80 KB     shared with processor(s): 2
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 2
    Physical die: 0

Processor 19:
    L2 cache: 1024 KB   shared with processor(s): 3
    L1 cache: 80 KB     shared with processor(s): 3
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 3
    Physical die: 0

Processor 20:
    L2 cache: 1024 KB   shared with processor(s): 4
    L1 cache: 80 KB     shared with processor(s): 4
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 4
    Physical die: 0

Processor 21:
    L2 cache: 1024 KB   shared with processor(s): 5
    L1 cache: 80 KB     shared with processor(s): 5
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 5
    Physical die: 0

Processor 22:
    L2 cache: 1024 KB   shared with processor(s): 6
    L1 cache: 80 KB     shared with processor(s): 6
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 6
    Physical die: 0

Processor 23:
    L2 cache: 1024 KB   shared with processor(s): 7
    L1 cache: 80 KB     shared with processor(s): 7
    L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 7
    Physical die: 0

Processor 24:
    L2 cache: 1024 KB   shared with processor(s): 8
    L1 cache: 80 KB     shared with processor(s): 8
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 8
    Physical die: 1

Processor 25:
    L2 cache: 1024 KB   shared with processor(s): 9
    L1 cache: 80 KB     shared with processor(s): 9
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 9
    Physical die: 1

Processor 26:
    L2 cache: 1024 KB   shared with processor(s): 10
    L1 cache: 80 KB     shared with processor(s): 10
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 10
    Physical die: 1

Processor 27:
    L2 cache: 1024 KB   shared with processor(s): 11
    L1 cache: 80 KB     shared with processor(s): 11
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 11
    Physical die: 1

Processor 28:
    L2 cache: 1024 KB   shared with processor(s): 12
    L1 cache: 80 KB     shared with processor(s): 12
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 12
    Physical die: 1

Processor 29:
    L2 cache: 1024 KB   shared with processor(s): 13
    L1 cache: 80 KB     shared with processor(s): 13
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 13
    Physical die: 1

Processor 30:
    L2 cache: 1024 KB   shared with processor(s): 14
    L1 cache: 80 KB     shared with processor(s): 14
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 14
    Physical die: 1

Processor 31:
    L2 cache: 1024 KB   shared with processor(s): 15
    L1 cache: 80 KB     shared with processor(s): 15
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 15
    Physical die: 1
```

```
$ cputil -u -avg
Average:
    total:              0.75 %
    user:               0.12 %
    nice:               0.0 %
    system:             0.0 %
    idle:               99.25 %
    iowait:             0.62 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    Frequency:          4042.61 MHz
```