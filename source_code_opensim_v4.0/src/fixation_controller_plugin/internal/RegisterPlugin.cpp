#include "RegisterPlugin.h"
#include <OpenSim/Simulation/Model/ExpressionBasedCoordinateForce.h>
#include "../FixationController.h"

using namespace OpenSim;

// OpenSim bug: when <OpenSim/OpenSim.h> is included then instantiator is
// redefined so make sure not to include <OpenSim/OpenSim.h> in your
// implementation
static dllObjectInstantiator instantiator;

void RegisterPlugin() {
    // fix OpenSim bug: ExpressionBasedCoordinateForce is not registered, thus
    // it can't be used in the .osim model.
    Object::RegisterType(ExpressionBasedCoordinateForce());
    // Object::RegisterType(FixationController());
}

dllObjectInstantiator::dllObjectInstantiator() {
    registerDllClasses();
}

void dllObjectInstantiator::registerDllClasses() {
    RegisterPlugin();
}