from rl.agents import DQNAgent as DqnAgent_rl
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy


class SimpleAgent:
    def __init__(self, model, actions, optimizer, metrics: list = None):
        self._model = model
        self._policy = BoltzmannQPolicy()
        self._memory = SequentialMemory(limit=1000000, window_length=1)
        self._agent = DqnAgent_rl(model=self._model, memory=self._memory, policy=self._policy,
                                  nb_actions=actions, nb_steps_warmup=5000, target_model_update=1e-3)

        if metrics is None:
            metrics = ['mse']
        self._agent.compile(optimizer, metrics=metrics)

    def run(self, env, steps=10000):
        env.reset()
        # Learn
        self._agent.fit(env, nb_steps=steps, visualize=False, verbose=1)

    def test(self, env, episodes=1):
        self._agent.test(env, nb_episodes=episodes, visualize=False)

    def save(self, filepath: str = "saved_agent.h5"):
        self._agent.save_weights(filepath, overwrite=True)

    def load(self, filepath: str = "saved_agent.h5"):
        self._agent.load_weights(filepath)
