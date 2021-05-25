import json
from flask import Flask, request
from FB_Graph import FB_Graph
import requests

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def token_page():

    if request.method == "POST":

        authUser = request.form["authUser"]
        authPass = request.form["authPass"]
        maID = request.form["maID"]

        # If input supplied is valid
        if authUser and authPass and maID:

            # Object of the FB_Graph Class
            fb = FB_Graph()

            # Call Social Studio API with user input to authenticate details
            authResponse = fb.authSocialAPI(authUser, authPass, maID)

            # Proceed only if credentials are correct
            if fb.http_code == 200:

                # Get the FB OAuth token
                fbToken = fb.getFbToken(authResponse, maID)

                # Store the desired output in a string to return to screen
                fbTokenString = f"The OAuth Token for {fb.socialAccTitle} is: {fbToken}"

                # Querying the Graph API directly
                graphURL = "https://graph.facebook.com/" + fb.socialAccResponse['providerUserId'] + \
                           "/accounts?fields=instagram_business_account,name,username,tasks&limit=300&access_token=" + fbToken

                graphURLResponse = requests.get(graphURL)

                graphResponseJson = json.dumps(graphURLResponse.json(), sort_keys=True, indent=4)

                return '''
                    <html>
                        <body>
                            <br><br>
                            <div align="center">
                            <p>User tasks from the FB Graph API: </p>
                            <p>{graphResponseJson}</p><br>
                            <p>You may format this response <a href="https://jsonformatter.org/" target="_blank" rel="noopener noreferrer">here</a>.</p><br><br>
                            <p>If you need to use the Facebook token for other queries: </p>
                            <p>{fbTokenString}</p><br>
                            <p>Please use the token <a href="https://developers.facebook.com/tools/explorer/" target="_blank" rel="noopener noreferrer">here</a>.</p><br><br>
                            <p><a href="/">Click here to get details again</a>
                            </div>
                        </body>                    
                    </html>                
                '''.format(graphResponseJson=graphResponseJson,fbTokenString=fbTokenString)

            # Return error string if invalid credentials
            else:
                return '''
                <html>
                    <body>
                        <br><br>
                        <div align="center">
                        <p><a href="/">{authResponse}</a>
                        </div>
                    </body>
                </html>
            '''.format(authResponse=authResponse)

        # If the any of the 3 input items is empty, throw error to customer and ask to retry
        else:
            return '''
                <html>
                    <body>
                        <br><br>
                        <div align="center">
                        <p><a href="/">Please enter all the details and try again</a>
                        </div>
                    </body>
                </html>
            '''

    # Main Page HTML
    return '''
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Get OAuth Token for Facebook Graph API</title>

                <h2 style="text-align:center;">Get OAuth Token for Facebook Graph API</h2>

                <style>
                    .img-container {
                    text-align: center;
                    }

                        </style>
            </head>
            <body>
                <div class="img-container">
                <img src="https://socialstudio.radian6.com/static/webcore/img/logo-blue-socialstudio.png" alt="socialstudio.radian6.com" style="width:device-width;height:device-height;">
                </div>
                <br><br>
                <div align="center">
                <form method="post" action=".">

                <label for="authUser">Username:</label><br>
                <input type="text" id="authUser" name="authUser"><br><br><br>

                <label for="authPass">Password:</label><br>
                <input type="text" id="authPass" name="authPass"><br><br><br>

                <label for="maID">Social Account ID:</label><br>
                <input type="text" id="maID" name="maID"><br><br><br>

                <input type="submit" value="Submit">

                </form>
                </div>
            </body>
        </html>
    '''


if __name__ == '__main__':
    app.run()