from common.env_factory import get_fake_set, get_real_set

from tensorflow.keras.optimizers import Adam


class Tester(object):
    def __init__(self, env_class, model_class, agent_class, test_set: int = 1,
                 optimizer=Adam(learning_rate=1e-3), metrics: list = None, real: bool = False):
        get_set_func = get_fake_set
        if real:
            get_set_func = get_real_set
        self._env, self._states, self._actions = get_set_func(env_class, test_set)

        # Model
        self._model = model_class(self._states, self._actions)

        if metrics is None:
            metrics = ['mse']
        # Agent
        self._agent = agent_class(model=self._model, actions=self._actions, optimizer=optimizer, metrics=metrics)

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

        # self._model.summary()

        self._agent.run(env=env, steps=steps)

    def test(self, env=None, number_episodes: int = 1):
        # Test
        if env is None:
            env = self._env

        env.testing = True
        env.reset()
        self._agent.test(env, episodes=number_episodes)

        env.render()

        env.testing = False

    def save(self, filepath: str = "saved_agent.h5"):
        self._agent.save(filepath)

    def load(self, filepath: str = "saved_agent.h5"):
        self._agent.load(filepath)
