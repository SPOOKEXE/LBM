
import traceback
import os
import torch
import librosa

from math import ceil
from transformers import AutoModelForCTC, Wav2Vec2Processor

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Audio2Text:
	device : str = 'cuda'
	model : AutoModelForCTC
	processor = Wav2Vec2Processor

	# https://github.com/huggingface/transformers/issues/14162
	def transcript( self, filepath : str, sample_rate : int = 16000, padding_duration : float = 0.5 ) -> tuple[bool, str]:
		try:
			audio, _ = librosa.load(filepath, sr=sample_rate)

			chunk_duration = ceil(librosa.get_duration(path=filepath))
			chunk_len = chunk_duration*sample_rate
			input_padding_len = int(padding_duration*sample_rate)
			output_padding_len = self.model._get_feat_extract_output_lengths(input_padding_len) # type: ignore

			all_preds = []
			for start in range(input_padding_len, len(audio)-input_padding_len, chunk_len):
				chunk = audio[start-input_padding_len:start+chunk_len+input_padding_len]
				input_values = self.processor(chunk, sampling_rate=sample_rate, return_tensors="pt").input_values  # type: ignore
				with torch.no_grad():
					logits = self.model(input_values.to(self.device)).logits[0] # type: ignore
					logits = logits[output_padding_len:len(logits)-output_padding_len]
					predicted_ids = torch.argmax(logits, dim=-1)
					all_preds.append(predicted_ids.cpu())
			return True, self.processor.decode(torch.cat(all_preds))  # type: ignore
		except Exception as exception:
			return False, f'Failed to transcript the target audio: { traceback.format_exception(exception) }'

	def load_model( self, model_path : str = "facebook/wav2vec2-base-960h" ) -> tuple[bool, str]:
		try:
			self.model = AutoModelForCTC.from_pretrained(model_path).to(self.device)
			self.processor = Wav2Vec2Processor.from_pretrained(model_path)
			return True, 'Models have been loaded.'
		except Exception as exception:
			return False, f'Failed to loadp retrained models: { traceback.format_exception(exception) }'

	def __init__(self, device='cuda'):
		self.device = device
