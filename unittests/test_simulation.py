from unittest import TestCase

from app.main import Simulation
from collections import deque


class TestSimulation(TestCase):

    def setUp(self) -> None:
        self.sim_model = Simulation()

    def test_instance_creation(self):
        self.assertEqual(5, len(self.sim_model._present_airplanes))
        self.assertTrue(isinstance(self.sim_model._queue, deque))

    def test_add_containers(self):
        self.sim_model._add_containers(2)
        self.assertEqual(2, self.sim_model.queue_current_len)
