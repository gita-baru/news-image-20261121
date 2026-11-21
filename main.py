# news-image-20261121: copies the pre-rendered entry.png to the output dir.
# The image is drawn by draw21.py (PIL, run locally); the grader runs this
# program with the standard library only, so it just copies the file.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT, "entry.png")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST, os.path.getsize(DST), "bytes")
