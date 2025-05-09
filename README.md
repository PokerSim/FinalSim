PokerSim: Multi-Agent Poker Environment
=======================================

Overview
--------
PokerSim is a Python-based multi-agent poker simulation environment that supports different types of poker bots playing No-Limit Texas Hold'em. It integrates Gym-style environment control, poker rules, chip management, hand evaluation, and player strategies such as:

- StatsBot: Uses statistical heuristics and expected value calculations.
- AllInBot: Always raises all-in.
- PPOBot: Uses a mock neural network policy.
- RandomBot: Chooses random legal actions.

This simulator is useful for testing reinforcement learning strategies, evaluating poker bot performance, and analyzing statistical outcomes over many simulated hands.

Features
--------
- Custom Gym-style environment `PokerEnv`
- Simplified Texas Hold’em rules:
  - Blinds, preflop, postflop (flop/turn/river) handling
  - All-in and raise/call/fold logic
  - Limited re-raise control
- Multiple types of players (bots)
- Full game state printing
- Win distribution and chip charting via Matplotlib
- Action tracking (folds, calls, raises)

File Descriptions
-----------------
PokerSim.py  - Main simulation environment with player classes and match loop.
StatsBot.py  - Implements a statistically-driven bot using preflop/postflop logic.
AllInBot.py  - Simplistic bot that always raises all-in.
pokerkit     - External poker logic module assumed to be used in StatsBot. (Not provided)

Requirements
------------
Python 3.8+
Libraries:
- numpy
- torch
- matplotlib
- gymnasium

Install via:
pip install numpy torch matplotlib gymnasium

Running the Simulation
----------------------
To simulate a game of poker between bots:

python PokerSim.py

Modify the `players` list in `main()` to select which bots participate.
The default runs 50 hands and prints action summaries + chip graph.

Player Types
------------
StatsPlayer   - Uses preflop charts and postflop EV heuristics from StatsBot.py.
AllInPlayer   - Always raises all-in (intended for bluff/exploit testing).
PPOPlayer     - Dummy policy using PyTorch. Meant to be replaced with a trained agent.
RandomPlayer  - Random legal action selection for stochastic baseline comparison.

Game Rules Summary
------------------
- 2 hole cards per player
- 5 community cards (Flop, Turn, River)
- Small blind = 10 chips, Big blind = 20 chips
- Players go all-in if they cannot match bets
- Folded or bankrupt players do not participate in blinds
- Showdown resolves hand strengths and splits pots when needed

Output
------
- Per-hand status printouts:
  - Chip counts
  - Community cards
  - Player decisions
- A line graph of chip totals for each player
- Final summary of fold, call, and raise counts per player

To-Do / Possible Improvements
-----------------------------
- Support side pots and multiple all-ins
- Trainable PPOPlayer via Stable Baselines3 or other RL libraries
- GUI interface for game playback
- Unit testing and modular cleanup

License
-------
This project is provided for educational and research purposes only. Modify and use freely, but attribution is appreciated.
