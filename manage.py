from app.main import Simulation

if __name__ == '__main__':
    sim_model = Simulation(seed_value=495, show_stats=True)
    stats = sim_model.run(steps=10000)
    stats.show_stats()