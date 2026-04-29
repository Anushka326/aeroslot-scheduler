#pragma once
#include "ISchedulerStrategy.h"
#include <queue>
#include <vector>

struct PriorityAgingCompare {
    bool operator()(const Aircraft& a, const Aircraft& b) {
        int effective_priority_a = a.priority_score + a.waiting_time_factor;
        int effective_priority_b = b.priority_score + b.waiting_time_factor;
        if (effective_priority_a == effective_priority_b) {
            return a.arrival_time > b.arrival_time; // FCFS fallback
        }
        return effective_priority_a < effective_priority_b; 
    }
};

class PriorityStrategy : public ISchedulerStrategy {
private:
    std::priority_queue<Aircraft, std::vector<Aircraft>, PriorityAgingCompare> pq;

public:
    void addAircraft(const Aircraft& a) override {
        pq.push(a);
    }
    Aircraft extractNext() override {
        Aircraft next_flight = pq.top();
        pq.pop();
        return next_flight;
    }
    bool isEmpty() const override {
        return pq.empty();
    }
};
