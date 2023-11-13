
from IPython.display import Audio
from dataclasses import dataclass

DEFAULT_SAMPLING_RATE : int = 160000

@dataclass
class AudioItem:
	wav : Audio
	sample_rate : int
