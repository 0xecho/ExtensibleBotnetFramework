import socket 
import threading
import os
import json
import logging

from .baseServer import *

class SocketServer(BaseServer):

	def __init__(self, handler, bot):
		self.host = bot.host
		self.port = 45454
		self.handler = handler
		self.stopFlag = False
		logging.info("[+] Initializing socket")
		self.conversations = []
		self.bot = bot
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		while 1:
			if(self.port>50000):
				break
			try:
				logging.info("[+] Trying to bind to port",self.port)
				self.connection.bind((self.host, self.port))
				self.bot.port = self.port
				break
			except Exception as e:
				logging.error(e)
				self.port += 1
		self.connection.listen(5)
		logging.info("[+] Now listening on", ":".join((self.host,str(self.port))))
		## report connection
		if not os.path.exists("live"):
			os.system("touch live")
		with open("live","a") as f:
			f.write(":".join((self.host,str(self.port)))+"\n")

	def start(self):
		logging.info("[+] Server now accepting responses")
		while not self.stopFlag:
			conn, addr = self.connection.accept()
			logging.info("[+] Server now connected to", addr)
			t = SocketHandlerThread(conn, addr, self.handler, self.bot)
			t.start()
			self.conversations.append(t)

	def stop(self):
		self.stopFlag = True
		self.connection.close()
		for thread in self.conversations:
			thread.stop()
		
class SocketHandlerThread(threading.Thread):

	def __init__(self, connection, addr, handler, bot):
		super().__init__()
		self.connection = connection
		self.handler = handler
		self.addr = addr
		self.stopFlag = False
		self.bot = bot

	def run(self):
		logging.info("[+] Server now connected to", self.addr, ", Creating new Thread to handle conversation")
		self.connection.sendall(bytes("1","ascii"))

		while not self.stopFlag:
			data = self.connection.recv(1024)
			if not data: break
			data = data.decode("utf-8")
			ret = self.handler.handleRequest(data, self.connection)
			if not ret:
				logging.info("[+] Processing data failed for")
				logging.info(data)

	def stop(self):
		self.stopFlag = True
		self.connection.close()
		# self.join()