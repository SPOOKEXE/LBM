from __future__ import annotations

import os
import traceback

from typing import Any
from ..queue import Queue
from ..model import BaseModel

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class Text2Audio(BaseModel):

	def _internal_load_model(self, filepath: str) -> None:
		return super()._internal_load_model(filepath)

	def _internal_unload_model(self) -> None:
		return super()._internal_unload_model()

	def generate_audio( self, text : str ) -> tuple[bool, Any]:
		'''
		Generate the audio given a text block.

		Returns the filepath to the audio file(?)
		'''
		self.queue.join()
		return False, 'NotImplementedError'

	def __init__(self):
		pass
