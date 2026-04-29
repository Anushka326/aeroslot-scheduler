#include <iostream>
#include <cassert>
#include "models/Aircraft.h"

void testAircraftAging() {
    // Flight arrive at T=1000, Wake H, Base Priority 5
    Aircraft a("AAL123", 1000, 'H', 5, false, "B777");
    
    // Simulate elapsed time (Current T=1050)
    a.updateWaitingTime(1050);
    
    // Effective Priority Test: Base 5 + (alpha * waiting_time)
    double alpha = 0.5;
    int expected_effective = 5 + static_cast<int>(0.5 * 50); // 5 + 25 = 30
    
    assert(a.getEffectivePriority(alpha) == expected_effective);
    std::cout << "[PASS] Aircraft Priority Aging Validation\n";
}

void testAircraftOccupancy() {
    Aircraft a1("AAL123", 1000, 'H', 5, false, "B777");
    Aircraft a2("DAL456", 1000, 'L', 5, false, "CRJ9");
    
    // Heavy vs Light constraints test bounds directly 
    assert(a1.occupancyEstimate() == 65);
    assert(a2.occupancyEstimate() == 45);
    std::cout << "[PASS] Aircraft ROT Category Evaluation\n";
}

int main() {
    std::cout << "--- Starting Unit Tests: test_aircraft.cpp ---\n";
    testAircraftAging();
    testAircraftOccupancy();
    std::cout << "--- All Aircraft Tests PASSED ---\n";
    return 0;
}
