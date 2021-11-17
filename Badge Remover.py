'''
chris12902
Written on November 16-17, 2021

This script, once run, will remove all of the badges you've received from
a list of experiences. Use with caution. I've added warnings to inform
the user that this is what the program does, but these warnings can be
disabled by the user. Only do this if you're comfortable with the program
and want to quickly remove badges from your inventory.

Also note that this script requires a ROBLOSECURITY to operate. If you are not
comfortable with providing this, do not use this program. The program will
automatically forget your ROBLOSECURITY after you run it, and does not use it
in any way besides removing badges from your inventory.

APIs used

https://badges.roblox.com/v1/user/{userId}/badges/{badgeId}
Removes a badge from the user's inventory

https://badges.roblox.com/v1/universes/{universeId}/badges
Provides a list of badges for a game

https://api.roblox.com/universes/get-universe-containing-place?placeid={placeId}
Gets the universe ID of a game
'''
# imports
import re, json
import urllib.request as url
import urllib.request
import urllib.error
from urllib.request import Request
from urllib import parse
# settings
warnBeforeDelete = True
#variables
listOfPlaces = []
listOfUniverses = []
takingInput = True
listOfBadges = []
#main
def convertUniverses(places):
    global listOfUniverses
    # goes through the list of places and converts everything to universe IDs for simplicity
    for i in range(len(places)):
        req = Request("https://api.roblox.com/universes/get-universe-containing-place?placeid="+str(places[i]), headers={'User-Agent': 'Roblox/WinINet'})
        webpage = url.urlopen(req).read().decode('utf-8')
        listOfUniverses.append(re.findall(re.compile('{"UniverseId":(.+?)}'), webpage)[0])

def getBadges(universeID):
    global listOfBadges
    morePages = True
    nextPage = ""
    # gets a list of badges for a place
    while morePages:
        req = Request("https://badges.roblox.com/v1/universes/"+str(universeID)+"/badges?limit=100&sortOrder=Asc&cursor="+str(nextPage), headers={'User-Agent': 'Roblox/WinINet'})
        webpage = url.urlopen(req).read().decode('utf-8')
        listOfBadges.append(re.findall(re.compile('\[\{"id":(.+?),'), webpage)[0])
        badges = re.findall(re.compile(',{"id":(.+?),'), webpage)
        for i in badges:
            listOfBadges.append(i)
        try:
            nextPage = re.findall(re.compile('"nextPageCursor":"(.+?)"'), webpage)[0]
        except:
            morePages = False

def deleteAllBadges(badges, cookie):
    for Badge in badges:
        try:
            url.urlopen(urllib.request.Request(url = "https://badges.roblox.com/v1/user/badges/"+str(Badge), headers=headers, method = "DELETE"))
            print("Deleted badge ID "+str(Badge))
        except:
            print("User does not own badge ID "+str(Badge)+", skipping")
            pass

def rbx_request(method, url, body = ""):
    global requestResults
    method = method.upper()
    try:
        requestResults = urllib.request.urlopen(urllib.request.Request(method = method, url = url, headers = headers, data = bytes(body.encode("utf-8"))))
    except urllib.error.HTTPError as error:
        if error.code == 403:
            headers["x-csrf-token"] = error.headers["x-csrf-token"]
        rbx_request(method, url, body)
    return requestResults
        
cookie = input("Please input your ROBLOSECURITY. Read the source code to understand how your ROBLOSECURITY is used, if you're uncomfortable doing so: ")
headers = {
    "Cookie": f".ROBLOSECURITY={cookie}",
}
req = rbx_request("POST", "https://auth.roblox.com/")
print("Insert all of the place IDs for the game(s) you'd like to wipe your badge data for. Enter 0 to break the loop.")
while takingInput:
    placeId = int(input())
    if placeId != 0: listOfPlaces.append(placeId)
    else: takingInput = False

convertUniverses(listOfPlaces)
for i in range(len(listOfUniverses)):
    confirmContinue = ""
    if warnBeforeDelete:
        print("WARNING: You are about to delete all badges earned for the place ID "+str(listOfPlaces[i])+".")
        confirmContinue = input("Continue? (y/n) ")
    if 'y' in confirmContinue.lower():
        getBadges(listOfUniverses[i])
        deleteAllBadges(listOfBadges, cookie)
        listOfBadges = []
