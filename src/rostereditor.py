import sys, rostertool
from models import League, Team, Player
from tabulate import tabulate
from os import system

def getInput():
	inp = raw_input("\n")
	inp = inp.rstrip().lstrip()
	cmd = inp.split()
	if(len(cmd) == 0):
		return [" "]
	for i in range(len(cmd)):
		cmd[i] = cmd[i].rstrip().lstrip()
		cmd[i] = cmd[i].replace("_", " ")
	return cmd

def init():
	system("clear")
	if(len(sys.argv) == 1):
		league = League("")
	else:
		league = rostertool.loadLeague(sys.argv[1])
	return MainShell(league)

class MainShell(object):

	def __init__(self, league):
		self.league = league
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			print("League: %s\n" % self.league.leagueName)
			self.printTeams()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["add X", "Add a team named X to the league"])
		table.append(["rm X", "Remove team X from the league"])
		table.append(["view X", "View the details of team X"])
		table.append(["set name X", "Set the name of the leauge to X"])
		table.append(["mktrade X Y", "Make a trade between Team X and Team Y"])
		table.append(["quit","End the program"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			try:
				if(cmd[0] == "add"):
					self.add(cmd[1])
				elif(cmd[0] == "rm"):
					self.rm(cmd[1])
				elif(cmd[0] == "view"):
					self.view(cmd[1])
				elif(cmd[0] == "set"):
					self.set(cmd[1], cmd[2])
				elif(cmd[0] == "save"):
					self.save()
				elif(cmd[0] == "mktrade"):
					self.mktrade(cmd[1], cmd[2])
				elif(cmd[0] == "help"):
					self.help()
					self.doRefresh = False
				elif(cmd[0] == "quit"):
					break
				else:
					print("Invalid command")
					self.doRefresh = False
			except IndexError:
				print("Error parsing command")
				self.doRefresh = False

	def printTeams(self):
		table = []
		for team in self.league.allTeams():
			table.append([team.teamName])
		print tabulate(table,["Teams"])

	def view(self,teamName):
		try:
			team = self.league.getTeam(teamName)
			ts = TeamShell(team)
			ts.run()
		except KeyError:
			print("Error parsing team name")
			self.doRefresh = False

	def add(self,teamName):
		self.league.addTeam(Team(teamName))

	def rm(self,teamName):
		try:
			self.league.removeTeam(teamName)
		except KeyError:
			print("Error parsing team name")
			self.doRefresh = False

	def set(self,item,value):
		if(item == "name"):
			self.league.leagueName = value

	def save(self):
		rostertool.writeLeague(self.league)

	def mktrade(self, team1Name, team2Name):
		try:
			team1 = self.league.getTeam(team1Name)
			team2 = self.league.getTeam(team2Name)
			ts = TradeShell(team1, team2)
			ts.run()
		except KeyError:
			print("Error parsing team names")
			self.doRefresh = False

class TeamShell(object):

	def __init__(self, team):
		self.team = team
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printRoster()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["add", "Add player to the team"])
		table.append(["addrand", "Add a random player to the team"])
		table.append(["rm X", "Remove player X from the team"])
		table.append(["view X","View the details of player X"])
		table.append(["back","Return to the league screen"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			try:
				if(cmd[0] == "view"):
					self.view(cmd[1])
				elif(cmd[0] == "add"):
					self.add()
				elif(cmd[0] == "addrand"):
					self.addrand()
				elif(cmd[0] == "rm"):
					self.team.removePlayer(cmd[1])
				elif(cmd[0] == "help"):
					self.help()
					self.doRefresh = False
				elif(cmd[0] == "back"):
					break
				else:
					print("Invalid command")
					self.doRefresh = False
			except IndexError:
				print("Error parsing command")
				self.doRefresh = False

	def printRoster(self):
		table = []
		for player in self.team.allPlayers():
			table.append([player.fullName(), player.offense, player.defense])
		print self.team.teamName	
		print tabulate(table,["Name","Offense","Defense"])

	def view(self, playerName):
		try:
			player = self.team.getPlayer(playerName)
			ps = PlayerShell(player)
			ps.run()
		except KeyError:
			print("Error parsing player name")
			self.doRefresh = False

	def add(self):
		first = raw_input("First Name: ")
		last = raw_input("Last Name: ")
		off = raw_input("Offense: ")
		defs = raw_input("Defense: ")
		self.team.addPlayer(Player(first,last,off,defs))

	def addrand(self):
		self.team.addPlayer(rostertool.createRandomPlayer(50,99))

class PlayerShell(object):

	def __init__(self, player):
		self.player = player
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printPlayer()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["set off X","Set the offense of the current player to X"])
		table.append(["set def X", "Set the defense of the current player to X"])
		table.append(["back","Return to the previous screen"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			try:
				if(cmd[0] == "set"):
					self.set(cmd[1], cmd[2])
				elif(cmd[0] == "help"):
					self.help()
					self.doRefresh = False
				elif(cmd[0] == "back"):
					break
				else:
					print("Invalid command")
					self.doRefresh = False
			except IndexError:
				print("Error parsing command")
				self.doRefresh = False

	def printPlayer(self):
		print(("Name: %s") % (self.player.fullName()))
		print(("Offense: %d") % (self.player.offense))
		print(("Defense: %d") % (self.player.defense))

	def set(self, item, value):
		if(item == "off"):
			self.player.offense = int(value)
		if(item == "def"):
			self.player.defense = int(value)

class TradeShell(object):
	def __init__(self, team1, team2):
		self.team1 = team1
		self.team2 = team2
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printRosters()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["trade X Y","Trade Player X from Team 1 to Team 2 \nand Player Y from Team 2 to Team 1 \nType '*' in place of a blank player \nType ',' to separate multiple players"])
		table.append(["back","Return to the previous screen"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			try:
				if(cmd[0] == "trade"):
					self.trade(cmd[1],cmd[2])
				elif(cmd[0] == "help"):
					self.help()
					self.doRefresh = False	
				elif(cmd[0] == "back"):
					break
				else:
					print("Invalid command")
					self.doRefresh = False
			except IndexError:
				print("Error parsing command")
				self.doRefresh = False

	def printRosters(self):
		table1 = []
		for player in self.team1.allPlayers():
			table1.append([player.fullName(),player.offense,player.defense])
		table2 = []
		for player in self.team2.allPlayers():
			table2.append([player.fullName(),player.offense,player.defense])
		print self.team1.teamName
		print tabulate(table1,["Name","Offense","Defense"])
		print ""
		print self.team2.teamName
		print tabulate(table2,["Name","Offense","Defense"])

	def trade(self,team1Names, team2Names):
		try:
			players1 = []
			players2 = []
			if((team1Names == "*") != True):
				names1 = team1Names.split(",")
				for name in names1:
					players1.append(self.team1.getPlayer(name))
			if((team2Names == "*") != True):
				names2 = team2Names.split(",")
				for name in names2:
					players2.append(self.team2.getPlayer(name))
		except KeyError:
			print("Error parsing player names")
			self.doRefresh = False
			return

		for player in players1:
			self.team1.removePlayer(player.fullName())
			self.team2.addPlayer(player)
		for player in players2:
			self.team2.removePlayer(player.fullName())
			self.team1.addPlayer(player)

main = init()
main.run()



