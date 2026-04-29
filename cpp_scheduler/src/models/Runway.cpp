#include "models/Runway.h"

// Construct standard generic runway objects natively
Runway::Runway(std::string id, std::string type)
    : runway_id(id), runway_type(type), status("free"), release_time(0), is_locked(false) {}

bool Runway::isAvailable(int64_t current_time) const {
    if (is_locked) {
        // Automatically signals unlock if chronological progression clears boundary constraint
        return current_time >= release_time;
    }
    return true; // Idle
}

void Runway::lockRunway(int64_t occupancy_duration, int64_t current_time) {
    is_locked = true;
    status = "locked";
    release_time = current_time + occupancy_duration;
}

void Runway::unlockRunway() {
    is_locked = false;
    status = "free";
    release_time = 0;
}
