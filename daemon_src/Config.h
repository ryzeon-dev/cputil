//
// Created by master on 7/3/25.
//

#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <iostream>

using namespace std;

class Config {
public:
    Config(string p) : path(p) {}

    void update();

    void reveal() {
        cout << "governor: " << governor << "\nmin_scaling_freq: " << minScalingFreq << "\nmax_scaling_freq: " << maxScalingFreq << "\nenergy_performance_preference: " << energyPerformancePreference << "\npolling_interval: " << pollingInterval << endl;
    }

    string getGovernor() const {
        return governor;
    }

    int getMinScalingFreq() const {
        return minScalingFreq;
    }

    int getMaxScalingFreq() const {
        return maxScalingFreq;
    }

    string getEnergyPerformancePreferece() const {
        return energyPerformancePreference;
    }

    int getPollingInterval() const {
        return pollingInterval;
    }

private:
    string path;

    string governor = "";
    int minScalingFreq = 0;
    int maxScalingFreq = 0;
    string energyPerformancePreference = "";
    int pollingInterval = 0;
};



#endif //CONFIG_H
