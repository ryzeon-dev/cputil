//
// Created by master on 7/2/25.
//

#ifndef UTILS_H
#define UTILS_H

#include <vector>
using namespace std;

namespace utils {
    template <class T>
    inline bool contains(vector<T> iterable, T target) {
        for (auto entry : iterable) {
            if (entry == target) {
                return true;
            }
        }

        return false;
    }
}

#endif //UTILS_H
