import requests
import bs4
import re
import time
import easygui
#searching match ID here
allMatches = 'http://www.cricbuzz.com/api/html/homepage-scag'
matchIdRegexPattern = r'\/[0-9]{5}\/'
numberOfMatches = 1

matches = requests.get(allMatches)

matchesSoup = bs4.BeautifulSoup(matches.text,'html.parser')
matchID = []
for link in matchesSoup.find_all('a'):
	if link.get('href').find('live-cricket-score')!=-1:
		matchSearch = re.search(matchIdRegexPattern, link.get('href'))

		if matchSearch:
			numberOfMatches -= 1
			matchID.append(matchSearch.group(0)[1:-1])

	if numberOfMatches == 0:
		break

matchResults = {}

for id in matchID:
	matchResults[id]={}

#Extracting data here
baseUrlLeft = 'http://www.cricbuzz.com/match-api/'
baseUrlRight = '/commentary.json'

for id in matchID:
	url = baseUrlLeft+id+baseUrlRight
	matchDets = requests.get(url)
	matchDets = matchDets.json()
	matchResults[id]["team1"] = matchDets["team1"]["name"]
	matchResults[id]["team1Id"] = matchDets["team1"]["id"]
	matchResults[id]["team2"] = matchDets["team2"]["name"]
	matchResults[id]["team2Id"] = matchDets["team2"]["id"]
	matchResults[id]["teams"] = {matchResults[id]["team1Id"]:matchResults[id]["team1"],matchResults[id]["team2Id"]:matchResults[id]["team2"]}
	matchResults[id]["tosswinner"] = matchDets["toss"]["winner"]
	matchResults[id]["decision"] = matchDets["toss"]["decision"]
	matchResults[id]["bowling"] = "-"
	matchResults[id]["batting"] = "0/0 (0.0 Ovs)"
	# matchResults[id]["battingTeam"] = matchDets["score"]["batting"]["id"]
	matchResults[id]["overDets"] = matchDets["score"]["prev_overs"]
	matchResults[id]["playerDets"] = {}

	for player in matchDets["players"]:
		matchResults[id]["playerDets"][player["id"]] = player["name"]

while True:
	# if(matchResults[id]["battingTeam"] == matchResults[id]["team1Id"]):
	# 	matchResults[id]["currBatting"] = matchResults[id]["team1"]
	# else:
	# 	matchResults[id]["currBatting"] = matchResults[id]["team2"]
	matchDets = requests.get(url)
	matchDets = matchDets.json()
	matchResults[id]["batting"] = matchDets["score"]["batting"]["score"]
	matchResults[id]["overDets"] = matchDets["score"]["prev_overs"]
	if matchResults[id]["bowling"] == "-" and "bowling" in matchDets["score"].keys():
		matchResults[id]["bowling"] = matchResults[id]["teams"][matchDets["score"]["bowling"]["id"]]+" "+matchDets["score"]["bowling"]["score"]

	title = matchResults[id]["team1"]+" v/s "+matchResults[id]["team2"]
	score = matchResults[id]["teams"][matchDets["score"]["batting"]["id"]]+" "+ matchResults[id]["batting"]
	batsmen = []
	for batsman in matchDets["score"]["batsman"]:
		batsmen.append(matchResults[id]["playerDets"][batsman["id"]])
		batsmen.append("runs:")
		batsmen.append(batsman["r"])
		batsmen.append("balls:")
		batsmen.append(batsman["b"])
		batsmen.append("\n")
	bowlers = []
	for bowler in matchDets["score"]["bowler"]:
		bowlers.append(matchResults[id]["playerDets"][bowler["id"]])
		bowlers.append("overs:")
		bowlers.append(bowler["o"])
		bowlers.append("runs:")
		bowlers.append(bowler["r"])
		bowlers.append("wickets:")
		bowlers.append(bowler["w"])
		bowlers.append("\n")		
	# matchResults[id]["playerDets"][matchDets["score"]["batsman"][0]["id"]]
	overdets = matchResults[id]["overDets"]
	finalprint = []
	finalprint.append(score)
	finalprint.append("\n")
	batsmen.pop()
	bowlers.pop()
	finalprint.append(" ".join(batsmen))
	finalprint.append("\n")
	finalprint.append(" ".join(bowlers))
	finalprint.append("\n")
	finalprint.append(overdets)
	finalprint.append("\n")
	finalprint.append(matchResults[id]["bowling"])
	finalprint.append("\n")
	easygui.msgbox("".join(finalprint),title=title)
	time.sleep(200)


