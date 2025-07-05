#include <unistd.h>
#include "lib_cputild.h"
#include "Config.h"

int main() {
    Config config("/etc/cputild/cputild.conf");

    while (true) {
        config.update();

        if (config.getGovernor() != "auto") {
            cout << "setting governor to " << config.getGovernor() << endl;

            if (!lib_cputild::setGovernor(config.getGovernor()))
                cout << "failure while setting governor" << endl;

        }

        if (config.getMaxScalingFreq() != -1) {
            cout << "setting max_scaling_freq to " << config.getMaxScalingFreq() << endl;

            if (!lib_cputild::setMaxScalingFrequency(config.getMaxScalingFreq()))
                cout << "failure while setting max_scaling_freq" << endl;
        }

        if (config.getMinScalingFreq() != -1) {
            cout << "setting min_scaling_freq to " << config.getMinScalingFreq() << endl;

            if (!lib_cputild::setMinScalingFrequency(config.getMinScalingFreq()))
                cout << "failure while setting min_scaling_freq" << endl;
        }

        if (config.getEnergyPerformancePreferece() != "auto") {
            cout << "setting energy_performance_preference to " << config.getEnergyPerformancePreferece() << endl;

            if (!lib_cputild::setEnergyPerformancePreference(config.getEnergyPerformancePreferece()))
                cout << "failure while setting energy_performance_preference" << endl;
        }

        sleep(config.getPollingInterval());

    }

    return 0;
}