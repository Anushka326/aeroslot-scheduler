#pragma once
#include "Aircraft.h"
#include "IEmergencyObserver.h"
#include <vector>

class EmergencyManager {
private:
    std::vector<IEmergencyObserver*> observers;

public:
    void registerObserver(IEmergencyObserver* obs) {
        observers.push_back(obs);
    }
    
    static bool compareEmergencies(const Aircraft& a, const Aircraft& b) {
        if (a.fuel_critical != b.fuel_critical) return a.fuel_critical;
        if (a.medical_distress != b.medical_distress) return a.medical_distress;
        if (a.technical_distress != b.technical_distress) return a.technical_distress;
        return a.arrival_time < b.arrival_time;
    }
    
    void handleSystemInterrupt(const Aircraft& a) {
        if(a.emergency_flag) {
            for(auto* obs : observers) {
                obs->onEmergency(a);
            }
        }
    }
};
