#pragma once
#include <string>
#include <list>
#include <optional>
#include "Aircraft.h"

struct Runway {
    std::string runway_id;
    std::string runway_type; // "arrival", "departure", "mixed"
    std::string status;
    
    std::list<Aircraft> queue_of_reserved_slots;
    int64_t occupancy_release_time;
    
    bool is_locked;
    std::optional<Aircraft> current_occupant;
};
