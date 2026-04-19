#ifndef LIB_CPUTILD_H
#define LIB_CPUTILD_H

#include <string>
#include <vector>

using namespace std;
const string CPUFREQ_DIR = "/sys/devices/system/cpu/cpufreq";

namespace lib_cputild {
    vector<string> readScalingGovernors();
    vector<int> readScalingFrequencies();
    vector<string> readEnergyPerformancePreferences();
    vector<string> readClocksources();
    bool setMinScalingFrequency(int frequency);
    bool setMaxScalingFrequency(int frequency);
    bool setGovernor(string governor);
    bool setEnergyPerformancePreference(string energyPerformancePreference);
    bool setClocksource(string clocksource);
}

#endif //LIB_CPUTILD_H
