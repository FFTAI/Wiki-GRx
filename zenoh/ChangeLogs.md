# Change Logs
- **2024-7-01**
    - README updates:
        - Updated the install link for the new `.whl` file.
        - fixed error in description of `enable` and `disable` function in robot_client
        -  Fix description about `list_frame` and `get_transform` function
    - New whl file:
        - robot_rcs has been updated to version `robot_rcs-0.4.0.11`
        - robot_rcs_gr has been updated to version `robot_rcs_gr-1.9.1.10`
    - Config file updates:
        - Released a new version of the config file, targeting the new robot_rcs and robot_rcs_gr packages. Changes were made to T2 config files.


- **2024-6-28**
    - README updates:
        - Added firewall setup instructions, including a sample result to check whether the firewall setup is correct.
        - Updated the install link for the new `.whl` file.
        - Provided more details about using different sample config files.
        - Added instructions for the new demo, `demo_set_home`, to clarify the calibration process for the absolute encoder.
        - Fixed small mistakes

    - Config file updates:
        - Released a new version of the config file, targeting the new robot_rcs and robot_rcs_gr packages. Changes were made to both T1 and T2 config files.

    - New Demo file: `demo_set_home.py`:
        - Simplified and clarified the `set_home` function in the client part to make the calibration process clearer and simpler.

    - New whl file:
        - robot_rcs has been updated to version `robot_rcs-0.4.0.10`
        - robot_rcs_gr has been updated to version `robot_rcs_gr-1.9.1.8`


- **2024-6-27**
    - README updates:
        - Updated the install link for the new `.whl` file.
        - Added instructions for two functions updated in the robot client: `list_frame` and `get_transformation`.
        - `robot_client` changed name to `demo_robot_client.py`

    - Robot server updates:
        - Added a new function: visualization. When set to `True` (default), users can check the URDF online from the link shown in the terminal.

    - New function added into robot client:
        - `list_frame`: List all the links and joints from the robot URDF.
        - `get_transformation`: Get the transformation from one link to another.

    - New whl file:
        - robot_rcs has been updated to version `robot_rcs-0.4.0.9`
        - robot_rcs_gr has been updated to version `robot_rcs_gr-1.9.1.7`

    - URDF file added
        - Added both GR1T1 and GR1T2 URDF files into folders for the new server and client. Users can visualize the URDF with the run_server.py function.
        - Added mesh files for GR1T1 and GR1T2 in STL format.

    - New demo file: `demo_print_joints.py`:
        - Prints out joint positions and joint information.

- **2024-6-24**
    - README updates:
        - Added instructions for the updated functions in the robot client: `set_gains`.
        - Provided more details for running demos, including opening a second terminal before running the robot client after starting the server.

    - New function added into robot client:
        - `set_gains`: Set the PD parameters for the motors.

- **2024-6-22**
    - README updates:
        - Mentioned the sequential significance of installing the `.whl` file.
    - Robot server updates:
        - Fixed server bugs.
    - Config updates:
        - Fixed sample config bugs.

- **2024-6-21**
    - Working space created:
        - Created the `zenoh` folder.
    - Robot server updates:
        - Changed mode to `arg.parse` mode
    