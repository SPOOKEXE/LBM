
from __future__ import annotations

import traceback
import os

from uuid import uuid4
from ..queue import Queue
from ..model import BaseModel

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class LanguageModel(BaseModel):
	history = { }

	def _internal_load_model(self, filepath: str) -> None:
		return super()._internal_load_model(filepath)

	def _internal_unload_model(self) -> None:
		return super()._internal_unload_model()

	def new_session( self ) -> tuple[bool, str]:
		'''
		Create a new session id to keep conversations separate.
		'''
		newid = uuid4().hex
		self.history[newid] = [ ]
		return True, newid

	def session_query( self, session_id : str, text : str ) -> tuple[bool, str]:
		'''
		Query the language model with an input and return the response.
		'''
		self.queue.join()
		return False, 'NotImplementedError'

	def session_clear( self, session_id : str ) -> tuple[bool, str]:
		'''
		Clear the current ongoing history of the session.
		'''
		self.queue.join()
		if self.history.get(session_id) == None:
			return False, 'No such session.'
		self.history.pop(session_id)
		return True, 'Session has been removed.'

	def __init__( self ):
		pass
