# cputil
A Linux CLI tool and daemon for CPU inspection, diagnostics, and tuning. One command to see everything about your processor — and one command to change it.

cputil combines what you'd normally get from lscpu, cpupower, sensors, and manual sysfs poking into a single tool with a clean interface. It has first-class support for AMD P-State and Zen-specific features like prefcore ranking and CCD-aware topology.

## Quick look
```commandline
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
```

```commandline
$ cputil cstate
States:
  C1   -> ACPI FFH MWAIT 0x0 [latency: 1]
  C2   -> ACPI IOPORT 0x414 [latency: 18]
  C3   -> ACPI IOPORT 0x415 [latency: 350]
  POLL -> CPUIDLE CORE POLL IDLE [latency: 0]

Percent values since boot

Core  0    C1 [enabled]:   0.22 %    C2 [enabled]:   0.58 %    C3 [enabled]:  99.18 %    POLL [enabled]:   0.02 %
Core  1    C1 [enabled]:   0.36 %    C2 [enabled]:   0.98 %    C3 [enabled]:  98.64 %    POLL [enabled]:   0.02 %
Core  2    C1 [enabled]:   0.18 %    C2 [enabled]:   1.28 %    C3 [enabled]:  98.51 %    POLL [enabled]:   0.03 %
Core  3    C1 [enabled]:   0.43 %    C2 [enabled]:   1.60 %    C3 [enabled]:  97.94 %    POLL [enabled]:   0.03 %
Core  4    C1 [enabled]:   0.24 %    C2 [enabled]:   0.62 %    C3 [enabled]:  99.12 %    POLL [enabled]:   0.02 %
Core  5    C1 [enabled]:   0.27 %    C2 [enabled]:   0.64 %    C3 [enabled]:  99.07 %    POLL [enabled]:   0.02 %
Core  6    C1 [enabled]:   0.20 %    C2 [enabled]:   1.16 %    C3 [enabled]:  98.62 %    POLL [enabled]:   0.02 %
Core  7    C1 [enabled]:   0.28 %    C2 [enabled]:   0.69 %    C3 [enabled]:  99.01 %    POLL [enabled]:   0.03 %
...
```

```commandline
$ cputil info
Model name:             AMD Ryzen 9 9950X 16-Core Processor
Architecture:           amd64 / x86_64 (64bit)
Byte order:             Little Endian (first bit is LSB)
Cores count:            16
Threads count:          32
Clock boost:            active
Minimum clock:          0.6 GHz
Maximum clock:          5.75 GHz
BogoMIPS:               8583.31
Virtualization:         enabled
AMD P-State status:     active
AMD P-State prefcore:   enabled
Flags:                  fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good amd_lbr_v2 nopl xtopology nonstop_tsc cpuid extd_apicid aperfmperf rapl pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_pstate ssbd mba perfmon_v2 ibrs ibpb stibp ibrs_enhanced vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm rdt_a avx512f avx512dq adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local user_shstk avx_vnni avx512_bf16 clzero irperf xsaveerptr rdpru wbnoinvd cppc arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload vgif v_spec_ctrl vnmi avx512vbmi umip pku ospke avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid bus_lock_detect movdiri movdir64b overflow_recov succor smca fsrm avx512_vp2intersect flush_l1d amd_lbr_pmc_freeze
```

# Features
**Inspect** — CPU info, topology, cache hierarchy, scaling configuration, temperatures, energy consumption (Intel RAPL), per-core usage breakdown, C-state idle residency, AMD prefcore ranking with CCD grouping, and known CPU vulnerabilities with mitigation status.

**Tune** — Set scaling governors, frequency limits, energy performance preferences, clocksource, and C-state enable/disable per core. Or use `cputil max` / `cputil min` to instantly switch between performance and powersave profiles.

**Persist** — The companion daemon (`cputild`) continuously enforces your configuration, re-applying it on a configurable polling interval so settings survive suspend/resume cycles and system events.

**Export** — Full system data available in JSON and YAML for scripting and automation.

# Install
### Debian amd64

```bash
wget https://github.com/ryzeon-dev/cputil/releases/download/v8.0.0/cputil_8.0.0_amd64.deb 
sudo apt install ./cputil_8.0.0_amd64.deb
```
> **Note**: the `.deb` package was built on Debian 13, which may result in incompatibility with older Debian versions 

### Build from source
Requires: `python3, python3-venv, python3-pip, cmake, make, build-essential`

```bash
git clone https://github.com/ryzeon-dev/cputil
cd cputil

# Install everything (CLI + daemon)
sudo bash install.sh all

# Or install individually
sudo bash install.sh bin        # CLI ONLY
sudo bash install.sh daemon     # daemon only
```

### Uninstall
```bash
sudo bash uninstall.sh all # or: bin / daemon
```

# Usage
`cputil [COMMAND [arg] [OPTION]]`

###  Information commands
| Command       | Alias | Description                                                      |
|:--------------|:---:|------------------------------------------------------------------|
| `info`        | `i` | CPU model, architecture, cores, clocks, flags (default)          |
| `scaling`     | `s` | Governors, frequencies, energy preferences, per-core settings    |
| `topology`    | `t` | Cache hierarchy and sharing, physical core/die mapping           | 
| `temperature` | `T` | CPU temperature sensor readings                                  |
| `energy`      | `e` | Energy consumption via Intel RAPL sensors                        |
| `prefcore`    | `p` | Prefcore ranking per core with CCD grouping                      | 
| `cstate`      | `c` | C-state idle residency per core, with latency and enable status  | 
| `vuln`        | `v` | CPU vulnerabilities and mitigation status                        | 
| `usage` | `u` | Average and per-logical-processor usage and frequency | 
| `watch`       | `w` | Continuous live reading of usage and temperature                 |
| `all`         | `a` | Show all of the above in sequence                                |

### Tuning commands (root required)
| Command                             | Alias | Description                                                                |
|:------------------------------------|:-----:|----------------------------------------------------------------------------|
| `set governor VALUE`                | `sg`  | Set scaling governor                                                       |
| `set frequency minimum VALUE`       | `sfm` | Set minimum scaling frequency                                              |
| `set frequency maximum VALUE`       | `sfM` | Set maximum scaling frequency                                              |
| `set energy preference VALUE`       | `sep` | Set energy performance preference                                          | 
| `set clocksource VALUE`             | `sc`  | Set clocksource                                                            |
| `set cstate STATE enabled/disabled` | `sC`  | Enable or disable a C-state                                                |
| `max`                               | - | Performance mode: `performance` governor, max frequency, `performance` EPP |
| `min` | - | Powersave mode: `powersave` governor, min frequency, `power` EPP           | 
| `load CONF` | `l` | Load a configuration template                                              | 

The `-cpu N` option can be used with `set governor`, `set frequency minimum`, and `set frequency maximum` to target a specific logical processor.

### Export commands

| Command | Alias | Description |
|:---|:---:|---|
| `json` | `j` | All available information in JSON format |
| `yaml` | `y` | All available information in YAML format |
| `dump` | `d` | Show currently loaded cputild configuration |

# Daemon

The `cputild` daemon maintains your CPU configuration persistently. It runs as a systemd service and re-applies settings on a configurable polling interval (default: 10 seconds).
 
Configuration lives at `/etc/cputild/cputild.conf`. Template configurations can be saved in `/etc/cputild/templates/` and loaded with `cputil load`.
 
Configuration parameters:
 
| Parameter | Description                              |
|-----------|------------------------------------------|
| `governor` | Scaling governor to enforce              |
| `min_scaling_frequency` | Minimum frequency to enforce|
| `max_scaling_frequency` | Maximum frequency to enforce|
| `energy_performance_preference` | EPP value to enforce|
| `clocksource` | Clocksource to enforce|
| `polling_interval` | How often to re-apply settings (seconds) |
 
Set any parameter to `auto` to leave it unmanaged.

# How it compares
 
| | cputil | cpupower | auto-cpufreq | power-profiles-daemon |
|---|---|---|---|---|
| CPU info & diagnostics | ✓ | partial | ✗ | ✗ |
| Frequency tuning | ✓ | ✓ | automatic | profile-based |
| AMD prefcore ranking | ✓ | ✗ | ✗ | ✗ |
| C-state inspection & control | ✓ | ✓ | ✗ | ✗ |
| Energy monitoring (RAPL) | ✓ | ✗ | ✗ | ✗ |
| Vulnerability audit | ✓ | ✗ | ✗ | ✗ |
| Persistent daemon | ✓ | ✗ | ✓ | ✓ |
| JSON/YAML export | ✓ | ✗ | ✗ | ✗ |
 
# License
 
[AGPL-3.0](LICENSE)

***

### Sample output

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
...

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
...

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
...

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