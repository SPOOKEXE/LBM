
from __future__ import annotations

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class LanguageModel:

	def load_model( self, filepath : str ) -> bool:
		return False

	def query( self, text : str ) -> tuple[bool, str]:
		'''
		Query the language model with an input and return the response.
		'''
		return False, 'NotImplementedError'

	def __init__( self ):
		pass
