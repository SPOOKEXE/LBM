
import os
import sys
import time
import flask
import traceback

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

sys.path.append( os.path.join(FILE_DIRECTORY, "..") )

from project.audio import text2audio, transcript
from project.data import dataset
from project.language import conversation

from util import read_sysinfo

sys.path.pop()

if __name__ == '__main__':

	LOCALHOST = ('127.0.0.1', 500)

	#### MODELS ####
	textToAudio = text2audio.Text2Audio()
	transcripter = transcript.Transcripter()
	language = conversation.LanguageModel()

	print("Starting LBM Models")
	stime = time.time()

	print("Models Loaded after {} seconds.".format( round(time.time() - stime, 1) ))
	# textToAudio.load_model('filepath')
	# transcripter.load_model('filepath')
	# language.load_model('filepath')

	#### WEB-UI ####
	app = flask.Flask('LBM WebUI')

	# Unknown Paths
	@app.route('/', defaults={'path': ''})
	@app.route('/<path:path>')
	def catch_all(path : str):
		print('Could unknown path: ', path)
		return flask.redirect(flask.url_for('home'))

	# Pages
	@app.route('/home')
	def home():
		return 'Hello World!'

	# APIs
	@app.route('/sysinfo')
	def wrapper_sysinfo():
		return read_sysinfo( )

	@app.route('/text2audio', methods=["POST", "GET"])
	def text2audio_post():
		headers = dict(flask.request.headers.items())
		if headers.get('Content-Type') != "application/json":
			return "Content-Type is invalid", 406
		args : dict = flask.request.json or {}
		filepath = args.get('filepath')
		if filepath == None:
			return {"error" : "Filepath not included."}, 406

		wasLoaded = textToAudio.load_model( filepath )
		if wasLoaded:
			return {"success" : True}, 200
		return {"success" : False, "error" : "Failed to load model." }, 200

	print("Starting Flask WebUI.")
	app.run(port=LOCALHOST[1])
	print('Hosting WebUI at http://{}:{}'.format(*LOCALHOST))

# print(traceback.format_exception(e))
