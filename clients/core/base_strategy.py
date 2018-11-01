class BaseStrategy(object):
    debug = None

    def set_debug(self, debug):
        self.debug = debug.log

    def on_tick(self,  my_elevators, my_passengers, enemy_elevators, enemy_passengers):
        pass
