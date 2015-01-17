#!/usr/bin/env python

from theano import tensor

from blocks.datasets import DataStream
from blocks.datasets.mnist import MNIST
from blocks.datasets.schemes import SequentialScheme
from blocks.algorithms import GradientDescent, SteepestDescent
from blocks.bricks import MLP, Tanh, Identity
from blocks.bricks.cost import BinaryCrossEntropy
from blocks.main_loop import MainLoop
from blocks.extensions import FinishAfter, Printing


def main():
    mlp = MLP([Tanh(), Identity()], [784, 100, 10])
    x = tensor.matrix('features')
    y = tensor.lmatrix('targets')
    cost = BinaryCrossEntropy().apply_for_indices(y - 1, mlp.apply(x))

    mnist = MNIST("train")

    main_loop = MainLoop(
        mlp,
        DataStream(mnist,
                   iteration_scheme=SequentialScheme(mnist.num_examples, 20)),
        GradientDescent(cost=cost,
                        step_rule=SteepestDescent(learning_rate=0.1)),
        extensions=[FinishAfter(after_n_epochs=2),
                    Printing()])
    main_loop.run()

if __name__ == "__main__":
    main()
