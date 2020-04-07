class Peer:

	def __init__(self,ip,port):
		self.ip = ip

		if self.ip == "localhost" or self.ip == "0.0.0.0" or self.ip == "0":
			self.ip = "127.0.0.1"

		self.port = int(port)
		pass

	def __eq__(self, other):
		return self.ip == other.ip and self.port == other.port

	def __repr__(self):
		return f"Peer: {self.ip}:{self.port}"
		
	def __str__(self):
		return self.__repr__()

	def __hash__(self):
		return hash(self.ip)+hash(self.port)