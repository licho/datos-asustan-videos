import numpy as np
# (final_time T, original_video_time v)
K = [(0,0),(4.3,1.5),(6.0,3.0),(8.5,5.3),(11.1,8.0),(13.0,9.4),(13.96,11.0),(16.9,14.3),(17.35,15.0),
     (18.35,15.6),(20.4,17.2),(23.2,18.7),(23.85,19.7),(24.7,21.1),(25.7,22.5),(28.6,25.0),
     (30.05,28.5),(33.0,32.0),(35.9,36.0),(36.6,37.6),(39.75,42.0),(43.0,46.0),(45.8,50.0),
     (48.3,52.4),(50.1,53.4),(51.9,56.3),(52.3,57.0),(58.0,60.0)]
TK = np.array([a for a,b in K]); VK = np.array([b for a,b in K])
DUR = 58.0
def v_of_T(T): return float(np.interp(T, TK, VK))
def T_of_v(v): return float(np.interp(v, VK, TK))
GAP_AT, GAP = 48.6, 1.0   # silence inserted in narration
