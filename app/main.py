from collections import deque
from app.models import Container, Airplane, ModelStats
from typing import List, NoReturn, Union, MutableMapping


class Simulation:

    CONTAINERS_ARRIVAL_PER_INTERVAL: int = 2
    CONTAINERS_LOAD_PER_INTERVAL: int = 1
    AIRPLANES_CAPACITIES: MutableMapping = {80: 3, 140: 2}

    @property
    def queue_current_len(self) -> int:
        return len(self._arrival_queue)

    @property
    def loading_airplane(self) -> Airplane:
        return self._loading_airplane

    def __init__(self):
        self._timer: int = 0
        self._total_containers_passed = 0
        self._arrival_queue: deque = deque()
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
            self._add_containers(self.CONTAINERS_ARRIVAL_PER_INTERVAL)

            if self._loading_airplane is None:
                self._choose_airplane_for_load()

            if self._loading_airplane is None:  # better to write is still None
                self._timer += 1
                continue

            self._load_containers()

            if self._loading_airplane.is_full_loaded:
                self._depart_airplane()

            self._show_current_state()

            self._timer += 1

        return self._stats

    def _add_containers(self, n_to_add: int) -> NoReturn:
        """
        Put _containers into the _arrival_queue
        @return: None
        """
        for _ in range(n_to_add):
            self._arrival_queue.append(Container(arrival_time=self._timer))

        self._total_containers_passed += n_to_add

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

    def _load_containers(self) -> int:
        """
        Loads _containers into an airplane
        @return: number of loaded _containers
        """
        if self.CONTAINERS_LOAD_PER_INTERVAL == -1:
            containers_to_load = list(self._arrival_queue)

        else:
            if self._timer != 0:
                containers_to_load = list(self._arrival_queue)[:self.CONTAINERS_LOAD_PER_INTERVAL]
            else:
                containers_to_load = []

        for container in containers_to_load:
            self._arrival_queue.popleft()
            self._loading_airplane.load(container)
        return len(containers_to_load)

    def _put_container_into_history(self):
        """
        Puts loaded _containers into the statistics class
        @return:
        """
        pass

    def _show_current_state(self):
        """
        Shows current model state
        Returns: None
        """
        print(f'\nTimer: {self._timer}')
        print(f'Total containers arrived: {self._total_containers_passed}')
        print(f'Number of containers in queue: {len(self._arrival_queue)}')
        print(f'Number of present airplanes: {len(self._present_airplanes)}')
        print(f'Loading airplane ID: {self._loading_airplane.airplane_id}')
        print(f'Current airplane load: {self._loading_airplane.current_load}')





