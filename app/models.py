from dataclasses import dataclass, field
import numpy as np
from typing import List, NoReturn


@dataclass
class Container:

    arrival_time: np.int64
    loading_time: np.int64 = -1
    departure_time: np.int64 = -1

    @property
    def waiting_time(self):
        return self.departure_time - self.arrival_time


@dataclass
class Airplane:
    _current_id = 0

    airplane_id: int
    capacity: int
    current_load: int = 0

    @property
    def is_full_loaded(self):
        return self.capacity == self.current_load

    @staticmethod
    def get_new_airplane(capacity: int) -> "Airplane":
        """
        Airplanes factory
        @param capacity: creating airplanes capacity
        @return: an Airplane instance
        """
        Airplane._current_id += 1
        return Airplane(airplane_id=Airplane._current_id,
                        capacity=capacity)

    @staticmethod
    def get_list_of_airplanes(capacities: dict) -> List["Airplane"]:
        """
        Airplanes' list factory
        @param capacities: the dictionary of capacities
        @return: the list of airplanes with the predefined capacities
        """
        list_to_return = []
        for k, v in capacities.items():
            for _ in range(v):
                list_to_return.append(Airplane.get_new_airplane(capacity=k))
        return list_to_return


@dataclass
class ModelStats:

    departed_containers: List[Container] = field(default_factory=list)

    def show_stats(self) -> NoReturn:
        """
        Shows the simulations' statistics
        @return:
        """
        pass