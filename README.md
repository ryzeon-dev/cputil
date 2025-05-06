# cputil
CPU performance utils and information tool CLI written in Python

```
$ cputil --help
cputil: cpu utils CLI v3.5.2
usage: cputil [OPTIONS]

Options:
    -sg  --set-governor          GOVERNOR     Set governor (root)
    -sfm --set-minimum-frequency FREQUENCY    Set minimum frequency (root)
    -sfM --set-maximum-frequency FREQUENCY    Set maximum frequency (root)
    -cpu CPU                                  Select which processor to affect with action,
                                              if omitted the action will affect all processors,
                                              to be used with -sg, -sfm, -sfM, -u
    -i   --info                               Show info about CPU
    -g                                        Show general info only, to be used only with -i
    -u   --usage                              Show CPU usage
    -avg                                      If specified, only average usage is shown,
                                              to be used only with -u
    -j   --json                               Output all the available information in json format
    -V   --version                            Show cputil's version
    -h   --help                               Show this message and exit
```

Some systems might require root privilegies to read certain parameters. 
If some information is missing (e.g. current frequency in usage), try running `cputil` with sudo

The package also provides `cputil-tui`, which is a terminal-ui visualisation tool.
In order to use it, it is required to have `cputil` properly installed.

## Example outputs
```
$ cputil -i
Model name:     AMD Ryzen 9 9950X 16-Core Processor
Architecture:   amd64 / x86_64 (64bit)
Byte order:     Little Endian (first bit is LSB)
Cores count:    16
Threads count:  32
Clock boost:    active
Minimum clock:  3.0 GHz
Maximum clock:  4.3 GHz

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
    Physical die: 0

Processor 9:
    L2 cache: 1024 KB   shared with processor(s): 25
    L1 cache: 80 KB     shared with processor(s): 25
    L3 cache: 32768 KB  shared with processor(s): 8, 10, 11, 12, 13, 14, 15, 24
    Physical core: 9
    Physical die: 0

Processor 10:
    L2 cache: 1024 KB   shared with processor(s): 26
    L1 cache: 80 KB     shared with processor(s): 26
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 11, 12, 13, 14, 15, 24
    Physical core: 10
    Physical die: 0

Processor 11:
    L2 cache: 1024 KB   shared with processor(s): 27
    L1 cache: 80 KB     shared with processor(s): 27
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 12, 13, 14, 15, 24
    Physical core: 11
    Physical die: 0

Processor 12:
    L2 cache: 1024 KB   shared with processor(s): 28
    L1 cache: 80 KB     shared with processor(s): 28
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 13, 14, 15, 24
    Physical core: 12
    Physical die: 0

Processor 13:
    L2 cache: 1024 KB   shared with processor(s): 29
    L1 cache: 80 KB     shared with processor(s): 29
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 14, 15, 24
    Physical core: 13
    Physical die: 0

Processor 14:
    L2 cache: 1024 KB   shared with processor(s): 30
    L1 cache: 80 KB     shared with processor(s): 30
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 15, 24
    Physical core: 14
    Physical die: 0

Processor 15:
    L2 cache: 1024 KB   shared with processor(s): 31
    L1 cache: 80 KB     shared with processor(s): 31
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 24
    Physical core: 15
    Physical die: 0

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
    Physical die: 0

Processor 25:
    L2 cache: 1024 KB   shared with processor(s): 9
    L1 cache: 80 KB     shared with processor(s): 9
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 9
    Physical die: 0

Processor 26:
    L2 cache: 1024 KB   shared with processor(s): 10
    L1 cache: 80 KB     shared with processor(s): 10
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 10
    Physical die: 0

Processor 27:
    L2 cache: 1024 KB   shared with processor(s): 11
    L1 cache: 80 KB     shared with processor(s): 11
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 11
    Physical die: 0

Processor 28:
    L2 cache: 1024 KB   shared with processor(s): 12
    L1 cache: 80 KB     shared with processor(s): 12
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 12
    Physical die: 0

Processor 29:
    L2 cache: 1024 KB   shared with processor(s): 13
    L1 cache: 80 KB     shared with processor(s): 13
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 13
    Physical die: 0

Processor 30:
    L2 cache: 1024 KB   shared with processor(s): 14
    L1 cache: 80 KB     shared with processor(s): 14
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 14
    Physical die: 0

Processor 31:
    L2 cache: 1024 KB   shared with processor(s): 15
    L1 cache: 80 KB     shared with processor(s): 15
    L3 cache: 32768 KB  shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 15
    Physical die: 0

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