from sim_model.main import Simulation
import json

NUMBER_OF_STEPS = 4000


if __name__ == '__main__':

    results = {}
    for n_per_minute in range(1, 11):
        internal_results = []
        print(f'Arrival: {n_per_minute}')
        for _ in range(20):
            simulation = Simulation(show_stats=False, arrival_quantity=n_per_minute)
            sim_stats = simulation.run(steps=NUMBER_OF_STEPS)
            internal_results.append(sim_stats.result)
        results.update({n_per_minute: internal_results})
    with open('start_oscillations/main_research_1.json', 'w') as f:
        json.dump(results, f)