# **Backend implementation**

This directory contains the following

```bash
back
.
├── Q-learning_model.ipynb
├── player_module.py
├── readme.md
├── tictactoe.py
├── train_module.py
└── utils.py
```

where each will be described bellow.

## **Notebook for agent policy generator**(`Q-learning_model.ipynb`)

This notebook contains a complete and step by step process on how to generate `automatically & manually` policies and store it in a json file.

You will find all the macine learning part here.

## **Player classes** (`player_module.py`)

This file contains the implementation of a free tabular `QAgent` and `HumanPlayer` classes which all inherit the `Player` parent class.

## **The TIC TAC TOE environment** (`tictactoe.py`)

This file contain the full implementation of tictactoe environment. It is both used for training and deployment.

## **Agent trainer** (`train_module.py`)

It has an implementation of  `run_episode()` and `train()` functions which can be used to train agent with another agent or a human player.

Furthermore, it contains functions for visualization evaluations during training

## **Utility functions** (`utils.py`)

From its name, it is used to store the utility functions for `softmax`, `argmax`, probability generator, write and read json files, visualization, ...
