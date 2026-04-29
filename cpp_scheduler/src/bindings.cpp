#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/models/Aircraft.h"
#include "../include/Scheduler.h"

namespace py = pybind11;

/**
 * Pybind11 Shared Memory Bridging.
 * Exposes the exact C++ physical scheduling algorithms seamlessly into standard python API objects
 * ensuring absolute Sub-Second execution latencies without Microservice HTTP overhead organically natively.
 */
PYBIND11_MODULE(scheduler_engine_core, m) {
    m.doc() = "C++ Scheduler Engine bindings natively compiled for Python Orchestration.";

    py::class_<Aircraft>(m, "Aircraft")
        .def(py::init<std::string, int64_t, char, int, bool, std::string>())
        .def("getEffectivePriority", &Aircraft::getEffectivePriority)
        .def("occupancyEstimate", &Aircraft::occupancyEstimate)
        .def_property_readonly("flight_id", &Aircraft::getFlightId);

    py::class_<Scheduler>(m, "Scheduler")
        .def(py::init<>())
        .def("addPendingAircraft", &Scheduler::addPendingAircraft)
        .def("processNext", &Scheduler::processNext)
        
        // Critical Native Python -> C++ Override Command bypasses normal loops
        .def("onEmergency", &Scheduler::onEmergency);
        
        // Return ACK vectors back traversing memory space boundary here...
}
