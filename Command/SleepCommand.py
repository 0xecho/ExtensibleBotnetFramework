from .baseCommand import BaseCommand
from time import sleep

class SleepCommand(BaseCommand):

	def execute(self):
		sleep(5)
		return (True, b'YEPPERS')
