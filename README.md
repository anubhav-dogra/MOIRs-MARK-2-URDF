# MOIRs-MARK-2-URDF
This package provides the tools to generate the customized manipulator configurations (`n'-DoF), even with non-parallel and non-parallel jointed configurations, using the unconventional modular library. 

If you are using this work in any form, Please cite this article:

```
@article{DOGRAUnified2022,
title = {Unified modeling of unconventional modular and reconfigurable manipulation system},
journal = {Robotics and Computer-Integrated Manufacturing},
volume = {78},
pages = {102385},
year = {2022},
issn = {0736-5845},
doi = {https://doi.org/10.1016/j.rcim.2022.102385},
url = {https://www.sciencedirect.com/science/article/pii/S0736584522000722},
author = {Anubhav Dogra and Sakshay Mahna and Srikant Sekhar Padhee and Ekta Singla},
keywords = {Modular and reconfigurable design, Robot Operating System, Kinematics and dynamic modeling, Modular library, Reconfigurable software architecture}}
```

### Two type of tools are provided for generating unconventional modular compositions:
1. Using DH table (DH table to Automatic Modular Sequencing along with twist parameters)
2. Using Modular Sequence and types. (refer [Article](https://doi.org/10.1016/j.rcim.2022.102385))


Examples of the modular compositions as written below can also be found in the `moir_mark2_urdf_ros/src/urdf` directory of this package.
### Files Required in order for URDF visualization:

 1. `moir_mark2_urdf_ros/config/module_config.yaml`
 2. `moir_mark2_urdf_ros/urdf/modular_robot.urdf.xacro`
 3. `moir_mark2_urdf_ros/urdf/material.xacro`
 4. `moir_mark2_urdf_ros/meshes` (folder containing meshes for the modules for visualizing)
 4. `moir_mark2_urdf_ros/scripts/ElementTree_pretty.py`
 5. `moir_mark2_urdf_ros/scripts/moir_modular_composition_generator.py`
 6. `moir_mark2_urdf_ros/scripts/moir_modular_generator_DH.py`
The generated files will be saved in `moir_mark2_urdf_ros/urdf/generated/`

### Using DH parameters
- Write DH parameters in module_config.yaml
```
robot_name: mod<n>r_name  
offset_length: < in meters>    
dh_config:
- /alpha /a /d /theta /H or L  
```
#### Note: The DH table order is as follows.
   | Twist angle | Link length | Offset | Joint angle | Module Variant |
   | ----------- | ----------- | ------ | ----------- | -------------- |
  
 
 * `n` is the number of DoF of the configuration. Example: mod6r_standard or mod2r_planar
 * Use `/alpha` in radians, for 90: 1.56
 * Robot base is formed, just as a stand. Height of the stand is decided by the offset length.
 
 - Navigate to the directory: `moir_mark2_urdf_ros/scripts`
 - `python moir_modular_generator_DH.py`
 - Navigate to the main workspace.
```bash
source devel/setup.bash
cd /your_ws/src/moir_mark2_urdf_ros/urdf/generated
roslaunch urdf_tutorial display.launch model:=mod<n>r_name.xacro
```
taa daa...
### Using Modular Sequence
