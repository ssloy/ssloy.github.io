import random

class Launcher:
    g = -9.81
    measurement_noise = 0*.5
    nsamples = 30
    ntargets = 10
    target_xrange = [10, 50]
    target_yrange = [10, 50]

    targets = []
    history = []

    def launch(vx, vy):
        if not Launcher.targets:
            random.seed(1337)
            for _ in range(Launcher.ntargets):
                Launcher.targets.append((random.uniform(*Launcher.target_xrange), \
                                               random.uniform(*Launcher.target_yrange)))

        Launcher.history.append((vx, vy))
        time_of_flight = -2*vy/Launcher.g
        z = Launcher.measurement_noise
        T = sorted([ random.uniform(0, time_of_flight) for _ in range(Launcher.nsamples) ])
        return [
                 T,
                 [ vx*t + random.uniform(-z,z) for t in T ],
                 [ vy*t + Launcher.g*t**2/2  + random.uniform(-z,z) for t in T ]
               ]
