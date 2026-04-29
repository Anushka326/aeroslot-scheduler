#pragma once
#include "Aircraft.h"

class ISchedulerStrategy {
public:
    virtual ~ISchedulerStrategy() = default;
    virtual void addAircraft(const Aircraft& a) = 0;
    virtual Aircraft extractNext() = 0;
    virtual bool isEmpty() const = 0;
};
