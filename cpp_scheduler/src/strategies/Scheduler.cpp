#include "strategies/Scheduler.h"
#include <iostream>

namespace airport {
namespace strategies {

SmartScheduler::SmartScheduler(std::string runway_id) : primary_runway(runway_id) {}

void SmartScheduler::add_flight(const models::Aircraft& ac) {
    fcfs_queue.push(ac);
    priority_heap.push(ac);
}

int SmartScheduler::attempt_allocation(const models::Aircraft& ac, int target_start) {
    int separation = safety_detector.get_separation_padding(ac.wake_category);
    int current_attempt = target_start;
    
    // Scans dynamically identifying exactly minimum available threshold cleanly natively
    while (!safety_detector.is_safe(primary_runway, current_attempt, current_attempt + separation)) {
        current_attempt += 30; // 30 sec step resolution
    }
    
    safety_detector.allocate_interval(primary_runway, current_attempt, current_attempt + separation, ac.id);
    return current_attempt;
}

std::vector<std::string> SmartScheduler::engine_manifest() {
    return {
        "FCFS Queue: preserves arrival order for baseline runway sequencing",
        "Priority Queue: ranks emergency, fuel urgency, passenger and cargo priority",
        "Min-Delay Heap: greedily selects aircraft with lowest delay impact",
        "Graph Taxi Routing: models taxiway reroute and runway closure paths",
        "Hash Map Lookup: O(1) flight lookup for live tower decisions",
        "Greedy Heuristics: balances runway utilization and wake separation"
    };
}

void SmartScheduler::schedule_fcfs() {
    std::cout << "\n[Scheduler] Executing FCFS Engine Array...\n";
    std::cout << "-------------------------------------------\n";
    int delay_accumulator = 0;
    
    std::queue<models::Aircraft> local_q = fcfs_queue;
    while (!local_q.empty()) {
        models::Aircraft ac = local_q.front();
        local_q.pop();
        
        int assigned_time = attempt_allocation(ac, ac.eta);
        int delay = assigned_time - ac.eta;
        delay_accumulator += delay;
        
        std::cout << "Flight " << ac.id << " [ETA: " << ac.eta << "s] -> Runway 27L @ " 
                  << assigned_time << "s | Delay: " << delay << "s\n";
    }
    std::cout << "=> Total FCFS System Delay: " << delay_accumulator << "s\n";
}

void SmartScheduler::schedule_priority() {
    std::cout << "\n[Scheduler] Executing Priority Heap Engine...\n";
    std::cout << "-------------------------------------------\n";
    int delay_accumulator = 0;
    
    // Clear old state safely resolving natively
    safety_detector = ConflictDetector(); 
    
    std::priority_queue<models::Aircraft, std::vector<models::Aircraft>, PriorityComparator> local_pq = priority_heap;
    while (!local_pq.empty()) {
        models::Aircraft ac = local_pq.top();
        local_pq.pop();
        
        int assigned_time = attempt_allocation(ac, ac.eta);
        int delay = assigned_time - ac.eta;
        delay_accumulator += delay;
        
        std::string flag = ac.is_emergency ? " [EMERGENCY]" : "";
        std::cout << "Flight " << ac.id << flag << " [ETA: " << ac.eta << "s | ML: " << ac.ml_delay_score 
                  << "] -> Runway 27L @ " << assigned_time << "s | Delay: " << delay << "s\n";
    }
    std::cout << "=> Total Priority System Delay: " << delay_accumulator << "s\n";
}

}
}
