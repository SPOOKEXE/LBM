
from __future__ import annotations
from typing import Any, Callable

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class Transcripter:

	def load_model( self, filepath : str ) -> bool:
		return False

	def transcribe_audio( self, audio : Any ) -> tuple[bool, str]:
		return False, 'NotImplementedError'

	def transcribe_audiofile( self, filepath : str ) -> tuple[bool, str]:
		'''
		Returns a list of tuples where the integer is the timestamp and the string is the word(s) at the timestamp.
		'''
		# self.transcribe_audio(  )
		return False, 'NotImplementedError'

	def __init__( self ):
		pass

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()
