//
// Created by master on 7/2/25.
//

#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <vector>
#include <string>
using namespace std;

namespace string_utils {
    vector<string> split(string text, char delimiter);
    string strip(string text);
}

#endif //STRING_UTILS_H
