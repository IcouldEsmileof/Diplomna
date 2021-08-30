from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential


class SimpleModel(object):
    @staticmethod
    def build_model(observation, actions, name=None):
        return Sequential([
            Flatten(input_shape=(1, observation)),
            Dense(observation * 8, activation='relu'),
            Dense(observation * 4, activation='relu'),
            Dense(actions, activation='linear'),
        ], name=name)
