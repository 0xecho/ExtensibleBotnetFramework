from .baseCommand import BaseCommand
import subprocess

class RawCommand(BaseCommand):

	def setup(self, cmd, *args, **kwargs):
		self.cmd = cmd

	def execute(self):
		cmd = self.cmd
		output = subprocess.run(cmd, capture_output=True)
		print(output)
		return output.stdout.decode("utf-8") if not output.returncode else output.stderr.decode("utf-8")
