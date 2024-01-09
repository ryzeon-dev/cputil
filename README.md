# cputil
CPU performance utils and information tool CLI written in Python

```
$ cputil --help
cputil: cpu util CLI v3.3.1
usage: cputil [OPTIONS]

Options:
-sg  --set-governor          GOVERNOR     set governor (root)
-sfm --set-minimum-frequency FREQUENCY    set minimum frequency (root)
-sfM --set-maximum-frequency FREQUENCY    set maximum frequency (root)
-cpu CPU       Select which processor to affect with action,
               if omitted the action will affect all processors,
               to be used with -sg, -sfm, -sfM, -u
-i   --info    Show info about CPU
-u   --usage   Show CPU usage
-avg           If specified, only average usage is shown,
               to be used only with -u
-j   --json    Outputs all the available informations in json format
```

## Example outputs
```
$ cputil -i
Model name:	AMD Ryzen 7 5800X 8-Core Processor
Architecture:	amd64 / x86_64 (64bit)
Byte order:	Little Endian (first bit is LSB)
Cores count:	8
Threads count:	16
Clock boost:	active
Minimum clock:	2.2 GHz
Maximum clock:	4.85 GHz

Processor 0:
    L1 cache: 64 KB	shared with processor(s): 8
    L2 cache: 512 KB	shared with processor(s): 8
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 0
    Physical die: 0

Processor 1:
    L1 cache: 64 KB	shared with processor(s): 9
    L2 cache: 512 KB	shared with processor(s): 9
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 1
    Physical die: 0

Processor 2:
    L1 cache: 64 KB	shared with processor(s): 10
    L2 cache: 512 KB	shared with processor(s): 10
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 2
    Physical die: 0

Processor 3:
    L1 cache: 64 KB	shared with processor(s): 11
    L2 cache: 512 KB	shared with processor(s): 11
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 3
    Physical die: 0

Processor 4:
    L1 cache: 64 KB	shared with processor(s): 12
    L2 cache: 512 KB	shared with processor(s): 12
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 4
    Physical die: 0

Processor 5:
    L1 cache: 64 KB	shared with processor(s): 13
    L2 cache: 512 KB	shared with processor(s): 13
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 5
    Physical die: 0

Processor 6:
    L1 cache: 64 KB	shared with processor(s): 14
    L2 cache: 512 KB	shared with processor(s): 14
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 6
    Physical die: 0

Processor 7:
    L1 cache: 64 KB	shared with processor(s): 15
    L2 cache: 512 KB	shared with processor(s): 15
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 7
    Physical die: 0

Processor 8:
    L1 cache: 64 KB	shared with processor(s): 0
    L2 cache: 512 KB	shared with processor(s): 0
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 0
    Physical die: 0

Processor 9:
    L1 cache: 64 KB	shared with processor(s): 1
    L2 cache: 512 KB	shared with processor(s): 1
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 1
    Physical die: 0

Processor 10:
    L1 cache: 64 KB	shared with processor(s): 2
    L2 cache: 512 KB	shared with processor(s): 2
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 2
    Physical die: 0

Processor 11:
    L1 cache: 64 KB	shared with processor(s): 3
    L2 cache: 512 KB	shared with processor(s): 3
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 3
    Physical die: 0

Processor 12:
    L1 cache: 64 KB	shared with processor(s): 4
    L2 cache: 512 KB	shared with processor(s): 4
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 4
    Physical die: 0

Processor 13:
    L1 cache: 64 KB	shared with processor(s): 5
    L2 cache: 512 KB	shared with processor(s): 5
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 5
    Physical die: 0

Processor 14:
    L1 cache: 64 KB	shared with processor(s): 6
    L2 cache: 512 KB	shared with processor(s): 6
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 6
    Physical die: 0

Processor 15:
    L1 cache: 64 KB	shared with processor(s): 7
    L2 cache: 512 KB	shared with processor(s): 7
    L3 cache: 32768 KB	shared with processor(s): all
    Physical core: 7
    Physical die: 0
```

```
$ cputil -u -avg
Average:
total:              1.73 %
user:               0.74 %
nice:               0.0 %
system:             0.5 %
idle:               98.27 %
iowait:             0.5 %
interrupt:          0.0 %
soft-interrupt:     0.0 %
Frequency:          3041.76 MHz
```