# **<font color="red">Tic</font><font color="green">Tac</font><font color="blue">Toe</font> Game**

## **What is this?**

This is a draft of a kivy app which can do basics tictactoe game. User can choose to play against cpu.

## **<font color="red">WARNING!!!</font>**

The iterface is not nice. Yeah! but it can do the job.

## **Why do I write this?**

- Mainly for fun
- To apply my understanding of kivy and Q-learning free tabular

## **Next plan ?**

- [x] ~~My next plan is to implement a reinforcement learning model from scratch to allow cpu to play on its own.~~
- [ ] It seems that the model plays offensive only. I will train it to play against myself after against itself when I have time for that.

## **How to use it?**

First of all, you need to download and install it. It runs on `python3`.

### **Installation**

#### Clone this repository by running

```bash
git clone https://github.com/aheritianad/kivy-tictactoe.git
```

#### Enter into the directory

```bash
cd kivy-tictactoe
```

#### **[OPTIONAL]** Create a virtual environment

Do the following if you want to run it in a virtual environment.

##### Create a virtual environment named `.venv`

```bash
python3 -m venv .venv
```

##### Activate the virtual environment you just created with

```bash
source .venv/bin/activate
```

#### Install the requirements in the environment

```bash
pip3 install -r requirements.txt
```

### **Run the game**

#### Use the following command to run the game

```bash
python3 main.py
```

#### Solo vs Multiplayer setups

- For solo, you can choose to either the first player or the second by setting CPU player's by either `cpu1` or `cpu2` or `cpu3` depending on the level you want to play with

- For multiplayer, only avoid  `cpu1`, `cpu2` and `cpu3` for players' names
