from sim_model.main import Simulation
import json

if __name__ == '__main__':

    results = {}
    for n_steps in range(300, 10000, 100):
        internal_results = []
        for _ in range(20):
            print(f'Simulation steps: {n_steps}')
            simulation = Simulation(show_stats=False)
            sim_stats = simulation.run(steps=n_steps)
            internal_results.append(sim_stats.result)
        results.update({n_steps: internal_results})
    with open('start_oscillations/interval_data_1_1.json', 'w') as f:
        json.dump(results, f)



