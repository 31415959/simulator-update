import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulator.utils
simulator.utils.VISUALIZATION_MODE = False

import logging
logging.getLogger().setLevel(logging.ERROR)

from simulator.simulate import main

for n in [25, 50, 75, 100]:
    acc = main('arknights.csv', num_matches=n, sim_runs=3, parallel=6)
    print(f"RESULT: 1-{n} = {acc:.1f}%")
