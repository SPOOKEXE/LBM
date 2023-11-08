
import os
import sys
import traceback
import uvicorn
import flask
import fastapi

from fastapi.middleware.wsgi import WSGIMiddleware
from threading import Thread
from time import sleep

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

sys.path.append( os.path.join(FILE_DIRECTORY, "..") )

from project.audio import text2audio, transcript
from project.data import dataset
from project.language import language

from methods import read_sysinfo

sys.path.pop()

def construct_template( filepath : str ) -> str:
	pass

def run_webui( ):
	txt2audio = text2audio.Text2Audio()
	audio2text = transcript.Transcripter()
	conversation = language.LanguageModel()

	webui = flask.Flask('LBM WebUI')
	api = fastapi.FastAPI()

	#### FAST API ####
	@api.get('/sysinfo')
	def sysinfo():
		return read_sysinfo( )

	# @api.post('text2audio')
	# def post_text2audio():
	# 	return {'success' : False, 'error' : 'NotImplementedError'}

	# @api.post('audio2text')
	# def post_audio2text():
	# 	return {'success' : False, 'error' : 'NotImplementedError'}

	# @api.post('conversation')
	# def post_conversation():
	# 	return {'success' : False, 'error' : 'NotImplementedError'}

	#### WEBUI ####
	api.mount('/', WSGIMiddleware(webui))
	@webui.get('/')
	def home():
		return 'Hello!'

	uvicorn.run(api, host='127.0.0.1', port=500)

#### MAIN ####
if __name__ == '__main__':
	run_webui( )
