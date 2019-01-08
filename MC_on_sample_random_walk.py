import random
from pprint import pprint

def every_visit_MC(episodes, states):
    N = {state : 0 for state in states}
    S = {state : 0.0 for state in states}
    V = {state : 0.0 for state in states}

    for episode in episodes:
        if episode[-1] == "E":
            for s in episode:
                N[s] += 1
                S[s] += 1.0
        else:
            for s in episode:
                N[s] += 1
                S[s] += 0.0
    for s in V:
        try:
            V[s] = S[s]/N[s]
        except ZeroDivisionError:
            V[s] = None
    return V

def first_visit_MC(episodes, states):
    N = {state : 0 for state in states}
    S = {state : 0.0 for state in states}
    V = {state : 0.0 for state in states}

    for episode in episodes:
        visited = []
        # Checking if the penultimate state was E since
        # we have a reward of 1 only for E to Stop
        # Also assuming that there's no discounting
        if episode[-1] == "E":
            for s in episode:
                if s not in visited:
                    N[s] += 1
                    S[s] += 1.0
                    visited.append(s)
        else:
            for s in episode:
                if s not in visited:
                    N[s] += 1
                    S[s] += 0.0
                    visited.append(s)
    for s in V:
        try:
            V[s] = S[s]/N[s]
        except ZeroDivisionError:
            V[s] = None
    return V


def generate_episode(start_state, stop_state, random_walk):
    episode = [start_state]
    current_state = start_state
    # The random policy
    next_state = random.choice(random_walk[current_state])
    while next_state != stop_state:
        episode.append(next_state)
        current_state = next_state
        next_state = random.choice(random_walk[current_state])
    return episode

def main(rounds = 10, MC = "Every-visit"):
    random_walk = {
        "A" : ["Stop", "B"],
        "B" : ["A", "C"],
        "C" : ["B", "D"],
        "D" : ["C", "E"],
        "E" : ["D", "Stop"]
    }
    states = list(random_walk.keys())
    start_state = "C"
    stop_state = "Stop"
    episodes = []
    for i in range(rounds):
        episodes.append(generate_episode(start_state, stop_state, random_walk))

    if MC == "Every-visit":
        V = every_visit_MC(episodes, states)
    else:
        V = first_visit_MC(episodes, states)
    print("Value function after {} episodes".format(rounds))
    pprint(V)
    print("")

if __name__ == "__main__":
    print("Results with First Visit MC:\n")
    main(rounds=10, MC="First-visit")
    main(rounds=100, MC="First-visit")
    main(rounds=1000, MC="First-visit")
    main(rounds=10000, MC="First-visit")

    print("\nResults with Every Visit MC:\n")
    main(rounds = 10, MC = "Every-visit")
    main(rounds = 100, MC = "Every-visit")
    main(rounds = 1000, MC = "Every-visit")
    main(rounds = 10000, MC = "Every-visit")