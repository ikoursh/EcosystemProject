from model2 import Sim
import argparse
import math

parser = argparse.ArgumentParser(description='Run the default simulation')
parser.add_argument("-s", type=int, dest="steps",
                    help='Number of steps to run the sim', required=True)

parser.add_argument("-p", type=int, dest="pop",
                    help='Initial population size', default=500)

parser.add_argument("-f", type=int, dest="food",
                    help='Account of food')

parser.add_argument("-a", help="enable animation", dest="animate", action='store_true')
parser.add_argument("-v", help="enable verbose", dest="v", action='store_true')

max_e = 1048576
parser.add_argument("-dp", type=int, dest="dp",
                    help='Maximum number of data points, defaults to excel maximum (' + str(
                        max_e) + ') if excel is used. Else, defaults to the number of steps', default=max_e)

parser.add_argument("--spss", help="output data in SPSS data format. Note that this will NOT force data points to max.",
                    dest="spss", action='store_true')

parser.add_argument("--no-excel",
                    help="Don't output data to excel format. Will be enabled automatically if the number of data points exceed " + str(
                        max_e),
                    dest="no_excel", action='store_true')

parser.add_argument("--no-plt", help="Don't generate plt preview",
                    dest="no_plt", action='store_true')

parser.add_argument("--gui", help="Used to output progress in json format for GUI (in beta)",
                    dest="gui", action='store_true')

args = parser.parse_args()

ms = Sim(args.pop, args.food)

# because this model will only run once, we can maximise the amount of data points without exceeding the maximum of 18277
# total_data_points = steps/data_point_freq

args.dp = min(args.dp, args.steps)  # make sure that data points is smaller than steps
if args.dp is None:
    args.dp = args.steps if args.no_excel else min(args.steps, max_e)
data_point_freq = math.floor(args.steps / args.dp)
data_point_freq += 1 if data_point_freq == 0 else 0

if args.v:
    print("data point frequency selected {}".format(data_point_freq))
    print("expected data points: {}".format(args.steps / data_point_freq))

if args.animate:
    ms.animate(args.steps, data_point_freq=data_point_freq, gui=args.gui)
else:
    ms.run(args.steps, max_attempts=-1, data_point_freq=data_point_freq, gui=args.gui)

req_formats = ()
if not args.no_plt:
    req_formats += ("plt",)
if not args.no_excel:
    req_formats += ("excel",)
if args.spss:
    req_formats += ("spss",)

print("Simulation complete. Requested files are stored at: " + ms.graph(info="generated via auto.py", output=req_formats))
