class CommandHandler:
	def __init__(self, commands):
		self.commands = commands

	def process(self,data,connection):
		cmd, *args = data.split(" ")
		print(cmd,args)
		if cmd in self.commands:
			commandInstance = self.commands[cmd]()
			commandInstance.setup(args)
			return commandInstance.execute()
		else:
			print("[+] Command Not found")
			return -1