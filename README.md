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
import asyncio

async def main():
    await mill.open_connection()

    mill.access_token
    mill.authorization_code
    mill.refresh_token

    await mill.refresh_access_token()

    await mill.get_home_list()
    mill.homes_information

    await mill.get_room_by_home(home_id)
    mill.rooms_information

    await mill.get_device_by_room(room_id)
    mill.devices_information

    await mill.get_independent_devices(home_id)
    mill.independent_devices_information

    await mill.switch_control_device(device_id, status, retry=1)
    await mill.temperature_control_device(device_id, status, hold_temp=None, retry=1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    mill = Mill(
        access_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        secret_token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        username="example@mail.com",
        password="password123",
        loop=loop,
    )
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(mill.close_connection())
```
