# cputil
CPU performance utils and information tool CLI & daemon written in Python and C++

# Install
### Debian amd64

```commandline
wget https://github.com/ryzeon-dev/cputil/releases/download/v8.0.0/cputil_8.0.0_amd64.deb && sudo apt install ./cputil_8.0.0_amd64.deb
```
Please note that the `.deb` package was built on Debian 13, which may result in incompatibility with older Debian versions 

### Compile from source and install

- compilation requires 
  - `python3`
  - `python3-venv`
  - `python3-pip` 
  - `cmake`
  - `make`
  - `build-essential`
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
`cputil [COMMAND [arg] [OPTION]]`

## Available commands
`set, max, min, load, all, info, scaling, toplogy, temperature, usage, energy, prefcore, cstate, vuln, json, yaml, version, watch, help`

All the commands flagged with `*` require execution as `root`

## `set`*
- allows to set the value one cpu's parameter
- available parameters `governor, frequency minimum, frequency maximum, energy preference, clocksource`
- usage: `cputil set PARAMETER VALUE [-cpu]`
  - the `-cpu` flag allows to select the logical processor to affect with the setter
  - does not work with `set clocksource` and `set cstate`
- cstate setting has a different syntax:
  - `set cstate STATE enabled/disabled`
- setters abbreviations:
  - `set governor -> sg`
  - `set frequency minimum -> sfm`
  - `set frequency maximum -> sfM`
  - `set energy prefrence -> sep`
  - `set clocksource -> sc`
  - `set cstate -> sC`

## `max`*
- sets the processor into `maximum performance` mode
  - sets `performance` scaling governor
  - sets both minimum and maximum frequency to the highest available value
  - sets the energy performance preference to `performance`

## `min`*
- sets the processor into `minimum performance` mode
  - sets `powersave` scaling governor
  - sets both minimum and maximum frequency to the lowest available value
  - sets the energy performance preference to `power`

## `load`*
- loads a performance template configuration file
- the configuration files can be saved into `/etc/cputild/templates`
- usage: `cputil load CONF_FILE`
- `CONF_FILE` can either be a filepath, or a filename if saved into `/etc/cputild/templates`

## `all`
- can be abbreviated as `cputil a`
- shows, in order, the following information:
  - processor info 
  - scaling info
  - topology info
  - energy info
  - prefcore info
  - c-state info
  - vulnerabilities info
  - temperature info
  - usage info

## `info`
- can be abbreviated as `cputil i`
- `cputil info` shows:
  - model name
  - architecture
  - byte order
  - cores count
  - threads count
  - clock boost availability
  - minimum clock
  - maximum clock
  - bogomips
  - virtualization availability
  - AMD p-state (if available)
  - flags

# `scaling`
- can be abbreviated as `cputil s`
- `cputil scaling` shows:
  - available scaling governors
  - available scaling frequencies
  - available energy performance preferences
  - available clocksourecs
  - current scaling driver
  - current clocksource
  - per-processor setting of `scaling governor, frequencies, energy performance preference`

## `topology`
- can be abbreviated as `cputil t`
- `cputil topology` shows per-processor:
  - `L1` cache size and sharing
  - `L2` cache size and sharing
  - `L3` cache size and sharing
  - `physical core` id
  - `physical die` id 

## `temperature`
- can be abbreviated as `cputil T`
- `cputil temperature` shows the reading of all the cpu related temperature sensors

## `usage`
- can be abbreviated as `cputil u`
- `cputil usage` shows average and per-processor:
  - `total` usage
  - `user` usage
  - `nice` usage
  - `system` usage
  - `idle` usage
  - `iowait` usage
  - `interrupt` usage
  - `soft-interrupt` usage
  - `steal` usage
  - `guest` usage
  - `guest_nice` usage
  - `frequency` in MHz
- if the `-avg` flag is added, ony shows average usage info

## `energy`
- can be abbreviated as `cputil e`
- shows energy consumption in Joule, listing every available sensor
- may require root privilegies to execute

## `prefcore`
- can be abbreviated as `cputil p`
- shows per-core prefcore ranking

## `cstate`
- can be abbreviated as `cputil c`
- shows:
  - available idle states, with relative description and latency
  - per-core c-state usage and if enabled/disabled

## `vuln`
- can be abbreviated as `cputil v`
- shows the system-known CPU vulnerabilities and if the processor is affected
  - if affected, shows how they are mitigated

## `json`
- can be abbreviated as `cputil j`
- `cputil json` shows all the available information in `JSON` format

## `yaml`
- can be abbreviated as `cputil y`
- `cputil yaml` shows all the available information in `YAML` format

## `version`
- can be abbreviated as `cputil V`
- `cputil version` shows the current `cputil` version

## `watch`
- can be abbreviated as `cputil w`
- `cputil watch` shows continuous reading of:
  - average cpu usage
  - current temperature(s) reading(s)

## `help`
- can be abbreviated as `cputil h`
- `cputil help` shows the help message and exits

## Daemon
- maintains cpu parameters setting
- in the installation process, it is configured as a systemd service, and started
- once installed (refer to the Install section), the daemon will loop, executing its procedure every 60 seconds
  - it reads the configuration file, located at `/etc/cputild/cputild.conf`
  - parses the configuration, and applies it 
- the value assigned to configuration parameters must be allowed, check the available values in your system running `cputil` 
- if any parameter is set to `auto`, it will not be modified
- configuration parameters are:
  - `governor`
  - `min_scaling_frequency`
  - `max_scaling_frequency`
  - `energy_performance_preference`
  - `polling_interval` (default value is 10 seconds)

## Sample output

```
$ cputil info
Model name:             AMD Ryzen 9 9950X 16-Core Processor
Architecture:           amd64 / x86_64 (64bit)
Byte order:             Little Endian (first bit is LSB)
Cores count:            16
Threads count:          32
Clock boost:            active
Minimum clock:          0.6 GHz
Maximum clock:          5.75 GHz
BogoMIPS:               8583.74
Virtualization:         enabled
AMD P-State status:     active
AMD P-State prefcore:   enabled
Flags:                  fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good amd_lbr_v2 nopl xtopology nonstop_tsc cpuid extd_apicid aperfmperf rapl pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_pstate ssbd mba perfmon_v2 ibrs ibpb stibp ibrs_enhanced vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm rdt_a avx512f avx512dq adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local user_shstk avx_vnni avx512_bf16 clzero irperf xsaveerptr rdpru wbnoinvd cppc arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload vgif v_spec_ctrl vnmi avx512vbmi umip pku ospke avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid bus_lock_detect movdiri movdir64b overflow_recov succor smca fsrm avx512_vp2intersect flush_l1d amd_lbr_pmc_freeze

$ cputil scaling
Available scaling governors:
	powersave
	performance

Available scaling frequencies:
	600000
	2981000
	5752000

Energy performance preferences:
	balance_power
	power
	default
	balance_performance
	performance

Clocksources:
	acpi_pm
	tsc
	hpet

Current scaling driver: amd-pstate-epp

Current clocksource: tsc

Current status:
Processor  0:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  1:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  2:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  3:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  4:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  5:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  6:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  7:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  8:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor  9:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 10:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 11:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 12:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 13:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 14:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 15:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 16:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 17:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 18:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 19:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 20:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 21:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 22:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 23:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 24:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 25:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 26:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 27:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 28:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 29:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 30:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 31:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance

$ cputil topology

Processor 0:
    L2 cache: 1024 KB	shared with processor(s): 16
    L1 cache: 80 KB	shared with processor(s): 16
    L3 cache: 32768 KB	shared with processor(s): 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 0
    Physical die: 0

Processor 1:
    L2 cache: 1024 KB	shared with processor(s): 17
    L1 cache: 80 KB	shared with processor(s): 17
    L3 cache: 32768 KB	shared with processor(s): 0, 2, 3, 4, 5, 6, 7, 16
    Physical core: 1
    Physical die: 0

Processor 2:
    L2 cache: 1024 KB	shared with processor(s): 18
    L1 cache: 80 KB	shared with processor(s): 18
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 3, 4, 5, 6, 7, 16
    Physical core: 2
    Physical die: 0

Processor 3:
    L2 cache: 1024 KB	shared with processor(s): 19
    L1 cache: 80 KB	shared with processor(s): 19
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 4, 5, 6, 7, 16
    Physical core: 3
    Physical die: 0

Processor 4:
    L2 cache: 1024 KB	shared with processor(s): 20
    L1 cache: 80 KB	shared with processor(s): 20
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 5, 6, 7, 16
    Physical core: 4
    Physical die: 0

Processor 5:
    L2 cache: 1024 KB	shared with processor(s): 21
    L1 cache: 80 KB	shared with processor(s): 21
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 6, 7, 16
    Physical core: 5
    Physical die: 0

Processor 6:
    L2 cache: 1024 KB	shared with processor(s): 22
    L1 cache: 80 KB	shared with processor(s): 22
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 7, 16
    Physical core: 6
    Physical die: 0

Processor 7:
    L2 cache: 1024 KB	shared with processor(s): 23
    L1 cache: 80 KB	shared with processor(s): 23
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 16
    Physical core: 7
    Physical die: 0

Processor 8:
    L2 cache: 1024 KB	shared with processor(s): 24
    L1 cache: 80 KB	shared with processor(s): 24
    L3 cache: 32768 KB	shared with processor(s): 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 8
    Physical die: 1

Processor 9:
    L2 cache: 1024 KB	shared with processor(s): 25
    L1 cache: 80 KB	shared with processor(s): 25
    L3 cache: 32768 KB	shared with processor(s): 8, 10, 11, 12, 13, 14, 15, 24
    Physical core: 9
    Physical die: 1

Processor 10:
    L2 cache: 1024 KB	shared with processor(s): 26
    L1 cache: 80 KB	shared with processor(s): 26
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 11, 12, 13, 14, 15, 24
    Physical core: 10
    Physical die: 1

Processor 11:
    L2 cache: 1024 KB	shared with processor(s): 27
    L1 cache: 80 KB	shared with processor(s): 27
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 12, 13, 14, 15, 24
    Physical core: 11
    Physical die: 1

Processor 12:
    L2 cache: 1024 KB	shared with processor(s): 28
    L1 cache: 80 KB	shared with processor(s): 28
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 13, 14, 15, 24
    Physical core: 12
    Physical die: 1

Processor 13:
    L2 cache: 1024 KB	shared with processor(s): 29
    L1 cache: 80 KB	shared with processor(s): 29
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 14, 15, 24
    Physical core: 13
    Physical die: 1

Processor 14:
    L2 cache: 1024 KB	shared with processor(s): 30
    L1 cache: 80 KB	shared with processor(s): 30
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 15, 24
    Physical core: 14
    Physical die: 1

Processor 15:
    L2 cache: 1024 KB	shared with processor(s): 31
    L1 cache: 80 KB	shared with processor(s): 31
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 24
    Physical core: 15
    Physical die: 1

Processor 16:
    L2 cache: 1024 KB	shared with processor(s): 0
    L1 cache: 80 KB	shared with processor(s): 0
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 0
    Physical die: 0

Processor 17:
    L2 cache: 1024 KB	shared with processor(s): 1
    L1 cache: 80 KB	shared with processor(s): 1
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 1
    Physical die: 0

Processor 18:
    L2 cache: 1024 KB	shared with processor(s): 2
    L1 cache: 80 KB	shared with processor(s): 2
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 2
    Physical die: 0

Processor 19:
    L2 cache: 1024 KB	shared with processor(s): 3
    L1 cache: 80 KB	shared with processor(s): 3
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 3
    Physical die: 0

Processor 20:
    L2 cache: 1024 KB	shared with processor(s): 4
    L1 cache: 80 KB	shared with processor(s): 4
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 4
    Physical die: 0

Processor 21:
    L2 cache: 1024 KB	shared with processor(s): 5
    L1 cache: 80 KB	shared with processor(s): 5
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 5
    Physical die: 0

Processor 22:
    L2 cache: 1024 KB	shared with processor(s): 6
    L1 cache: 80 KB	shared with processor(s): 6
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 6
    Physical die: 0

Processor 23:
    L2 cache: 1024 KB	shared with processor(s): 7
    L1 cache: 80 KB	shared with processor(s): 7
    L3 cache: 32768 KB	shared with processor(s): 0, 1, 2, 3, 4, 5, 6, 7, 16
    Physical core: 7
    Physical die: 0

Processor 24:
    L2 cache: 1024 KB	shared with processor(s): 8
    L1 cache: 80 KB	shared with processor(s): 8
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 8
    Physical die: 1

Processor 25:
    L2 cache: 1024 KB	shared with processor(s): 9
    L1 cache: 80 KB	shared with processor(s): 9
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 9
    Physical die: 1

Processor 26:
    L2 cache: 1024 KB	shared with processor(s): 10
    L1 cache: 80 KB	shared with processor(s): 10
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 10
    Physical die: 1

Processor 27:
    L2 cache: 1024 KB	shared with processor(s): 11
    L1 cache: 80 KB	shared with processor(s): 11
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 11
    Physical die: 1

Processor 28:
    L2 cache: 1024 KB	shared with processor(s): 12
    L1 cache: 80 KB	shared with processor(s): 12
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 12
    Physical die: 1

Processor 29:
    L2 cache: 1024 KB	shared with processor(s): 13
    L1 cache: 80 KB	shared with processor(s): 13
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 13
    Physical die: 1

Processor 30:
    L2 cache: 1024 KB	shared with processor(s): 14
    L1 cache: 80 KB	shared with processor(s): 14
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 14
    Physical die: 1

Processor 31:
    L2 cache: 1024 KB	shared with processor(s): 15
    L1 cache: 80 KB	shared with processor(s): 15
    L3 cache: 32768 KB	shared with processor(s): 8, 9, 10, 11, 12, 13, 14, 15, 24
    Physical core: 15
    Physical die: 1

$ cputil temperature
Tctl: 40.875 C

$ cputil usage
Average:
    total:              0.75 %
    user:               0.25 %
    nice:               0.0 %
    system:             0.38 %
    idle:               99.25 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.13 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency:		4281.98 MHz

Processor: 0
    total:              3.85 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               96.15 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     3.85 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3702.17 MHz

Processor: 1
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3917.58 MHz

Processor: 2
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3860.97 MHz

Processor: 3
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		4016.32 MHz

Processor: 4
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 5
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 6
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5720.48 MHz

Processor: 7
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5716.27 MHz

Processor: 8
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5427.97 MHz

Processor: 9
    total:              3.85 %
    user:               0.0 %
    nice:               0.0 %
    system:             3.85 %
    idle:               96.15 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		4154.04 MHz

Processor: 10
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 11
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 12
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5459.81 MHz

Processor: 13
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 14
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 15
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5459.36 MHz

Processor: 16
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 17
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3738.72 MHz

Processor: 18
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 19
    total:              3.85 %
    user:               3.85 %
    nice:               0.0 %
    system:             0.0 %
    idle:               96.15 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3799.37 MHz

Processor: 20
    total:              4.0 %
    user:               4.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               96.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5721.52 MHz

Processor: 21
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3878.06 MHz

Processor: 22
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5722.47 MHz

Processor: 23
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5723.14 MHz

Processor: 24
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5465.84 MHz

Processor: 25
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		4909.28 MHz

Processor: 26
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5428.47 MHz

Processor: 27
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3532.7 MHz

Processor: 28
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		3917.49 MHz

Processor: 29
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5459.13 MHz

Processor: 30
    total:              0.0 %
    user:               0.0 %
    nice:               0.0 %
    system:             0.0 %
    idle:               100.0 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		2981.0 MHz

Processor: 31
    total:              11.11 %
    user:               0.0 %
    nice:               0.0 %
    system:             11.11 %
    idle:               88.89 %
    iowait:             0.0 %
    interrupt:          0.0 %
    soft-interrupt:     0.0 %
    steal:              0.0 %
    guest:              0.0 %
    guest_nice:         0.0 %
    Frequency: 		5463.3 MHz

$ cputil energy
Intel RAPL: enabled
Sensors:
    core: 0.60196 J/s
    package-0: 36.612976 J/s

$ cputil prefcore
Core  0 [CCD0]: 216
Core  1 [CCD0]: 221
Core  2 [CCD0]: 236  [preferred]
Core  3 [CCD0]: 231
Core  4 [CCD0]: 236  [preferred]
Core  5 [CCD0]: 226
Core  6 [CCD0]: 206
Core  7 [CCD0]: 211
Core  8 [CCD1]: 176
Core  9 [CCD1]: 191
Core 10 [CCD1]: 196
Core 11 [CCD1]: 201
Core 12 [CCD1]: 181
Core 13 [CCD1]: 186
Core 14 [CCD1]: 166
Core 15 [CCD1]: 171

$ cputil cstate
States:
  C1   -> ACPI FFH MWAIT 0x0 [latency: 1]
  C2   -> ACPI IOPORT 0x414 [latency: 18]
  C3   -> ACPI IOPORT 0x415 [latency: 350]
  POLL -> CPUIDLE CORE POLL IDLE [latency: 0]

Core  0    C1 [enabled]:   0.81 %    C2 [enabled]:   1.91 %    C3 [enabled]:  97.25 %    POLL [enabled]:   0.04 %
Core  1    C1 [enabled]:   1.23 %    C2 [enabled]:   2.68 %    C3 [enabled]:  96.04 %    POLL [enabled]:   0.04 %
Core  2    C1 [enabled]:   0.75 %    C2 [enabled]:   1.80 %    C3 [enabled]:  97.42 %    POLL [enabled]:   0.04 %
Core  3    C1 [enabled]:   1.44 %    C2 [enabled]:   3.37 %    C3 [enabled]:  95.15 %    POLL [enabled]:   0.04 %
Core  4    C1 [enabled]:   0.77 %    C2 [enabled]:   1.92 %    C3 [enabled]:  97.26 %    POLL [enabled]:   0.04 %
Core  5    C1 [enabled]:   0.61 %    C2 [enabled]:   4.23 %    C3 [enabled]:  95.12 %    POLL [enabled]:   0.04 %
Core  6    C1 [enabled]:   0.57 %    C2 [enabled]:   3.19 %    C3 [enabled]:  96.20 %    POLL [enabled]:   0.04 %
Core  7    C1 [enabled]:   0.96 %    C2 [enabled]:   2.18 %    C3 [enabled]:  96.81 %    POLL [enabled]:   0.04 %
Core  8    C1 [enabled]:   1.58 %    C2 [enabled]:   3.35 %    C3 [enabled]:  95.04 %    POLL [enabled]:   0.03 %
Core  9    C1 [enabled]:   1.80 %    C2 [enabled]:   5.52 %    C3 [enabled]:  92.65 %    POLL [enabled]:   0.04 %
Core 10    C1 [enabled]:   1.66 %    C2 [enabled]:   3.55 %    C3 [enabled]:  94.75 %    POLL [enabled]:   0.04 %
Core 11    C1 [enabled]:   3.06 %    C2 [enabled]:   5.74 %    C3 [enabled]:  91.12 %    POLL [enabled]:   0.08 %
Core 12    C1 [enabled]:   1.20 %    C2 [enabled]:   2.37 %    C3 [enabled]:  96.40 %    POLL [enabled]:   0.03 %
Core 13    C1 [enabled]:   1.21 %    C2 [enabled]:   2.17 %    C3 [enabled]:  96.59 %    POLL [enabled]:   0.03 %
Core 14    C1 [enabled]:   1.16 %    C2 [enabled]:   2.02 %    C3 [enabled]:  96.79 %    POLL [enabled]:   0.03 %
Core 15    C1 [enabled]:   1.64 %    C2 [enabled]:  17.43 %    C3 [enabled]:  80.91 %    POLL [enabled]:   0.02 %

$ cputil vuln
spectre_v2                -> Mitigation: Enhanced / Automatic IBRS; IBPB: conditional; STIBP: always-on; PBRSB-eIBRS: Not affected; BHI: Not affected
indirect_target_selection -> Not affected
itlb_multihit             -> Not affected
vmscape                   -> Mitigation: IBPB on VMEXIT
mmio_stale_data           -> Not affected
mds                       -> Not affected
reg_file_data_sampling    -> Not affected
tsa                       -> Not affected
l1tf                      -> Not affected
spec_store_bypass         -> Mitigation: Speculative Store Bypass disabled via prctl
tsx_async_abort           -> Not affected
spectre_v1                -> Mitigation: usercopy/swapgs barriers and __user pointer sanitization
gather_data_sampling      -> Not affected
retbleed                  -> Not affected
spec_rstack_overflow      -> Mitigation: IBPB on VMEXIT only
srbds                     -> Not affected
meltdown                  -> Not affected
```