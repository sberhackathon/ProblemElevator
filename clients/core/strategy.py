from math import fabs
import operator
from core.base_strategy import BaseStrategy


class Strategy(BaseStrategy):

    def nearest_floor_with_pass(self, passengers, floor):

        near = 15

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
        if len(rating) > 0:
            dest = max(rating.items(), key=operator.itemgetter(1))[0]
        else:
            dest = near
        # если ближайший по пути к самому вкусному, останавливаемся
        if (dest <= near <= floor or
                dest >= near >= floor):
            return near
        else:
            return dest

    #если на этаже нет людей, едем на этаж где они есть
    def nearest_floor_without_pass(self, passengers, floor, not_interested):
        near = 15
        for p in passengers:
            if fabs(floor - p.dest_floor) < near and p.dest_floor not in not_interested:
                near = p.dest_floor
        return near

    # def nearest_floor_without_pass(self, passengers, floor, not_interested):
    #     floor_value = {}
    #     for p in passengers:
    #         if p.dest_floor in floor_value.keys() and p.dest_floor not in not_interested:
    #             floor_value[p.dest_floor] = floor_value[p.dest_floor] + fabs(floor - p.dest_floor) * 10
    #         elif p.dest_floor not in not_interested:
    #             floor_value[p.dest_floor] = fabs(floor - p.dest_floor) * 10
    #
    #     if len(floor_value) > 0:
    #         dest = max(floor_value.items(), key=operator.itemgetter(1))[0]
    #     else:
    #         dest = near
    #
    #     dest = max(floor_value.items(), key=operator.itemgetter(1))[0]
    #     return dest
    def get_floors_to_go(self, elevator):
        return list(set([p.dest_floor for p in elevator.passengers]))

    def distance_from_floor_to_mass_floors(self, floors, floor):
        if len(floors) == 0:
            return 0
        return sum([fabs(f - floor) for f in floors]) / len(floors)

    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        my_passengers = my_passengers + enemy_passengers
        # список этажей, на которые уже едут лифты за пассажирами
        next_floor_set = set()
        for elevator in my_elevators:
            if elevator.state == 1:
                next_floor_set.add(elevator.next_floor)

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
                    distance = self.distance_from_floor_to_mass_floors(self.get_floors_to_go(k), passenger.dest_floor)
                    if v < 4 and distance < 4 or len(pass_elevators) == 1:
                        passenger.set_elevator(k)

        for elevator in my_elevators:
            no_passengers_on_floor = True

            for passenger in my_passengers:
                if passenger.floor == elevator.floor and passenger.state in [1, 2, 3]:
                    no_passengers_on_floor = False

            if elevator.state == 3:
                if no_passengers_on_floor or len(elevator.passengers) > 19:
                    go_to = self.nearest_floor_with_pass(elevator.passengers, elevator.floor)
                    elevator.go_to_floor(go_to)

                if len(elevator.passengers) == 0 and no_passengers_on_floor:
                    res = []
                    for p in my_passengers:
                        if not p.has_elevator() and p.state == 1:
                            res.append(p)
                    go_to = self.nearest_floor_without_pass(res, elevator.floor, next_floor_set)
                    elevator.go_to_floor(go_to)

            if elevator.state in [1] and len(elevator.passengers) == 0:
                res = []
                for p in my_passengers:
                    if not p.has_elevator() and p.state == 1:
                        res.append(p)
                go_to = self.nearest_floor_without_pass(res, elevator.floor, next_floor_set)
                elevator.go_to_floor(go_to)

            if elevator.state in [1] and 0 < len(elevator.passengers) < 10:
                res = []
                for p in my_passengers:
                    if not p.has_elevator() and p.state == 1:
                        res.append(p)
                go_to = self.nearest_floor_without_pass(res, elevator.floor, next_floor_set)
                if (elevator.next_floor < go_to < elevator.floor or
                        elevator.next_floor > go_to > elevator.floor):
                    elevator.go_to_floor(go_to)


