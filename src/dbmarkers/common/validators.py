import os

from lica.validators import vfile

def vtranscribe(path: str) -> str:
	vfile(path)
	_, ext = os.path.splitext(path)
	if ext.lower() != ".xsc":
		raise ValueError("Not a Transcribe .xsc file: %s") % (ext,)
	return path