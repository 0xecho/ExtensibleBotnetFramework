import socket
import threading
import logging
from .baseClient import BaseClient

class SocketClient(BaseClient):

	def __init__(self, peer):
		super().__init__()
		self.peer = peer
		self.ip = peer.ip
		self.port = peer.port
		self.connection = None
		self.isActive = False
		self.connect()
		self.threads = []

	def connect(self):
		try:
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.connection.connect((self.ip, self.port))
			ack = self.connection.recv(1024)
			logging.info("ACK:",ack)
			if ack.decode("utf-8")=="1":
				self.isActive = True
		except Exception as e:
			logging.error(e)
			logging.error("[-]", "Connection Error: Cannot create socket")
			self.disconnect()

	def disconnect(self):
		self.isActive = False
		try:
			self.connection.close()
			for thread in self.threads:
				thread.join()
		except:
			logging.error("[-]", "Connection Error: Cannot close Socket")

	def send(self, data):
		data = data.encode("utf-8")
		try:
			self.connection.sendall(data)
			t = threading.Thread(target=self.waitAndReciece)
			t.start()
			self.threads.append(t)
		except Exception as e:
			logging.error("[-]", "Connection Error: Cannot send data")

	def waitAndReciece(self):
		recv = self.connection.recv(32768)
		print(recv.decode("utf-8"))
		# self.join() JOIN A THREAD STARTED AS A TARGET FUNCTION

	def __str__(self):
		return "Connection to: " + self.ip + ":" + str(self.port)

	def __repr__(self):
		return "Connection to: " + self.ip + ":" + str(self.port)