from collections import deque
from typing import List, NoReturn, Union, MutableMapping

from numpy.random import normal, seed

from sim_model.models import Container, Airplane, ModelStats, AirplaneWaitTime


class Simulation:
    CONTAINERS_LOAD_PER_INTERVAL: int = 1
    AIRPLANES_CAPACITIES: MutableMapping = {80: 3, 140: 2}
    MEAN_TIME = 180
    SCALE = 60

    @property
    def queue_current_len(self) -> int:
        return len(self._arrival_queue)

    @property
    def loading_airplane(self) -> Airplane:
        return self._loading_airplane

    def __init__(self, seed_value: int = -1, show_stats: bool = True, arrival_quantity: int = 2):
        self.CONTAINERS_ARRIVAL_PER_INTERVAL: int = arrival_quantity
        self._timer: int = 1
        self._total_containers_passed = 0
        self._arrival_queue: deque = deque()
        self._loading_airplane: Union[Airplane, None] = None
        self._present_airplanes: List = Airplane.get_list_of_airplanes(self.AIRPLANES_CAPACITIES)
        self._flown_away_airplanes: List = []
        self._stats = ModelStats()
        self._model_used: bool = False
        self._flown_flag: bool = False
        self.seed_value = seed_value
        self.show_stats = show_stats
        if self.seed_value > 0:
            seed(seed_value)

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

            self._check_arrival()

            if self._loading_airplane is None:
                self._choose_airplane_for_load()

            if self._loading_airplane is None:  # better to write is still None
                self._timer += 1
                self._show_current_state()
                continue

            try:
                self._load_containers()
            except Exception as ex:
                pass

            if self._loading_airplane.is_full_loaded:
                if self.show_stats:
                    self._show_airplane_info(self._depart_airplane())
                else:
                    self._depart_airplane()

            self._show_current_state()

            self._timer += 1

        self._model_used = True

        return self._stats

    def _add_containers(self, n_to_add: int) -> NoReturn:
        """
        Put _containers into the _arrival_queue
        @return: None
        """
        for _ in range(n_to_add):
            self._arrival_queue.append(Container(arrival_time=self._timer))

        self._total_containers_passed += n_to_add

    def _check_arrival(self) -> NoReturn:
        """
        Check and process airplane arrival
        Returns:
        """
        if len(self._flown_away_airplanes) > 0:
            for airplane in self._flown_away_airplanes:
                if airplane.arrival_time == self._timer:
                    self._make_arrival(airplane)

    def _choose_airplane_for_load(self) -> NoReturn:
        """
        Chooses the airplane for load using pre-defined rules
        @return: None
        """
        if len(self._present_airplanes) > 0:
            lowest_capacity = min([airplane.capacity for airplane in self._present_airplanes])
            self._loading_airplane = list(filter(lambda x: x.capacity == lowest_capacity, self._present_airplanes))[0]

    def _depart_airplane(self) -> Airplane:
        """
        Makes all the work with an airplane departure
        @return: None
        """
        self._loading_airplane.set_containers_departure_time(self._timer)
        self._loading_airplane.departure_time = self._timer

        self._stats.put_containers_loading_time(self._loading_airplane.containers_loading_times)
        self._stats.put_containers_departure_time(self._loading_airplane.containers_departure_times)
        self._stats.put_airplane_time(AirplaneWaitTime(airplane_capacity=self._loading_airplane.capacity,
                                                       wait_time=self._loading_airplane.load_time))

        self._loading_airplane.arrival_time = self._timer + self._generate_flight_time()

        departed_airplane = self._present_airplanes.pop(self._present_airplanes.index(self._loading_airplane))
        self._flown_away_airplanes.append(departed_airplane)

        self._loading_airplane, self._flown_flag = None, True

        return departed_airplane

    def _generate_flight_time(self) -> int:
        """
        Generates an airplane's flight time using pre-defined rules
        @return: None
        """
        while True:
            if self.MEAN_TIME - self.SCALE <= (
                    value := normal(self.MEAN_TIME, self.SCALE)) <= self.MEAN_TIME + self.SCALE:
                return int(value)

    def _load_containers(self) -> int:
        """
        Loads _containers into an airplane
        @return: number of loaded _containers
        """
        if self.CONTAINERS_LOAD_PER_INTERVAL == -1:
            containers_to_load = list(self._arrival_queue)[:self._loading_airplane.capacity]
        else:
            if self._timer != 0:
                containers_to_load = list(self._arrival_queue)[:self.CONTAINERS_LOAD_PER_INTERVAL]
            else:
                containers_to_load = []

        for container in containers_to_load:
            container.set_loading_time(self._timer)
            self._arrival_queue.popleft()
            if self._loading_airplane.is_full_loaded:
                pass
            self._loading_airplane.load(container)
        return len(containers_to_load)

    def _make_arrival(self, airplane: Airplane) -> NoReturn:
        airplane.departure_time = -1
        airplane.unload()
        self._present_airplanes.append(airplane)
        self._flown_away_airplanes.pop(self._flown_away_airplanes.index(airplane))

    @staticmethod
    def _show_airplane_info(airplane: Airplane) -> NoReturn:
        print('\n=== AIRPLANE DEPARTURE INFO ===')
        print(f'Airplane ID: {airplane.airplane_id}')
        print(f'Number of containers: {airplane.current_load}')
        print(f'Departure moment: {airplane.departure_time}')
        print(f'Arrival moment: {airplane.arrival_time}')

    def _show_current_state(self) -> NoReturn:
        """
        Shows current model state
        Returns: None
        """
        if self.show_stats:
            print(f'\nTimer: {self._timer}')
            print(f'Total containers arrived: {self._total_containers_passed}')
            print(f'Number of containers in queue: {len(self._arrival_queue)}')
            print(f'Number of present airplanes: {len(self._present_airplanes)}')
            if self._loading_airplane:
                print(f'Loading airplane ID: {self._loading_airplane.airplane_id}'
                      f' (capacity: {self._loading_airplane.capacity})')
                print(f'Current airplane load: {self._loading_airplane.current_load}')
            else:
                if self._flown_flag:
                    print('Airplane has just departed')
                    self._flown_flag = False
                else:
                    print('There are no available airplanes')




