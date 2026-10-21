import numpy as np
# (T_real, v_nominal)
K = [(0,0),(6.6,5),(12.65,10),(15.4,11.8),(16.85,14),(21.6,16.3),(22.45,19),(27.4,22),(29.1,25),(32.1,30),(34.35,30.8),
     (35.8,33),(37.55,35),(40.85,39),(44.2,41),(45.65,43),(47.7,46),(52.6,50),(58.2,55),(60.8,58),(63.0,59),(66.0,61),(69.2,65),(73.5,69.3)]
TK = np.array([a for a,b in K]); VK = np.array([b for a,b in K])
DUR = 73.5
def v_of_T(T): return float(np.interp(T, TK, VK))
def T_of_v(v): return float(np.interp(v, VK, TK))
