import json

class JSONHandler:

	def __init__(self, bot):
		self.bot = bot

	def process(self, jsonData, connection):
		data = json.loads(jsonData)
		if data["type"] == "cmd":
			if data["cmdtype"] in self.bot.commands:
				command = self.bot.commands[data["cmdtype"]]
				commandInstance = command()
				commandInstance.setup(data["payload"])
				ret = commandInstance.execute()
				return (True, ret)
			else:
				return (True, "[+] COMMAND NOT SUPPORTED")
		return (True, json.dumps(data).encode("utf-8"))