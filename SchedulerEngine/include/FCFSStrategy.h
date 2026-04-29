#pragma once
#include "ISchedulerStrategy.h"
#include <queue>

class FCFSStrategy : public ISchedulerStrategy {
private:
    std::queue<Aircraft> q;

public:
    void addAircraft(const Aircraft& a) override {
        q.push(a);
    }
    Aircraft extractNext() override {
        Aircraft next_flight = q.front();
        q.pop();
        return next_flight;
    }
    bool isEmpty() const override {
        return q.empty();
    }
};
