#pragma once
#include "ISchedulerStrategy.h"
#include <queue>
#include <vector>

// Uses Min Heap coupled with a mathematical heuristic scoring function
struct GreedyDelayCompare {
    bool operator()(const Aircraft& a, const Aircraft& b) {
        // Minimizing separation times while acknowledging baseline priorities natively
        int penalty_a = a.separation_requirement * 2 - a.priority_score;
        int penalty_b = b.separation_requirement * 2 - b.priority_score;
        
        return penalty_a > penalty_b; // Operates Min Heap Extraction 
    }
};

class GreedyStrategy : public ISchedulerStrategy {
private:
    std::priority_queue<Aircraft, std::vector<Aircraft>, GreedyDelayCompare> candidate_pool;

public:
    void addAircraft(const Aircraft& a) override {
        candidate_pool.push(a);
    }

    Aircraft extractNext() override {
        Aircraft best_fit = candidate_pool.top();
        candidate_pool.pop();
        return best_fit;
    }

    bool isEmpty() const override {
        return candidate_pool.empty();
    }
};
