//
// Created by master on 7/2/25.
//

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
    bool setMinScalingFrequency(int frequency);
    bool setMaxScalingFrequency(int frequency);
    bool setGovernor(string governor);
    bool setEnergyPerformancePreference(string energyPerformancePreference);
}

#endif //LIB_CPUTILD_H
