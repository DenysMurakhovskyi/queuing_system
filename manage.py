from sim_model.main import Simulation

if __name__ == '__main__':
    sim_model = Simulation(show_stats=True)
    stats = sim_model.run(steps=261)
    stats.show_stats()