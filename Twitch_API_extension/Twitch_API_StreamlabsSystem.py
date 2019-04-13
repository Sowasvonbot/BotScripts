#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import codecs
from math import floor
from datetime import datetime
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
    global SettingsFile
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    global ScriptSettings
    ScriptSettings = MySettings(SettingsFile)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if IsValidChatMessage(data):
        if data.GetParam(1) != "":
            Parent.SendStreamMessage(getFollowerAge(data, data.GetParam(1)))
        else:
            Parent.SendStreamMessage(getFollowerAge(data, Parent.GetChannelName()))
    return

    
#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------

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


# Get the follower age for given streamer
def getFollowerAge(data, streamer):
    header = {"Client-ID": ScriptSettings.clientID, "Accept":"application/vnd.twitchtv.v5+json"}
    try:
        response = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/users?login="+ data.UserName, header))
        response = json.loads(response["response"])
        USerID = response["users"][0]["_id"]
    except:
        Parent.Log(ScriptName, "No Request possible. Maybe no Client ID")
        return

    try:
        StreamerId = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/users?login="+ streamer, header))
        StreamerId = json.loads(StreamerId["response"])
        StreamerId = StreamerId["users"][0]["_id"]
    except:
        return "Der Streamer " + streamer + " existiert nicht"

    Follows = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/users/" + USerID + "/follows/channels", header))
    Follows = json.loads(Follows["response"])
    #Parent.SendStreamMessage(str(Follows))
    with codecs.open(os.path.join(os.path.dirname(__file__), "ImFollowing.json"), encoding="utf-8-sig", mode="w+") as f:
        f.write(json.dumps(Follows, indent=3, ensure_ascii=False, encoding='utf-8'))


    FollowData = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/users/" + USerID + "/follows/channels/" + StreamerId, header))
    try:
        status = FollowData["status"]
        if status == 404:
            return "@" + data.UserName + " Du bist kein Follower bei " + streamer
    except:
        return "Something went wrong searching for " + streamer

    
    FollowData = json.loads(FollowData["response"])
    date = datetime.strptime(FollowData["created_at"], '%Y-%m-%dT%H:%M:%SZ')
    date = datetime.today() - date

    years = (date.days - date.days % 365) / 365
    days = date.days - 365 * years
    hours = floor(date.seconds/ 3600)

    if years > 0:
        return data.UserName + " folgt " + streamer + " nun seit "  +str(years) + " Jahren, "+str(days) + " Tagen und " + str(int(hours)) + " Stunden"
    else:
        return data.UserName + " folgt " + streamer + " nun seit " +str(days) + " Tagen und " + str(int(hours)) + " Stunden"

