from player_module import Player, HumanPlayer
from tictactoe import TicTacToe

from typing import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def run_episode(
    player1: Player,
    player2: Player,
    environment: TicTacToe,
    eval: bool = False,
    max_step: int = 100,
):
    """Runing episode between two adgents players.

    Args:
        player1 (Player): first QAgent player
        player2 (Player): second QAgent player
        environment (TicTacToe): the tic tac toe environment where the two agents will play
        eval (bool, optional): flag saying wether it is an evaluation or a training with update.
                        If it is an evaluation, then both player will play greedily. Defaults to .
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
    done = False
    p = 0
    winners = []
    while True:
        if done and isinstance(players[p], HumanPlayer):
            action = 0
        else:
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
    player1: Player,
    player2: Player,
    environment: TicTacToe,
    num_episodes: int,
    eval_every_N: int,
    num_eval_episodes: int,
    max_step: int = 100,
):
    """Train QAgent player

    Args:
        player1 (Player): first player
        player2 (Player): _description_
        environment (TicTacToe): the tic tac toe environment where the two agents will play
        num_episodes (int): number of episodes to do for the training
        eval_every_N (int): episode period for evaluation
        num_eval_episodes (int): number of episode for each evaluation
        max_step (int, optional): maximum step allowed for the episode. Defaults to 100

    Returns:
        tuple[list, np.ndarray, np.darray]: - list of episodes number during evaluation
                                            - 2-d array of average reward for each evaluation
                                            - 2-d array of average number of [draw, player1 wins, player2 wins]
                                            for each evaluation during training
    """
    there_is_a_human_player = isinstance(player1, HumanPlayer) or isinstance(
        player2, HumanPlayer
    )
    all_rewards = []
    episodes = []
    winners = []
    print("\nYou can choose to stop training at any time by interrupting.")
    try:
        for episode in tqdm(range(num_episodes)):
            if there_is_a_human_player:
                print(f"\n\n---------- Episode : {episode} ----------")
            run_episode(player1, player2, environment, eval=False, max_step=max_step)

            if episode % eval_every_N == 0:
                if there_is_a_human_player:
                    print("\n-----Running evaluation-----\n")
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


def visualize_rewards(
    episodes: list,
    all_rewards: np.ndarray,
    num_eval_episodes: int,
    name1: str = None,
    name2: str = None,
    from_index: int = 0,
    end_index: int = -1,
):
    """Reward visualization for the evaluation during training

    Args:
        episodes (list): list of episode number of traing for evaluation
        all_rewards (np.ndarray): average reward of both players for each evaluation
                                    during training
        num_eval_episodes (int): number of episode for each evaluation
        name1 (str, optional): name of player 1. Defaults to None. If None is given,
                                it will be `Player 1`
        name2 (str, optional): name of player 2. Defaults to None. If None is given,
                                it will be `Player 2`
        from_index (int, optional): start index. Defaults to 0.
        end_index (int, optional): end index. Defaults to -1.
    """
    if not name1:
        name1 = "Player 1"
    if not name2:
        name2 = "Player 2"
    plt.figure(figsize=(15, 6))
    plt.title(f"Average rewards over {num_eval_episodes} episodes")
    plt.xlabel("Number of training episodes")
    plt.ylabel(f"Average rewards")
    plt.plot(
        episodes[from_index:end_index],
        all_rewards[0][from_index:end_index],
        label=name1,
    )
    plt.plot(
        episodes[from_index:end_index],
        all_rewards[1][from_index:end_index],
        label=name2,
    )
    plt.legend()
    plt.show()


def visuzalize_winners(
    winners: np.ndarray[int],
    num_eval_episodes: int,
    name1: str = None,
    name2: str = None,
    from_index: int = 0,
    end_index: int = -1,
):
    """Histogram visualization of number episode time players win for each evaluation

    Args:
        winners (np.ndarray): `3xn`-array number of time for draw or player 1 or 2 wins for each
                                evaluation
        num_eval_episodes (int): number of episode for each evaluation
        name1 (str, optional): name of player 1. Defaults to None. If None is given,
                                it will be `Player 1`
        name2 (str, optional): name of player 2. Defaults to None. If None is given,
                                it will be `Player 2`
        from_index (int, optional): start index. Defaults to 0.
        end_index (int, optional): end index. Defaults to -1.

    Returns:
        str: percentage of draw and winning time of both players
    """
    if not name1:
        name1 = "Player 1"
    if not name2:
        name2 = "Player 2"
    plt.figure(figsize=(15, 6))
    plt.title("Histogram of number of time Player's win.")
    plt.hist(winners[0][from_index:end_index], label="Draw")
    plt.hist(winners[1][from_index:end_index], label=name1)
    plt.hist(winners[2][from_index:end_index], label=name2)
    plt.legend()
    plt.show()

    draw, p1, p2 = (
        np.mean(winners[:, from_index:end_index], axis=-1) * 100 / num_eval_episodes
    )
    return f"{draw:.2f}% is Draw\n{p1:.2f}% {name1} wins\n{p2:.2f}% {name2} wins"
