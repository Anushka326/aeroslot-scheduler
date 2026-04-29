#ifndef CONFLICT_DETECTOR_H
#define CONFLICT_DETECTOR_H

#include <vector>
#include <string>
#include <map>

namespace airport {
namespace strategies {

// Simple Interval representation tracking structural boundaries
struct TimeInterval {
    int start_time;
    int end_time;
    std::string aircraft_id;
};

class ConflictDetector {
private:
    // Runway ID -> Vector of allocated intervals 
    std::map<std::string, std::vector<TimeInterval>> runway_schedule;
    
public:
    ConflictDetector();
    
    // Interval check preventing overlaps natively
    bool is_safe(const std::string& runway_id, int requested_start, int requested_end) const;
    
    // Lock physics bounding structurally
    void allocate_interval(const std::string& runway_id, int start, int end, const std::string& ac_id);
    
    // Resolving specific Wake Separation restrictions generically
    int get_separation_padding(const std::string& wake_category) const;
};

}
}

#endif
