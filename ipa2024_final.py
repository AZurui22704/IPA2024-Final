#######################################################################################
# Yourname: wasuphon phonsawat
# Your student ID: 65070206
# Your GitHub Repo: https://github.com/AZurui22704/IPA2024-Final.git

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.
import os
import json
import requests
import time
from restconf_final import create, delete, enable, disable, status

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

#######################################################################################
# 3. Prepare parameters to get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vOTdiNzNmMjAtNWU5ZC0xMWVmLWE3MWItNmY2NjIyMGE3ZTgx"

while True:
    # Always add a 1-second delay to avoid rate limits on API calls
    time.sleep(1)

    # Parameters and headers for Webex Teams API
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    # 4. Provide the URL to the Webex Teams messages API and extract the message location
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    if r.status_code != 200:
        raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

    json_data = r.json()
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    messages = json_data["items"]
    message = messages[0]["text"]
    print("Received message: " + message)

    if message.startswith("/"):
        parts = message.split()
        student_id, command = parts[0][1:], parts[1]

        # Execute commands
        if command == "create":
            responseMessage = create(student_id)
        elif command == "delete":
            responseMessage = delete(student_id)
        elif command == "enable":
            responseMessage = enable(student_id)
        elif command == "disable":
            responseMessage = disable(student_id)
        elif command == "status":
            responseMessage = status(student_id)
        else:
            responseMessage = "Error: No command or unknown command"

        # Post message back to Webex Teams
        postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
        postData = json.dumps(postData)
        postHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=postHTTPHeader,
        )
        if r.status_code != 200:
            raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")