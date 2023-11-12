
from time import sleep
from typing import Any
from uuid import uuid4

def array_find( array : list, value : Any ) -> int:
	try: return array.index(value)
	except: return -1

class Queue:

	queue : list[str] = []

	def join( self ) -> None:
		job_id = uuid4().hex
		self.queue.append(job_id)
		i = array_find( self.queue, job_id )
		while i > 0: # while in queue
			sleep(0.1)
			i = array_find( self.queue, job_id )
		# out of queue

	def __init__(self):
		pass
