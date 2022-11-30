from unittest import TestCase

from sim_model.models import Airplane


class TestModels(TestCase):

    LIST_OF_CAPACITIES = {80: 3, 140: 2}

    def test_airplane_model(self):
        list_of_airplanes = Airplane.get_list_of_airplanes(self.LIST_OF_CAPACITIES)
        self.assertEqual(5, len(list_of_airplanes))
        self.assertEqual(5, list_of_airplanes[-1].airplane_id)


