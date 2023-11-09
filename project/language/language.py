
from __future__ import annotations

import traceback
import os

from uuid import uuid4
from llama_cpp import Llama, ChatCompletionResponseChoice
from transformers import pipeline, ConversationalPipeline, Conversation

from ..queue import Queue
from ..model import BaseModel

if __name__ == '__main__':
	print('You cannot run this script directly - it must be imported.')
	exit()

class BaseLanguageModel(BaseModel):
	history = { }
	states = { }

	def _internal_load_model(self, filepath: str) -> None:
		raise NotImplementedError('You cannot use this model, use one of the superclasses.')

	def _internal_unload_model(self, filepath: str) -> None:
		raise NotImplementedError('You cannot use this model, use one of the superclasses.')

	def _internal_query( self, session_id : str, text : str, max_tokens : int = 32 ) -> tuple[bool, str | list]:
		raise NotImplementedError('You cannot use this model, use one of the superclasses.')

	def new_session( self ) -> tuple[bool, str]:
		'''
		Create a new session id to keep conversations separate.
		'''
		newid = uuid4().hex
		self.history[newid] = [ ]
		self.states[newid] = None
		return True, newid

	def session_query( self, session_id : str, text : str, max_tokens : int = 32 ) -> tuple[bool, str | list]:
		'''
		Query the language model with an input and return the response.
		'''
		# queue in the job queue
		self.queue.join()
		if self.history.get(session_id) == None:
			return False, 'This is not a valid session id. Use new_session to get a new id.'
		if not self.is_a_model_loaded():
			return False, 'No model is currently loaded!'
		# infrance outputs
		success, outputs = self._internal_query( session_id, text, max_tokens=max_tokens )
		if not success:
			return False, outputs
		# save the input and output
		self.history[session_id].append([ text, outputs ])
		# return the choices
		return True, outputs

	def session_delete( self, session_id : str ) -> tuple[bool, str]:
		'''
		Delete the session completely - requires a new session id to be used after deletion.
		'''
		if self.history.get(session_id) == None:
			return False, 'This is not a valid session id. Use new_session to get a new id.'
		try: self.history.pop(session_id)
		except: pass
		try: self.states.pop(session_id)
		except: pass
		return True, 'Session has been deleted.'

	def session_clear( self, session_id : str ) -> tuple[bool, str]:
		'''
		Clear the current ongoing history/state of the session.
		'''
		self.queue.join()
		if self.history.get(session_id) == None:
			return False, 'This is not a valid session id. Use new_session to get a new id.'
		self.session_delete(session_id)
		self.history[session_id] = []
		return  True, 'Session has been cleared.'

	def __init__( self ):
		pass

class LlamaModel(BaseLanguageModel):

	loaded_model : Llama | None = None

	def _internal_load_model(self, filepath: str) -> None:
		self.loaded_model = Llama(model_path=filepath)
		self.states = { }

	def _internal_unload_model(self) -> None:
		self.loaded_model = None
		self.states = { }

	def _internal_query( self, session_id : str, text : str, max_tokens : int = 32 ) -> tuple[bool, str | list]:
		if self.loaded_model == None:
			return False, 'No model is loaded.'
		# load the previous state if available, keeps ongoing conversation
		try:
			ongoing_state = self.states.get(session_id)
			if ongoing_state != None:
				self.loaded_model.load_state( ongoing_state )
		except Exception as exception:
			print('Failed to load previous state of the model: ')
			print( traceback.format_exception(exception) )
			pass
		# infrance the model and get the result information
		try:
			result = self.loaded_model( text, max_tokens=max_tokens, stop=["\n"], stream=False )
		except Exception as exception:
			print('An error occured trying to infrance the language model: ')
			print( traceback.format_exception(exception) )
			return False, 'Could not infrance the loaded model as an error occured.'
		# save the model state
		self.states[session_id] = self.loaded_model.save_state()
		if result.get('choices') == None:
			return False, 'Failed to generate output.'
		return True, [ choice.get('text') for choice in result.get('choices') if choice.get('text') != None ]

# class TextGenerationModel(BaseLanguageModel):

# 	loaded_model : ConversationalPipeline = None

# 	def _internal_load_model(self, filepath: str) -> None:
# 		self.loaded_model = pipeline('conversational', model=filepath)
# 		self.states = { }

# 	def _internal_unload_model(self) -> None:
# 		self.loaded_model = None
# 		self.states = { }

# 	def _internal_query( self, session_id : str, text : str, max_tokens : int = 32 ) -> tuple[bool, str | list]:
# 		# load the previous state if available, keeps ongoing conversation
# 		try:
# 			ongoing_state = self.states.get(session_id)
# 			if ongoing_state != None:
# 				self.loaded_model.load_state( ongoing_state )
# 		except Exception as exception:
# 			print('Failed to load previous state of the model: ')
# 			print( traceback.format_exception(exception) )
# 			pass
# 		# infrance the model and get the result information
# 		try:
# 			result = self.loaded_model( text, max_tokens=max_tokens, stop=["\n"] )
# 		except Exception as exception:
# 			print('An error occured trying to infrance the language model: ')
# 			print( traceback.format_exception(exception) )
# 			return False, 'Could not infrance the loaded model as an error occured.'
# 		return True, [ choice.get('text') for choice in result.get('choices') if choice.get('text') != None ]
