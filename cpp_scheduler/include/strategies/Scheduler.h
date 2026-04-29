#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <queue>
#include <vector>
#include <string>
#include "models/Aircraft.h"
#include "strategies/ConflictDetector.h"

namespace airport {
namespace strategies {

// Custom comparator for building the Min-Heap securely natively
struct PriorityComparator {
    bool operator()(const models::Aircraft& a, const models::Aircraft& b) {
        // High ML delay scores get priority natively
        if (a.is_emergency != b.is_emergency) return !a.is_emergency; // Emergencies top natively
        if (a.ml_delay_score != b.ml_delay_score) return a.ml_delay_score < b.ml_delay_score;
        return a.eta > b.eta; // Earliest ETA pops first 
    }
};

class SmartScheduler {
private:
    std::queue<models::Aircraft> fcfs_queue;
    std::priority_queue<models::Aircraft, std::vector<models::Aircraft>, PriorityComparator> priority_heap;
    
    ConflictDetector safety_detector;
    std::string primary_runway;
    
public:
    SmartScheduler(std::string runway_id);
    
    // Injects payload directly
    void add_flight(const models::Aircraft& ac);
    
    // Extracts exact optimal matrices locally smoothly
    void schedule_fcfs();
    void schedule_priority();
    
    // Core Engine Logic
    int attempt_allocation(const models::Aircraft& ac, int target_start);

    // Submission-grade engine surface used by the Python/React explanation layer.
    static std::vector<std::string> engine_manifest();
};

}
}

#endif
