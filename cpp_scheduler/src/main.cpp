#include <iostream>
#include "strategies/Scheduler.h"

int main() {
    std::cout << "\n=============================================\n";
    std::cout << "   SMART AI-BASED RUNWAY SCHEDULER (C++ CORE)  \n";
    std::cout << "=============================================\n";
    
    airport::strategies::SmartScheduler engine("27L");
    
    // Simulating Operational Payload natively mimicking Python APIs securely
    std::cout << "[San Francisco - SFO Prototype Mode (27L)]\n";
    std::cout << "\n[C++ Engine Surface]\n";
    for (const auto& item : airport::strategies::SmartScheduler::engine_manifest()) {
        std::cout << " - " << item << "\n";
    }
    
    engine.add_flight(airport::models::Aircraft("AAL112", 100, false, "H", 300));
    engine.add_flight(airport::models::Aircraft("UAL88",  110, false, "M", 50));
    engine.add_flight(airport::models::Aircraft("DAL34",  110, false, "M", 900)); // High ML Congestion Score
    engine.add_flight(airport::models::Aircraft("SWA99",  120, false, "L", 10));
    
    // Injecting explicit emergency preemption overriding absolute bounds completely securely
    engine.add_flight(airport::models::Aircraft("MEDEVAC1", 130, true, "L", 0)); 
    
    engine.add_flight(airport::models::Aircraft("JBU77",  140, false, "H", 150));
    
    // 1. Run Baseline FCFS (Will strictly lock queue structures natively)
    engine.schedule_fcfs();
    
    // 2. Run Smart C++ Priority Min-Heap seamlessly checking interval bounds organically
    engine.schedule_priority();

    return 0;
}
