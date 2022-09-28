import numpy as np
from tqdm import tqdm
from typing import *
from utils import return_probabilities, generate_json_policy
from tictactoe import TicTacToe


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
        table = ""
        for action, number in zip(range(9), state):
            symbols = (str(action), "X", "+")
            table += symbols[int(number)] + " "
            if action in (2, 5):
                table += "\n"
        print(table)
        action = input("Choose your action :\t")
        return int(action)


class QAgent(Player):
    def __init__(
        self, num_actions: int, gamma: float, learning_rate: float, epsilon: float
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
        """
        self.set_learning_params(gamma, learning_rate, epsilon)
        self.qfunction = {}
        self._num_actions = num_actions

    def set_learning_params(self, gamma: float, learning_rate: float, epsilon: float):
        """Setting learning parameters

        Args:
            gamma (float): discount factor (between 0 to 1, 1 excluded from theory).
                            The higher gamma is, the more the agent look at a bigger horizon.
            learning_rate (floar): learning rate for update Q-function (from 0 to 1).
                                    The higher learning rate is, the higher exploitation.
            epsilon (float): probability of acting non greedily (from 0 to 1). The higher epsilon is,
                            the more the agent explore.
        """
        self._gamma = gamma
        self._alpha = learning_rate
        self._epsilon = epsilon

    def act(self, state: str, eval: bool = False):
        """Sample action at a given state

        Args:
            state (str): state where to chose a sample action according to
                            the `qfunction` and the `eval` flag.
            eval (bool, optional): a flag saying wether the sampling should be
                                    done greedily (if `eval` is set to `True`) or epsilon-greedy. Defaults to False.

        Returns:
            int: a sample action at the given state.
        """
        if state not in self.qfunction:
            self.qfunction[state] = np.zeros(self._num_actions)
        Q_s = self.qfunction[state]
        value_are_not_the_same = np.any(Q_s - Q_s[0])
        if (eval or np.random.uniform() > self._epsilon) and value_are_not_the_same:
            idx_max = np.arange(self._num_actions)[
                Q_s == Q_s.max()
            ]  # find all indices with max value
            action = np.random.choice(idx_max)  # grab argmax uniformely
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
            self.qfunction[state] = np.zeros(self._num_actions)

        if done:
            self.qfunction[state][action] = (1 - self._alpha) * self.qfunction[state][
                action
            ] + self._alpha * reward
        else:
            if next_state not in self.qfunction:
                self.qfunction[next_state] = np.zeros(self._num_actions)
            self.qfunction[state][action] = (1 - self._alpha) * self.qfunction[state][
                action
            ] + self._alpha * (reward + self._gamma * self.qfunction[next_state].max())

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
            if "0" in state:  # only consider the case that there is an empty slot
                policy[state] = return_probabilities(
                    state=state, qvalue_state=qvalue, kind=kind
                )
        if json_policy_path is not None:
            generate_json_policy(policy, json_policy_path)
        return policy


def run_episode(
    player1: Player,
    player2: Player,
    environment: TicTacToe,
    eval: bool,
    max_step: int = 100,
):
    """Runing episode between two adgents players.

    Args:
        player1 (Player): first Q-agent player
        player2 (Player): second q-agent player
        environment (TicTacToe): the tic tac toe environment where the two agents will play
        eval (bool): flag saying wether it is an evaluation or a training with update.
                        If it is an evaluation, then both player will play greedily.
        max_step (int, optional): maximum step allowed for the episode. Defaults to 100.

    Returns:
        tuple(list[int,int], int): where the list will contain the reward of player1 and player2
                                    respectedly during the episode. The second element is an
                                    integer (1 or 2) value of the  winner. It will be 0 if it is a draw.
    """
    state = environment.reset()
    n_steps = 0
    players = [player1, player2]
    rewards = [0, 0]
    dones = [False, False]
    p = 0
    winners = []
    while True:
        action = players[p].act(state, eval=eval)
        next_state, reward, done, switch = environment.step(action)

        if not eval:
            players[p].update(state, action, next_state, reward, done)
        rewards[p] += reward
        dones[p] = done
        if done:
            winners.append(p + 1)
        n_steps += 1
        state = next_state
        if all(dones) or n_steps > max_step:
            break
        if switch:  # do not pass the hand until player put in an empty place
            p = int(not p)
    winner = winners[0] if winners else 0
    return rewards, winner


def train(
    player1,
    player2,
    environment,
    num_episodes,
    max_step,
    eval_every_N,
    num_eval_episodes,
):
    all_rewards = []
    episodes = []
    winners = []
    print("\nYou can choose to stop training at any time by interrupting.")
    try:
        for episode in tqdm(range(num_episodes)):
            run_episode(player1, player2, environment, eval=False, max_step=max_step)

            if episode % eval_every_N == 0:
                rewards_list = []
                winners_list = [0, 0, 0]
                for _ in range(num_eval_episodes):
                    rewards, winner = run_episode(
                        player1, player2, environment, eval=True, max_step=max_step
                    )
                    rewards_list.append(rewards)
                    winners_list[winner] += 1
                rewards = np.mean(rewards_list, axis=-1)
                winners.append(winners_list.copy())
                all_rewards.append(rewards)
                episodes.append(episode)
    except KeyboardInterrupt:
        pass

    all_rewards = np.array(all_rewards).T
    winners = np.array(winners).T
    return episodes, all_rewards, winners
