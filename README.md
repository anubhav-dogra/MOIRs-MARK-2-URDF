# MOIRs-MARK-2-URDF
This package provides the tools to generate URDF of any customized manipulator configurations (`n'-DoF), even with non-parallel and non-parallel jointed configurations, using the unconventional modular library. 

-This package is supported for Melodic branch, as the scripts are based upon python2, this can be used in different version with minute changes in the script from python2 to python3.
-The mesh files are used only for visualization of the generated configurations. 

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

The detailed usage of the package can be seen in [Wiki](https://github.com/anubhav-dogra/MOIRs-MARK-2-URDF/wiki) of this repository. 
