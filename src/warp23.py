import numpy as np
# (T_real, v_nominal)
K = [(0,0),(5.45,5),(9.28,8.5),(11.44,10.3),(13.6,12),(16.9,15),(20.6,18),(24.2,22),(28.1,26.5),(34.1,31),(39.6,35.5),
     (42.7,37),(44.35,40),(46.4,42),(47.95,45),(50.65,48.5),(54.1,52),(56.9,56),(62.0,61.1)]
TK = np.array([a for a,b in K]); VK = np.array([b for a,b in K])
DUR = 62.0
def v_of_T(T): return float(np.interp(T, TK, VK))
def T_of_v(v): return float(np.interp(v, VK, TK))
