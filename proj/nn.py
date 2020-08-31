import configparser
import numpy
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read(os.path.join(dir_path, 'config.ini'))

if config["GPU"]["USE_GPU"].lower() == "true":
    print("use GPU is on")
    try:
        import cupy as xp
    except:
        raise Exception(
            "Error importing CuPy. To ensure that your installation is setup properly go to https://docs-cupy.chainer.org/en/stable/install.html")
else:
    import numpy as xp
var = numpy.ndarray


def sigmoid(a: numpy.ndarray) -> numpy.ndarray:
    """
    Sigmoid Function

    Args:
        a(numpy.ndarray): Input

    Returns:
        numpy.ndarray: Result
    """
    return 1 / (1 + xp.exp(-a))


def mutate(a: numpy.ndarray) -> numpy.ndarray:
    """
    Mutate Function

    Args:
        a(numpy.ndarray): Input


    Returns:
        numpy.ndarray: Result
    """
    return a + xp.random.normal(0, 0.1)


class NNLayer:
    """
    A class that represents a single neural network layer


    Args:
        nodes(int): The number of nodes this layer should have
        prev_nodes(int): The number of nodes the previous layer has

    Attributes:
        nodes(int): The number of nodes this layer should have
        prev_nodes(int): The number of nodes the previous layer has

        weights(numpy.ndarray): A matrix consisting of the weights of the layer
        bias(numpy.ndarray): A vector consisting of the biases of the layer
    """

    def __init__(self, nodes: int, prev_nodes: int) -> None:
        self.nodes = nodes
        self.prev_nodes = prev_nodes
        self.weights = xp.random.random((prev_nodes, nodes))
        self.bias = xp.random.random(nodes)

    def feed_forward(self, xs: numpy.ndarray) -> numpy.ndarray:
        """
        Feed forward inputs into the layer

        .. math:: a^{(L)} = \\sigma (\\sum_{i=1}^{m} W_{i}^{(L)}  a_{i}^{(L-1)}  + b)

        Args:
            xs(numpy.ndarray): Inputs

        Returns:
            numpy.ndarray: Layer outputs for the inputs
        """
        if len(xs) != self.prev_nodes:
            raise Exception(
                "error, wrong input size, expected {} got {}".format(
                    self.prev_nodes, len(xs)))
        return sigmoid(xp.add(xp.matmul(xp.array(xs), self.weights), self.bias))

    def mutate(self) -> None:
        """
        Mutates the layer
        """
        self.weights = mutate(self.weights)
        self.bias = mutate(self.bias)

    def __repr__(self) -> str:
        return "weights: {} bias: {}".format(self.weights, self.bias)


class NeuralNetwork:
    """
    A neural network

    Args:
        nodes(list[int]): A list of the amount of nodes for every layer

    Attributes:
        layers(list[NNLayer]): A list of all the layers composing the neural network

    Raises:
        Exception: If the nodes list is shorter than 2

    """

    def __init__(self, nodes: list) -> None:
        if len(nodes) < 2:
            raise Exception(
                "error, the neural network needs to have an input and output layer"
            )
        self.layers = []
        for i in range(len(nodes) - 1):
            self.layers.append(NNLayer(nodes[i + 1], nodes[i]))

    def feed_forward(self, xs: numpy.ndarray) -> numpy.ndarray:
        """
        Feed forward the input throughout all the layers of the neural network

        Args:
            xs(numpy.ndarray): Input


        Returns:
            numpy.ndarray: The output of the neural network

        Warnings:
            it is advised that all inputs be between 0 and 1
        """
        ys = None
        for l in self.layers:
            if ys is None:
                ys = l.feed_forward(xs)
            else:
                ys = l.feed_forward(ys)
        return ys

    def __repr__(self) -> str:
        return str([l.__repr__()
                    for l in self.layers]).replace("\\n",
                                                   "").replace(",", "\n")

    def mutate(self) -> None:
        """
        Mutate all the layers of the neural network
        """
        for l in self.layers:
            l.mutate()
