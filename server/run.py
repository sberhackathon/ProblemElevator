# coding=utf-8
import argparse
import json
import os
from datetime import datetime, timedelta

import tornado.gen
import tornado.gen
import tornado.ioloop
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from server.core import settings
from server.core.api import API


class Client(object):
    max_client_time = int(os.environ.get('MAX_CLIENT_TIME', 120))

    def __init__(self, stream):
        self.solution_id = None
        self.stream = stream
        self.total_time = 0
        self.is_close = False

    def set_solution_id(self, solution_id):
        self.solution_id = solution_id

    def send(self, message):
        self.stream.write(self.dump_message(message))

    def close(self):
        self.is_close = True
        self.stream.close()

    @staticmethod
    def dump_message(message):
        message = '{}\n'.format(json.dumps(message, separators=(',', ':')).encode('string-escape'))
        return message

    @tornado.gen.coroutine
    def read_messages(self):
        message = []
        try:
            before_read_time = datetime.now()
            message = yield tornado.gen.with_timeout(timedelta(seconds=10), self.stream.read_until('\n'))
            tick_time = datetime.now() - before_read_time
            message = message.strip()
            try:
                message = json.loads(message, strict=False)
            except ValueError as e:
                message = [{
                    'command': 'fatal_error',
                    'args': {
                        'text': u'Ошибка парсинга ответов'
                    }
                }]
                raise ValueError(e)
            self.total_time += tick_time.total_seconds()
        except tornado.gen.TimeoutError:
            self.is_close = True
            message.append({
                'command': 'fatal_error',
                'args': {
                    'text': u'Время выполнения одного тика превышено'
                }
            })
        except StreamClosedError:
            self.is_close = True
            message.append({
                'command': 'fatal_error',
                'args': {
                    'text': u'Стратегия аварийно завершила работу'
                }
            })

        if self.total_time > self.max_client_time:
            self.close()

            message.append({
                'command': 'fatal_error',
                'args': {
                    'text': u'Время выполнения стратегии первышено'
                }
            })
        raise tornado.gen.Return(message)


class WorldHandler(object):
    api = API()
    red_client = None
    blue_client = None
    ticks_count = int(os.environ.get('TICKS_COUNT', 7200))
    disable_log_flag = True
    result = []

    client_player = {}

    def __init__(self, disable_log_flag):
        self.disable_log_flag = disable_log_flag

    @tornado.gen.coroutine
    def connect(self, stream, address):
        current_client = Client(stream)
        try:
            messages = yield current_client.read_messages()
            solution_id = int(messages.get('solution_id'))
        except (ValueError, TypeError):
            solution_id = None
        except StreamClosedError:
            solution_id = None
        current_client.set_solution_id(solution_id)

        if self.red_client is None:
            self.red_client = current_client
        elif self.blue_client is None:
            self.blue_client = current_client
            self.start()
        else:
            pass

    def shutdown(self):
        if not self.blue_client.is_close:
            self.blue_client.send({'message': 'down'})
            self.blue_client.close()

        if not self.red_client.is_close:
            self.red_client.send({'message': 'down'})
            self.red_client.close()

        tornado.ioloop.IOLoop.instance().stop()

    @staticmethod
    def write_result(data):
        f = open('{}/../visualizer/game.js'.format(os.path.dirname(os.path.realpath(__file__))), 'w')
        f.write("var data = ")
        f.write(json.dumps(data, indent=4))
        f.write(";")
        f.close()

    @staticmethod
    def write_score(data):
        f = open('{}/../visualizer/score.json'.format(os.path.dirname(os.path.realpath(__file__))), 'w')
        f.write(json.dumps(data, indent=4))
        f.close()

    @tornado.gen.coroutine
    def start(self):
        self.api.create_players(self.red_client, self.blue_client)
        self.red_client.send({'message': 'beginning', 'color': 'FIRST_PLAYER'})
        self.blue_client.send({'message': 'beginning', 'color': 'SECOND_PLAYER'})

        for _ in range(0, self.ticks_count):
            blue_message = []
            if not self.blue_client.is_close:
                self.blue_client.send(self.api.get_world_state_for(self.blue_client))
                blue_message = yield self.blue_client.read_messages()

            red_message = []
            if not self.red_client.is_close:
                self.red_client.send(self.api.get_world_state_for(self.red_client))
                red_message = yield self.red_client.read_messages()

            self.api.apply_commands(blue_message, self.blue_client)
            self.api.apply_commands(red_message, self.red_client)
            self.api.tick()
            self.result.append(self.api.get_visio_state())

        try:
            if self.disable_log_flag == "N":
                self.write_result({
                    'config': settings.BUILDING_VISIO,
                    'game_data': self.result,
                    'players': {
                        "FIRST_PLAYER": self.red_client.solution_id,
                        "SECOND_PLAYER": self.blue_client.solution_id,
                    }
                })
            score_result = {
                'result': self.api.get_score_state()
            }
            self.write_score(score_result)
            print(score_result)
        except Exception as e:
            print(e)

        self.shutdown()


class Server(TCPServer):
    def __init__(self, save_vision_log_flag):
        self.world_handler = WorldHandler(save_vision_log_flag)
        super(Server, self).__init__()

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        self.world_handler.connect(stream, address)


parser = argparse.ArgumentParser(description='Run server Hackathon 2018.')
parser.add_argument('-disable_log_flag', help='saving vision log file')
parser.set_defaults(disable_log_flag="N")
args = parser.parse_args()

server = Server(args.disable_log_flag).listen(8000)
tornado.ioloop.IOLoop.instance().start()
