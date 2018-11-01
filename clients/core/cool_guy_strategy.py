# from core.base_strategy import BaseStrategy
# import time
# from typing import List
# from server.core.game_objects.elevator import Elevator
# from server.core.game_objects.passenger import Passenger
#
# from core.navigationPlan import NavigationPlan, Plan, Request
#
# class GlobalSchedulerStrategy(BaseStrategy):
#     def on_tick(self, my_elevators: List[Elevator], my_passengers: List[Passenger], enemy_elevators: List[Elevator], enemy_passengers: List[Passenger]) -> None:
#         for i, my_elevator in enumerate(my_elevators):
#
#             my_elevator._id: int = i
#
#             my_elevator.deferred_plans = None
#             my_elevator.requests: List[Request] = []  # Все запросы без дублей и вызовов на тот же этаж
#
#             for my_passenger in my_passengers:
#                 my_elevator.requests.append(Request(my_passenger.dest_floor, time.strftime("%c")))
#                 my_elevator.requests = set(my_elevator.requests)
#                 my_elevator.requests = list(my_elevator.requests).remove(my_elevator.current_floor)
#
#
#             def prioritize():
#                 requests = my_elevator.requests
#                 plan: Plan = NavigationPlan(my_elevator.current_floor(), my_elevator.loadFactor, requests).do_stuff_that_should_function_do
#                 my_elevator.deferred_plans = plan.path
#
#             my_elevator.prioritize = prioritize
#
#             if my_elevator.idle: # такого метода нет
#                 my_elevator.prioritize()
#                 my_elevator.go_to_floor(my_elevator.current_floor())
#
#
#             if len(my_elevator.requests) > 0: # Такого метода нет
#
#                 pass
#
#             if my_elevator.is_moving:
#                 my_elevator.prioritize()
#
#             if my_elevator.on_the_floor: # Такого метода нет
#                 pass
