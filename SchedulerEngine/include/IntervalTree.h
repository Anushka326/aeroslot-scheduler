#pragma once
#include "Aircraft.h"

struct IntervalNode {
    int64_t start_time;
    int64_t end_time;
    int64_t max_end;
    Aircraft occupant;
    IntervalNode* left;
    IntervalNode* right;

    IntervalNode(int64_t s, int64_t e, const Aircraft& a)
        : start_time(s), end_time(e), max_end(e), occupant(a), left(nullptr), right(nullptr) {}
};

class IntervalTree {
private:
    IntervalNode* root;

    IntervalNode* insert(IntervalNode* node, int64_t start, int64_t end, const Aircraft& a) {
        if (!node) return new IntervalNode(start, end, a);
        if (start < node->start_time) {
            node->left = insert(node->left, start, end, a);
        } else {
            node->right = insert(node->right, start, end, a);
        }
        if (node->max_end < end) {
            node->max_end = end;
        }
        return node;
    }

    bool isOverlapping(IntervalNode* node, int64_t start, int64_t end) const {
        if (!node) return false;
        if (node->start_time < end && start < node->end_time) return true;
        if (node->left && node->left->max_end >= start) {
            return isOverlapping(node->left, start, end);
        }
        return isOverlapping(node->right, start, end);
    }

public:
    IntervalTree() : root(nullptr) {}

    void addInterval(int64_t start, int64_t end, const Aircraft& a) {
        root = insert(root, start, end, a);
    }

    bool checkOverlap(int64_t start, int64_t end) const {
        return isOverlapping(root, start, end);
    }
};
