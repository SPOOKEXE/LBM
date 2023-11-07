from __future__ import annotations

import os

from typing import Any

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class Text2Audio:

	def load_model( self, filepath : str ) -> tuple[bool, Any]:
		'''
		Load a model.
		'''
		if not os.path.exists( filepath ):
			return False, "Model filepath does not exist."
		return False, 'NotImplementedError'

	def generate_audio( self, text : str ) -> tuple[bool, Any]:
		'''
		Generate the audio given a text block.

		Returns the filepath to the audio file(?)
		'''
		if type(text) != str:
			err = 'Invalid Argument - got type {}, expected {}'.format(type(text), type(''))
			return False, err
		return False, 'NotImplementedError'

	def __init__(self):
		pass
