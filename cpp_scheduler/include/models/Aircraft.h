#ifndef AIRCRAFT_H
#define AIRCRAFT_H

#include <string>

namespace airport {
namespace models {

class Aircraft {
public:
    std::string id;
    int eta;                   // Scheduled estimated time of arrival (Unix epoch or relative seconds)
    int actual_arrival_time;   // Calculated time after scheduling
    int ml_delay_score;        // Advisory ML predicted congestion delay
    bool is_emergency;
    std::string wake_category; // "H", "M", "L"
    
    // Constructors
    Aircraft();
    Aircraft(std::string id, int eta, bool is_emergency, std::string wake_cat, int ml_delay_score = 0);
    
    // Core Operator: Priority Queue natively uses this to construct a Min-Heap
    bool operator<(const Aircraft& other) const; 
};

} // namespace models
} // namespace airport

#endif // AIRCRAFT_H
