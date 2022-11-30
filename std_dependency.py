from sim_model.main import Simulation
import json

NUMBER_OF_STEPS = 4000


if __name__ == '__main__':

    results = {}
    for n in range(10, 50):
        internal_results = []
        print(f'Simulation iterations: {n}')
        for _ in range(n):
            simulation = Simulation(show_stats=False)
            sim_stats = simulation.run(steps=NUMBER_OF_STEPS)
            internal_results.append(sim_stats.result)
        results.update({n: internal_results})
    with open('start_oscillations/std_dependence_results.json', 'w') as f:
        json.dump(results, f)