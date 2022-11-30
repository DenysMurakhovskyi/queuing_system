from dataclasses import dataclass, field
from typing import List, NoReturn, MutableMapping, Union, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import namedtuple


AirplaneWaitTime = namedtuple('AirplaneWaitTime', 'airplane_capacity wait_time')


@dataclass
class Container:
    """
    The class which represents container entity
    """

    arrival_time: np.int64 = -1
    _departure_time: np.int64 = -1
    _loading_time: np.int64 = -1

    @property
    def loading_time(self) -> Union[int, np.nan]:
        if (value := self._loading_time - self.arrival_time) >= 0:
            return value
        else:
            return np.nan

    @property
    def departure_time(self) -> Union[int, np.nan]:
        if (value := self._departure_time - self.arrival_time) >= 0:
            return value
        else:
            return np.nan

    def set_arrival_time(self, value: int) -> NoReturn:
        self.arrival_time = value

    def set_departure_time(self, value: int) -> NoReturn:
        self._departure_time = value

    def set_loading_time(self, value: int) -> NoReturn:
        self._loading_time = value


@dataclass
class Airplane:
    """
    The class which represents an airplane entity
    """

    _current_id = 0

    airplane_id: int
    capacity: int
    arrival_time: int = 0
    departure_time: int = -1

    _containers: List[Container] = field(default_factory=list)

    @property
    def containers_list(self):
        return self._containers

    @property
    def containers_departure_times(self) -> List[int]:
        return [container.departure_time for container in self._containers]

    @property
    def containers_loading_times(self) -> List[int]:
        return [container.loading_time for container in self._containers]

    @property
    def current_load(self):
        return len(self._containers)

    @property
    def is_full_loaded(self):
        return self.capacity == self.current_load

    @property
    def load_time(self):
        return self.departure_time - self.arrival_time

    def load(self, container: Container) -> NoReturn:
        if self.is_full_loaded:
            raise RuntimeError('The airplane is fully loaded')
        self._containers.append(container)

    def set_containers_departure_time(self, value):
        for container in self._containers:
            container.set_departure_time(value)

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
    """
    The class which represents model statistics.
    Used for the statistics accumulation and representation after the end of the simulation.
    """

    _airplanes_wait_time: List[AirplaneWaitTime] = field(default_factory=list)
    _containers_wait_departure_time: List[int] = field(default_factory=list)
    _containers_wait_loading_time: List[int] = field(default_factory=list)

    @property
    def containers_load_mean_time(self) -> Tuple[float, float]:
        return float(np.mean(np.array(self._containers_wait_loading_time))),\
               float(np.std(np.array(self._containers_wait_departure_time)))

    @property
    def containers_depart_mean_time(self) -> Tuple[float, float]:
        return float(np.mean(np.array(self._containers_wait_departure_time))),\
               float(np.std(np.array(self._containers_wait_departure_time)))

    @property
    def airplanes_load_mean_time(self) -> Dict:
        result = {}
        for capacity in set([item.airplane_capacity for item in self._airplanes_wait_time]):
            list_of_values = [item.wait_time for item in self._airplanes_wait_time
                              if item.airplane_capacity == capacity]
            mu, sigma = np.mean(np.array(list_of_values)), np.std(np.array(list_of_values))
            result.update({capacity: (mu, sigma)})
        return result

    def put_airplane_time(self, value: AirplaneWaitTime) -> NoReturn:
        self._airplanes_wait_time.append(value)

    def put_airplanes_time(self, value: List[AirplaneWaitTime]) -> NoReturn:
        self._airplanes_wait_time.extend(value)

    def put_container_departure_time(self, value: int) -> NoReturn:
        self._containers_wait_departure_time.append(value)

    def put_containers_departure_time(self, value: List[int]) -> NoReturn:
        self._containers_wait_departure_time.extend(value)

    def put_container_loading_time(self, value: int) -> NoReturn:
        self._containers_wait_loading_time.append(value)

    def put_containers_loading_time(self, value: List[int]) -> NoReturn:
        self._containers_wait_loading_time.extend(value)

    def show_stats(self) -> NoReturn:
        """
        Shows the simulations' statistics
        @return:
        """
        print('\n\n=== MODEL STATISTICS ===\n')
        mu, sigma = self.containers_load_mean_time
        print(f'Containers loading time: mean={mu:.1f}, std={sigma:.1f}')

        mu, sigma = self.containers_depart_mean_time
        print(f'Containers departure time: mean={mu:.1f}, std={sigma:.1f}')

        for capacity, value in self.airplanes_load_mean_time.items():
            print(f'\nStatistics for airplane with capacity = {capacity}')
            mu, sigma = value
            print(f'Airplanes load time: mean={mu:.1f}, std={sigma:.1f}')

        sns.displot(self._containers_wait_loading_time, bins=10)
        plt.title('Containers wait for loading time distribution')
        plt.show()

        sns.displot(self._containers_wait_departure_time, bins=10)
        plt.title('Containers wait for departure time distribution')
        plt.show()