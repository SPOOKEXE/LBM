

if __name__ == '__main__':

	import os
	FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

	from torch.hub import download_url_to_file

	print('Downloading sample audio.')
	download_url_to_file('https://models.silero.ai/vad_models/en.wav', os.path.join( FILE_DIRECTORY, 'example.wav' ) )

	from audio2text import Audio2Text
	from speech_detect import SpeechDetector
	from structs import DEFAULT_SAMPLING_RATE

	speech_detector = SpeechDetector()
	_, _ = speech_detector.load_model( )

	print('==== SLICING AUDIO FILE ====')
	print('Loading audio file:')
	_, audio = speech_detector.load_audiofile( os.path.join( FILE_DIRECTORY, 'example.wav' ), SAMPLING_RATE=DEFAULT_SAMPLING_RATE )
	print('Slicing Audio')
	_, chunks = speech_detector.get_audiofile_speech_slices( audio ) # type: ignore
	print('Saving Audio')
	_, _ = speech_detector.save_audio_item( audio, os.path.join( FILE_DIRECTORY, 'sliced.wav' ) ) # type: ignore

	print('==== Audio2Text Transcription ====')
	aud2txt = Audio2Text( )
	_, _, = aud2txt.load_model( )

	print('Transcripting audio')
	_, text = aud2txt.transcript( os.path.join( FILE_DIRECTORY, 'sliced.wav' ) )

	print('Transcript:', text)

	print('==== COMPLETED ====')
