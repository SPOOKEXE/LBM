
import traceback
import torch

from IPython.display import Audio

torch.set_num_threads(1)

# convert to class-based and change the name
# also fix dupe code

class IAudio:

	model_instance = None
	model_utilities = None

	@staticmethod
	def get_voice_timestamps_from_file( filepath : str, SAMPLING_RATE : int = 16000 ) -> list:

		if IAudio.model_utilities == None:
			raise RuntimeError('You must load a model first before using this.')

		(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = IAudio.model_utilities
		wav = read_audio(filepath, sampling_rate=SAMPLING_RATE)
		return get_speech_timestamps(wav, IAudio.model_instance, sampling_rate=SAMPLING_RATE)

	@staticmethod
	def build_wav_voice_timestamps_from_file( input_filepath : str, output_filepath : str, SAMPLING_RATE : int = 16000 ) -> None:
		if IAudio.model_utilities == None:
			raise RuntimeError('You must load a model first before using this.')

		(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = IAudio.model_utilities

		wav = read_audio(input_filepath, sampling_rate=SAMPLING_RATE)
		speech_timestamps = IAudio.get_voice_timestamps_from_file( input_filepath, SAMPLING_RATE=SAMPLING_RATE )
		save_audio(output_filepath, collect_chunks(speech_timestamps, wav), sampling_rate=SAMPLING_RATE)
		Audio(output_filepath)

	@staticmethod
	def load_model_from_github(
		repo_or_dir : str = 'snakers4/silero-vad',
		model : str = 'silero_vad',
		onnx : bool = False
	) -> bool:
		IAudio.model_instance = None
		IAudio.model_utilities = None
		try:
			tmodel, tutils = torch.hub.load( source='github', repo_or_dir=repo_or_dir, model=model, force_reload=True, onnx=onnx, )
			IAudio.model_instance = tmodel
			IAudio.model_utilities = tutils
			return True
		except Exception as exception:
			print('Failed to load the audio models!')
			print( traceback.format_exception(exception) )
			return False

IAudio.load_model_from_github()
