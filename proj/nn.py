import configparser
import numpy

config = configparser.ConfigParser(inline_comment_prefixes="#")
# config.read('config.ini')
config.read('C:\\Users\\Student\\Documents\\EcoSystemProject\\proj\\config.ini')
if config["GPU"]["USE_GPU"].lower() == "true":
    print("use GPU is on")
    try:
        import cupy as xp
    except:
        raise Exception(
            "Error importing cupy. To ensure that your installation is setup properly go to https://docs-cupy.chainer.org/en/stable/install.html")
else:
    import numpy as xp
var = numpy.ndarray


def s(a: numpy.ndarray) -> numpy.ndarray:
    """
    Sigmoid Function

    Args:
        a(numpy.ndarray): input

    Returns:
        numpy.ndarray: result
    """
    return 1 / (1 + xp.exp(-a))


def m(a: numpy.ndarray) -> numpy.ndarray:
    """
    Mutate Function

    Args:
        a(numpy.ndarray): input


    Returns:
        numpy.ndarray: result
    """
    return a + xp.random.normal(0, 0.1)


class NNLayer:
    """
    A class that represents a single neural network layer


    Args:
        nodes(int): the number of nodes this layer should have
        prev_nodes(int): the number of nodes the previous layer has

    Attributes:
        nodes(int): the number of nodes this layer should have
        prev_nodes(int): the number of nodes the previous layer has

        weights(numpy.ndarray): a matrix consisting of the weights of the layer
        bias(numpy.ndarray): a vector consisting of the biases of the layer
    """

    def __init__(self, nodes: int, prev_nodes: int) -> None:
        self.nodes = nodes
        self.prev_nodes = prev_nodes
        self.weights = xp.random.random((prev_nodes, nodes))
        self.bias = xp.random.random(nodes)

    def feed_forward(self, xs: numpy.ndarray) -> numpy.ndarray:
        """
        Feed forward inputs into the layer

        Args:
            xs(numpy.ndarray): inputs

        Returns:
            numpy.ndarray: Layer outputs for the inputs
        """
        if len(xs) != self.prev_nodes:
            raise Exception(
                "error, wrong input size, expected {} got {}".format(
                    self.prev_nodes, len(xs)))
        return s(xp.add(xp.matmul(xp.array(xs), self.weights), self.bias))

    def mutate(self):
        """
        Mutates the layer
        """
        self.weights = m(self.weights)
        self.bias = m(self.bias)

    def __repr__(self) -> str:
        return "weights: {} bias: {}".format(self.weights, self.bias)


class NeuralNetwork:
    """
    A neural network

    Args:
        nodes(list[int]): a list of the amount of nodes for every layer

    Attributes:
        layers(list[NNLayer]): a list of all the layers composing the neural network

    Examples:
        my_nn = NeuralNetwork([5, 3, 3, 2])

    Raises:
        Exception: if the nodes list is shorter than 2

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
            xs(numpy.ndarray): input


        Returns:
            numpy.ndarray: the output of the neural network

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

    def mutate(self):
        """
        Mutate all the layers of the neural network
        """
        for l in self.layers:
            l.mutate()
