from urllib.request import urlopen, Request
import requests
import json
import xmltodict

# Use of Class to access important Global Variables
class FB_Graph:

    def __init__(self):
        # Set the variables to be used across the app
        self.baseURL = "https://api.radian6.com/socialcloud/"
        self.authCall = "v1/auth/authenticate"
        self.socialPropertiesCall = "v2/socialProperties/"
        self.socialAccountsCall = "v2/socialAccounts/"
        self.authAppKey = "Internal"
        self.http_code = None
        self.socialAccTitle = None
        self.socialAccResponse = None


    def authSocialAPI(self, authUser, authPass, maID):
        '''
        Function to authenticate the Social Studio API with user input

        Arguments: Username, Password and Managed Account ID
        Returns a string with Social Studio authentication token if successful or a failure message if authentication fails
        '''

        authUser = authUser
        authPass = authPass
        maID = maID

        # Header data to query the Social API
        headerData = {'auth_user': authUser,
                      'auth_pass': authPass,
                      'auth_appkey': self.authAppKey}

        # Get authentication response from the API
        authResponse = requests.get(url=self.baseURL + self.authCall, headers=headerData)
        self.http_code = authResponse.status_code
        xmlAuthResponse = authResponse.content

        # Process this chunk of code if credentials are valid
        if self.http_code == 200:
            # convert XML to JSON for easier processing
            jsonAuthResponse = json.loads(json.dumps(xmltodict.parse(xmlAuthResponse)))
            authToken = jsonAuthResponse['auth']['token']

            # Return Social Studio token
            return authToken

        else:
            # Return failure message if credentials are not valid
            return f"Script failed with status code {self.http_code} and error {authResponse.content}"


    def getFbToken(self, token, maID):

        '''
        Function to get OAuth Token for use on Facebook Graph API

        Arguments: Social Studio auth token and Managed Account ID
        Returns a JSON object with the required information for the FB Managed Account
        '''

        try:

            socialToken = token
            maID = maID

            # Get Social Property details
            socialPropResponse = requests.get(url=self.baseURL + self.socialPropertiesCall + maID,
                                              headers={"auth_token": socialToken,
                                                       "auth_appkey": self.authAppKey}
                                              ).json()

            # Extract information about Social Property for later use
            socialAccRegID = socialPropResponse['registration']['id']
            self.socialAccTitle = socialPropResponse['title']

            # Get and return FB OAuth Token
            self.socialAccResponse = requests.get(url=self.baseURL + self.socialAccountsCall + socialAccRegID,
                                             headers={"auth_token": socialToken,
                                                      "auth_appkey": self.authAppKey}
                                             ).json()

            fbOAuthToken = self.socialAccResponse['oauthToken']

            return fbOAuthToken

        # If the FB Managed Account ID entered is not recognised
        except:
            return "Please check the Managed Account ID and try again"