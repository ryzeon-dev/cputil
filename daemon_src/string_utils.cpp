//
// Created by master on 7/2/25.
//

#include "string_utils.h"
vector<string> string_utils::split(string text, char delimiter) {
    string chunk = "";
    vector<string> chunks;

    for (auto chr : text) {
        if (chr == delimiter) {
            chunks.push_back(chunk);
            chunk = "";
        } else {
            chunk += chr;
        }
    }

    chunks.push_back(chunk);

    return chunks;
}

string string_utils::strip(string text) {
    int startIndex = 0;

    while (startIndex < text.length() && (text[startIndex] == ' ' || text[startIndex] == '\n' || text[startIndex] == '\r' || text[startIndex] == '\t')) {
        startIndex++;
    }

    int endIndex = text.length() - 1;
    while (endIndex > startIndex && (text[endIndex] == ' ' || text[endIndex] == '\n' || text[endIndex] == '\r' || text[endIndex] == '\t')) {
        endIndex--;
    }

    return text.substr(startIndex, endIndex - startIndex + 1);
}
