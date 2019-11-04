"""Library to connect with millheat open API"""
import json
import asyncio
import aiohttp
import logging
import urllib3
import async_timeout

from .errors import ApplyAuthCode, MillHeatSystem, MillHeatUds, AccessToken, RefreshToken, DeviceControlForOpenApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOGGER = logging.getLogger(__name__)

API_ENDPOINT = "https://api.millheat.com"


class Mill:
    """Class to connect to Millheat API."""
    def __init__(self, username, password, access_key, secret_token, timeout=10, loop=None):
        async def _create_session():
            return aiohttp.ClientSession()
        self.loop = loop or asyncio.get_event_loop()
        self.websession = self.loop.run_until_complete(_create_session())
        self._timeout = timeout
        self._username = username
        self._password = password
        self._access_key = access_key
        self._secret_token = secret_token
        self._authorization_code = None
        self._access_token = None
        self._refresh_token = None
        self._home_list = []
        self._room_list = []
        self._device_list = []
        self._independent_device_list = []

    async def open_connection(self):
        """Connect to API."""
        headers = {
            "accept" : "*/*",
            "access_key" : f"{self._access_key}",
            "secret_token" : f"{self._secret_token}"
        }
        end_url = "/share/applyAuthCode"
        response = await self.execute(end_url, headers)
        if not response:
            LOGGER.error("Invalid response from API.")
            return False
        if response.get("errorCode") == 201:
            raise ApplyAuthCode("201, access_key is wrong")
        self._authorization_code = response["data"]["authorization_code"]
        headers = {
            "accept": "*/*",
            "authorization_code": f"{self._authorization_code}"
        }
        params = (
            ("username", f"{self._username}"),
            ("password", f"{self._password}")
        )
        end_url = "/share/applyAccessToken"
        response = await self.execute(end_url, headers, params)
        if not response:
            LOGGER.error("Invalid response from API.")
            return False
        if response.get("errorCode") == 221:
            raise ApplyAuthCode("221, user is not exist")
        if response.get("errorCode") == 222:
            raise ApplyAuthCode("221, authorization code is invalid")
        if response.get("errorCode") == 223:
            raise ApplyAuthCode("223, application account has lapsed")
        if response.get("errorCode") == 224:
            raise ApplyAuthCode("224, user is not exist")
        self._access_token = response["data"]["access_token"]
        self._refresh_token = response["data"]["refresh_token"]
        return True

    @property
    def access_token(self):
        """Get access token."""
        return self._access_token

    @property
    def authorization_code(self):
        """Get authorization token."""
        return self._authorization_code

    @property
    def refresh_token(self):
        """Get refresh token."""
        return self._refresh_token

    async def close_connection(self):
        """Close connection to API."""
        await self.websession.close()

    async def refresh_access_token(self):
        """Get new access and refresh token."""
        headers = {
            "accept": "*/*",
        }
        params = (
            ("refreshtoken", f"{self._refresh_token}"),
        )
        end_url = "/share/refreshtoken"
        response = await self.execute(end_url, headers, params)
        if not response:
            return False
        self._access_token = response["data"]["access_token"]
        self._refresh_token = response["data"]["refresh_token"]
        return True

    async def execute(self, end_url, headers, params=None):
        """Execute API call."""
        url = f"{API_ENDPOINT}{end_url}"
        try:
            with async_timeout.timeout(self._timeout):
                response = await self.websession.post(url, headers=headers, params=params, verify_ssl=False)
        except asyncio.TimeoutError:
            LOGGER.error("Timed out while sending command to Mill.")
            return None
        except aiohttp.ClientError:
            LOGGER.error("Error sending command to Mill.")
            return None

        if response.status == 200:
            response = await response.json()
            if response.get("errorCode") == 101:
                raise MillHeatSystem("101, system error")
            if response.get("errorCode") == 102:
                raise MillHeatSystem("102, uds error")
            if response.get("errorCode") == 303:
                raise DeviceControlForOpenApi("303, the device is not yours")
            if response.get("errorCode") == 304:
                raise DeviceControlForOpenApi("304, cannot find device info")
            if response.get("errorCode") == 999:
                LOGGER.error("999, refreshing token.")
                self.refresh_access_token()
                return response
            else:
                return response
        if response.status == 204:
            LOGGER.error("204, No Content")
            return response
        if response.status == 401:
            LOGGER.error("401, Unauthorized")
            return response
        if response.status == 403:
            LOGGER.error("403, Forbidden")
            return response

    async def get_home_list(self):
        """Get information about homes."""
        headers = {
            "accept": "*/*",
            "access_token": f"{self._access_token}"
        }
        end_url = "/uds/selectHomeList"
        response = await self.execute(end_url, headers)
        if not response:
            LOGGER.error("Error trying to get homes.")
            return False
        for i in response["data"]["homeList"]:
            if not any(d["homeName"] == i["homeName"] for d in self._home_list):
                self._home_list.append(i)

    @property
    def homes_information(self):
        """Get information about homes"""
        if len(self._home_list) == 0:
            LOGGER.error("There are no homes to display information for.")
            return False
        return self._home_list

    async def get_room_by_home(self, home_id):
        """Get information about rooms in specific home."""
        headers = {
            "accept": "*/*",
            "access_token": f"{self._access_token}"
        }
        params = (
            ("homeId", f"{home_id}"),
        )
        end_url = "/uds/selectRoombyHome"
        response = await self.execute(end_url, headers, params)
        if not response:
            LOGGER.error("Error trying to get rooms by home.")
            return False
        for i in response["data"]["roomList"]:
            if not any(d["roomId"] == i["roomId"] for d in self._room_list):
                self._room_list.append(i)

    @property
    def rooms_information(self):
        """Get information about rooms in specific home."""
        if len(self._room_list) == 0:
            LOGGER.error("There are no rooms to display information for.")
            return self._room_list
        return self._room_list

    async def get_device_by_room(self, room_id):
        """Get information about devices in specific room."""
        headers = {
            "accept": "*/*",
            "access_token": f"{self._access_token}"
        }
        params = (
            ("roomId", f"{room_id}"),
        )
        end_url = "/uds/selectDevicebyRoom"
        response = await self.execute(end_url, headers, params)
        if not response:
            LOGGER.error("Error trying to get devices by room.")
            return False
        for i in response["data"]["deviceList"]:
            if not any(d["deviceId"] == i["deviceId"] for d in self._device_list):
                self._device_list.append(i)

    @property
    def devices_information(self):
        """Get information about devices in specific room."""
        if len(self._device_list) == 0:
            LOGGER.error("There are no devices to display information for.")
            return self._device_list
        return self._device_list

    async def get_independent_devices(self, home_id):
        """Get information about independent devices in specific home."""
        headers = {
            "accept": "*/*",
            "access_token": f"{self._access_token}"
        }
        params = (
            ("homeId", f"{home_id}"),
        )
        end_url = "/uds/getIndependentDevices"
        response = await self.execute(end_url, headers, params)
        if not response:
            LOGGER.error("Error trying to get devices.")
            return False
        for i in response["data"]["deviceInfoList"]:
            if not any(d["deviceId"] == i["deviceId"] for d in self._independent_device_list):
                self._independent_device_list.append(i)

    @property
    def independent_devices_information(self):
        """Get information about independent devices in specific home."""
        if len(self._independent_device_list) == 0:
            LOGGER.error("There are no independent devices to display information for.")
            return self._independent_device_list
        return self._independent_device_list

    async def switch_control_device(self, device_id, status, retry=1):
        """Control specific device."""
        headers = {
            "accept": "*/*",
            "access_token": f"{self._access_token}"
        }
        params = (
            ("deviceId", f"{str(device_id)}"),
            ("operation", "0"),
            ("status", f"{str(status)}")
        )
        end_url = "/uds/deviceControlForOpenApi"
        response = await self.execute(end_url, headers, params)
        if not response:
            LOGGER.error("Error trying to toggle device.")
            return False
        if not response.get("errorCode") == 0:
            if retry > 1:
                await self.switch_control_device(device_id, status, retry-1)
        else:
            return response

    async def temperature_control_device(self, device_id, status, retry=1, hold_temp=None):
        """Control specific device."""
        headers = {
            "accept": "*/*",
            "access_token": f"{self._access_token}"
        }
        if hold_temp:
        	dig = hold_temp.isdigit()
        	if dig:
        		_hold_temp = ("holdTemp", hold_temp),
        		params += _hold_temp
        params = (
            ("deviceId", f"{str(device_id)}"),
            ("operation", "1"),
            ("status", f"{str(status)}")
        )
        end_url = "/uds/deviceControlForOpenApi"
        response = await self.execute(end_url, headers, params)
        if not response:
            LOGGER.error("Error trying to toggle device.")
            return False
        if not response.get("errorCode") == 0:
            if retry > 1:
                await self.temperature_control_device(device_id, status, retry-1, hold_temp=None)
        else:
            return response
