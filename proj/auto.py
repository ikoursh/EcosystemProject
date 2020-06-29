from model2 import Sim
import argparse

parser = argparse.ArgumentParser(description='Run the default simulation')
parser.add_argument("-s", type=int, dest="steps",
                    help='Number of steps to run the sim', required=True)

ms = Sim()
ms.run(parser.parse_args().steps, max_attempts=-1)
ms.graph(info="v3")
