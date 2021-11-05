from tensorflow.keras.layers import Input, Conv2D
from tensorflow.keras.models import Model

input_layer = Input((608, 608, 3))
x = Conv2D(32, (3, 3), padding='same', name='conv2d_layer1')(input_layer)
x = Conv2D(32, (3, 3), strides=(2,2), padding='same', name='conv2d_layer2')(x)
x = Conv2D(32, (3, 3), padding='same', name='conv2d_layer3')(x)
output_layer = Conv2D(32, (3, 3), strides=(2,2), padding='same', name='conv2d_layer4')(x)
model = Model(input_layer, output_layer)
model.summary()

l1 = model.layers[1].output
l2 = model.layers[2].output
l3 = model.layers[3].output
print(l1.shape, l2.shape, l3.shape)

l1 = model.get_layer('conv2d_layer1').output
l2 = model.get_layer('conv2d_layer2').output
l3 = model.get_layer('conv2d_layer3').output
print(l1.shape, l2.shape, l3.shape)
