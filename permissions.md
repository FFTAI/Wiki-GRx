# System Permissions

1. Add user to input group to access the joystick. Run the follwoing command in the terminal:

```bash
# add input to user group
sudo usermod -a -G input $USER
```

Then logout or reboot. If you want to check if the user is in the input group, run the following command:

```bash
# check if user is in input group
groups $USER
```

To temporarily add the user to the input group without logging out, run the following command:

```bash
# add input to user group
newgrp input
```

2. Add udev rules for imu (10c4:ea60)

First add user to the dialout group, then logout and login:
```bash
sudo usermod -a -G dialout $USER
```

```bash
# create a new file
sudo nano /etc/udev/rules.d/99-hipnuc-imu.rules
```

Add the following content to the file, which will give permission to the user to access the imu, and create a symlink `/dev/sensors/imu_hipnuc`:

```txt
SUBSYSTEMS=="usb", KERNEL=="ttyUSB[0-9]*", ACTION=="add", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666", SYMLINK+="sensors/imu_hipnuc", GROUP="dialout"
```

Then reload the udev rules, and unplug and plug the imu back in to apply the new rules:

```bash
# reload udev rules
sudo udevadm control --reload-rules
```

