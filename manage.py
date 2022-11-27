from app.main import Simulation

if __name__ == '__main__':
    sim_model = Simulation()
    stats = sim_model.run(steps=1000)
    stats.show_stats()