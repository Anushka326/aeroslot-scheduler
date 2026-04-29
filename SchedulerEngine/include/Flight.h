#pragma once
#include <string>
#include <cstdint>

struct Flight {
    std::string flight_id;
    int64_t arrival_time;
    int64_t departure_ready;
    int runway_occupancy;
    char wake_category;      // 'L', 'M', 'H', 'J'
    int priority_score;      // Baseline systemic priority 
    double congestion_level; // Snapshot of macro congestion
    
    // Safety & Interrupts
    bool emergency_flag;
    
    // Emergency specifics for tie-breaking
    bool fuel_critical;
    bool medical_distress;
    bool technical_distress;
    
    // Priority aging
    int waiting_time_factor; 
};
