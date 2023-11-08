
import os
import sys

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

sys.path.append( os.path.join(FILE_DIRECTORY, "..") )

import gui
import api

from project.audio import text2audio, transcript
from project.data import dataset
from project.language import language

sys.path.pop()

#### MAIN ####
if __name__ == '__main__':
	from multiprocessing import Process

	txt2audio = text2audio.Text2Audio()
	audio2text = transcript.Transcripter()
	conversation = language.LanguageModel()

	gui.audio2text = audio2text
	gui.txt2audio = txt2audio
	gui.conversation = conversation

	api.audio2text = audio2text
	api.txt2audio = txt2audio
	api.conversation = conversation

	p2 = Process(target=gui.run_display)
	p2.start()
	api.run_api()
	p2.terminate()
