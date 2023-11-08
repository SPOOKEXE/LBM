
import uvicorn
import fastapi

from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from methods import read_sysinfo

txt2audio = None
audio2text = None
conversation = None

def run_api( port : int = 500 ) -> None:
	api = fastapi.FastAPI()

	api.add_middleware(
		CORSMiddleware,
		allow_origins=['http://localhost', f'http://localhost:{port}'],
		allow_credentials=False,
		allow_methods=['POST', 'GET'],
		allow_headers=[]
	)

	api.add_api_route('/sysinfo', read_sysinfo)

	@api.get("/", include_in_schema=False)
	async def root_redirect():
		return RedirectResponse(url='/docs')

	#### text to audio ####
	@api.get('/text2audio/active')
	async def t2a_active() -> str | None:
		'''
		Returns the active model filepath or None.
		'''
		return txt2audio.loaded_filepath

	@api.get('/text2audio/models')
	async def t2a_models() -> list:
		'''
		Returns a list of filepaths
		'''
		return txt2audio.get_available_models(fullpath=True)

	@api.post('/text2audio/load')
	async def t2a_load(filepath : str) -> dict:
		'''
		Load a model file.
		'''
		success, err = txt2audio.load_model(filepath)
		return { 'success' : success, 'message' : err }

	@api.post('/text2audio/unload')
	async def t2a_unload() -> dict:
		'''
		Unload the current loaded model.
		'''
		success, err = txt2audio.unload_model()
		return { 'success' : success, 'message' : err }

	#### audio to text ####
	@api.get('/audio2text/active')
	async def a2t_active() -> str | None:
		'''
		Returns the active model filepath or None.
		'''
		return audio2text.loaded_filepath

	@api.get('/audio2text/models')
	async def a2t_models() -> list:
		'''
		Returns a list of filepaths
		'''
		return audio2text.get_available_models(fullpath=True)

	@api.post('/audio2text/load')
	async def a2t_load(filepath : str) -> dict:
		'''
		Load the model.
		'''
		success, err = audio2text.load_model(filepath)
		return { 'success' : success, 'message' : err }

	@api.post('/audio2text/unload')
	async def a2t_unload() -> dict:
		'''
		Unload the model.
		'''
		success, err = audio2text.unload_model()
		return { 'success' : success, 'message' : err }

	#### conversational ####
	@api.get('/convo/active')
	async def convo_active() -> str | None:
		'''
		Returns the active model filepath or None.
		'''
		return conversation.loaded_filepath

	@api.get('/convo/models')
	async def convo_models() -> list:
		'''
		Returns a list of filepaths
		'''
		return conversation.get_available_models(fullpath=True)

	@api.post('/convo/load')
	async def convo_load(filepath : str) -> dict:
		'''
		Load the model.
		'''
		success, err = conversation.load_model(filepath)
		return { 'success' : success, 'message' : err }

	@api.post('/convo/unload')
	async def convo_unload() -> dict:
		'''
		Unload the model.
		'''
		success, err = conversation.unload_model()
		return { 'success' : success, 'message' : err }

	# TODO: /audio2text/file/ (filepath : string) -> string
	# TODO: /audio2text/hex/ (bytes_hex : string) -> string

	# TODO: /text2audio/text/ (text : str) -> bytes_hex
	# TODO: /text2audio/file/ (filepath : str) -> bytes_hex

	# TODO: /convo/create/ () -> string
	# TODO: /convo/query/ (hash : string) -> string
	# TODO: /convo/get_history/ (hash : string) -> list[string]
	# TODO: /convo/soft_clear/ (hash : string) -> None
	# TODO: /convo/hard_clear/ (hash : string) -> None
	# TODO: /convo/undo/ (hash : string) -> None
	# TODO: /convo/redo/ (hash : string) -> None

	uvicorn.run(api, host='127.0.0.1', port=port)
	API_IS_RUNNING = False
