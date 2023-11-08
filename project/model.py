
import os
import traceback

from queue import Queue

class BaseModel:
	loaded_model = None
	loaded_filepath = None
	models_directory = None
	model_extensions = ['safetensor', 'safetensors', 'chpt', 'pt']
	queue = Queue()

	def is_model_loaded( self, filepath : str ) -> bool:
		'''
		Is the model filepath loaded?
		'''
		return (self.loaded_filepath == filepath)

	def is_filepath_a_model( self, filepath : str ) -> bool:
		ext = os.path.splitext( os.path.basename(filepath) )[1]
		return os.path.isfile(filepath) and self.model_extensions.count( ext ) > 0

	def _internal_unload_model( self ) -> None:
		raise NotImplementedError

	def unload_model( self ) -> tuple[bool, str]:
		'''
		Unload the loaded model.
		'''
		self.queue.join()
		try:
			self._internal_unload_model()
			self.loaded_model = None
			self.loaded_filepath = None
		except Exception as exception:
			print('An error occured when trying to unload the model.')
			print( traceback.format_exception(exception) )
			return False, 'Could not unload the target model due to an error.'
		return True, 'Unloaded the model.'

	def _internal_load_model( self, filepath : str ) -> None:
		raise NotImplementedError

	def load_model( self, filepath : str ) -> tuple[bool, str]:
		'''
		Load the filepath model.
		'''
		self.queue.join()
		if self.loaded_filepath == filepath:
			return True, 'Already loaded.'
		if self.loaded_model != None:
			success, err = self.unload_model()
			if not success:
				return False, err
		if not os.path.exists( filepath ):
			return False, "Model filepath does not exist."
		try:
			# TODO: load model via additional call
			self._internal_load_model( filepath )
			self.loaded_filepath = filepath
		except Exception as exception:
			print('An error occured when trying to load the model.')
			print( traceback.format_exception(exception) )
			return False, 'Could not load the target model due to an error.'
		return True, 'The model has been loaded.'

	def get_available_models( self, fullpath : bool = True ) -> list:
		'''
		Get the available models in the local directory.
		'''
		if self.models_directory == None: return []
		available = []
		for filename in os.listdir( self.models_directory ):
			filepath = os.path.join( self.models_directory, filename )
			if not self.is_filepath_a_model( filepath ):
				continue
			available.append( fullpath and filepath or filename )
		return available

	def __init__(self):
		pass

