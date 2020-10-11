#!/usr/bin/env python3

# Ecosystem project - studying natural biological systems using a simulated ecosystem and reinforcement learning.
# Copyright (C) 2020 Inbar Koursh
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


from model2 import Sim
import argparse
import math

parser = argparse.ArgumentParser(description='Run an ecosystem simulation', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", type=int, dest="steps",
                    help='Number of steps to run the sim', default=1000)

parser.add_argument("-p", type=int, dest="pop",
                    help='Initial population size', default=500)

parser.add_argument("-f", type=int, dest="food",
                    help='Ammount of food')

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
    ms.run(args.steps, data_point_freq=data_point_freq, gui=args.gui)

req_formats = ()
if not args.no_plt:
    req_formats += ("plt",)
if not args.no_excel:
    req_formats += ("excel",)
if args.spss:
    req_formats += ("spss",)

print("Simulation complete. Requested files are stored at: " + ms.graph(info="generated via auto.py", output=req_formats))
