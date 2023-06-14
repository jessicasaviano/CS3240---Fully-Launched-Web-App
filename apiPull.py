import requests
import json


def pullData(deptID, classNum):
    responseURL = "http://luthers-list.herokuapp.com/api/dept/" + deptID.upper() + \
        "/?format=json"
    response_API = requests.get(responseURL)
    responseAPIText = response_API.text
    responseAPIJson = json.loads(responseAPIText)
    for foundClass in responseAPIJson:
        if (foundClass["catalog_number"] == str(classNum)) and (foundClass["component"] == "LEC"):
            print(foundClass)


#pullData("CS", 1110)


def makeDeptHTML():
    responseURL = "https://luthers-list.herokuapp.com/api/deptlist/?format=json"
    response_API = requests.get(responseURL)
    responseAPIText = response_API.text
    responseAPIJson = json.loads(responseAPIText)
    for dept in responseAPIJson:
        #<option value="1">One</option>
        print("<option value=\""+dept["subject"]+"\">"+dept["subject"]+"</option>")

makeDeptHTML()