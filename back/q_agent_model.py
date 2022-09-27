
import numpy as np
from utils import return_probabilities, generate_json_policy

class Player:
    def __init__(self, num_actions, gamma, learning_rate, epsilon) -> None:
        self.qfunction = {}
        self._gamma = gamma
        self._alpha = learning_rate
        self._epsilon =  epsilon
        self._num_actions = num_actions
    
    def act(self, state, eval = False):
        if state not in self.qfunction:
            self.qfunction[state] = np.zeros(self._num_actions)
        Q_s = self.qfunction[state]
        if (eval or np.random.uniform() > self._epsilon) and np.any(Q_s - Q_s[0]):
            action = np.argmax(self.qfunction[state])
        else :
            action = np.random.randint(self._num_actions)
        return action
    

    def update(self, state, action, next_state, reward, done) -> None:
        if state not in self.qfunction:
            self.qfunction[state] = np.zeros(self._num_actions)
        
        if done:
            self.qfunction[state][action] = (1-self._alpha) * self.qfunction[state][action] + self._alpha * reward
        else:
            if next_state not in self.qfunction:
                self.qfunction[next_state] = np.zeros(self._num_actions)
            self.qfunction[state][action] = (1-self._alpha) * self.qfunction[state][action] + self._alpha * (reward + self._gamma * self.qfunction[next_state].max()) 
    
    def generate_policy(self, kind, json_policy_path = None):
        policy = {}
        for state, qvalue in self.qfunction.items():
            if '0' in state: # only consider the case that there is an empty slot
                policy[state] = return_probabilities(state=state, qvalue_state=qvalue, kind = kind)
        if json_policy_path is not None:    
            generate_json_policy(policy, json_policy_path)
        return policy


def run_episode(player1, player2, environment, eval, max_step = 100):
    state = environment.reset()
    n_steps = 0
    player = [player1, player2]
    rewards = [0,0]
    dones = [False, False]
    p = 0
    winners = []
    while True:
        action = player[p].act(state, eval=eval)
        next_state, reward, done, switch = environment.step(action)
        
        if not eval:
            player[p].update(state, action, next_state, reward, done)
        rewards[p] += reward
        dones[p] = done
        if done:
            winners.append(p+1)
        n_steps += 1
        state = next_state
        if all(dones) or n_steps > max_step:
            break
        if switch: # do not pass the hand until player put in an empty place
            p = int(not p) 
    winner = winners[0] if winners else 0
    return rewards, winner
