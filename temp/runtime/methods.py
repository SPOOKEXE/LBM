from __future__ import annotations

import platform
import cpuinfo
import psutil
import os
import subprocess

from typing import Any
from shutil import which

def find_nvidia_GPUs( ) -> list[Any]:
	'''
	Returns a list of GPU devices:

	Example:
	[{"index": "0", "name": "NVIDIA GeForce RTX 3060", "vram": "12288"}]
	'''
	if platform.system() == "Windows":
		nvidia_smi = which('nvidia-smi')
		if nvidia_smi is None:
			nvidia_smi = f"{os.environ['systemdrive']}\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe"
	else:
		nvidia_smi = "nvidia-smi"

	try:
		p = subprocess.Popen([nvidia_smi, "--query-gpu=index,name,memory.total", "--format=csv,noheader,nounits"], stdout=subprocess.PIPE)
		stdout, _ = p.communicate()
		output = stdout.decode('UTF-8')
	except:
		return []

	devices = []
	for device in output.split(os.linesep)[:-1]:
		values = [ v.strip() for v in device.split(',') ]
		devices.append({ "index" : values[0], "name" : values[1], "vram" : values[2] })
	return devices

def read_sysinfo( ) -> dict[str, Any]:
	'''
	Returns the system information:

	- `python-version : string`
	- `os : string`
	- `cpu : dict( name : string, cores : int, processors : int )`
	- `memory : dict( total : int, free : int, used : int )`
	- `gpu : list( dict( index : int, name : str, vram : int ) )`
	'''
	virtual_mem = psutil.virtual_memory()
	gpuz = find_nvidia_GPUs()
	return {
		"python-version" : os.popen('py --version').read()[:-1],
		"os" : f"{platform.system()}:{platform.version()}",
		"cpu" : {
			"name" : cpuinfo.get_cpu_info().get('brand_raw') or "Unknown",
			"cores" : psutil.cpu_count(logical=False) or -1,
			"processors" : psutil.cpu_count(logical=True) or -1,
		},
		"memory" : {
			"total" : virtual_mem.total,
			"free" : virtual_mem.free,
			"used" : virtual_mem.used
		},
		"gpu" : len(gpuz) == 0 and "No NVIDIA GPUs" or gpuz
	}
