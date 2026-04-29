#pragma once
#include "Flight.h"
#include <map>
#include <utility>

class WakeSeparationManager {
private:
    // pair<leader, follower> -> time_seconds buffer
    std::map<std::pair<char, char>, int> wake_matrix = {
        {{'H', 'L'}, 180}, {{'H', 'M'}, 120}, {{'H', 'H'}, 90},
        {{'M', 'L'}, 120}, {{'M', 'M'}, 60},  {{'M', 'H'}, 60},
        {{'L', 'L'}, 60},  {{'L', 'M'}, 60},  {{'L', 'H'}, 60}
    };
    
    double weather_factor;

public:
    WakeSeparationManager() : weather_factor(1.0) {}
    
    void updateWeatherFactor(double factor) {
        weather_factor = factor; // Extrapolation for poor visibility/crosswinds
    }
    
    int getSeparationBuffer(char leader_wake, char follower_wake) const {
        auto it = wake_matrix.find({leader_wake, follower_wake});
        int base_sep = (it != wake_matrix.end()) ? it->second : 60; // Baseline 60s generic limit
        return static_cast<int>(base_sep * weather_factor);
    }
    
    bool check_wake_separation(const Flight& candidate, const Flight& last_flight, int64_t current_time) const {
        int req_sep = getSeparationBuffer(last_flight.wake_category, candidate.wake_category);
        int64_t elapsed_since_last = current_time - last_flight.arrival_time;
        return elapsed_since_last >= req_sep;
    }
};
