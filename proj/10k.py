from model2 import Sim

ms = Sim()
ms.run(100000, max_attempts=-1)
ms.graph(info="v3")
