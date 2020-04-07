import threading
import logging

class ServerThread(threading.Thread):

	def __init__(self, serverObject, *args, **kwargs):
		super().__init__()
		logging.info("[+] Staring server instance")
		self.serverInstance = serverObject(*args, **kwargs)
		
	def run(self):
		logging.info("[+] Staring server thread")
		self.serverInstance.start()

	def stop(self):
		self.serverInstance.stop()
		# self.join()