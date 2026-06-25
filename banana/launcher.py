import random

class BananaLauncher:
    g = -9.81
    measurement_noise = .01
    nsamples = 30
    ntargets = 10
    target_xrange = [10, 50]
    target_yrange = [10, 50]

    targets = []
    history = []

    def launch(vx, vy):
        if not BananaLauncher.targets:
            random.seed(1337)
            for _ in range(BananaLauncher.ntargets):
                BananaLauncher.targets.append((random.uniform(*BananaLauncher.target_xrange), \
                                               random.uniform(*BananaLauncher.target_yrange)))

        BananaLauncher.history.append((vx, vy))
        time_of_flight = -2*vy/BananaLauncher.g
        z = BananaLauncher.measurement_noise
        T = [ random.uniform(0, time_of_flight) for _ in range(BananaLauncher.nsamples) ]
        return sorted([T,
                       [ vx*t + random.uniform(-z,z) for t in T ],
                       [ vy*t + BananaLauncher.g*t**2/2  + random.uniform(-z,z) for t in T ] ],
                        key= lambda x: x[0])
