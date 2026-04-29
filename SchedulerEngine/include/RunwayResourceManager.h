#pragma once
#include "Aircraft.h"
#include <mutex>
#include <optional>

class RunwayResourceManager {
private:
    bool is_locked;
    std::optional<Aircraft> current_occupant;
    std::mutex mtx;

public:
    RunwayResourceManager() : is_locked(false) {}

    bool check_runway_availability() {
        std::lock_guard<std::mutex> lock(mtx);
        return !is_locked; 
    }

    void assign(const Aircraft& f) {
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
        is_locked = false; 
        current_occupant = std::nullopt;
    }
};
