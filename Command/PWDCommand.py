from .baseCommand import BaseCommand
from subprocess import run

class PWDCommand(BaseCommand):

	def execute(self):
		output = run("pwd", capture_output=True)
		if output.returncode == 0:
			return (True, output.stdout.decode('utf-8'))
		return (False, output.stderr.decode('utf-8'))
