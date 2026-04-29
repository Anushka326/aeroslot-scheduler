#pragma once
#include "Flight.h"
#include <mutex>
#include <optional>

class RunwayStateManager {
private:
    bool is_locked;
    std::optional<Flight> current_occupant;
    std::mutex mtx;

public:
    RunwayStateManager() : is_locked(false) {}

    bool check_runway_availability() {
        std::lock_guard<std::mutex> lock(mtx);
        return !is_locked; // True if tarmac is unobstructed
    }

    void assign(const Flight& f) {
        std::lock_guard<std::mutex> lock(mtx);
        is_locked = true;
        current_occupant = f;
    }

    void release() {
        std::lock_guard<std::mutex> lock(mtx);
        is_locked = false;
        current_occupant = std::nullopt;
    }
    
    void reservation_override() {
        std::lock_guard<std::mutex> lock(mtx);
        // Force break existing holds specifically designed for Preemptive Emergencies
        is_locked = false; 
        current_occupant = std::nullopt;
    }
};
