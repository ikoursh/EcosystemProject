from model2 import Sim
import argparse
import os
import gc
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()


def concatenate(elenco_video, output):
    """
    adapted from https://pythonprogramming.altervista.org/join-all-mp4-with-python-and-ffmpeg/
    """
    stringa = "ffmpeg -i \"concat:"
    elenco_file_temp = []
    for f in elenco_video:
        file = "temp" + str(elenco_video.index(f) + 1) + ".ts"
        os.system("ffmpeg -i " + f + " -c copy -bsf:v h264_mp4toannexb -f mpegts " + file)
        elenco_file_temp.append(file)
    print(elenco_file_temp)
    for f in elenco_file_temp:
        stringa += f
        if elenco_file_temp.index(f) != len(elenco_file_temp) - 1:
            stringa += "|"
        else:
            stringa += "\" -c copy  -bsf:a aac_adtstoasc " + output
    print(stringa)
    os.system(stringa)


s = Sim()

parser = argparse.ArgumentParser(
    description='Animate the simulation in a non ram intensive way (will be rounded to a multiple of 20)')
parser.add_argument("-s", type=int, dest="steps",
                    help='Number of steps to run the sim', required=True)

args = parser.parse_args()
from pympler import muppy, summary

parts = []
for i in range(round(args.steps / 20)):
    print("{} out of {}".format(i, round(args.steps / 20)))
    parts.append("/"+"/".join(os.path.realpath(__file__).split("\\")[1:-1])+"/"+s.animate(20))
    gc.collect()
    print(parts)

all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)  # Prints out a summary of the large objects
summary.print_(sum1)  # Get references to certain types of objects such as dataframe

concatenate(parts, "/"+"/".join(os.path.realpath(__file__).split("\\")[1:-1])+"/animations-0.1/" + s.get_fn() + '_concatenated.mp4')

# cleanup:
for p in parts:
    os.remove(p)
