import json
import logging

class Handler:

	def __init__(self):
		self.handlers = []

	def addHandler(self, handler):
		self.handlers.append(handler)
		logging.info("[+] Added " + handler.__class__.__name__)

	def removeHandler(self, handler):
		self.handlers = [_handler for _handler in self.handlers if not type(_handler) is type(handler)]
		logging.info("[+] Removed " + handler.__class__.__name__)

	def handleRequest(self, data, connection):
		for handler in self.handlers:
			logging.info("[+] Trying " + handler.__class__.__name__ + " on request")
			ret = handler.process(data, connection)
			if not ret == -1:
				connection.sendall(ret[1].encode("utf-8"))
				return True
		return False

