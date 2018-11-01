from core.base_strategy import BaseStrategy
from math import fabs


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

    def nearest_floor_with(self, passengers, floor):
        near = 100
        for p in passengers:
            if fabs(floor - p.dest_floor) < near:
                near = p.dest_floor

        return near
        # near = passengers[0].dest_floor
        #
        # rating = {}
        # for p in passengers:
        #     if p.dest_floor in rating.keys:
        #         rating[p.dest_floor] = rating[p.dest_floor] + 1
        #
        #     if fabs(floor - p.dest_floor) < near:
        #         near = p.dest_floor
        #
        # key, value = rating.pop
        # for k, v in rating:
        #     if v > value: key = k
        #
        # if (near > key and near < floor or
        #         near < key and near > floor):
        #     return near
        # else:
        #     return key

    def nearest_floor_without(self, passengers, floor, not_interested):
        near = 100
        for p in passengers:
            if fabs(floor - p.dest_floor) < near and not p.dest_floor in not_interested:
                near = p.dest_floor

        return near

    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        getting_passengers = set()

        for elevator in my_elevators:
            no_passengers_on_floor = True
            for passenger in my_passengers:
                if passenger.floor == elevator.floor:
                    no_passengers_on_floor = False
                if (passenger.floor == elevator.floor and
                        elevator.state == 3 and
                        not passenger.has_elevator()):
                    passenger.set_elevator(elevator)

            if elevator.state == 1:
                getting_passengers.add(elevator.next_floor)

            if elevator.state == 3:
                if (len(elevator.passengers) > 0 and
                        (elevator.time_on_floor > 500 or no_passengers_on_floor) or
                        len(elevator.passengers) > 9):
                    elevator.go_to_floor(self.nearest_floor_with(elevator.passengers, elevator.floor))

                if len(elevator.passengers) == 0 and no_passengers_on_floor:
                    res = []
                    for p in my_passengers:
                        if not p.has_elevator() and p.state == 1:
                            res.append(p)
                    go_to = self.nearest_floor_without(res, elevator.floor, getting_passengers)
                    print('no passengers on floor, go to ', go_to)
                    elevator.go_to_floor(go_to)

            if elevator.state == 1:
                if elevator.floor > elevator.next_floor:
                    direction = "down"
                elif elevator.floor == elevator.next_floor:
                    direction = "on_floor"
                else:
                    direction = "up"

                if len(elevator.passengers) < 5 and not no_passengers_on_floor:
                    res = []

# class Strategy(BaseStrategy):
#     max_floor = 16
#
#     def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
#          for elevator in my_elevators:
#             if elevator.id % 2 == 0:
#                 d = elevator.id
#             else: d = elevator.id - 1
#
#             print(d)
#
#             if elevator.floor == 1:
#                 going_to = (d + 1) * 2
#             elif elevator.floor == (d + 1) * 2:
#                 going_to = (d + 1) * 2 + 1
#             else:
#                 going_to = 1
#
#             #print(elevator.id, going_to)
#             if elevator.state == 3 and len(elevator.passengers) > 2 or elevator.time_on_floor > 2000:
#                 #   print('elevator ', d, ' going to ', going_to)
#                 elevator.go_to_floor(going_to)
#
#             passengers = [p for p in my_passengers if p.state < 5]
#             for p in passengers:
#                 if p.floor == 1:
#                     #      print('pass going', p.dest_floor, 'elevator', p.dest_floor / 2 - 1)
#                     p.set_elevator(p.dest_floor / 2 - 1)
#                 elif p.dest_floor == 1:
#                     p.set_elevator(p.from_floor / 2 - 1)
