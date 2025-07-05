//
// Created by master on 7/3/25.
//

#include "Config.h"
#include <fstream>
#include "string_utils.h"


void Config::update() {
    ifstream file(this->path);

    if (!file.is_open()) {
        throw std::runtime_error("Config::update: Could not open config file");
    }

    string line;
    while (getline(file, line)) {
        if (line.starts_with('#') || line.empty()) {
            continue;
        }


        if (line.substr(0, 9) == "governor:") {\
            int colonIndex = line.find(':') + 1;
            int length = line.length();

            this->governor = string_utils::strip(line.substr(colonIndex, length - colonIndex));

        } else if (line.substr(0, 30) ==  "energy_performance_preference:") {
            int colonIndex = line.find(':') + 1;
            int length = line.length();

            this->energyPerformancePreference = string_utils::strip(line.substr(colonIndex, length - colonIndex));

        } else if (line.substr(0, 22) == "min_scaling_frequency:") {
            int colonIndex = line.find(':') + 1;
            int length = line.length();

            string stripped = string_utils::strip(line.substr(colonIndex, length - colonIndex));
            if (stripped == "auto") {
                this->minScalingFreq = -1;

            } else {
                this->minScalingFreq = atoi(stripped.c_str());;
            }

        } else if (line.substr(0, 22) == "max_scaling_frequency:") {
            int colonIndex = line.find(':') + 1;
            int length = line.length();

            string stripped = string_utils::strip(line.substr(colonIndex, length - colonIndex));
            if (stripped == "auto") {
                this->maxScalingFreq = -1;

            } else {
                this->maxScalingFreq = atoi(stripped.c_str());;
            }

        } else if (line.substr(0, 17) == "polling_interval:") {
            int colonIndex = line.find(':') + 1;
            int length = line.length();

            string stripped = string_utils::strip(line.substr(colonIndex, length - colonIndex));
            if (stripped == "auto") {
                this->pollingInterval = 10;

            } else {
                this->pollingInterval = atoi(stripped.c_str());;
            }
        }
    }
}
