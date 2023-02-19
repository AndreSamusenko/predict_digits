import keras


class Predictor:
    def __init__(self):
        self._model = keras.models.load_model('mlp_digits_28x28.h5')

    def predict(self, image):
        prediction = self._model.predict(image)
        return prediction, prediction.argmax()


