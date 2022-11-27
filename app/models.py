from dataclasses import dataclass, field
import numpy as np
from typing import List, NoReturn, MutableMapping


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
    _containers: List[Container] = field(default_factory=list)

    @property
    def current_load(self):
        return len(self._containers)

    @property
    def is_full_loaded(self):
        return self.capacity == self.current_load

    def load(self, container: Container) -> NoReturn:
        if self.is_full_loaded:
            raise RuntimeError('The airplane is fully loaded')
        self._containers.append(container)

    def unload(self):
        self._containers = []

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
    def get_list_of_airplanes(capacities: MutableMapping) -> List["Airplane"]:
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