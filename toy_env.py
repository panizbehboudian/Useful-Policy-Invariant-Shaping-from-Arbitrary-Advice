#!/usr/bin/env python

"""
  Author: Paniz Behboudian
"""

import numpy as np
from rl_glue import BaseEnvironment


class ToyEnv(BaseEnvironment):

    def __init__(self, number_of_rows=None, number_of_columns=None):
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.global_reward = 0
        self.outer_walls = np.concatenate((np.mgrid[0:1, 0:number_of_columns + 2].reshape(2, -1).T,
                                           np.mgrid[1:number_of_rows + 2, 0:1].reshape(2, -1).T,
                                           np.mgrid[1:number_of_rows + 2,
                                           number_of_columns + 1:number_of_columns + 2].reshape(2, -1).T,
                                           np.mgrid[number_of_rows + 1:number_of_rows + 2,
                                           1:number_of_columns + 1].reshape(2, -1).T))
        self.inner_walls = {(2, 2): (1, 2), (1, 2): (2, 2)}
        self.goal_coord = np.asarray([1, 2])
        self.start_coord = np.asarray([2, 1])
        self.before_action_state = None
        self.total_reward = 0
        self.episode_reward = 0

    def env_init(self):

        self.before_action_state = np.zeros(2)
        self.total_reward = 0
        self.episode_reward = 0

    def env_start(self):

        self.before_action_state = np.ndarray.astype(self.start_coord, dtype=int)
        self.episode_reward = 0
        return self.before_action_state

    def env_step(self, action):
        """
        Arguments
        ---------
        action : int
            the action taken by the agent in the current state

        Returns
        -------
        result : dict
            dictionary with keys {reward, state, isTerminal} containing the results
            of the action taken
        """
        # applying action
        after_action_state = [0, 0]
        if action == 0:
            after_action_state = [self.before_action_state[0] - 1, self.before_action_state[1]]
        elif action == 1:
            after_action_state = [self.before_action_state[0], self.before_action_state[1] + 1]
        elif action == 2:
            after_action_state = [self.before_action_state[0] + 1, self.before_action_state[1]]
        elif action == 3:
            after_action_state = [self.before_action_state[0], self.before_action_state[1] - 1]

        for wall in self.outer_walls:
            if after_action_state[0] == wall[0] and after_action_state[1] == wall[1]:
                after_action_state = self.before_action_state
                break
        for wall_side1 in self.inner_walls.keys():
            if self.before_action_state[0] == wall_side1[0] and self.before_action_state[1] == wall_side1[1] and \
                    after_action_state[0] == self.inner_walls[wall_side1][0] and after_action_state[1] == \
                    self.inner_walls[wall_side1][1]:
                after_action_state = self.before_action_state
        self.before_action_state = np.ndarray.astype(np.asarray(after_action_state), dtype=int)
        reward = self.global_reward
        is_terminal = False
        if np.array_equal(self.goal_coord, self.before_action_state):
            reward = self.global_reward + 1
            is_terminal = True
            self.before_action_state = None
        self.total_reward += reward
        self.episode_reward += reward
        result = reward, self.before_action_state, is_terminal

        return result

    def env_message(self, in_message):
        pass

