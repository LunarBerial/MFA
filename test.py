#coding:utf-8

import re, codecs
import mxnet.ndarray as nd
from mxnet.gluon import nn
from mxnet import autograd, gluon
a = nd.ones(( 2, 9))
print(nd.sum(a, axis=[1], keepdims=False))
b = nd.random.uniform(shape =(2, 1))
net = nn.Sequential()
net.add(nn.Dense(2),
        nn.Dense(1))
net.initialize()
trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': 1e-3})
a.con

for i in range(10):
    with autograd.record():
        p = net(a)
        l = (b - p) ** 2
        print(i, l)
    l.backward()
    print(trainer._params[-2]._grad)
    trainer.step(2)

