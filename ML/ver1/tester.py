import time

from common.env_factory import get_fake_set, get_real_set

from tensorflow.keras.optimizers import Adam


class Tester(object):
    def __init__(self, env_class, model_class, agent_class, optimizer=Adam(learning_rate=1e-3), metrics: list = None,
                 test_set: int = 1, real: bool = False):
        get_set_func = get_fake_set
        if real:
            get_set_func = get_real_set
        self._env, observation, actions = get_set_func(env_class, test_set)

        # Model
        self._model = model_class(observation, actions)

        # Agent
        if metrics is None:
            metrics = ['mse']
        self._agent = agent_class(self._model, actions, optimizer=optimizer, metrics=metrics)

    @property
    def env(self):
        return self._env

    @property
    def model(self):
        return self._model

    @property
    def agent(self):
        return self._agent

    def run(self, env=None, steps=100000):
        # Train
        if env is None:
            env = self._env

        self._agent.run(env=env,
                        steps=steps)

    def test(self, env=None, number_episodes: int = 1):
        # Test
        if env is None:
            env = self._env

        env.reset()
        env.testing = True
        start = time.time()
        self._agent.test(env, episodes=number_episodes)
        end = time.time()
        env.render()
        print("Time = "+str(end - start))

    def save(self, filepath: str = "saved_agent.h5"):
        self._agent.save(filepath)

    def load(self, filepath: str = "saved_agent.h5"):
        self._agent.load(filepath)
