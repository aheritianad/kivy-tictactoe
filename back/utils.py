import numpy as np
import json
from typing import *


def softmax(logits: np.ndarray):
    """Compute the softmax of a logits.

    Args:
        logits (np.ndarray): a 1-d array logits

    Returns:
        np.ndarray: probability distribution of the logits using softmax
    """
    exp_logits = np.exp(logits - logits.max())
    return exp_logits / np.sum(exp_logits)


def argmax_uniform(qvalue: np.ndarray):
    """Argmax function where the index will be chosen uniformely if there are more than one max

    Args:
        qvalue (np.ndarray): a 1-d array argument for the argmax function

    Returns:
        int: argmax chosen uniformely from all maximum
    """
    idx_max = np.arange(qvalue.shape[0])[qvalue == qvalue.max()]
    return np.random.choice(idx_max)


def return_probabilities(state: str, qvalue_state: np.ndarray, kind: str):
    """Generate a probability distribution of actions at a given state, knowing the Q-value

    If the state is for filled board, action 0 will be given.

    Args:
        state (str): current state
        qvalue_state (np.ndarray): `1-D`of the Q-value at the given state
        kind (str): one of the strings `'random'`, `'greedy'` or `'softmax'` which will be used to define the probability.

    Raises:
        NotImplementedError: raise Error if kind is not one of `'random'`, `'greedy'` and `'softmax'`

    Returns:
        list: the policy distribution at the given state
    """
    index_state = np.array(list(map(int, list(state))))
    probs = np.zeros_like(qvalue_state, dtype=np.float)
    logits = qvalue_state[index_state == 0]
    if len(logits) == 0:
        probs[0] = 1
        return list(probs)
    elif kind == "greedy":
        p = np.zeros_like(logits)
        idx_max = np.where(logits - logits.max() == 0)[0]
        p[idx_max] = 1 / len(
            idx_max
        )  # Give the same probability when there are more than one maximum
    elif kind == "softmax":
        p = softmax(logits)
    elif kind == "random":
        p = 1 / len(logits)
    else:
        raise NotImplementedError
    probs[index_state == 0] = p
    return list(probs)


def generate_json_policy(policy: dict, json_policy_path: str):
    """Generate a json file of the policy dictionary

    Args:
        policy (dict): a policy of an agent
        json_policy_path (str): a path where the json file will be stored
    """
    with open(json_policy_path, "w") as json_file:
        json.dump(policy, json_file, indent=2)


def read_json_policy(json_policy_path: str):
    """Generate a policy in a dictionary from a json file

    Args:
        json_policy_path (str): path where the json file is stored

    Returns:
        dict[str: list]: a policy dictionary with states (`str`) as keys and action distributions (`list`) as values
    """
    with open(json_policy_path, "r") as json_file:
        policy = json.load(json_file)
    return policy
