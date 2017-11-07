# Published Jan 2013
# Revised Jan 2014 (to add new modules data)
# Revised Nov 2017 (to add support for Vaillant vSmart authentication)
# Forked from jabesq repo, added philippelt changes for file credentials
# Author : Philippe Larduinat, philippelt@users.sourceforge.net
# Public domain source code
"""
This API provides access to the Netatmo weather station or/and the Netatmo
cameras or/and the Netatmo smart thermostat
This package can be used with Python2 or Python3 applications and do not
require anything else than standard libraries

PythonAPI Netatmo REST data access
coding=utf-8
"""
import time
from os import getenv
from os.path import expanduser, exists
import json, time
from smart_home.WeatherStation import WeatherStationData, DeviceList
from smart_home.Camera import CameraData
from smart_home.Thermostat import ThermostatData
from smart_home.VaillantThermostat import VaillantThermostatData
from smart_home import _BASE_URL, postRequest, NoDevice

#########################################################################

cred = {                       # You can hard code authentication information in the following lines
        "CLIENT_ID"     : "",     #   Your client ID from Netatmo app registration at http://dev.netatmo.com/dev/listapps
        "CLIENT_SECRET" : "",  #   Your client app secret   '     '
        "USERNAME"      : "",       #   Your netatmo account username
        "PASSWORD"      : "",        #   Your netatmo account password
        "APP_VERSION"   : "",   # The app version
        "USER_PREFIX"   : "",   # The user prefix
        "SCOPE"         : ""
        }

# Other authentication setup management (optionals)

CREDENTIALS = expanduser("~/.netatmo.credentials")

def getParameter(key, default):
    return getenv(key, default[key])

# 2 : Override hard coded values with credentials file if any
if exists(CREDENTIALS) :
    with open(CREDENTIALS, "r") as f:
        cred.update({k.upper():v for k,v in json.loads(f.read()).items()})

# 3 : Override final value with content of env variables if defined
_CLIENT_ID     = getParameter("CLIENT_ID", cred)
_CLIENT_SECRET = getParameter("CLIENT_SECRET", cred)
_USERNAME      = getParameter("USERNAME", cred)
_PASSWORD      = getParameter("PASSWORD", cred)
_APP_VERSION   = getParameter("APP_VERSION", cred)
_USER_PREFIX   = getParameter("USER_PREFIX", cred)
_SCOPE   = getParameter("SCOPE", cred)


# Common definitions
_AUTH_REQ       = _BASE_URL + "oauth2/token"

class ClientAuth:
    """
    Request authentication and keep access token available through token method. Renew it automatically if necessary

    Args:
        clientId (str): Application clientId delivered by Netatmo on dev.netatmo.com
        clientSecret (str): Application Secret key delivered by Netatmo on dev.netatmo.com
        username (str)
        password (str)
        scope (Optional[str]): Default value is 'read_station'
            read_station: to retrieve weather station data (Getstationsdata, Getmeasure)
            read_camera: to retrieve Welcome data (Gethomedata, Getcamerapicture)
            access_camera: to access the camera, the videos and the live stream.
            read_thermostat: to retrieve thermostat data ( Getmeasure, Getthermostatsdata)
            write_thermostat: to set up the thermostat (Syncschedule, Setthermpoint)
            read_presence: to retrieve Presence data (Gethomedata, Getcamerapicture)
            access_presence: to access the live stream, any video stored on the SD card and to retrieve Presence's lightflood status
            Several value can be used at the same time, ie: 'read_station read_camera'
    """

    def __init__(self, clientId=_CLIENT_ID,
                       clientSecret=_CLIENT_SECRET,
                       username=_USERNAME,
                       password=_PASSWORD,
                       scope=_SCOPE,
                       app_version=_APP_VERSION,
                       user_prefix=_USER_PREFIX):
        postParams = {
                "grant_type": "password",
                "client_id": clientId,
                "client_secret": clientSecret,
                "username": username,
                "password": password,
                "scope": scope
                }

        if user_prefix:
          postParams.update({"user_prefix":user_prefix})
        if app_version:
          postParams.update({"app_version":app_version})
        resp = postRequest(_AUTH_REQ, postParams)
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._accessToken = resp['access_token']
        self.refreshToken = resp['refresh_token']
        self._scope = resp['scope']
        self.expiration = int(resp['expire_in'] + time.time())

    @property
    def accessToken(self):

        if self.expiration < time.time():  # Token should be renewed
            postParams = {
                    "grant_type": "refresh_token",
                    "refresh_token": self.refreshToken,
                    "client_id": self._clientId,
                    "client_secret": self._clientSecret
                    }
            resp = postRequest(_AUTH_REQ, postParams)
            self._accessToken = resp['access_token']
            self.refreshToken = resp['refresh_token']
            self.expiration = int(resp['expire_in'] + time.time())
        return self._accessToken


class User:
    """
    This class returns basic information about the user

    Args:
        authData (ClientAuth): Authentication information with a working access Token
    """
    def __init__(self, authData):
        postParams = {
                "access_token" : authData.accessToken
                }
        resp = postRequest(_GETSTATIONDATA_REQ, postParams)
        self.rawData = resp['body']
        self.devList = self.rawData['devices']
        self.ownerMail = self.rawData['user']['mail']

# auto-test when executed directly

if __name__ == "__main__":

    from sys import exit, stdout, stderr

    if not _CLIENT_ID or not _CLIENT_SECRET or not _USERNAME or not _PASSWORD :
           stderr.write("Library source missing identification arguments to check lnetatmo.py (user/password/etc...)")
           exit(1)

    authorization = ClientAuth(scope="read_station read_camera access_camera read_thermostat write_thermostat read_presence access_presence")  # Test authentication method

    try:
        devList = DeviceList(authorization)         # Test DEVICELIST
    except NoDevice:
        if stdout.isatty():
            print("lnetatmo.py : warning, no weather station available for testing")
    else:
        devList.MinMaxTH()                          # Test GETMEASUR


    try:
        Camera = CameraData(authorization)
    except NoDevice :
        if stdout.isatty():
            print("lnetatmo.py : warning, no camera available for testing")

    try:
        Thermostat = ThermostatData(authorization)
    except NoDevice :
        if stdout.isatty():
            print("lnetatmo.py : warning, no thermostat available for testing")

    # If we reach this line, all is OK

    # If launched interactively, display OK message
    if stdout.isatty():
        print("lnetatmo.py : OK")

    exit(0)

