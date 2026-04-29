#pragma once
#include <memory>
#include "ISchedulerStrategy.h"
#include "FCFSStrategy.h"
#include "PriorityStrategy.h"
#include "GreedyStrategy.h"

class SchedulerPolicyManager {
public:
    std::unique_ptr<ISchedulerStrategy> determineActiveStrategy(double system_load, const std::string& context) {
        // Applies Hybrid mechanism logic
        if (context == "Emergency") {
             // Forcibly drop down to emergency pipeline overrides instead of traditional queues
             return std::make_unique<PriorityStrategy>(); 
        }
        
        if (system_load > 0.85) {
             return std::make_unique<GreedyStrategy>(); // Heavy congestion 
        } else if (system_load > 0.50) {
             return std::make_unique<PriorityStrategy>(); // Medium 
        } else {
             return std::make_unique<FCFSStrategy>(); // Normal
        }
    }
};
