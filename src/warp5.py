import numpy as np
K = [(0,0),(2.85,2.5),(5.7,5.0),(11.75,8.0),(14.6,8.2),(17.1,11.0),(18.3,11.4),(20.85,14.0),(23.65,16.0),
     (27.0,19.0),(28.7,20.0),(34.6,24.5),(38.55,29.0),(42.8,33.5),(45.3,37.5),(48.0,43.0),(51.1,46.5),(55.0,50.0)]
TK = np.array([a for a,b in K]); VK = np.array([b for a,b in K])
DUR = 55.0
def v_of_T(T): return float(np.interp(T, TK, VK))
def T_of_v(v): return float(np.interp(v, VK, TK))
