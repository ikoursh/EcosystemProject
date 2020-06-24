from model2 import Sim
ms = Sim()
ms.run(100000, print_freq=1000)
ms.graph(info="v3")


