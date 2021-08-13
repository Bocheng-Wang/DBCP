import numpy as np

features_path = './Subject_0001.npy'
raw = np.load(features_path)

# thickness
thickness = raw[2793:3792]

# volume
volume = raw[16979:17979]

features = np.hstack((thickness, volume))
pass