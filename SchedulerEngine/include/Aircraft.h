#pragma once
#include <string>
#include <cstdint>

struct Aircraft {
    std::string flight_id;
    int64_t arrival_time;
    int64_t departure_ready;
    int runway_occupancy;
    char wake_category;      // 'L', 'M', 'H', 'J'
    int priority_score;      // Baseline systemic priority 
    double congestion_level; // Snapshot of macro congestion
    
    // Safety & Interrupts
    bool emergency_flag;
    bool fuel_critical;
    bool medical_distress;
    bool technical_distress;
    
    // Priority aging
    int waiting_time_factor; 
    
    // Direct Operational Attributes
    std::string aircraft_type;
    int64_t eta_timestamp;
    int separation_requirement;
    std::string assigned_runway;
    std::string flight_status; // "Holding", "Taxiing", "Landing", "Departing", "Emergency"

    // Behavioral Methods ensuring Encapsulation
    void computeETA() {
        // Domain logic calculating physical delays to assign an exact ETA
    }
    
    void updateState(const std::string& new_status) {
        flight_status = new_status;
    }
    
    void calculateRunwayOccupancy() {
        // Empirically determine base ROT from aircraft_type, weather, speed mappings
    }
    
    int getEffectivePriority() const {
        return priority_score + waiting_time_factor;
    }
};
