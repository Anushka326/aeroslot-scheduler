#pragma once
#include "Aircraft.h"
#include "ISchedulerStrategy.h"
#include "SchedulerPolicyManager.h"
#include "RunwayResourceManager.h"
#include "ConflictDetector.h"
#include "ConstraintManager.h"
#include "IEmergencyObserver.h"
#include <memory>
#include <iostream>

class Scheduler : public IEmergencyObserver {
private:
    std::unique_ptr<ISchedulerStrategy> current_strategy;
    SchedulerPolicyManager policy_manager;
    RunwayResourceManager resource_manager;
    ConflictDetector detector;
    ConstraintManager constraint_manager;
    
    double system_load;
    Aircraft last_scheduled;

public:
    Scheduler() : system_load(0.0) {}

    void generateStrategyEnvelope(const std::string& context) {
        current_strategy = policy_manager.determineActiveStrategy(system_load, context);
    }

    void addPendingAircraft(const Aircraft& a) {
        if (!current_strategy) {
            generateStrategyEnvelope("Normal"); 
        }
        current_strategy->addAircraft(a);
    }

    void processNext() {
        if (!current_strategy || current_strategy->isEmpty()) return;

        Aircraft candidate = current_strategy->extractNext();

        // Execution Pipeline:
        // 1. Evaluate Wake Matrices & Operational Constraints Layer
        if (constraint_manager.evaluateOperationalConstraints(candidate, last_scheduled)) {
            // 2. Tarmac Resource Verification Layer
            if (resource_manager.check_runway_availability()) {
                // 3. Absolute Mathematical Interval / Graph Safety Layer
                if (detector.is_safe(candidate)) {
                    
                    // Approved
                    resource_manager.assign(candidate);
                    detector.commit_allocation(candidate);
                    last_scheduled = candidate;
                } else {
                    candidate.updateWaitingTime();
                    addPendingAircraft(candidate); 
                }
            } else {
                addPendingAircraft(candidate); 
            }
        } else {
            addPendingAircraft(candidate); 
        }
    }

    // IEmergencyObserver Native System Interrupt Handler mapping
    void onEmergency(const Aircraft& emergency_f) override {
        std::cout << "[SYSTEM HALT] Interrupt Triggered by " << emergency_f.flight_id << "\n";
        
        generateStrategyEnvelope("Emergency");
        
        resource_manager.reservation_override();
        detector.clear_path_for(emergency_f);
        
        current_strategy->addAircraft(emergency_f);
        processNext(); 
    }
};
