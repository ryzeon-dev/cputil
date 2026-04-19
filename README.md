# cputil
CPU performance utils and information tool CLI & daemon written in Python

# Install
### Debian amd64

```commandline
wget https://github.com/ryzeon-dev/cputil/releases/download/v7.0.0/cputil_7.0.0_amd64.deb && sudo apt install ./cputil_7.0.0_amd64.deb
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
`set, max, min, load, info, scaling, toplogy, temperature, usage, json, yaml, version, watch, help`

All the commands flagged with `*` require execution as `root`

## `set`*
- allows to set the value one cpu's parameter
- available parameters `governor, frequency minimum, frequency maximum, energy preference, clocksource`
- usage: `cputil set PARAMETER VALUE [-cpu]`
  - the `-cpu` flag allows to select the logical processor to affect with the setter
  - does not work with `set clocksource` 
- setters abbreviations:
  - `set governor -> sg`
  - `set frequency minimum -> sfm`
  - `set frequency maximum -> sfM`
  - `set energy prefrence -> sep`
  - `set clocksource -> sc`

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

## `json`
- can be abbreviated as `cputil j`
- `cputil json` shows all the available information in `JSON` format

## `yaml`
- can be abbreviated as `cputil y`
- `cputil yaml` shows all the available information in `YAML` format

## `version`
- can be abbreviated as `cputil v`
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

## Example outputs

```
$ cputil scaling

Available scaling governors:
	powersave
	performance

Available scaling frequencies:
	600000
	2981000
	5752000

Energy performance preferences:
	power
	balance_power
	balance_performance
	performance
	default

Clocksources:
	hpet
	acpi_pm
	tsc

Current scaling driver: amd-pstate-epp

Current clocksource: acpi_pm

Current status:
Processor 0:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 1:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 2:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 3:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 4:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 5:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 6:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 7:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 8:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
Processor 9:	powersave governor    frequency max = 5752000, min = 2981000    energy preference = balance_performance
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
```

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
BogoMIPS:               8583.71
Virtualization:         enabled
AMD P-State status:     active
AMD P-State prefcore:   enabled
Flags:                  fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good amd_lbr_v2 nopl xtopology nonstop_tsc cpuid extd_apicid aperfmperf rapl pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_pstate ssbd mba perfmon_v2 ibrs ibpb stibp ibrs_enhanced vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm rdt_a avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local user_shstk avx_vnni avx512_bf16 clzero irperf xsaveerptr rdpru wbnoinvd cppc arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload vgif v_spec_ctrl vnmi avx512vbmi umip pku ospke avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid bus_lock_detect movdiri movdir64b overflow_recov succor smca fsrm avx512_vp2intersect flush_l1d amd_lbr_pmc_freeze
```

```
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
```

```
$ cputil usage -avg
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
