import torch
import librosa

from math import ceil
from transformers import AutoModelForCTC, Wav2Vec2Processor

device = "cuda"
model_path = "facebook/wav2vec2-base-960h"

model = AutoModelForCTC.from_pretrained(model_path).to(device)
processor = Wav2Vec2Processor.from_pretrained(model_path)

def transcript( filepath : str, sample_rate : int = 16000, padding_duration : float = 0.5 ) -> str:
	audio, _ = librosa.load(filepath, sr=sample_rate)

	chunk_duration = ceil(librosa.get_duration(path=filepath))
	chunk_len = chunk_duration*sample_rate
	input_padding_len = int(padding_duration*sample_rate)
	output_padding_len = model._get_feat_extract_output_lengths(input_padding_len)

	all_preds = []
	for start in range(input_padding_len, len(audio)-input_padding_len, chunk_len):
		chunk = audio[start-input_padding_len:start+chunk_len+input_padding_len]
		input_values = processor(chunk, sampling_rate=sample_rate, return_tensors="pt").input_values
		with torch.no_grad():
			logits = model(input_values.to(device)).logits[0]
			logits = logits[output_padding_len:len(logits)-output_padding_len]
			predicted_ids = torch.argmax(logits, dim=-1)
			all_preds.append(predicted_ids.cpu())

	return processor.decode(torch.cat(all_preds))

print( transcript( "sliced.wav", sample_rate=16000 ) )
