#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

#   Import your Settings class
from Settings_Module import MySettings
from petitions import myPetitions
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Roulette Script"
Website = ""
Description = "!roulette will start the roulette"
Creator = "Coonh Club"
Version = "1.0.0.0"

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
    ScriptSettings.Response = "Overwritten pong! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    Parent.SendStreamMessage(str(time.clock()))
    if IsValidChatMessage(data):
        Parent.SendStreamMessage(ScriptSettings.Response)    # Send your message to chat

    # placeholder ---
    if IsValidChatCommitment(data):
        True
        
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return


#---------------------------
#   [Required]  Valid Commitment method (Valid string or colour or zero and the Commitment)
#   
#---------------------------
def IsValidChatCommitment(jsonData):
    #if data.IsChatMessage() and (data.GetParam(1).lower()

     for i in liste:
        if "Tag" in i:
            print 'Gefunden:', i

    def ValidChatCommitment():
    for i in range(len(liste)):
        if "Tag" in liste[i]:
            print '"Tag" gefunden in item %s' % i
    ValidChatCommitment()

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


def evaluatePerUser(jetons, amount, winningNumber):
    Pet = myPetitions.instance()
    return


def IsValidChatMessage(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == ScriptSettings.Command or data.GetParam(0).lower() == ScriptSettings.Command_short) and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        
        
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))
        return False 

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and (data.GetParam(0).lower() == ScriptSettings.Command or data.GetParam(0).lower() == ScriptSettings.Command_short) and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        
        
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
        return True
    return False
