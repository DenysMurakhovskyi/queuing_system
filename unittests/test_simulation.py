from unittest import TestCase

from app.main import Simulation
from collections import deque
from app.models import Airplane
import seaborn as sns
import matplotlib.pyplot as plt


class TestSimulation(TestCase):

    def setUp(self) -> None:
        self.sim_model = Simulation()
        Airplane._current_id = 0

    def test_instance_creation(self):
        self.assertEqual(5, len(self.sim_model._present_airplanes))
        self.assertTrue(isinstance(self.sim_model._arrival_queue, deque))

    def test_add_containers(self):
        self.sim_model._add_containers(2)
        self.assertEqual(2, self.sim_model.queue_current_len)

    def test_choose_airplane_for_load(self):
        self.sim_model._choose_airplane_for_load()
        self.assertEqual(1, self.sim_model.loading_airplane.airplane_id)

    def test_load_containers(self):
        self.sim_model._choose_airplane_for_load()

        self.sim_model.CONTAINERS_LOAD_PER_INTERVAL = -1
        self.sim_model._add_containers(2)
        self.assertEqual(2, self.sim_model._load_containers())
        self.assertEqual(2, self.sim_model.loading_airplane.current_load)

        self.sim_model.CONTAINERS_LOAD_PER_INTERVAL = 1
        self.sim_model._add_containers(2)
        self.assertEqual(0, self.sim_model._load_containers())
        self.assertEqual(2, self.sim_model.loading_airplane.current_load)

    def test_generate_flight_time(self):
        values = [self.sim_model._generate_flight_time() for _ in range(2000)]
        sns.displot(values, bins=20)
        plt.show()



