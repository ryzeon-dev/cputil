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

    string getClocksource() const {
        return this->clocksource;
    }

private:
    string path;

    string governor = "auto";
    int minScalingFreq = -1;
    int maxScalingFreq = -1;
    string energyPerformancePreference = "auto";
    int pollingInterval = 10;
    string clocksource = "auto";
};



#endif //CONFIG_H
