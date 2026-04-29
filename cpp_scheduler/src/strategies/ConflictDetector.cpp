#include "strategies/ConflictDetector.h"
#include <iostream>
#include <algorithm>

namespace airport {
namespace strategies {

ConflictDetector::ConflictDetector() {}

int ConflictDetector::get_separation_padding(const std::string& wake_category) const {
    if (wake_category == "H") return 120; // Heavy Wake = 2 minutes
    if (wake_category == "M") return 90; 
    return 60; // Light Wake
}

bool ConflictDetector::is_safe(const std::string& runway_id, int requested_start, int requested_end) const {
    auto it = runway_schedule.find(runway_id);
    if (it == runway_schedule.end()) return true; // Empty runway optimally safe natively
    
    // Interval intersection logic structurally verifying overlaps cleanly
    for (const auto& interval : it->second) {
        // Condition for strict strict overlap: [S1, E1] intersects [S2, E2] if max(S1,S2) < min(E1,E2)
        int latest_start = std::max(interval.start_time, requested_start);
        int earliest_end = std::min(interval.end_time, requested_end);
        
        if (latest_start < earliest_end) {
            return false; // Physical Overlap Detected natively
        }
    }
    return true;
}

void ConflictDetector::allocate_interval(const std::string& runway_id, int start, int end, const std::string& ac_id) {
    runway_schedule[runway_id].push_back({start, end, ac_id});
}

}
}
