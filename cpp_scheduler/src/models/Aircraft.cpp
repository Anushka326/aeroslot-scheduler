#include "models/Aircraft.h"

namespace airport {
namespace models {

Aircraft::Aircraft() : id(""), eta(0), actual_arrival_time(0), ml_delay_score(0), is_emergency(false), wake_category("M") {}

Aircraft::Aircraft(std::string id, int eta, bool is_emergency, std::string wake_cat, int ml_delay_score)
    : id(id), eta(eta), actual_arrival_time(0), is_emergency(is_emergency), wake_category(wake_cat), ml_delay_score(ml_delay_score) {}

// Standard Min-Heap comparator default natively
bool Aircraft::operator<(const Aircraft& other) const {
    if (this->eta == other.eta) {
        return this->ml_delay_score < other.ml_delay_score;
    }
    return this->eta < other.eta;
}

}
}
