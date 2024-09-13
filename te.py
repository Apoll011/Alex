from precise_runner import PreciseEngine, PreciseRunner

engine = PreciseEngine('precise', 'christopher-precise/christopher-precise.pb')
runner = PreciseRunner(engine, on_activation=lambda: print('hello'), sensitivity=0.5)
runner.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)