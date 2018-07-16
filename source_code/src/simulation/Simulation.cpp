/**
 * @file Simulation.cpp
 *
 * \brief Loads the baseline model, removes the linear tissue forces and adds
 * and ExpressionBasedCoordinateForce. A custom FixationController is added to
 * the model and a forward simulation is carried. All results are stored in the
 * model/ folder.
 *
 * @author Constantinos Filip <filipconstantinos@gmail.com>
 *         Dimitar Stanev     <jimstanev@gmail.com>
 *
 * @see <a href="https://simtk.org/projects/eye">[SimTK Project]</a>, <a
 * href="XXX">[Publication]</a>
 */
#include <iostream>
#include <OpenSim/OpenSim.h>
#include <FixationController.h>
#include <Settings.h>

using namespace std;
using namespace OpenSim;
using namespace SimTK;

// Used to pause the flow of the program.
#define PAUSE cout << endl << "press a key to continue ..." << endl; getchar();

void addExpressionCoordinateForce(Model* model) {
    // remove other forces first
    model->updForceSet().remove(
        model->updForceSet().getIndex(
        &model->updForceSet().get("add_adb_tissue"), 0));

    model->updForceSet().remove(
        model->updForceSet().getIndex(
        &model->updForceSet().get("sup_inf_tissue"), 0));

    model->updForceSet().remove(
        model->updForceSet().getIndex(
        &model->updForceSet().get("inc_exc_tissue"), 0));

    // Add expression based coordinate forces (don't use spaces in the
    // expression). Linux users may experience problem with Lepton (v3.3), most
    // recent versions may not have this problem.
    auto add_adb_tissue =
        new ExpressionBasedCoordinateForce("r_eye_add_abd",
                                           "-0.002225*q-34.5297*0.0001*q^3-0*0.002*qdot");
    add_adb_tissue->setName("add_adb_tissue");
    model->addForce(add_adb_tissue);

    auto sup_inf_tissue =
        new ExpressionBasedCoordinateForce("r_eye_sup_inf",
                                           "-0.002225*q-34.5297*0.0001*q^3-0*0.002*qdot");
    sup_inf_tissue->setName("sup_inf_tissue");
    model->addForce(sup_inf_tissue);

    auto inc_exc_tissue =
        new ExpressionBasedCoordinateForce("r_eye_inc_exc",
                                           "-0.002225*q-34.5297*0.0001*q^3-0*0.002*qdot");
    inc_exc_tissue->setName("inc_exc_tissue");
    model->addForce(inc_exc_tissue);
}

void simulateModel() {
    Model model(MODEL_DIR + "UPAT_Eye_Model_Passive_Pulleys_v2.osim");
    model.setName("UPAT_Eye_Model_Passive_Pulleys_v3");

    // Add expression based coordinate force
    addExpressionCoordinateForce(&model);

    // Create a controller
    FixationController* controller = new FixationController();
    controller->setName("fixation_controller");
    controller->set_thetaH(-15);
    controller->set_thetaV(15);
    controller->set_kpH(50);
    controller->set_kdH(1.5);
    controller->set_kpV(50);
    controller->set_kdV(1.5);
    controller->set_kpT(100);
    controller->set_kdT(0.5);
    controller->set_saccade_onset(0.5);
    controller->set_saccade_velocity(600); // deg / s
    model.addController(controller);

    // Build and initialize model
    auto& state = model.initSystem();
    model.equilibrateMuscles(state);

    // Create the integrator and manager for the simulation
    RungeKuttaMersonIntegrator integrator(model.getMultibodySystem());
    Manager manager(model, integrator);

    // Integrate from initial time to final time
    manager.setInitialTime(0);
    manager.setFinalTime(1.0);
    manager.integrate(state);

    // Save simulation results
    model.printControlStorage(MODEL_DIR + model.getName() + "_Controls.sto");
    manager.getStateStorage().print(MODEL_DIR + model.getName() + "_States.sto");
    model.print(MODEL_DIR + model.getName() + ".osim");
}

int main(int argc, char *argv[]) {
    try {
        simulateModel();
    } catch (exception &e) {
        cout << typeid(e).name() << ": " << e.what() << endl;
        PAUSE;
        return -1;
    }
    PAUSE;
    return 0;
}