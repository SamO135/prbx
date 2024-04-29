# a singleton to store statistics from the simulations
class Stats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        if not hasattr(self, "algs"):
            self.algs = kwargs.get("algs")
        if not hasattr(self, 'rollouts'):
            self.rollouts = {self.algs[0]: 0, self.algs[1]: 0}

    def reset_stats(self):
        for attr in vars(self):
            if attr == "rollouts":
                setattr(self, attr, {self.algs[0]: 0, self.algs[1]: 0})
