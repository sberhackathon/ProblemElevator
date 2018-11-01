from math import fabs
from random import randint
from typing import List
from core.api import Elevator, Passenger
from core.base_strategy import BaseStrategy

FLOOR_COUNTS = 15
MAX_FLOOR = 15
MIN_FLOOR = 1
ELEVATOR_COUNTS = 7
ELEVATOR_MAX_PASSENGERS_COUNT = 20
ELEVATOR_STATES = {0: 'waiting', 1: 'moving', 2: 'opening', 3: 'filling', 4: 'closing'}
# filling => closing => waiting => moving => opening => filling

PASSENGER_STATES = {1: 'waiting_for_elevator', 2: 'moving_to_elevator', 3: 'returning',
                    4: 'moving_to_floor', 5: 'using_elevator', 6: 'exiting'}


def passenger_state(passenger: Passenger):
    return PASSENGER_STATES.get(passenger.state)


def passenger_waiting(passenger: Passenger):
    return passenger_state(passenger) == 'waiting_for_elevator' \
           or passenger_state(passenger) == 'returning' \
           or passenger_state(passenger) == 'moving_to_floor'


def passenger_current_floor(passenger: Passenger):
    return passenger.floor


def passenger_dest_floor(passenger: Passenger):
    return passenger.dest_floor


def elevator_state(elevator: Elevator):
    return ELEVATOR_STATES.get(elevator.state)


def elevator_filling(elevator: Elevator):
    return elevator_state(elevator) == 'filling'


def elevator_closing(elevator: Elevator):
    return elevator_state(elevator) == 'closing'


def elevator_waiting(elevator: Elevator):
    return elevator_state(elevator) == 'waiting'


def elevator_moving(elevator: Elevator):
    return elevator_state(elevator) == 'moving'


def elevator_moving_up(elevator: Elevator):
    return elevator_state(elevator) == 'moving' \
           and elevator.next_floor > elevator.floor


def elevator_moving_down(elevator: Elevator):
    return elevator_state(elevator) == 'moving' \
           and elevator.next_floor < elevator.floor


def elevator_opening(elevator: Elevator):
    return elevator_state(elevator) == 'opening'


def elevator_current_floor(elevator: Elevator):
    return elevator.floor


def elevator_dest_floor(elevator: Elevator):
    return elevator.next_floor


def elevator_empty(elevator: Elevator):
    return len(elevator.passengers) == 0


def elevator_passengers_count(elevator: Elevator):
    return len(elevator.passengers)


def elevator_passengers_dest(elevator: Elevator):
    return {passenger.id: passenger.dest_floor for passenger in elevator.passengers}


def elevator_load_factor(elevator: Elevator):
    return elevator_passengers_count(elevator) / ELEVATOR_MAX_PASSENGERS_COUNT


def elevator_type(elevator: Elevator):
    return elevator.type


def elevator_id(elevator: Elevator):
    return elevator.id


def elevator_going_empty(elevator: Elevator):
    if elevator_id(elevator) > FLOOR_COUNTS / 2:
        return randint(int(FLOOR_COUNTS / 2), MAX_FLOOR)
    return randint(MIN_FLOOR, int(FLOOR_COUNTS / 2))


def elevator_going_floor(elevator: Elevator):
    dest_floors = list(set([passenger.dest_floor for passenger in elevator.passengers]))
    dest_floors_sorted = sorted(dest_floors, key=lambda x: fabs(x - elevator.floor))
    return dest_floors_sorted[0]


# def floor_exsisting_passenger(passengers: List[Passenger], floor: int):
#     for passenger in passengers:
#         if passenger_current_floor(passenger) == floor:
#             return True
#     return False


def file_log(elevator: Elevator):
    file_path = 'C:\\Users\\olyae\\PycharmProjects\\ProblemElevator\\clients\\core\\'
    file_name = str(elevator_type(elevator)) + '.txt'
    with open(file=file_path + file_name, mode='a', encoding='utf-8') as file:
        file.write('------------------------------\n')
        file.write('type: {}\n'.format(elevator_type(elevator)))
        file.write('id: {}\n'.format(elevator_id(elevator)))
        file.write('state: {}\n'.format(elevator_state(elevator)))
        file.write('elevator empty ?: {}\n'.format(elevator_empty(elevator)))
        file.write('elevator passengers count: {}\n'.format(elevator_passengers_count(elevator)))
        file.write('elevator passengers: {}\n'.format(elevator_passengers_dest(elevator)))
        file.write('elevator moving ?: {}\n'.format(elevator_moving(elevator)))
        file.write('moving UP ?: {}\n'.format(elevator_moving_up(elevator)))
        file.write('moving DOWN ?: {}\n'.format(elevator_moving_down(elevator)))
        file.write('load factor: {}\n'.format(elevator_load_factor(elevator)))
        file.write('floor: {}\n'.format(elevator_current_floor(elevator)))
        file.write('next_floor: {}\n'.format(elevator_dest_floor(elevator)))


class DesjoerdStrategy(BaseStrategy):
    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        for elevator in my_elevators:
            if elevator_id(elevator) == 1:
                file_log(elevator)

        for elevator in my_elevators:
            if elevator_filling(elevator):
                # наполняем лифт людьми до тех пор, пока не будет достаточно по их общему маршруту(Очки)
                # if not floor_exsisting_passenger([p for p in my_passengers if passenger_waiting(p)],
                #                                  elevator_current_floor(elevator)):
                #     elevator.go_to_floor(elevator_going_floor(elevator))
                if elevator_load_factor(elevator) > 0.5 or len(list(filter(lambda x: passenger_current_floor(x) == elevator_current_floor(elevator), my_passengers))) == 0:
                    elevator.go_to_floor(elevator_going_floor(elevator))
            elif elevator_closing(elevator):
                # закрываем лифт, новых людей в него не пускаем
                if elevator_empty(elevator):
                    elevator.go_to_floor(elevator_going_empty(elevator))
                else:
                    elevator.go_to_floor(elevator_going_floor(elevator))
            elif elevator_waiting(elevator):
                # считаем маршрут следующий этаж или все этажи маршрута(Очки)
                if elevator_empty(elevator):
                    elevator.go_to_floor(elevator_going_empty(elevator))
                else:
                    elevator.go_to_floor(elevator_going_floor(elevator))
            elif elevator_moving(elevator):
                if elevator_moving_up(elevator):
                    # забираем в лифт людей, которые ему по пути и если в лифте есть место для них(Очки)
                    pass
                elif elevator_moving_down(elevator):
                    # забираем в лифт людей, которые ему по пути и если в лифте есть место для них(Очки)
                    pass
            elif elevator_opening(elevator):
                # выгружаем людей, убеждаемся, что все люди с этим этажем на нем вышли
                if elevator_empty(elevator):
                    elevator.go_to_floor(elevator_going_empty(elevator))
                else:
                    elevator.go_to_floor(elevator_going_floor(elevator))

            for passenger in [p for p in my_passengers if passenger_waiting(p)]:
                if elevator_empty(elevator) and (elevator_waiting(elevator) or elevator_moving(elevator)):
                    elevator.go_to_floor(passenger_current_floor(passenger))
                if elevator_current_floor(elevator) == passenger_current_floor(passenger):
                    passenger.set_elevator(elevator)
