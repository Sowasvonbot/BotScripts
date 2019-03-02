#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import codecs
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Twitch API"
Website = ""
Description = "Bundle of commands for Twitch API"
Creator = "Sowasvonbot"
Version = "1.0.0.1"

#---------------------------
#   Define Global Variables
#---------------------------
global CLIENT_ID
CLIENT_ID = "u0qw6k8svmddooisgqjbg2sxd30xpz"
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if IsValidChatMessage(data):
        header = {"Client-ID": CLIENT_ID, "Accept":"application/vnd.twitchtv.v5+json"}
        response = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/users?login=sowasvonbaf_aka_tobi", header))
        response = json.loads(response["response"])
        USerID = response["users"][0]["_id"]

        Follows = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/users/" + USerID + "/follows/channels", header))
        Follows = json.loads(Follows["response"])
        #Parent.SendStreamMessage(str(Follows))
        with codecs.open(os.path.join(os.path.dirname(__file__), "result.json"), encoding="utf-8-sig", mode="w+") as f:
            f.write(json.dumps(Follows, indent=3, ensure_ascii=False, encoding='utf-8'))

        
    return

    
#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return


def IsValidChatMessage(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))
        return False 

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
        return True
    return False
