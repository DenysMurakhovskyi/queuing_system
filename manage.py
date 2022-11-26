from app.main import Simulation

if __name__ == '__main__':
    sim_model = Simulation()
    stats = sim_model.run()
    stats.show_stats()