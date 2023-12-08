# cputil
CPU performance utils CLI written in Python

### Disclaimer
This software has only be tested on AMD CPUs yet. If you experience any unexpected behaviour, please open up an issue

```
$ cputil --help
cputil: cpu util CLI
usage: cputil [OPTIONS]

Options:
    -sg  --set--governor GOVERNOR             set governor
    -sfm --set-minimum-frequency FREQUENCY    set minimum frequency
    -sfM --set-maximum-frequency FREQUENCY    set maximum frequency
    -i   --info    Show info about CPU
    -cpu CPU       Select which thread to affect with action,
                   if omitted any action will affect all threads
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
Thread 0:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 1:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 10:      "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 11:      "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 12:      "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 13:      "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 14:      "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 15:      "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 2:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 3:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 4:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 5:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 6:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 7:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 8:       "schedutil" governor    frequency max = 3800000, min = 2200000
Thread 9:       "schedutil" governor    frequency max = 3800000, min = 2200000
```
