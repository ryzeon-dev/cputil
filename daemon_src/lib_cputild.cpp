//
// Created by master on 7/2/25.
//

#include "lib_cputild.h"

#include <filesystem>
#include <sys/dir.h>
#include <fstream>
#include <iostream>
#include <ranges>
#include "string_utils.h"
#include "utils.h"

bool isPolicy(string policy) {
    return policy.starts_with("policy");
}

bool writeCpufreqFile(string filename, string value) {
    for (auto entry : filesystem::directory_iterator(CPUFREQ_DIR)) {
        if (entry.is_directory() && isPolicy(entry.path().filename())) {
            string filePath = entry.path().string() + "/" + filename;
            ofstream file(filePath);

            if (!file.is_open()) {
                return false;
            }

            file << value;
            file.close();
        }
    }

    return true;
}



vector<string> lib_cputild::readScalingGovernors() {
    DIR* cpufreq = opendir(CPUFREQ_DIR.c_str());

    if (cpufreq == NULL) {
        return vector<string>();
    }
    vector<string> governors;

    struct dirent* entry;

    while ((entry = readdir(cpufreq)) != NULL) {
        if (!isPolicy(entry->d_name)) {
            continue;
        }

        string governorFilePath = CPUFREQ_DIR + "/" + entry->d_name + "/scaling_available_governors";
        ifstream governorFile(governorFilePath.c_str());

        string fileContent = "";
        string buffer;

        while (getline(governorFile, buffer)) {
            fileContent += buffer;
        }

        vector<string> govs = string_utils::split(fileContent, ' ');
        for (auto gov : govs) {
            if (!gov.empty() && !utils::contains(governors, gov)) {
                governors.push_back(gov);
            }
        }
    }

    closedir(cpufreq);
    return governors;
}

vector<int> lib_cputild::readScalingFrequencies() {
    DIR* cpufreq = opendir(CPUFREQ_DIR.c_str());

    if (cpufreq == NULL) {
        return vector<int>();
    }
    vector<int> frequencies;

    struct dirent* entry;

    while ((entry = readdir(cpufreq)) != NULL) {
        if (!isPolicy(entry->d_name)) {
            continue;
        }

        string maxFreqPath = CPUFREQ_DIR + "/" + entry->d_name + "/scaling_max_freq";
        ifstream maxFreqFile(maxFreqPath.c_str());

        string fileContent = "";
        string buffer;

        while (getline(maxFreqFile, buffer)) {
            fileContent += buffer;
        }

        int ufreq = atoi(fileContent.c_str());
        if (ufreq != 0 && !utils::contains(frequencies, ufreq)) {
            frequencies.push_back(ufreq);
        }

        maxFreqFile.close();

        string minFreqPath = CPUFREQ_DIR + "/" + entry->d_name + "/scaling_min_freq";
        ifstream minFreqFile(minFreqPath.c_str());

        fileContent = "";

        while (getline(minFreqFile, buffer)) {
            fileContent += buffer;
        }

        minFreqFile.close();

        ufreq = atoi(fileContent.c_str());
        if (ufreq && !utils::contains(frequencies, ufreq)) {
            frequencies.push_back(ufreq);
        }
    }

    closedir(cpufreq);
    return frequencies;
}

vector<string> lib_cputild::readEnergyPerformancePreferences() {
    DIR* cpufreq = opendir(CPUFREQ_DIR.c_str());

    if (cpufreq == NULL) {
        return vector<string>();
    }
    vector<string> epps;

    struct dirent* entry;

    while ((entry = readdir(cpufreq)) != NULL) {
        if (!isPolicy(entry->d_name)) {
            continue;
        }

        string eppPath = CPUFREQ_DIR + "/" + entry->d_name + "/energy_performance_available_preferences";
        ifstream eppFile(eppPath.c_str());

        if (!eppFile.is_open()) {
            continue;
        }

        string fileContent = "";
        string buffer;

        while (getline(eppFile, buffer)) {
            fileContent += buffer;
        }

        vector<string> epp = string_utils::split(fileContent, ' ');
        for (auto e : epp) {
            if (!e.empty() && !utils::contains(epps, e)) {
                epps.push_back(e);
            }
        }
    }

    closedir(cpufreq);
    return epps;
}

vector<string> lib_cputild::readClocksources() {
    vector<string> clocksources;

    string clocksourcesPath = "/sys/devices/system/clocksource/clocksource0/available_clocksource";
    ifstream clocksourceFile(clocksourcesPath.c_str());

    if (!clocksourceFile.is_open()) {
        return clocksources;
    }

    string fileContent = "";
    string buffer;

    while (getline(clocksourceFile, buffer)) {
        fileContent += buffer;
    }

    clocksources = string_utils::split(fileContent, ' ');
    return clocksources;
}



bool lib_cputild::setGovernor(string governor) {
    if (utils::contains(lib_cputild::readScalingGovernors(), governor)) {
        return writeCpufreqFile("scaling_governor", governor);
    }
    return false;
}

bool lib_cputild::setMinScalingFrequency(int frequency) {
    if (utils::contains(lib_cputild::readScalingFrequencies(), frequency)) {
        return writeCpufreqFile("scaling_min_freq", to_string(frequency));
    }

    return false;
}

bool lib_cputild::setMaxScalingFrequency(int frequency) {
    if (utils::contains(lib_cputild::readScalingFrequencies(), frequency)) {
        return writeCpufreqFile("scaling_max_freq", to_string(frequency));
    }

    return false;
}

bool lib_cputild::setEnergyPerformancePreference(string energyPerformancePreference) {
    if (utils::contains(lib_cputild::readEnergyPerformancePreferences(), energyPerformancePreference)) {
        return writeCpufreqFile("energy_performance_preference", energyPerformancePreference);
    }

    return false;
}

bool lib_cputild::setClocksource(string clocksource) {
    if (utils::contains(lib_cputild::readClocksources(), clocksource)) {
        string filePath = "/sys/devices/system/clocksource/clocksource0/current_clocksource";
        ofstream file(filePath);

        if (!file.is_open()) {
            return false;
        }

        file << clocksource;
        file.close();
        return true;
    }

    return false;
}
