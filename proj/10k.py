from model2 import Sim
ms = Sim()
ms.run(10000, print_freq=100)
ms.graph(info="v3")
