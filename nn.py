#nn:
import numpy as np
import configparser

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('config.ini')

if config["GPU"]["USE_GPU"].lower()=="true":
	print("use GPU is on")
	try:
		import cupy as xp
	except:
		raise Exception("Error importing cupy. To ensure that your installation is setup properly go to https://docs-cupy.chainer.org/en/stable/install.html")
else:
	import numpy as xp
	
s = lambda a: 1 / (1 + xp.exp(-a))
m = lambda a: a + xp.random.normal(0, 0.1)

'''
A neural network layer class

varibles:
    weight[matrix] - a matrix consisting of the weights of the layer
    bias[vector] - a vector consisting of the biases of the layer
    nodes[int] - the number of nodes the neural network contains
'''


class nnLayer:
    def __init__(self, nodes, prev_nodes):
        self.nodes = nodes
        self.prev_nodes = prev_nodes
        self.weights = xp.random.random((prev_nodes, nodes))
        self.bias = xp.random.random(nodes)

    def feed_forward(self, xs):
        if len(xs) != self.prev_nodes:
            raise Exception(
                "error, wrong input size, expected {} got {}".format(
                    self.prev_nodes, len(xs)))
        return s(xp.add(xp.matmul(xp.array(xs), self.weights), self.bias))

    def mutate(self):
        self.weights = m(self.weights)
        self.bias = m(self.bias)

    
    def __repr__(self):
        return "weights: {} bias: {}".format(self.weights, self.bias)


'''
A neural network  class

varibles:
    layers[list of nnLayers] - an array consisting of all the network's layers
'''


class neuralNetwork:
    """
    @parm nodes a list of the number of nodes in each layer
    """
    def __init__(self, nodes):
        if len(nodes) < 2:
            raise  Exception(
                "error, the neural network needs to have an input and output layer"
            )
        self.layers = []
        for i in range(len(nodes) - 1):
            self.layers.append(nnLayer(nodes[i + 1], nodes[i]))

    def feed_forward(self, xs):
        ys = None
        for l in self.layers:
            if not (ys is None):
                ys = l.feed_forward(ys)
            else:
                ys = l.feed_forward(xs)
        return ys

    def __repr__(self):
        return str([l.__repr__()
                    for l in self.layers]).replace("\\n",
                                                   "").replace(",", "\n")

    def mutate(self):
        for l in self.layers:
            l.mutate()