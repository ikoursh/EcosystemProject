from model2 import Sim
import argparse
import math

parser = argparse.ArgumentParser(description='Run the default simulation')
parser.add_argument("-s", type=int, dest="steps",
                    help='Number of steps to run the sim', required=True)

parser.add_argument("-a", help="enable animation", dest="animate", action='store_true')

args = parser.parse_args()

ms = Sim()

# because this model will only run once, we can maximise the amount of data points without exceeding the maximum of 18277
# total_data_points = steps/data_point_freq
data_point_freq = math.floor(args.steps / 18277) - 1
if data_point_freq == -1:
    data_point_freq = 1
if args.animate:
    ms.animate(args.steps, data_point_freq=data_point_freq)
else:
    ms.run(args.steps, max_attempts=-1, data_point_freq=data_point_freq)
ms.graph(info="v3")
