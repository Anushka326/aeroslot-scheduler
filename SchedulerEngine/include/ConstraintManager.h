#pragma once
#include "Aircraft.h"
#include "WakeSeparationManager.h"
#include <memory>

class ConstraintManager {
private:
    std::unique_ptr<WakeSeparationManager> wake_manager;

public:
    ConstraintManager() : wake_manager(std::make_unique<WakeSeparationManager>()) {}

    bool evaluateOperationalConstraints(const Aircraft& candidate, const Aircraft& preceding) {
        // Passes to the operational boundary checkers
        if(!wake_manager->check_wake_separation(candidate, preceding, candidate.eta_timestamp)) {
            return false;
        }
        
        // Can hold future logic representing standard operations (Gate sizes, Slot caps)
        return true; 
    }
};
