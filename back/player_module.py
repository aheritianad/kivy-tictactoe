import numpy as np
from typing import *

from back.utils import return_probabilities, generate_json, argmax_uniform


class Player:
    def act(self, state: str):
        """Player will generate action depending on the state

        Args:
            state (str): current state
        """
        pass

    def update(
        self, state: str, action: int, next_state: str, reward: int, done: bool
    ) -> None:
        """Update function for the qfunction at a given `state` with a given
        `action` which takes it to a given state (`next_state`) and obtain a
        reward `reward` and a flag `done` saying wether the new state is a
        terminal sate or not.

        Args:
            state (str): current state
            action (int): action to perfom
            next_state (str): next state after performing the action at the state
                                reward (int): reward obtained by performing the action at the state
            done (bool): falg saying wether the next state is a terminal state or not
        """
        pass


class HumanPlayer(Player):
    def __init__(self, player_number: int, name: str = None):
        """This is the class of human player

        Args:
            player_number (int): either 1 or 2, which says the player
                                    if the first player or the second
            name (str, optional): name of the player. Defaults to None.
                                    If none is given, the player will
                                    be `Player1` or `Player2` depending on their number
        """
        super().__init__()
        self.player_number = player_number
        self.name = name if name else f"Player{player_number}"

    def act(self, state: str, *args, **kwargs):
        """It will ask the human players to choose action that they will take
        by giving the corresponding value shown in the board

        Args:
            state (str): current state

        Returns:
            int: the action that user will take
        """
        print(
            f"{self.name}, it is your turn. You are {('X','+')[self.player_number-1]}."
        )
        available_actions = []
        table = ""
        for action, state_number in zip(range(9), state):
            s_num = int(state_number)
            if s_num == 0:
                available_actions.append(action)
            symbols = (str(action), "X", "+")
            table += symbols[s_num] + " "
            if action in (2, 5):
                table += "\n"
        print(table)

        while True:
            action = int(input(f"Choose your action {available_actions}:\t").strip())
            if action in available_actions:
                break
        print("->", action)

        return action


class QAgent(Player):
    def __init__(
        self,
        num_actions: int,
        gamma: float,
        learning_rate: float,
        epsilon: float,
        qfunction: dict = None,
    ) -> None:
        """A free tabular Q-agent class for Tic Tac Toe player

        Args:
            num_actions (int): the total number of actions for the environment
            gamma (float): discount factor (between 0 to 1, 1 excluded from theory).
                            The higher gamma is, the more the agent look at a bigger horizon.
            learning_rate (floar): learning rate for update Q-function (from 0 to 1).
                                    The higher learning rate is, the higher exploitation.
            epsilon (float): probability of acting non greedily (from 0 to 1). The higher epsilon is,
                            the more the agent explore.
            qfunction (dict): Q-value function of each state at each action. Default to None.
        """
        self.set_learning_params(gamma, learning_rate, epsilon)
        self.qfunction = qfunction if qfunction is not None else {}
        self._num_actions = num_actions

    def set_learning_params(
        self, gamma: float = None, learning_rate: float = None, epsilon: float = None
    ):
        """Setting learning parameters.
        At least one of the parameters is given.

        Args:
            gamma (float, optional): discount factor (between 0 to 1, 1 excluded from theory).
                            The higher gamma is, the more the agent look at a bigger horizon.
            learning_rate (float, optional): learning rate for update Q-function (from 0 to 1).
                                    The higher learning rate is, the higher exploitation.
            epsilon (float, optional): probability of acting non greedily (from 0 to 1). The higher epsilon is,
                            the more the agent explore.
        """
        assert gamma or learning_rate or epsilon
        if gamma is not None:
            self._gamma = gamma
        if learning_rate is not None:
            self._alpha = learning_rate
        if epsilon is not None:
            self._epsilon = epsilon

    def act(self, state: str, eval: bool = False, policy: dict = None):
        """Sample action at a given state

        Args:
            state (str): state where to chose a sample action according to
                            the `qfunction` and the `eval` flag.
            eval (bool, optional): a flag saying wether the sampling should be
                                    done greedily (if `eval` is set to `True`) or epsilon-greedy. Defaults to False.
            policy (dict, optional): a dictionary policy to use if it is not None. Default to None. If policy is given
                                    then eval will be ignored. If the given state is not available in the policy, action
                                    will be choosen uniformly from all allowed move.

        Returns:
            int: a sample action at the given state.
        """
        if policy is not None and isinstance(policy, dict):
            if state in policy:
                proba = policy[state]
            else:
                proba = return_probabilities(
                    state, np.zeros(self._num_actions), "random"
                )
            action = np.random.choice(np.arange(self._num_actions), p=proba)
            return action

        if state not in self.qfunction:
            self.qfunction[state] = np.array(
                return_probabilities(state, np.zeros(self._num_actions), "random")
            )

        if eval or np.random.uniform() > self._epsilon:
            action = argmax_uniform(self.qfunction[state])  # grab argmax uniformely
        else:
            action = np.random.randint(self._num_actions)
        return action

    def update(
        self, state: str, action: int, next_state: str, reward: int, done: bool
    ) -> None:
        """Update function for the qfunction at a given `state` with a given `action`
        which takes it to a given state (`next_state`) and obtain a reward `reward` and a flag `done` saying wether the .
        the new state is a terminal sate or not.

        Args:
            state (str): current state
            action (int): action to perfom
            next_state (str): next state after performing the action at the state
            reward (int): reward obtained by performing the action at the state
            done (bool): falg saying wether the next state is a terminal state or not
        """
        if state not in self.qfunction:
            self.qfunction[state] = np.array(
                return_probabilities(state, np.zeros(self._num_actions), "random")
            )

        if done:
            self.qfunction[state][action] = (1 - self._alpha) * self.qfunction[state][
                action
            ] + self._alpha * reward
        else:
            if next_state not in self.qfunction:
                self.qfunction[next_state] = np.array(
                    return_probabilities(
                        next_state, np.zeros(self._num_actions), "greedy"
                    )
                )
            self.qfunction[state][action] = (1 - self._alpha) * self.qfunction[state][
                action
            ] + self._alpha * (reward + self._gamma * self.qfunction[next_state].max())

    def save_qfunction(self, json_qfunction_path: str):
        """Save Q function in a json file

        Args:
            json_qfunction_path (str): path where json file will be saved
        """
        generate_json(self.qfunction, json_qfunction_path)

    def generate_policy(self, kind: str, json_policy_path: str = None):
        """Generate a policy of an agent from its qfunction.

        Args:
            kind (str): one of the strings `'random'`, `'greedy'` or `'softmax'`
                        which will be used to define the probability.
            json_policy_path (str, optional): A path to save the policy as a json file.
                                                Defaults to None. If it is none, then the policy
                                                will only be returned as a dictionary.

        Returns:
            dict: generated policy
        """
        policy = {}
        for state, qvalue in self.qfunction.items():
            policy[state] = return_probabilities(
                state=state, qvalue_state=qvalue, kind=kind
            )
        if json_policy_path is not None:
            generate_json(policy, json_policy_path)
        return policy
