
from __future__ import annotations
from typing import Any, Callable

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class Transcripter:

	def load_model( self, filepath : str ) -> bool:
		return False

	def transcribe_audiofile( self, filepath : str ) -> None: #list[tuple[int, str]]:
		'''
		Returns a list of tuples where the integer is the timestamp and the string is the word(s) at the timestamp.
		'''
		pass

	def __init__( self ):
		pass

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()
