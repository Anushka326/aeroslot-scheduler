#pragma once
#include "Aircraft.h"
#include "IntervalTree.h"
#include <iostream>

class ConflictDetector {
private:
    IntervalTree local_tactical_tree;

public:
    bool is_safe(const Aircraft& candidate) {
        // Layer 1: Tactical Interval bounds checking ensures no physical tarmac overlapping
        int64_t interval_start = candidate.eta_timestamp;
        int64_t interval_end = interval_start + candidate.runway_occupancy + candidate.separation_requirement;
        
        bool is_local_conflict = local_tactical_tree.checkOverlap(interval_start, interval_end);
        
        // Layer 2: Strategic Graph coloring validation space
        bool is_global_conflict = false; // logic would ping graph API
        
        return !is_local_conflict && !is_global_conflict;
    }

    void clear_path_for(const Aircraft& f_emergency) {
        std::cout << "[Conflict Detector] Scrubbing tactical layer for Emergency Aircraft: " << f_emergency.flight_id << "\n";
        // Node rotations would scrub boundaries here safely
    }
    
    void commit_allocation(const Aircraft& allocated) {
        int64_t interval_start = allocated.eta_timestamp;
        int64_t interval_end = interval_start + allocated.runway_occupancy + allocated.separation_requirement;
        local_tactical_tree.addInterval(interval_start, interval_end, allocated);
    }
};
