from keras.models import load_model
import numpy as np
def prediction(file):
    _img=[]
    _img.append(np.load(file))
    img = np.array(_img)
    img = img.astype('float32')
    img = img.reshape(img.shape[0], 32, 32, 1)
    predict = (model.predict_classes(img)[0])
    return predict
model = load_model(
    "C:\\Users\\PhucCoi\\Documents\\ML-by-CBD-Robotics\\Deep Learning\\Week5 Lung cancer part 2\\CNN_model.h5")
prediction("D:\\npy\\0\\1.3.6.1.4.1.14519.5.2.1.6279.6001.102133688497886810253331438797-35.21-35.21176.9632.41.npy")