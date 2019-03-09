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
global users
users = []
global evaluationAvailable
evaluationAvailable = True

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
    if IsValidChatCommitment(data):
        True
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    global evaluationAvailable
    if int(time.strftime("%M"))%ScriptSettings.Delay==0  and evaluationAvailable == True:
        Parent.SendStreamMessage("Es sind wieder 5 min rum also wird jetzt die Auswertung aufgerufen GEWINNE GEWINNE GEWINNE !!!!")
        evaluationAvailable = False
    if (int(time.strftime("%M"))%ScriptSettings.Delay==1 and evaluationAvailable == False):
        evaluationAvailable = True
    return


#---------------------------
#   [Required]  Valid Commitment method (Valid string or colour or zero and the Commitment)
#---------------------------

def IsValidChatCommitment(data):
    Pet = myPetitions.getInstance()
    for i in Pet.allPetitions:
        if data.GetParam(2) in Pet.allPetitions:
            print ('Gefunden: ', i)

    return True

#---------------------------
#   [Required]  Get userID
#---------------------------
def userID():
    [data.User, data.UserName, data.GetParam(3), data.GetParam(2)].join()
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

def rolling():
    randomInt = Parent.GetRandom(0,36)
    winnerString = ""
    for user in users:
        userData = user.split(",")
        amount = evaluatePerUser(userData[2], userData[3], randomInt)
        Parent.AddPoints(userData[0], userData[1], amount)
        if amount > 0:
            winnerString = winnerString + ", " + userData[1] + "(" + str(randomInt) + ")"
    
    output  = "Es wurde gedreht und die Kugel landete auf der " + str(randomInt) + ". Somit gewinnen dieses mal " + winnerString
    Parent.SendStreamMessage(output)


def evaluatePerUser(jetons, amount, winningNumber):
    if winningNumber == 0:
        residual = 2 
    else: 
        residual = winningNumber % 2

    if jetons == "red" and residual == 1:
        return amount * 1
    elif jetons == "black" and residual == 0:
        return amount * 1
    elif jetons == winningNumber:
        return amount * 35
    return (-1 * amount)


def IsValidChatMessage(data):
    if data.IsChatMessage() and (data.GetParam(0).lower() == ScriptSettings.Command or data.GetParam(0).lower() == ScriptSettings.Command_short) and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        
        
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))
        return False 

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and (data.GetParam(0).lower() == ScriptSettings.Command or data.GetParam(0).lower() == ScriptSettings.Command_short) and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        
        
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
        return True
    return False
