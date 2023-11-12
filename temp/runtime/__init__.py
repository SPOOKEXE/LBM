
import os
import sys

from multiprocessing import Process

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

sys.path.append( os.path.join(FILE_DIRECTORY, "..") )

import gui
import api

from project.audio import text2audio, audio2text
from project.data import dataset
from project.language import language

sys.path.pop()

#### MAIN ####
def main( audio2text, txt2audio, conversation ) -> None:
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

if __name__ == '__main__':
	txt2audio = text2audio.Text2Audio()
	audio2text = audio2text.Audio2Text()
	conversation = language.LlamaModel()

	txt2audio.load_model("ABSOLUTE_PATH")
	#audio2text.load_model("ABSOLUTE_PATH")
	conversation.load_model("G:\\text-audio-ai\\text-generation-webui-snapshot-2023-10-29\\models\\TheBloke_Xwin-MLewd-13B-v0.2-GPTQ\\model.safetensors")

	_, sessionid = conversation.new_session()
	_, value = conversation.session_query( sessionid, "What is your name?" )
	_, rawaudio = txt2audio.generate_audio( value[0] )

	main( txt2audio, audio2text, conversation )
