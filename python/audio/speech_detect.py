
import torch
import traceback

from structs import AudioItem, DEFAULT_SAMPLING_RATE
from IPython.display import Audio
from typing import Any

torch.set_num_threads(1)

class SpeechDetector:

	loaded_model = None
	loaded_utilities = None

	def unload_model( self ) -> None:
		self.loaded_model = None
		self.loaded_utilities = None

	def load_model( self, source : str = 'github', repo : str = "snakers4/silero-vad", model : str = 'silero_vad', onnx : bool = False, force_reload : bool = True ) -> tuple[bool, str | None]:
		self.unload_model( )
		try:
			_model, _utils = torch.hub.load( source=source, repo_or_dir=repo, model=model, onnx=onnx, force_reload=force_reload, )
		except Exception as exception:
			return False, 'Failed to load the Audio2Text model:\n{}'.format( traceback.format_exception( exception ) )
		self.loaded_model = _model
		self.loaded_utilities = _utils
		return True, 'Audio2Text model has been loaded.'

	def load_audiofile( self, filepath : str, SAMPLING_RATE : int = DEFAULT_SAMPLING_RATE ) -> tuple[bool, AudioItem | str]:
		if (self.loaded_model == None) or (self.loaded_utilities == None):
			return False, 'You must load an audio model first before using this.'
		try:
			( _, _, read_audio, _, _ ) = self.loaded_utilities
			wav = read_audio(filepath, sampling_rate=SAMPLING_RATE)
			return True, AudioItem( wav=wav, sample_rate=SAMPLING_RATE )
		except Exception as exception:
			return False, f'Cannot load audio file at filepath: {filepath}\n{traceback.format_exception(exception)}'

	def get_audiofile_speech_timestamps( self, audio : AudioItem ) -> tuple[bool, list[dict] | str]:
		if (self.loaded_model == None) or (self.loaded_utilities == None):
			return False, 'You must load an audio model first before using this.'
		try:
			( get_speech_timestamps, _, _, _, _ ) = self.loaded_utilities
			speech_timestamps = get_speech_timestamps(audio.wav, self.loaded_model, sampling_rate=audio.sample_rate)
			return True, speech_timestamps
		except Exception as exception:
			return False, 'Failed to read audio and pull speech timestamps:\n{}'.format( traceback.format_exception(exception) )

	def get_audiofile_speech_slices( self, audio : AudioItem ) -> tuple[bool, Any | str]:
		if (self.loaded_model == None) or (self.loaded_utilities == None):
			return False, 'You must load an audio model first before using this.'
		success, speech_timestamps = self.get_audiofile_speech_timestamps( audio )
		if success == False:
			return False, speech_timestamps
		try:
			( _, _, _, _, collect_chunks ) = self.loaded_utilities
			return True, AudioItem(collect_chunks(speech_timestamps, audio.wav), sample_rate=DEFAULT_SAMPLING_RATE)
		except Exception as exception:
			return False, 'Failed to collect audio chunks for speech slices:\n{}'.format( traceback.format_exception(exception) )

	def save_audio_item( self, audio : AudioItem, filepath : str ) -> tuple[bool, str | None]:
		if (self.loaded_model == None) or (self.loaded_utilities == None):
			return False, 'You must load an audio model first before using this.'
		try:
			(_, save_audio, _, _, _) = self.loaded_utilities
			save_audio(filepath, audio.wav, sampling_rate=audio.sample_rate)
			return True, None
		except Exception as exception:
			return False, 'Failed to save AudioItem to the filepath:\n{}'.format( traceback.format_exception(exception) )

	def __init__( self ):
		pass
