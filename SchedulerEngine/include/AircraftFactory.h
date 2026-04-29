#pragma once
#include "Aircraft.h"
#include <map>
#include <string>

class AircraftFactory {
public:
    // Implements Factory Pattern utilizing dependency inversion principles logically
    static Aircraft createFromDatasetRow(const std::map<std::string, std::string>& datasetRow) {
        Aircraft a;
        // Parse raw string datasetRow into strongly typed Aircraft attributes natively...
        // Eg. a.flight_id = datasetRow.at("flight_id");
        return a;
    }
};
