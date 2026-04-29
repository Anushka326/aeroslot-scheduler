#pragma once
#include <string>
#include <cstdint>

class Runway {
private:
    std::string runway_id;
    std::string runway_type; // "arrival", "departure", "mixed"
    std::string status;      // "free", "locked"
    int64_t release_time;
    bool is_locked;

public:
    Runway(std::string id, std::string type);

    // Operational Bounds
    bool isAvailable(int64_t current_time) const;
    void lockRunway(int64_t occupancy_duration, int64_t current_time);
    void unlockRunway();
    
    // Getters natively decoupling queue states
    std::string getId() const { return runway_id; }
    std::string getStatus() const { return status; }
};
