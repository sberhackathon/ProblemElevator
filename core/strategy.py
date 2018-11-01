#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.base_strategy import BaseStrategy
from math import fabs
import operator

# class Strategy(BaseStrategy):
#     def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
#         for elevator in my_elevators:
#             passengers = [p for p in my_passengers if p.state < 5]
#             for p in passengers:
#                 if elevator.state != 1:
#                     elevator.go_to_floor(p.from_floor)
#                 if elevator.floor == p.from_floor:
#                     p.set_elevator(elevator)
#             if len(elevator.passengers) > 0 and elevator.state != 1:
#                 elevator.go_to_floor(elevator.passengers[0].dest_floor)


class Strategy(BaseStrategy):

    def nearest_floor_with_pass(self, passengers, floor):

        near = passengers[0].dest_floor

        for p in passengers:
            if fabs(floor - p.dest_floor) < near:
                near = p.dest_floor

        rating = {}

        for p in passengers:
            if p.dest_floor in rating.keys():
                rating[p.dest_floor] = rating[p.dest_floor] + fabs(floor - p.dest_floor) * 10
            else:
                rating[p.dest_floor] = fabs(floor - p.dest_floor) * 10

        # функция берет ключ с максимальным значением (самый вкусный пункт назначения)
        dest = max(rating.items(), key=operator.itemgetter(1))[0]
        # если ближайший по пути к самому вкусному, останавливаемся
        if (dest < near < floor or
                dest > near > floor):
            return near
        else:
            return dest

    # если на этаже нет людей, едем на этаж где они есть
    def nearest_floor_without_pass(self, passengers, floor, not_interested):
        near = 100
        for p in passengers:
            if fabs(floor - p.dest_floor) < near and not p.dest_floor in not_interested:
                near = p.dest_floor

        return near

    def get_floors_to_go(self, elevator):
        return list(set([p for p in elevator.passengers]))


    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        # список этажей, на которые уже едут лифты за пассажирами
        getting_passengers = set()
        for elevator in my_elevators:
            if elevator.state == 1:
                getting_passengers.add(elevator.next_floor)

        for passenger in my_passengers:
            pass_elevators = [elevator for elevator in my_elevators
                              if elevator.floor == passenger.floor and elevator.state == 3]

            elevators_rating = {}

            for e in pass_elevators:
                floors_to_go = self.get_floors_to_go(e)
                elevators_rating[e] = len(floors_to_go)

                if passenger.dest_floor in floors_to_go and not passenger.has_elevator():
                    passenger.set_elevator(e)

            if not passenger.has_elevator() and len(pass_elevators) > 0:
                for k, v in elevators_rating.items():
                    if v < 3:# and fabs(k.next_floor - passenger.dest_floor) < 3:
                        passenger.set_elevator(k)

        for elevator in my_elevators:
            no_passengers_on_floor = True
            for passenger in my_passengers:
                if passenger.floor == elevator.floor:
                    no_passengers_on_floor = False

                # if (passenger.floor == elevator.floor and
                #         elevator.state == 3 and
                #         not passenger.has_elevator()):
                #     passenger.set_elevator(elevator)

            if elevator.state == 3:
                if (len(elevator.passengers) > 0 and
                        (elevator.time_on_floor > 1000 or no_passengers_on_floor) or
                        len(elevator.passengers) > 9):
                    go_to = self.nearest_floor_with_pass(elevator.passengers, elevator.floor)
                    print(elevator.id, 'on', elevator.floor, 'go to ', go_to)
                    elevator.go_to_floor(go_to)

                if len(elevator.passengers) == 0 and no_passengers_on_floor:
                    res = []
                    for p in my_passengers:
                        if not p.has_elevator() and p.state == 1:
                            res.append(p)
                    go_to = self.nearest_floor_without_pass(res, elevator.floor, getting_passengers)
                    print(elevator.id, 'no passengers on floor', elevator.floor, 'go to ', go_to)
                    elevator.go_to_floor(go_to)

            # if elevator.state == 1:
            #     if elevator.floor > elevator.next_floor:
            #         direction = "down"
            #     elif elevator.floor == elevator.next_floor:
            #         direction = "on_floor"
            #     else:
            #         direction = "up"
            #
            #     if len(elevator.passengers) < 5 and not no_passengers_on_floor:
            #         res = []
