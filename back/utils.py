
import numpy as np
import json

def softmax(logits: np.ndarray):
    exp_logits = np.exp(logits - logits.max())
    return exp_logits/np.sum(exp_logits)

def return_probabilities(state, qvalue_state, kind):
    index_state = np.array(list(map(int, list(state))))
    probs = np.zeros_like(qvalue_state, dtype=np.float)
    logits = qvalue_state[index_state == 0]
    if kind == "greedy":
        p = np.zeros_like(logits)
        p[logits.argmax()] = 1
    elif kind == "softmax":
        p = softmax(logits)
    elif kind == "random":
        p = 1/len(logits)
    else:
        raise NotImplementedError
    probs[index_state == 0] = p
    return list(probs)

def generate_json_policy(policy, json_policy_path):
    with open(json_policy_path, 'w') as json_file:
        json.dump(policy, json_file, indent=2)

def read_json_policy(json_policy_path):
    with open(json_policy_path, 'r') as json_file:
        policy = json.load(json_file)
    return policy
