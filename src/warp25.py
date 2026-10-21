import numpy as np
# (T_real, v_nominal)
K = [(0,0),(3.8,3.5),(9.0,6.5),(13.8,9.5),(18.4,13),(19.4,13.3),(20.6,16),(29.1,22),(33.7,26),(37.4,30),(42.3,35),(47.5,38),
     (50.9,41),(52.85,44.5),(52.95,47),(57.3,53),(61.8,59),(68.0,65.5)]
TK = np.array([a for a,b in K]); VK = np.array([b for a,b in K])
DUR = 68.0
def v_of_T(T): return float(np.interp(T, TK, VK))
def T_of_v(v): return float(np.interp(v, VK, TK))
