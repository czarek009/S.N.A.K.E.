import keras
from keras.models import load_model
import numpy as np

model = load_model('weights/dombx.h5')
false_input = [0,1,0,1,0,1]
false_input = np.reshape(false_input, newshape=(1,1,6))
prediction = model.predict(false_input)
print(prediction)