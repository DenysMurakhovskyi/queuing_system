from collections import deque
from app.models import Container, Airplane, ModelStats
from typing import List, NoReturn, Union


class Simulation:

    CONTAINERS_PER_INTERVAL = 2
    LOADING_TIME = 0
    AIRPLANES_CAPACITIES = {80: 3, 140: 2}

    @property
    def queue_current_len(self) -> int:
        return len(self._queue)

    def __init__(self):
        self._timer: int = 0
        self._queue: deque = deque()
        self._loading_airplane: Union[Airplane, None] = None
        self._present_airplanes: List = Airplane.get_list_of_airplanes(self.AIRPLANES_CAPACITIES)
        self._flown_away_airplanes: List = []
        self._stats = ModelStats()
        self._model_used: bool = False

    def run(self, steps=1000) -> ModelStats:
        """
        : steps - the number of simulation steps
        Main methods. Run the simulation
        @return: model statistics' instance
        """

        if self._model_used:
            raise RuntimeError('The instance can be used only for single simulation')

        while self._timer < steps:
            self._add_containers(self.CONTAINERS_PER_INTERVAL)

            if self._loading_airplane is None:
                self._choose_airplane_for_load()
            self._load_containers()

            if self._loading_airplane.is_full_loaded():
                self._depart_airplane()

            self._timer += 1

        return self._stats

    def _add_containers(self, n_to_add: int) -> NoReturn:
        """
        Put containers into the _queue
        @return: None
        """
        for container in [Container(arrival_time=self._timer)] * n_to_add:
            self._queue.append(container)

    def _choose_airplane_for_load(self) -> NoReturn:
        """
        Chooses the airplane for load using pre-defined rules
        @return: None
        """
        if len(self._present_airplanes) > 0:
            lowest_capacity = min([airplane.capacity for airplane in self._present_airplanes])
            self._loading_airplane = list(filter(lambda x: x.capacity == lowest_capacity, self._present_airplanes))[0]

    def _depart_airplane(self) -> NoReturn:
        """
        Makes all the work with an airplane departure
        @return: None
        """
        pass

    def _generate_flight_time(self) -> NoReturn:
        """
        Generates an airplane's flight time using pre-defined rules
        @return: None
        """
        pass

    def _load_containers(self):
        """
        Loads containers into an airplane
        @return: None
        """
        pass

    def _put_container_into_history(self):
        """
        Puts loaded containers into the statistics class
        @return:
        """
        pass





