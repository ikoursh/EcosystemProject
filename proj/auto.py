from model2 import Sim
import argparse

parser = argparse.ArgumentParser(description='Run the default simulation')
parser.add_argument("-s", type=int, dest="steps",
                    help='Number of steps to run the sim', required=True)

parser.add_argument("-a", help="enable animation", dest="animate", action='store_true')

args = parser.parse_args()

ms = Sim()
if args.animate:
    ms.animate(args.steps)
else:
    ms.run(args.steps, max_attempts=-1)
ms.graph(info="v3")
