import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")


#Import the settings object
from Settings_Module import MySettings

ScriptName = "Better hug command"
Website = "none"
Description = "!hug2 will perform a hug on a random user"
Creator = "Sowasvonbot"
Version = "1.0.0.2"


global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

def Init():
    # Create Settingsdirectory, if not exists
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    SettingsFile = os.path.join (os.path.dirname(__file__), "Settings\settings.json")
    global ScriptSettings
    ScriptSettings = MySettings(SettingsFile)

    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command:
        if not Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User):
            if Parent.GetPoints(data.User) >= ScriptSettings.Costs:
                response = ScriptSettings.Response
                response = response.replace("[user]",data.UserName)
                
                if CheckForUser(data.GetParam(1)):
                    response = response.replace("[randUser]",data.GetParam(1))
                else:
                    newRandUser = Parent.GetRandomActiveUser()
                    while newRandUser == data.UserName and len(Parent.GetViewerList()) != 1:
                            newRandUser = Parent.GetRandomActiveUser()
                    response = response.replace("[randUser]", newRandUser)
                
                Parent.AddUserCooldown(ScriptName, ScriptSettings.Command, data.User, ScriptSettings.Cooldown)
                Parent.RemovePoints(data.User, data.UserName, ScriptSettings.Costs)
                Parent.SendStreamMessage(response)
            else:
                Parent.SendStreamMessage("@" + str(data.UserName) + " Du brauchst mind. " + str(ScriptSettings.Costs) + " " + str(Parent.GetCurrencyName()))
        
    return

def Tick():
    return


def ReloadSettings(jsonData):
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)

#Checks the given user to be an active user in the chat
def CheckForUser(param):
    ListUsers = Parent.GetViewerList()
    for temp in ListUsers:
        if param.lower() == temp.lower():
            # Parent.SendStreamMessage(temp)
            return True
        
    return False

