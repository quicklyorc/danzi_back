import numpy as np
dummy_image = np.random.randint(0, 255, size=(416, 416, 3), dtype=np.uint8)
np.save('yolo_dummy.npy',dummy_image)

X_dummy = np.random.randn(1,224,224,3) 
r_dummy = np.random.randint(1, 45, size=(1,))

np.save('keras_dummy.npy',X_dummy)
np.save('ratio_dummy.npy',r_dummy)