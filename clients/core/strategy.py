from core.base_strategy import BaseStrategy


class Strategy(BaseStrategy):
    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        for elevator in my_elevators:
            needed_floors = set()
            passengers = [p for p in my_passengers if p.state < 5]

            passengers_on_el_floor = [p for p in passengers if p.floor == elevator.current_floor()]

            print('passengers: ' + str(len(passengers_on_el_floor)))

            while len(passengers_on_el_floor) > 0 and len(elevator.passengers) < 10:
                for passenger_on_el_floor in passengers_on_el_floor:
                    passenger_on_el_floor.set_elevator(elevator)
                    if passenger_on_el_floor.state == 'using_elevator':
                        needed_floors.add(passenger_on_el_floor.dest_floor)
                        passengers_on_el_floor.remove(passenger_on_el_floor)

            min_floor = 100
            for floor in needed_floors:
                if abs(elevator.current_floor() - floor) < min_floor:
                    min_floor = floor

            elevator.go_to_floor(min_floor)
