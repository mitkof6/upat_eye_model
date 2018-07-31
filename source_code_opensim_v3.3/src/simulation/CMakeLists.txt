file(GLOB includes *.h)
file(GLOB sources *.cpp)

include_directories(${CMAKE_SOURCE_DIR}/src/include/)
include_directories(${CMAKE_SOURCE_DIR}/src/fixation_controller_plugin)
set(DEPENDENCY_LIBRARIES FixationController)

# Simulation
set(target Simulation)
add_executable(${target} ${sources} ${includes})
target_link_libraries(${target} ${OpenSim_LIBRARIES} ${DEPENDENCY_LIBRARIES})

# set(ADDITIONAL_FILES
# )

foreach(dataFile ${ADDITIONAL_FILES})
  file(COPY "${dataFile}" DESTINATION "${CMAKE_CURRENT_BINARY_DIR}")
endforeach()


