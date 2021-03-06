#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import json

import numpy as np
import scripts.model
from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork
from scripts.sudoku_str import SudokuStr
from scripts import sudopy


def create_net(rel_path):
    with open(os.getcwd() + rel_path) as in_file:
        sizes, biases, wts = pickle.load(in_file)
    return NeuralNetwork(customValues=(sizes, biases, wts))

def get_cells(image_path):  # yields 9 * 9 = 81 cells
    net = create_net(rel_path='/SudokuSolver/networks/net')
    for row in Extractor(os.path.abspath(image_path)).cells:
        for cell in row:
            x = net.feedforward(np.reshape(cell, (784, 1)))
            x[0] = 0
            digit = np.argmax(x)
            yield str(digit) if list(x[digit])[0] / sum(x) > 0.8 else '.'

def get_cells2(image_path):  # yields 9 * 9 = 81 cells

    import tensorflow as tf
    x = tf.placeholder("float", [None, 784])
    sess = tf.Session()

    with tf.variable_scope("convolutional"):
        keep_prob = tf.placeholder("float")
        y2, variables = model.convolutional(x, keep_prob)
    saver = tf.train.Saver(variables)
    saver.restore(sess, "scripts/convolutional.ckpt")

    for row in Extractor(os.path.abspath(image_path)).cells:
        for cell in row:
            digit = np.argmax(sess.run(y2, feed_dict={x: np.reshape(cell, (784, 1)), keep_prob: 1.0}).flatten().tolist())
            yield str(digit) if list(x[digit])[0] / sum(x) > 0.8 else '.'


def solver(image_path):
    try:
        grid = ''.join(cell for cell in get_cells(image_path))
        s = sudopy.solve(grid)
        return s
    except:
        return 0


