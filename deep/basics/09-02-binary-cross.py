import tensorflow as tf
import numpy as np
from tensorflow.keras.backend import log

'''
https://intellipaat.com/community/6280/tensorflow-sigmoid-and-cross-entropy-vs-sigmoidcrossentropywithlogits
'''

p = np.array(
      [[0., 0., 0., 1., 0.],
       [1., 0., 0., 0., 0.]]
)
logit_q = np.array(
      [[0.2, 0.2, 0.2, 0.2, 0.2],
       [0.3, 0.3, 0.2, 0.1, 0.1]]
)

q = tf.nn.sigmoid(logit_q)

prob1 = -p * log(q)
prob2 = p * -log(q) + (1 - p) * -log(1 - q)
prob3 = p * -log(tf.sigmoid(logit_q)) + (1-p) * -log(1-tf.sigmoid(logit_q))
prob4 = tf.nn.sigmoid_cross_entropy_with_logits(labels=p, logits=logit_q)
print(prob1.numpy())
print(prob2.numpy())
print(prob3.numpy())
print(prob4.numpy())
