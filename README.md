# cputil
CPU performance utils CLI written in Python

```
$ cputil --help
cputil: cpu util CLI v2.1.0
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
```

## Example outputs
```
$ cputil -i
Model name:     AMD Ryzen 7 5800X 8-Core Processor
Architecture:   amd64 / x86_64 (64 bit)
Cores count:    8
Threads count:  16
Clock boost:    active
Minimum clock:  2.2 GHz
Maximum clock:  4.85 GHz

Processor 0:
L1 cache: 64 KB     shared with processor(s): 8
L2 cache: 512 KB    shared with processor(s): 8
L3 cache: 32768 KB  shared with processor(s): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core: 0

Processor 1:
L1 cache: 64 KB     shared with processor(s): 9
L2 cache: 512 KB    shared with processor(s): 9
L3 cache: 32768 KB  shared with processor(s): 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  1

Processor 2:
L1 cache: 64 KB     shared with processor(s): 10
L2 cache: 512 KB    shared with processor(s): 10
L3 cache: 32768 KB  shared with processor(s): 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  2

Processor 3:
L1 cache: 64 KB     shared with processor(s): 11
L2 cache: 512 KB    shared with processor(s): 11
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  3

Processor 4:
L1 cache: 64 KB     shared with processor(s): 12
L2 cache: 512 KB    shared with processor(s): 12
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  4

Processor 5:
L1 cache: 64 KB     shared with processor(s): 13
L2 cache: 512 KB    shared with processor(s): 13
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  5

Processor 6:
L1 cache: 64 KB     shared with processor(s): 14
L2 cache: 512 KB    shared with processor(s): 14
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  6

Processor 7:
L1 cache: 64 KB     shared with processor(s): 15
L2 cache: 512 KB    shared with processor(s): 15
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15
Physical core:  7

Processor 8:
L1 cache: 64 KB     shared with processor(s): 0
L2 cache: 512 KB    shared with processor(s): 0
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15
Physical core:  0

Processor 9:
L1 cache: 64 KB     shared with processor(s): 1
L2 cache: 512 KB    shared with processor(s): 1
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15
Physical core:  1

Processor 10:
L1 cache: 64 KB     shared with processor(s): 2
L2 cache: 512 KB    shared with processor(s): 2
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15
Physical core:  2

Processor 11:
L1 cache: 64 KB     shared with processor(s): 3
L2 cache: 512 KB    shared with processor(s): 3
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15
Physical core:  3

Processor 12:
L1 cache: 64 KB     shared with processor(s): 4
L2 cache: 512 KB    shared with processor(s): 4
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15
Physical core:  4

Processor 13:
L1 cache: 64 KB     shared with processor(s): 5
L2 cache: 512 KB    shared with processor(s): 5
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15
Physical core:  5

Processor 14:
L1 cache: 64 KB     shared with processor(s): 6
L2 cache: 512 KB    shared with processor(s): 6
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15
Physical core:  6

Processor 15:
L1 cache: 64 KB     shared with processor(s): 7
L2 cache: 512 KB    shared with processor(s): 7
L3 cache: 32768 KB  shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
Physical core:  7
```

```
$ cputil
Available governors:
        performance
        schedutil

Available scaling frequencies:
        3800000
        2800000
        2200000

Current status:
Processor 0:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 1:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 10:   "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 11:   "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 12:   "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 13:   "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 14:   "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 15:   "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 2:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 3:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 4:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 5:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 6:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 7:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 8:    "schedutil" governor    frequency max = 3800000, min = 2200000
Processor 9:    "schedutil" governor    frequency max = 3800000, min = 2200000
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