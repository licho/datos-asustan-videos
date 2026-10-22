import os, sys
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
if SRC not in sys.path: sys.path.insert(0, SRC)     # piezas viejas de src/reelNN.py
from reels_engine.lazy import make
