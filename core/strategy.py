from core.base_strategy import BaseStrategy


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


# {
#     init: function(elevators, floors) {
#         // first, wait ten seconds for the queues to fill up on each floor
#         setTimeout(function(){
#             // use only the first elevator
#             var e = elevators[0];
#
#             // ...and open up its doors on the ground floor
#             e.goToFloor(0);
#
#             var direction = 1;
#             e.on('idle', function(){
#                 // are we on the top floor? go down
#                 if(e.currentFloor() >= floors.length - 1) direction = -1;
#
#                 // are we on the ground floor? go up next time
#                 if(e.currentFloor() <= 0) direction = 1;
#
#                 // go to the next floor!
#                 e.goToFloor(e.currentFloor() + direction);
#             });
#         }, 10000);
#     },
#     update: function(dt, elevators, floors) {}
# }
# class n_elevator_moves_or_less(BaseStrategy):
class Strategy(BaseStrategy):
    max_floor = 16
    elevators_direction = {}

    def fdirection(from_floor, dest_floor):
        if from_floor > dest_floor:
            return -1
        else:
            return 1

    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        # init direction map
        if not Strategy.elevators_direction:
            for e in range(0, len(my_elevators)):
                Strategy.elevators_direction[e] = 0
        else:
            for d in range(0, len(Strategy.elevators_direction)):

                elevator = my_elevators[d]

                if elevator.floor == Strategy.max_floor:
                    Strategy.elevators_direction[d] = -1
                elif elevator.floor == 1:
                    Strategy.elevators_direction[d] = 1

                elevator.go_to_floor(elevator.floor + Strategy.elevators_direction[d])

                passengers = [p for p in my_passengers if p.state < 5 and p.from_floor == elevator.floor
                              and Strategy.fdirection(p.from_floor, p.dest_floor) == Strategy.elevators_direction[d]
                              and elevator.state != 1]

                for p in passengers:
                    p.set_elevator(elevator)
