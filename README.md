# pymillheat


Python3 wrapper for interacting with millheat api.   

**Features:**
- Temperature readings.
- Ability to change set temperature.
- Turn the device on/off.
- Device ID, room ID, user ID.

# Install
```
pip3 install pymillheat
```

# Example
```py
import pymillheat

mill = pymillheat.Mill(
    access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    secret_token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    username="example@email.com",
    password="password123"
)

mill.open_connection()

mill.access_token
mill.authorization_code
mill.refresh_token

mill.update_access_token()

mill.get_home_list()
mill.homes_information

mill.get_room_by_home(home_id)
mill.rooms_information

mill.get_device_by_room(room_id)
mill.devices_information

mill.get_independent_devices(home_id)
mill.independent_devices_information

mill.switch_control_device(device_id, status, retry=1)
mill.temperature_control_device(device_id, status, hold_temp=None, retry=1)

mill.close_connection()
```

Thanks to https://github.com/Danielhiversen for inspiration code-wise.
