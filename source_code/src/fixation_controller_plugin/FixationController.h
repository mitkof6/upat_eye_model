/**
* @file FixationController.h
*
* \brief A
*
* @author Constantinos Filip <filipconstantinos@gmail.com>
*         Dimitar Stanev     <jimstanev@gmail.com>
*/
#ifndef FIXATION_CONTROLLER_H
#define FIXATION_CONTROLLER_H

#include "internal/FixationControllerExports.h"
#include <OpenSim/Simulation/Control/Controller.h>

namespace OpenSim {
    /**
     * \brief A
     *
     *
     */
    class FixationController_API FixationController : public Controller {
        OpenSim_DECLARE_CONCRETE_OBJECT(FixationController, Controller);
    public:
        OpenSim_DECLARE_PROPERTY(thetaH, double, "fixation target angle horizontal axis (in degrees)");
        OpenSim_DECLARE_PROPERTY(thetaV, double, "fixation target angle vertical axis (in degrees)");
        OpenSim_DECLARE_PROPERTY(kpH, double, "horizontal position tracking gain");
        OpenSim_DECLARE_PROPERTY(kdH, double, "horizontal velocity tracking gain");
        OpenSim_DECLARE_PROPERTY(kpV, double, "vertical position tracking gain");
        OpenSim_DECLARE_PROPERTY(kdV, double, "vertical velocity tracking gain");
        OpenSim_DECLARE_PROPERTY(kpT, double, "torsion position tracking gain");
        OpenSim_DECLARE_PROPERTY(kdT, double, "torsion velocity tracking gain");
        OpenSim_DECLARE_PROPERTY(saccade_onset, double, "saccade onset (s)");
        OpenSim_DECLARE_PROPERTY(saccade_velocity, double, "saccade velocity (in rad/s^2)");

        FixationController();
        ~FixationController() {};
        void constructProperties();
        // Controller::computeControls
        void computeControls(const SimTK::State& s, SimTK::Vector& controls)
            const override;
    };
}

#endif
