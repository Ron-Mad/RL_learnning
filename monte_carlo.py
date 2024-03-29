import numpy as np
from grid_world import standard_grid, negative_grid
from iterative_policy_evaluation import print_values, print_policy

SMALL_ENOUGH = 10e-4
GAMMA = 0.9
ALL_POSSIBLE_ACTIONS = ('U', 'D', 'L', 'R')

def play_game(grid, policy):
    # return a list of states and corresponding returns

    # reset game to start at a random position
    # we need to do this because given our current deterministic policy we would never end
    # up at certain states, but we still want to measure the returns

    start_states = list(grid.actions.keys())
    start_idx = np.random.choice(len(start_states))
    grid.set_state(start_states[start_idx])

    s = grid.current_state()
    states_and_rewards = [(s, 0)]

    while not grid.game_over():
        a = policy[s]
        r = grid.move(a)

        s = grid.current_state()
        states_and_rewards.append((s, r))
    # calc returns:
    G = 0
    states_and_returns = []
    first = True
    for s, r in reversed(states_and_rewards):
        if first:
            first = False
        else:
            states_and_returns.append((s, G))
        G = G * GAMMA + r
    states_and_returns.reverse() #in visited order
    return states_and_returns


if __name__ == '__main__':
    N_ITER = 100
    grid = standard_grid()

    print('rewards:')
    print_values(grid.rewards, grid)

    policy = {
        (2, 0):'U',
        (1, 0): 'U',
        (0, 0): 'R',
        (0, 0): 'R',
        (0, 1): 'R',
        (0, 2): 'R',
        (1, 2): 'R',
        (2, 1): 'R',
        (2, 2): 'R',
        (2, 3): 'U',
    }

    V ={}
    returns = {}
    states = grid.all_states()
    for s in states:
        if s in grid.actions:
            returns[s] = []
        else:
            returns[s] = 0

    for t in range(N_ITER):
        states_and_returns = play_game(grid, policy)
        seen_states = set()
        for s, G in states_and_returns:
            if s not in seen_states:
                returns[s].append(G)
                V[s] = np.mean(returns[s])
                seen_states.add(s)
    print("Values:")
    print_values(V, grid)
    print("policy")
    print_policy(policy, grid)

