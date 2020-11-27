'''
https://stackoverflow.com/questions/50124158/keras-loss-function-with-additional-dynamic-parameter
'''
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.losses import categorical_crossentropy

def sample_loss( y_true, y_pred, is_weight ) :
    return is_weight * categorical_crossentropy( y_true, y_pred ) 

x = Input(shape=(32,32,3), name='image_in')
y_true = Input( shape=(10,), name='y_true' )
is_weight = Input(shape=(1,), name='is_weight')
f = Conv2D(16,(3,3),padding='same')(x)
f = MaxPool2D((2,2),padding='same')(f)
f = Conv2D(32,(3,3),padding='same')(f)
f = MaxPool2D((2,2),padding='same')(f)
f = Conv2D(64,(3,3),padding='same')(f)
f = MaxPool2D((2,2),padding='same')(f)
f = Flatten()(f)
y_pred = Dense(10, activation='softmax', name='y_pred' )(f)
model = Model( inputs=[x, y_true, is_weight], outputs=y_pred, name='train_only' )
model.add_loss( sample_loss( y_true, y_pred, is_weight ) )
model.compile(loss=None, optimizer='sgd')
model.summary()

# train
import numpy as np 
a = np.random.randn(8,32,32,3)
a_true = np.random.randn(8,10)
a_is_weight = np.random.randint(0,2,size=(8,1))
model.fit( [a, a_true, a_is_weight] )


# test model for prediction(infer) only
test_model = Model( inputs=x, outputs=y_pred, name='test_only' )
a_pred = test_model.predict( a )
