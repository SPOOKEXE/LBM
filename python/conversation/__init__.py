
'''
This is an adapater to connect the conversational model api with a generic api
so other applications can be built using this adapter without having to
worry how the inner workings on the model api itself works.
'''

from typing import Any
from enum import Enum

class OperationEnums:
	Generate = 0
	Regenerate = 1
	Clear = 2

class ConversationalAdapter:

	@staticmethod
	def invoke_operation( operation : OperationEnums, *args, **kwargs ) -> tuple[bool, str]:
		raise NotImplementedError

	@staticmethod
	def await_operation( operation_id : str ) -> tuple[bool, Any]:
		raise NotImplementedError

	@staticmethod
	def cancel_operation( operation_id : str ) -> None:
		raise NotImplementedError

class ConversationalAPI:

	def generate( self, input : str, tokens : int = 1024 ) -> str:
		raise NotImplementedError
