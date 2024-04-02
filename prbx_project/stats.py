# a singleton to store statistics from the simulations
class Stats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'rollouts'):
            self.rollouts = 0

    def reset_stats(self):
        for attr in vars(self):
            setattr(self, attr, 0)
