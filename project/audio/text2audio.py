from __future__ import annotations

import os

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class Text2Audio:

	def load_model( self, filepath : str ) -> None:
		if not os.path.exists( filepath ):
			raise FileNotFoundError("Model filepath does not exist.")


	def generate_audio( self, text : str ) -> None:
		'''
		Generate the audio given a text block.

		Returns the filepath to the audio file(?)
		'''
		pass

	def __init__(self):
		pass
