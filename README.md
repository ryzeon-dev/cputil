# cputil
CPU performance utils CLI written in Python

```
$ cputil --help
cputil: cpu util CLI
usage: cputil [OPTIONS]

Options:
-sg  --set--governor         GOVERNOR     set governor (root)
-sfm --set-minimum-frequency FREQUENCY    set minimum frequency (root)
-sfM --set-maximum-frequency FREQUENCY    set maximum frequency (root)
-cpu CPU       Select which thread to affect with action,
if omitted the action will affect all threads,
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
Cores count:    8
Threads count:  16
Clock boost:    active
Minimum clock:  2.2 GHz
Maximum clock:  3.8 GHz
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