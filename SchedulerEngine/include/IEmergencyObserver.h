#pragma once
#include "Aircraft.h"

// Listener interface for absolute preemptive system overrides
class IEmergencyObserver {
public:
    virtual ~IEmergencyObserver() = default;
    
    // Callback event forcing priority halts
    virtual void onEmergency(const Aircraft& a) = 0;
};
