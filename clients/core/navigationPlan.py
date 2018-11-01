# import core.utils as uti
# from typing import List
# import time
# import math
#
#
# class Request:
#     def __init__(self, dest_floor, start_time):
#         self.dest_floor = dest_floor
#         self.start_time = start_time
#
#
# class Node:
#     def __init__(self, floor, requests: List[Request], estimated_load, estimated_time, parent, cost):
#         self.floor = floor
#         self.requests = requests
#         self.estimated_load = estimated_load
#         self.estimated_time = estimated_time
#         self.parent = parent
#         self.cost = cost
#
#
# class Plan:
#     def __init__(self, path, cost):
#         self.path = path
#         self.cost = cost
#
#
# class NavigationPlan:
#     def __init__(self, current_floor, current_load, all_requests):
#         self.current_floor = current_floor
#         self.current_load = current_load
#         self.all_requests = all_requests
#         self.root = Node(
#                 floor=current_floor,
#                 requests=all_requests,
#                 estimated_load=current_load,
#                 estimated_time=time.strftime("%c"),
#                 parent=None,
#                 cost=0
#                 )
#
#
#     min_leaf: Node = None
#
#     def step_layer(self, current: Node):
#         requests = current.requests
#
#         if len(requests) == 0:
#             if self.min_leaf is None:
#                 self.min_leaf = current
#             elif current.cost < self.min_leaf.cost:
#                 self.min_leaf = current
#
#         for i, request in enumerate(requests):
#
#             path_time = uti.estimated_travel_time(self.current_floor, request.dest_floor)
#             max_wait_time = uti.max_client_wait_time(current.estimated_time, requests)
#
#             delta_cost = path_time + math.pow(max_wait_time / 4.0, 2) # TODO откуда эти константы
#
#             delta_load = 0
#
#             if (request.floorRequest) {
#                 deltaLoad -= 0.3;
#             } else if (request.callRequest) {
#                 deltaLoad += 0.25;
#             }
#
#             next_load = current.estimated_load + delta_load
#
#             if next_load > 1:
#                 next_load = 1
#             elif next_load < 0:
#                 next_load = 0
#
#             delta_cost += 5 * (next_load - 0.5) * (next_load * 0.5) # TODO Почему 0.5
#
#             other_requests = requests  # .slice() Создает копию объекта
#             other_requests.pop(i)  # .splice(i, 1) Вообще хз то ли оно делает или нет
#
#             node = Node(
#                 floor=request.dest_floor,
#                 requests=other_requests,
#                 estimated_load=current.estimated_load + delta_load,
#                 estimated_time=current.estimated_time + path_time * 1000.0,  # TODO Да схуя ли на 1000
#                 parent=current,
#                 cost=0
#                 )
#
#             self.step_layer(node)
#
#     def do_stuff_that_should_function_do(self) -> Plan:
#         self.step_layer(self.root)
#
#         if self.min_leaf is None:
#             return Plan(path=[], cost=9999999)
#
#         path = []
#         cost = self.min_leaf.cost
#
#         while self.min_leaf is not None:
#             path.append(self.min_leaf.floor)
#             self.min_leaf = self.min_leaf.parent
#
#         path.reverse()
#         if path[0] == self.current_floor:
#             path = path[0:1] # path.splice(0,1);
#
#         return Plan(path=path, cost=cost)
