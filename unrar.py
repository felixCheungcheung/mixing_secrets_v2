import os
import zipfile
from unrar import rarfile

f = rarfile.RarFile('./track.rar')
f.extractall('./dataset')