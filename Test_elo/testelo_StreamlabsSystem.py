# coding=utf-8-sig
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

#Import the settings object
from Settings_Module import MySettings

# Must have variables for Chatbot
ScriptName = "My own elo Command"
Website = "none"
Description = "!elo will perform a request at riot"
Creator = "Sowasvonbot"
Version = "2.0.0.0"

global getSummonerId
getSummonerId = '/lol/summoner/v4/summoners/by-name/'

global rankedId 
rankedId = '/lol/league/v4/entries/by-summoner/'

global urlRiot
urlRiot = 'https://euw1.api.riotgames.com'

global apiKey


global dictRank
dictRank = {
		"SILVER" : "Silber",
		"GOLD" : "Gold",
		"BRONZE" : "Holz",
		"PLATINUM" : "Platin",
		"DIAMOND" : "Diamant",
		"MASTER" : "Master",
		"GRANDMASTER" : "Grandmaster",
		"CHALLENGER" : "Challenger",
		"IRON" : "Unterste Schublade"
		}

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
	global apiKey
	apiKey = '?api_key=' + ScriptSettings.ApiKey
	
	return

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command:
		if Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User):
			Parent.Log(ScriptName, data.User + " wollte !elo ausführen trotzt Cooldown")
		
		elif Parent.GetPoints(data.User) < ScriptSettings.Costs:
			Parent.SendStreamMessage("@" + str(data.User) + " du benötigst " + ScriptSettings.Costs + " " + Parent.GetCurrencyName())
		
		else:
			Parent.AddUserCooldown(ScriptName, ScriptSettings.Command, data.User, ScriptSettings.Cooldown)
			Parent.RemovePoints(data.User, data.UserName, ScriptSettings.Costs)
			summonerName = 'Coonh'

			if data.GetParamCount() > 1:
				summonerName = ""
				for i in range(1,data.GetParamCount()):
					summonerName = summonerName + " " + data.GetParam(i)

			Parent.SendStreamMessage(getRankById(getSummonerIdByName(summonerName)))

        
	return

def Tick():
    return

def getSummonerIdByName(name):
	header = {"house" : "Haus", "cat":"Katze", "black":"schwarz"}
	
	try:
		result = Parent.GetRequest(urlRiot+getSummonerId+name +apiKey, header)
		dict = json.loads(result)
		status  = dict["status"]
	except Exception as e:
		Parent.Log(ScriptName, result)
		Parent.Log(ScriptName, e.with_traceback)
		Parent.SendStreamMessage(name + " not found :P")

	# Authorized Code ist 200
	if status == 200:
		dict = json.loads(dict["response"])
		id = dict["id"]
		return id
	
	# Access denied, maybe wrong API-key
	elif status == 403:
		Parent.Log(ScriptName, "Acces denied! Maybe false API-key")
	# Summoner not found
	elif status == 404:
		Parent.SendStreamMessage("Spieler " + name + " nicht gefunden")
	else:
		Parent.Log(ScriptName, "Something went wrong with http error code: " + status )
	return None
	

def getRankById(id):
	if id == None:
		return
	header = {"house" : "Haus", "cat":"Katze", "black":"schwarz"}
	try:
		result = Parent.GetRequest(urlRiot+rankedId+ id +apiKey, header)
		dict = json.loads(result)
		dict = dict["response"]
		dict = json.loads(dict)
		dict = dict[0] 

		tier = dict["tier"]
		if tier in dictRank:
			tier = dictRank[tier]

		r = dict["summonerName"] + " ist gerade " + tier + " " +dict["rank"] + " (" + str(dict["leaguePoints"]) + ")"
		if "miniSeries" in dict:
			seriesJson = dict["miniSeries"]
			r = r +" "+ parseWinLosses(seriesJson["progress"])
		return r
	except:
		Parent.SendStreamMessage("Da lief was schief")
		return

def parseWinLosses(progress):
	result = "("
	for x in progress:
		if(x == "W"):
			result = result + " S "
		elif(x == "L"):
			result = result + " N "
		else:
			result = result + " - "
	result = result + ")"
	return result

def ReloadSettings(jsonData):
	ScriptSettings.__dict__ = json.loads(jsonData)
	ScriptSettings.Save(SettingsFile)
	global apiKey
	apiKey = '?api_key=' + ScriptSettings.ApiKey