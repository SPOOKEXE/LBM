SAMPLING_RATE = 16000

import torch
torch.set_num_threads(1)

from IPython.display import Audio
from pprint import pprint

# download example
torch.hub.download_url_to_file('https://models.silero.ai/vad_models/en.wav', 'en_example.wav')

model, utils = torch.hub.load(
	source='github',
	repo_or_dir='snakers4/silero-vad',
	model='silero_vad',
	force_reload=True,
	onnx=False,
)

(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

wav = read_audio('en_example.wav', sampling_rate=SAMPLING_RATE)

# get speech timestamps from full audio file
speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)
pprint(speech_timestamps)

# merge all speech chunks to one audio
save_audio('only_speech.wav', collect_chunks(speech_timestamps, wav), sampling_rate=SAMPLING_RATE)
Audio('only_speech.wav')
