#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'widget')


# In[2]:


import pandas as pd
import numpy as np
from glob import glob
import os
import datetime
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Input, Concatenate, Dot, Add, ReLU, Activation
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import tensorflow as tf


# In[795]:


folder = 'data'
file_names = [['가평_2018.xlsx', '가평_2019.xlsx'], ['의암호_2018.xlsx', '의암호_2019.xlsx']]
#file_names = [['가평_2019.xlsx'], ['의암호_2019.xlsx']]

day = 24*60*60
year = (365.2425)*day

df_full = []
df = []

for loc in range(len(file_names)):
    
    df_loc = []
    for y in range(len(file_names[loc])):
        path = os.path.join(folder, file_names[loc][y])
        print(file_names[loc][y])
        df_loc.append(pd.read_excel(path))
    df_full.append(pd.concat(df_loc))
    df.append(df_full[loc].iloc[:, 2:11])
    date_time = pd.to_datetime(df_full[loc].iloc[:, 0], format='%Y.%m.%d %H:%M', utc=True)
    timestamp_s = date_time.map(datetime.datetime.timestamp)
    df[loc]['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df[loc]['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df[loc]['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df[loc]['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    df[loc] = df[loc].reset_index(drop=True)
        


# In[796]:


df[0]


# In[703]:


df[1]


# In[797]:


# normalize data

df_all = pd.concat(df)
df_all

train_mean = df_all.mean()
train_std = df_all.std()
for i in range(len(file_names)):
    df[i] = (df[i]-train_mean)/train_std


# In[705]:


df[0]


# In[706]:


train_df = df[0]
val_df = df[0]
test_df = df[0]


# In[798]:


class WindowGenerator():
  def __init__(self, input_width, label_width, shift,
               train_df=train_df, val_df=val_df, test_df=test_df,
            #train_df=None, val_df=None, test_df=None,
               label_columns=None):
    # Store the raw data.
    self.train_df = train_df
    self.val_df = val_df
    self.test_df = test_df

    # Work out the label column indices.
    self.label_columns = label_columns
    if label_columns is not None:
      self.label_columns_indices = {name: i for i, name in
                                    enumerate(label_columns)}
    self.column_indices = {name: i for i, name in
                           enumerate(train_df.columns)}

    # Work out the window parameters.
    self.input_width = input_width
    self.label_width = label_width
    self.shift = shift

    self.total_window_size = input_width + shift

    self.input_slice = slice(0, input_width)
    self.input_indices = np.arange(self.total_window_size)[self.input_slice]

    self.label_start = self.total_window_size - self.label_width
    self.labels_slice = slice(self.label_start, None)
    self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

  def __repr__(self):
    return '\n'.join([
        f'Total window size: {self.total_window_size}',
        f'Input indices: {self.input_indices}',
        f'Label indices: {self.label_indices}',
        f'Label column name(s): {self.label_columns}'])


# In[799]:


def split_window(self, features):
  inputs = features[:, self.input_slice, :]
  labels = features[:, self.labels_slice, :]
  if self.label_columns is not None:
    labels = tf.stack(
        [labels[:, :, self.column_indices[name]] for name in self.label_columns],
        axis=-1)

  # Slicing doesn't preserve static shape information, so set the shapes
  # manually. This way the `tf.data.Datasets` are easier to inspect.
  inputs.set_shape([None, self.input_width, None])
  labels.set_shape([None, self.label_width, None])

  return inputs, labels

WindowGenerator.split_window = split_window


# In[800]:


import matplotlib
import matplotlib.font_manager as fm
fm.get_fontconfig_fonts()
font_location = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
#font_location = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# font_location = 'C:/Windows/Fonts/NanumGothic.ttf' # For Windows
fprop = fm.FontProperties(fname=font_location)


# In[801]:


def plot(self, model=None, plot_col='T (degC)', max_subplots=3):
  inputs, labels = self.example
  plt.figure(figsize=(10, 8))
  plot_col_index = self.column_indices[plot_col]
  max_n = min(max_subplots, len(inputs))
  for n in range(max_n):
    plt.subplot(3, 1, n+1)
    plt.ylabel(f'{plot_col} [normed]', fontproperties=fprop)
    plt.plot(self.input_indices, inputs[n, :, plot_col_index],
             label='Inputs', marker='.', zorder=-10)

    if self.label_columns:
      label_col_index = self.label_columns_indices.get(plot_col, None)
    else:
      label_col_index = plot_col_index

    if label_col_index is None:
      continue

    plt.scatter(self.label_indices, labels[n, :, label_col_index],
                edgecolors='k', label='Labels', c='#2ca02c', s=64)
    if model is not None:
      predictions = model(inputs)
      plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                  marker='X', edgecolors='k', label='Predictions',
                  c='#ff7f0e', s=64)

    if n == 0:
      plt.legend()

  plt.xlabel('Time [h]')

WindowGenerator.plot = plot


# In[802]:


# not used
# original make_dataset code
def make_dataset(self, data):
  data = np.array(data, dtype=np.float32)
  ds = tf.keras.preprocessing.timeseries_dataset_from_array(
      data=data,
      targets=None,
      sequence_length=self.total_window_size,
      sequence_stride=1,
      shuffle=True,
      batch_size=32,)

  ds = ds.map(self.split_window)

  return ds

#WindowGenerator.make_dataset = make_dataset


# In[806]:


w2 = WindowGenerator(input_width=6, label_width=1, shift=1,
                     label_columns=None)
w2


# In[810]:


# Stack three slices, the length of the total window:
example_window = tf.stack([np.array(train_df[:w2.total_window_size]),
                           np.array(train_df[100:100+w2.total_window_size]),
                           np.array(train_df[200:200+w2.total_window_size])])


example_inputs, example_labels = w2.split_window(example_window)

print('All shapes are: (batch, time, features)')
print(f'Window shape: {example_window.shape}')
print(f'Inputs shape: {example_inputs.shape}')
print(f'labels shape: {example_labels.shape}')


# In[811]:


w2.example = example_inputs, example_labels


# In[812]:


w2.plot(plot_col='수온')


# In[813]:


@property
def train(self):
  return self.make_dataset(self.train_df)

@property
def val(self):
  return self.make_dataset(self.val_df)

@property
def test(self):
  return self.make_dataset(self.test_df)

@property
def example(self):
  """Get and cache an example batch of `inputs, labels` for plotting."""
  result = getattr(self, '_example', None)
  if result is None:
    # No example batch was found, so get one from the `.train` dataset
    result = next(iter(self.train))
    # And cache it for next time
    self._example = result
  return result

WindowGenerator.train = train
WindowGenerator.val = val
WindowGenerator.test = test
WindowGenerator.example = example


# In[814]:


def sample_batch_index(total, batch_size):
    '''Sample index of the mini-batch.

    Args:
        - total: total number of samples
        - batch_size: batch size

    Returns:
        - batch_idx: batch index
    '''
    total_idx = np.random.permutation(total)
    batch_idx = total_idx[:batch_size]
    return batch_idx


# In[627]:


def binary_sampler(p, shape):
  '''Sample binary random variables.
  
  Args:
    - p: probability of 1
    - shape: matrix shape
    
  Returns:
    - binary_random_matrix: generated binary random matrix.
  '''
  unif_random_matrix = np.random.uniform(0., 1., size = shape)
  binary_random_matrix = 1*(unif_random_matrix < p)
  return binary_random_matrix


# In[628]:


def uniform_sampler(low, high, shape):
  '''Sample uniform random variables.
  
  Args:
    - low: low limit
    - high: high limit
    - rows: the number of rows
    - cols: the number of columns
    
  Returns:
    - uniform_random_matrix: generated uniform random matrix.
  '''
  return np.random.uniform(low, high, size = shape)


# In[629]:


def normalization (data, parameters=None):
  '''Normalize data in [0, 1] range.
  
  Args:
    - data: original data
  
  Returns:
    - norm_data: normalized data
    - norm_parameters: min_val, max_val for each feature for renormalization
  '''

  # Parameters
  _, dim = data.shape
  norm_data = data.copy()

  if parameters is None:

    # MixMax normalization
    min_val = np.zeros(dim)
    max_val = np.zeros(dim)
   
    # For each dimension
    for i in range(dim):
      min_val[i] = np.nanmin(norm_data[:,i])
      norm_data[:,i] = norm_data[:,i] - np.nanmin(norm_data[:,i])
      max_val[i] = np.nanmax(norm_data[:,i])
      norm_data[:,i] = norm_data[:,i] / (np.nanmax(norm_data[:,i]) + 1e-6)

    # Return norm_parameters for renormalization
    norm_parameters = {'min_val': min_val,
                       'max_val': max_val}
  else:
    min_val = parameters['min_val']
    max_val = parameters['max_val']

    # For each dimension
    for i in range(dim):
      norm_data[:,i] = norm_data[:,i] - min_val[i]
      norm_data[:,i] = norm_data[:,i] / (max_val[i] + 1e-6)

    norm_parameters = parameters

  return norm_data, norm_parameters


# In[630]:


class MissData(object):
    def __init__(self, load_dir=None):
        if load_dir:
            self.missarr = np.load(os.path.join(load_dir, 'miss.npy'))
            self.idxarr = np.load(os.path.join(load_dir, 'idx.npy'))
            
    def make_missdata(self, data_x, missrate=0.2):
        data = data_x.copy()
        rows, cols = data_x.shape
        total_no = rows*cols
        total_miss_no = np.round(total_no*missrate).astype(int)
        total_idx = self.idxarr.shape[0]
        idxarr = self.idxarr
        missarr = self.missarr
        #print(total_miss_no)
        miss_no = 0
        cum_no = self.idxarr[:,3:4]
        cum_no = cum_no.reshape((total_idx))
        cum_sum = np.max(cum_no)
        #print(cum_no)
        #print(total_idx)
        while True:
            loc_count = np.around(np.random.random()*cum_sum)
            #print('loc_count =', loc_count)
            idx = len(cum_no[cum_no <= loc_count])-1
            #print(cum_no[cum_no <= loc_count])
            #print('idx =', idx)
            startnan = idxarr[idx][0]
            nanlen = idxarr[idx][2]
            loc = np.around(np.random.random()*(rows-nanlen)).astype(int)
            #print('loc =', loc)
            #print(loc_count, idx)
            #print(idxarr[idx])
            #data_copy = data[loc:loc+nanlen].copy()
            data_copy = data[loc:loc+nanlen]
            #print('startnan=', startnan)
            #isnan = missarr[startnan:startnan+nanlen].copy()
            isnan = missarr[startnan:startnan+nanlen]
            #print('isnan =',isnan)
            miss_no += idxarr[idx][1]
            if (miss_no > total_miss_no):
                break
            data_copy[isnan==1] = np.nan
            data[loc:loc+nanlen] = data_copy
        #print('miss_data =', data)
        return data
    
    def save(data, max_tseq, save_dir='save'):
        no, dim = data.shape
        #print((no, dim))
        isnan = np.isnan(data).astype(int)
        isany = np.any(isnan, axis=1).astype(int)
        shifted = np.roll(isany, 1)
        shifted[0] = 1
        #print(isnan)
        #print(isany.astype(int))
        #print(shifted)
        startnan = ((isany == 1) & (shifted ==0)).astype(int)
        #print(startnan)
        group = startnan.cumsum()
        group = group*isany
        #print(group)
        n = np.max(group)
        #print(n)
        missarr = None
        cum_no = 0
        rowidx = 0
        for i in range(1, n+1):
            g = (group == i).astype(int)
            i = np.argmax(g)
            rows = g.sum()
            #print(len)
            #print(i)
            #print(type(missarr))
            if rows <= max_tseq:
                nanseq = isnan[i:i+rows, :]
                no = np.sum(nanseq)
                #print(no)
                if missarr is None:
                    missarr = nanseq
                    idxarr = np.array([[rowidx, no, rows, cum_no]])
                else:
                    missarr = np.concatenate((missarr, nanseq))
                    idxarr = np.concatenate((idxarr, [[rowidx, no, rows, cum_no]]), axis=0)
                cum_no += no
                rowidx += rows

        #print(idxarr)
        miss_npy_file = os.path.join(save_dir, 'miss.npy')
        idx_npy_file = os.path.join(save_dir, 'idx.npy')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        np.save(miss_npy_file, missarr)
        np.save(idx_npy_file, idxarr)
        print('miss_data file saved')


# In[747]:


norm_df = pd.concat(df,axis=0)
n_data = norm_df.to_numpy()
MissData.save(n_data, max_tseq=12)
n_data
#n_data = n_data[0:100]
isnan = np.isnan(n_data).astype(int)
isnan[50:100]
miss = MissData(load_dir='save')
tt = miss.make_missdata(n_data)
tt = np.isnan(tt).astype(int)
tt[3000:3050]


# **miss data 준비**

# In[738]:


norm_df = pd.concat(df,axis=0)
norm_data = norm_df.to_numpy()
MissData.save(norm_data, max_tseq = 12)


# In[926]:


def interpolate(np_data, max_gap=3):
    #n = np_data.shape[1]
    data = pd.DataFrame(np_data)
    #data[0][0] = np.nan
    #data[0][1] = np.nan
    #data[0][2] = np.nan
    #data[data.columns[0]][0] = np.nan
    #data[data.columns[0]][1] = np.nan
    #data[data.columns[0]][2] = np.nan
    
    # create mask
    mask = data.copy()
    grp = ((mask.notnull() != mask.shift().notnull()).cumsum())
    grp['ones'] = 1
    for i in data.columns:
        mask[i] = (grp.groupby(i)['ones'].transform('count') < max_gap) | data[i].notnull()
    data = data.interpolate(method='polynomial', order=5, limit=max_gap, axis=0).bfill()[mask]
    return data.to_numpy()
    #return data
    
#filled_data = interpolate(norm_data, max_gap=3)
#np.arange(0, 5, dtype=int)
#['%d'%val for val in range(0,5)]


# In[955]:


from tensorflow import keras

class GainDataGenerator(keras.utils.Sequence):
    'Generates data for GAIN'
    def __init__(self,
                 data_list,
                 batch_size=32,
                 input_width=24*3,
                 label_width=24*3,
                 shift=0,
                 fill_no=4,
                 miss_rate=0.2,
                 hint_rate=0.9,
                 normalize=True,
                 miss_pattern=None,
                 alpha=100.):
        'Initialization'
        window_size = input_width
        
        # interpollation
        filled_data = []
        for data in data_list:
            data = interpolate(data, max_gap=fill_no)
            filled_data.append(data)
            
        data_list = filled_data
        
        # whole data
        self.data = np.concatenate(data_list)

        # TO-DO
        
        # pre calculation for  sequence data
        last_cum = 0
        cums = []
        for data in data_list:
            isnan = np.isnan(data)
            isany = np.any(isnan, axis=1)
            shifted = np.roll(isany, 1)
            shifted[0] = True # set to nan
            start_seq = ((isany == False) & (shifted == True)).astype(int)
            cum = start_seq.cumsum()
            cum += last_cum
            last_cum = np.max(cum)
            cum[isany] = 0
            cums.append(cum)
            
        
        # normlize for spam
        if normalize:
            self.data, norm_param = normalization(self.data)
        #print(norm_param)
        
        # Define mask matrix
        if miss_pattern is None:
            self.data_m = binary_sampler(1-miss_rate, self.data.shape)
        else:
            #MissData.save(self.data, max_tseq = 12)
            self.miss = MissData(load_dir='save')
            self.miss_rate = miss_rate
            miss_data = self.miss.make_missdata(self.data, self.miss_rate)
            self.data_m = 1. - np.isnan(miss_data).astype(float)
            
            self.data_m_rand = binary_sampler(1-(miss_rate/10.), self.data.shape)
            self.data_m[self.data_m_rand==0.] = 0.
        self.miss_pattern = miss_pattern
        
        # sequence data
        self.ids = np.concatenate(cums)
        data_idx = np.empty((0), dtype=int)
        for i in range(1, last_cum+1):
            seq_len = (self.ids == i).sum()
            start_id = np.argmax(self.ids == i)
            # possible data number in seqeunce
            time_len = seq_len - window_size + 1
            start_ids = np.arange(start_id, start_id+time_len)
            data_idx = np.append(data_idx, start_ids)
            
        # start index set for sequence data
        self.data_idx = data_idx
        self.input_width = input_width
        self.no = len(data_idx)
        
        #print('self.no = ', self.no)
        
        self.batch_size = batch_size
        
        # random shuffling  index
        self.batch_idx = sample_batch_index(self.no, self.no)
        self.batch_id = 0
        self.shape = (batch_size,self.input_width)+self.data.shape[1:]
        #self.hint_rate = hint_rate
            
    def __len__(self):
        'Denotes the number of batches per epoch'
        #return int(128/self.batch_size)
        #return 2
        return 1

    def __getitem__(self, index):
        'Generate one batch of data'
        #print('index =', index)
        # Sample batch
        x = np.empty((0, self.input_width, self.data.shape[1]))
        #m = np.empty((0, self.input_width, self.data.shape[1]))
        #h = np.empty((0, self.input_width, self.data.shape[1]))
        y = np.empty((0, self.input_width, self.data.shape[1]))
        #print(x.shape)
        #print(self.data.shape)
        #print(self.input_width)
        #self.batch_idx = sample_batch_index(self.no, self.batch_size)
        for cnt in range(0, self.batch_size):
            i = self.batch_idx[self.batch_id]
            self.batch_id += 1
            #self.batch_id %= self.batch_size
            self.batch_id %= self.no
            if self.miss_pattern and (self.batch_id == 0):
                self.batch_idx = sample_batch_index(self.no, self.no)
                miss_data = self.miss.make_missdata(self.data, self.miss_rate)
                self.data_m = 1. - np.isnan(miss_data).astype(float)
                self.data_m_rand = binary_sampler(1-self.miss_rate/10., self.data.shape)
                self.data_m[self.data_m_rand==0.] = 0.
            idx1 = self.data_idx[i]
            idx2 = self.data_idx[i]+self.input_width
            #print(idx1, idx2)
        
            Y_mb = self.data[idx1:idx2]
            X_mb = Y_mb.copy()
            M_mb = self.data_m[idx1:idx2]
            Z_mb = uniform_sampler(0, 0.01, shape=X_mb.shape)
            X_mb = M_mb*X_mb + (1-M_mb)*Z_mb
            #H_mb_temp = binary_sampler(self.hint_rate, shape=X_mb.shape)
            #H_mb = M_mb * H_mb_temp
            X_mb[M_mb == 0] = np.nan
            x = np.append(x, [X_mb], axis=0)
            #m = np.append(m, [M_mb], axis=0)
            #h = np.append(h, [H_mb], axis=0)
            y = np.append(y, [Y_mb], axis=0)
            
        #return [x, m, h], y
        return x, y
    
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        return

dgen = GainDataGenerator(df)


# In[932]:


df[1]


# In[876]:


it = iter(dgen)


# In[877]:


x,y = next(it)


# In[878]:


x.shape


# In[880]:


class GAIN(keras.Model):
    def __init__(self, shape, alpha=100., load=False, hint_rate=0.9, gen_sigmoid=True, **kwargs):
        super(GAIN, self).__init__(**kwargs)
        self.shape = shape
        self.dim = np.prod(shape).astype(int)
        self.h_dim = self.dim
        self.gen_sigmoid = gen_sigmoid
        self.build_generator()
        self.build_discriminator()
        self.hint_rate = hint_rate
        self.alpha = alpha
        self.generator_optimizer = Adam()
        self.discriminator_optimizer = Adam()

    ## GAIN models
    def build_generator(self):
        last_activation = 'sigmoid' if self.gen_sigmoid else None
        xavier_initializer = tf.keras.initializers.GlorotNormal()

        shape = self.shape
        #x = Input(shape=(self.dim,), name='generator_input_x')
        #m = Input(shape=(self.dim,), name='generator_input_m')
        x = Input(shape=shape, name='generator_input_x')
        m = Input(shape=shape, name='generator_input_m')
        
        x_f = Flatten()(x)
        m_f = Flatten()(m)

        a = Concatenate()([x_f, m_f])

        a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        #a = keras.layers.BatchNormalization()(a)
        a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        #a = keras.layers.BatchNormalization()(a)
        a = Dense(self.dim, activation=last_activation, kernel_initializer=xavier_initializer)(a)
        G_prob = keras.layers.Reshape(shape)(a)
        self.generator = keras.models.Model([x, m], G_prob, name='generator')

    def build_discriminator(self):
        xavier_initializer = tf.keras.initializers.GlorotNormal()
        shape = self.shape

        #x = Input(shape=(self.dim,), name='discriminator_input_x')
        #h = Input(shape=(self.dim,), name='discriminator_input_h')
        x = Input(shape=shape, name='discriminator_input_x')
        h = Input(shape=shape, name='discriminator_input_h')
        
        x_f = Flatten()(x)
        h_f = Flatten()(h)

        a = Concatenate()([x_f, h_f])

        a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        a = Dense(self.dim, activation='sigmoid', kernel_initializer=xavier_initializer)(a)
        D_prob = keras.layers.Reshape(shape)(a)
        self.discriminator = keras.models.Model([x, h], D_prob, name='discriminator')
        
    def call(self, inputs):
        if isinstance(inputs, tuple):
            inputs = inputs[0]
        shape = inputs.shape
        dims = np.prod(shape[1:])
        input_width = shape[1]
        #print('inputs.shape=',inputs.shape)
        x = inputs
        #x = x.reshape((n, -1))
        #print('dims=',dims)
        #x = keras.layers.Reshape((dims,))(x)
        #x = keras.layers.Reshape(tf.TensorShape((self.dim,)))(x)
        #print('x =', x)
        #print('x.shape = ', x.shape)
        #x = keras.layers.Reshape(tf.TensorShape([57]))(x)
        
        isnan = tf.math.is_nan(x)
        #m = 1.- keras.backend.cast(isnan, dtype=tf.float32)
        m = tf.where(isnan, 0., 1.)
        z = keras.backend.random_uniform(shape=tf.shape(x), minval=0.0, maxval=0.01)
        x = tf.where(isnan, z, x)
        #z = uniform_sampler(0, 0.01, shape=x.shape)
        #z = tf.keras.backend.random_uniform(shape=x.shape, minval=0.0, maxval=0.01)
        imputed_data = self.generator([x, m], training=False)
        #imputed_data = m*x + (1-m)*imputed_data
        imputed_data = tf.where(isnan, imputed_data, np.nan)
        #imputed_data = keras.layers.Reshape(shape[1:])(imputed_data)
        #print('imputed_data.shape = ', imputed_data.shape)
        
        return imputed_data
    
    def D_loss(M, D_prob):
        ## GAIN loss
        return -tf.reduce_mean(M * tf.keras.backend.log(D_prob + 1e-8)                          + (1-M) * tf.keras.backend.log(1. - D_prob + 1e-8))
    
    def G_loss(self, M, D_prob, X, G_sample):
        G_loss_temp = -tf.reduce_mean((1-M) * tf.keras.backend.log(D_prob + 1e-8))
        MSE_loss = tf.reduce_mean((M * X - M * G_sample)**2) / (tf.reduce_mean(M) + 1e-8)
        #G_loss_temp = GAIN.G_loss_bincross(M, D_prob)
        #MSE_loss = GAIN.MSE_loss(M, X, G_sample)
        G_loss = G_loss_temp + self.alpha * MSE_loss
        return G_loss
        
    def RMSE_loss(y_true, y_pred):
        isnan = tf.math.is_nan(y_pred)
        M = tf.where(isnan, 1., 0.)
        return tf.sqrt(tf.reduce_sum(tf.where(isnan, 0., y_pred-y_true)**2)/tf.reduce_sum(1-M))
    
    def train_step(self, data):
        #[x, m, h], y = data
        x, y = data
        #X = keras.layers.Reshape((self.dim,), input_shape=self.shape)(x)
        #Y = keras.layers.Reshape((self.dim,), input_shape=self.shape)(y)
        #X = keras.layers.Flatten()(x)
        #Y = keras.layers.Flatten()(y)
        X = x
        Y = y
        #X = tf.reshape(x, shape=(x.shape[0], -1))
        #Y = tf.reshape(y, shape=(x.shape[0], -1))
        isnan = tf.math.is_nan(X)
        #M = 1 - keras.backend.cast(isnan, dtype=tf.float32)
        M = tf.where(isnan, 0., 1.)
        Z = keras.backend.random_uniform(shape=tf.shape(X), minval=0.0, maxval=0.01)
        #H_temp = binary_sampler(self.hint_rate, shape=X.shape)
        H_rand = keras.backend.random_uniform(shape=tf.shape(X), minval=0.0, maxval=1.)
        #H_temp = 1*keras.backend.cast((H_rand < self.hint_rate), dtype=tf.float32)
        H_temp = tf.where(H_rand < self.hint_rate, 1., 0.)
        
        H = M * H_temp
        #X = M * X + (1-M) * Z
        X = tf.where(isnan, Z, X)
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            G_sample = self.generator([X, M], training=True)

            # Combine with observed data
            #Hat_X = tf.where(isnan, G_sample, X)
            Hat_X = X * M + G_sample * (1-M)
            D_prob = self.discriminator([Hat_X, H], training=True)
            gen_loss = self.G_loss(M, D_prob, X, G_sample)
            disc_loss = tf.keras.backend.mean(tf.keras.losses.binary_crossentropy(M, D_prob))
            #disc_loss = GAIN.D_loss(M, D_prob)
            #disc_loss = GAIN.D_loss(M, D_prob)

        gradients_of_generator = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)

        self.generator_optimizer.apply_gradients(zip(gradients_of_generator, self.generator.trainable_variables))
        self.discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, self.discriminator.trainable_variables))
        
        rmse = tf.sqrt(tf.reduce_sum(tf.where(isnan, G_sample - Y, 0.)**2)/tf.reduce_sum(1-M))
        return {
                 'gen_loss':     gen_loss,
                 'disc_loss':    disc_loss,
                 'rmse':         rmse,
               }
    
    def save(self, save_dir='savedta'):
        if not os.path.exists(save_dir):
          os.makedirs(save_dir)
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        self.discriminator.save_weights(disc_savefile)
        self.generator.save_weights(gen_savefile)

    def load(self, save_dir='savedata'):
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        try:
          self.discriminator.load_weights(disc_savefile)
          self.generator.load_weights(gen_savefile)
          print('model weights loaded')
        except:
          print('model loadinng error')


# In[579]:


from tensorflow.keras.layers import Conv1D

class GAIN_cnn(keras.Model):
    def __init__(self, shape, alpha=100., load=False, hint_rate=0.9, gen_sigmoid=True, **kwargs):
        super(GAIN_cnn, self).__init__(**kwargs)
        self.shape = shape
        self.dim = np.prod(shape).astype(int)
        self.h_dim = self.dim
        self.gen_sigmoid = gen_sigmoid
        self.build_generator()
        self.build_discriminator()
        self.hint_rate = hint_rate
        self.alpha = alpha
        self.generator_optimizer = Adam()
        self.discriminator_optimizer = Adam()

    ## GAIN models
    def build_generator(self):
        shape = self.shape
        last_activation = 'sigmoid' if self.gen_sigmoid else None
        xavier_initializer = tf.keras.initializers.GlorotNormal()

        x = Input(shape=shape, name='generator_input_x')
        m = Input(shape=shape, name='generator_input_m')

        a = Concatenate()([x, m])

        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        #a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        #a = keras.layers.BatchNormalization()(a)
        #a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        #a = keras.layers.BatchNormalization()(a)
        #G_prob = Conv1D(filters=shape[1], kernel_size=(7,), padding='same', activation=last_activation, kernel_initializer=xavier_initializer)(a)
        a = Dense(shape[-1]*2, activation='relu', kernel_initializer=xavier_initializer)(a)
        G_prob = Dense(shape[-1], activation=last_activation, kernel_initializer=xavier_initializer)(a)
        self.generator = keras.models.Model([x, m], G_prob, name='generator')

    def build_discriminator(self):
        xavier_initializer = tf.keras.initializers.GlorotNormal()
        shape = self.shape

        x = Input(shape=shape, name='discriminator_input_x')
        h = Input(shape=shape, name='discriminator_input_h')

        a = Concatenate()([x, h])
        
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)
        a = Conv1D(filters=shape[1]*2, kernel_size=(7,), padding='same', activation='relu')(a)

        #a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        #a = Dense(self.h_dim, activation='relu', kernel_initializer=xavier_initializer)(a)
        #D_prob = Dense(self.dim, activation='sigmoid', kernel_initializer=xavier_initializer)(a)
        #D_prob = Conv1D(filters=shape[1], kernel_size=(7,), padding='same', activation='sigmoid', kernel_initializer=xavier_initializer)(a)
        a = Dense(shape[-1]*2, activation='relu', kernel_initializer=xavier_initializer)(a)
        D_prob = Dense(shape[-1], activation='sigmoid', kernel_initializer=xavier_initializer)(a)
        self.discriminator = keras.models.Model([x, h], D_prob, name='discriminator')
        
    def call(self, inputs):
        if isinstance(inputs, tuple):
            inputs = inputs[0]
        shape = inputs.shape
        #dims = np.prod(shape[1:])
        #input_width = shape[1]
        # print('inputs.shape=',inputs.shape)
        x = inputs
        #x = x.reshape((n, -1))
        #print('dims=',dims)
        #x = keras.layers.Reshape((dims,))(x)
        #x = keras.layers.Reshape(tf.TensorShape((self.dim,)))(x)
        #print('x =', x)
        #print('x.shape = ', x.shape)
        #x = keras.layers.Reshape(tf.TensorShape([57]))(x)
        
        isnan = tf.math.is_nan(x)
        #m = 1.- keras.backend.cast(isnan, dtype=tf.float32)
        m = tf.where(isnan, 0., 1.)
        z = keras.backend.random_uniform(shape=tf.shape(x), minval=0.0, maxval=0.01)
        x = tf.where(isnan, z, x)
        #z = uniform_sampler(0, 0.01, shape=x.shape)
        #z = tf.keras.backend.random_uniform(shape=x.shape, minval=0.0, maxval=0.01)
        imputed_data = self.generator([x, m], training=False)
        #imputed_data = m*x + (1-m)*imputed_data
        imputed_data = tf.where(isnan, imputed_data, np.nan)
        #imputed_data = keras.layers.Reshape(shape[1:])(imputed_data)
        #print('imputed_data.shape = ', imputed_data.shape)
        
        return imputed_data
    
    def D_loss(M, D_prob):
        ## GAIN loss
        return -tf.reduce_mean(M * tf.keras.backend.log(D_prob + 1e-8)                          + (1-M) * tf.keras.backend.log(1. - D_prob + 1e-8))
    
    def G_loss(self, M, D_prob, X, G_sample):
        G_loss_temp = -tf.reduce_mean((1-M) * tf.keras.backend.log(D_prob + 1e-8))
        MSE_loss = tf.reduce_mean((M * X - M * G_sample)**2) / (tf.reduce_mean(M) + 1e-8)
        #G_loss_temp = GAIN.G_loss_bincross(M, D_prob)
        #MSE_loss = GAIN.MSE_loss(M, X, G_sample)
        G_loss = G_loss_temp + self.alpha * MSE_loss
        return G_loss
        
    def RMSE_loss(y_true, y_pred):
        isnan = tf.math.is_nan(y_pred)
        M = tf.where(isnan, 1., 0.)
        return tf.sqrt(tf.reduce_sum(tf.where(isnan, 0., y_pred-y_true)**2)/tf.reduce_sum(1-M))
    
    def train_step(self, data):
        #[x, m, h], y = data
        x, y = data
        #X = keras.layers.Reshape((self.dim,), input_shape=self.shape)(x)
        #Y = keras.layers.Reshape((self.dim,), input_shape=self.shape)(y)
        #X = keras.layers.Flatten()(x)
        #Y = keras.layers.Flatten()(y)
        X = x
        Y = y
        #X = tf.reshape(x, shape=(x.shape[0], -1))
        #Y = tf.reshape(y, shape=(x.shape[0], -1))
        isnan = tf.math.is_nan(X)
        #M = 1 - keras.backend.cast(isnan, dtype=tf.float32)
        M = tf.where(isnan, 0., 1.)
        Z = keras.backend.random_uniform(shape=tf.shape(X), minval=0.0, maxval=0.01)
        #H_temp = binary_sampler(self.hint_rate, shape=X.shape)
        H_rand = keras.backend.random_uniform(shape=tf.shape(X), minval=0.0, maxval=1.)
        #H_temp = 1*keras.backend.cast((H_rand < self.hint_rate), dtype=tf.float32)
        H_temp = tf.where(H_rand < self.hint_rate, 1., 0.)
        
        H = M * H_temp
        #X = M * X + (1-M) * Z
        X = tf.where(isnan, Z, X)
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            G_sample = self.generator([X, M], training=True)

            # Combine with observed data
            #Hat_X = tf.where(isnan, G_sample, X)
            Hat_X = X * M + G_sample * (1-M)
            D_prob = self.discriminator([Hat_X, H], training=True)
            gen_loss = self.G_loss(M, D_prob, X, G_sample)
            disc_loss = tf.keras.backend.mean(tf.keras.losses.binary_crossentropy(M, D_prob))
            #disc_loss = GAIN.D_loss(M, D_prob)
            #disc_loss = GAIN.D_loss(M, D_prob)

        gradients_of_generator = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)

        self.generator_optimizer.apply_gradients(zip(gradients_of_generator, self.generator.trainable_variables))
        self.discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, self.discriminator.trainable_variables))
        
        rmse = tf.sqrt(tf.reduce_sum(tf.where(isnan, G_sample - Y, 0.)**2)/tf.reduce_sum(1-M))
        return {
                 'gen_loss':     gen_loss,
                 'disc_loss':    disc_loss,
                 'rmse':         rmse,
               }
    
    def save(self, save_dir='savedta'):
        if not os.path.exists(save_dir):
          os.makedirs(save_dir)
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        self.discriminator.save_weights(disc_savefile)
        self.generator.save_weights(gen_savefile)

    def load(self, save_dir='savedata'):
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        try:
          self.discriminator.load_weights(disc_savefile)
          self.generator.load_weights(gen_savefile)
          print('model weights loaded')
        except:
          print('model loadinng error')


# In[934]:


gain = GAIN(shape=(2,7))
gain.compile(loss=GAIN.RMSE_loss)
#gain_cnn = GAIN_cnn(shape=(2,7))
#gain_cnn.compile(loss=GAIN.RMSE_loss)


# In[935]:


x = np.random.random((1,2,7))
x[0][0][2] = np.nan
m = np.random.random((1,2,7))
#y = gain_cnn.generator([x, m])
y = gain.generator.predict([x, m])
print(y.shape)
y = gain.discriminator.predict([x,m])
y.shape
print(x.shape)
y = gain.predict(x)


# In[884]:


gain.fit(x,y)
#gain_cnn.fit(x,y)


# ## spam data gain 학습 테스트

# In[958]:


df_spam = pd.read_csv('data/spam.csv')
dg_spam = GainDataGenerator([df_spam], batch_size=128, input_width=1, label_width=1)
it = iter(dg_spam)
x,y = next(it)
print(dg_spam.shape)
x.shape, y.shape


# In[959]:


model = GAIN(shape=dg_spam.shape[1:])
model.compile(loss=GAIN.RMSE_loss)


# In[938]:


#model = GAIN_cnn(shape=dg_spam.shape[1:])
#model.compile(loss=GAIN.RMSE_loss)


# In[960]:


model.fit(dg_spam, batch_size=128, epochs=10)
#model.fit(x, y, batch_size=128)
#model.fit(dg_spam, batch_size=4601, epochs=1)


# In[961]:


x = dg_spam.data.copy()
y = dg_spam.data
m = dg_spam.data_m
x[m == 0] = np.nan
x = x.reshape(x.shape[0], 1, x.shape[1])
y = y.reshape(y.shape[0], 1, y.shape[1])
x.shape


#model.fit(x,y)


# In[962]:


#model.load()


# **spam data rmse 측정**

# In[963]:


print(y.shape)
ret = model.evaluate(x, y)
print(ret)


# In[964]:


x_input = x[0:4601]
y_true = y[0:4601]
y_pred = model.predict(x_input)
#print(x_input)
#print(y_true)
#print(y_pred)
isnan = np.isnan(y_pred)
diff = y_pred - y_true
diff[isnan] = 0.
#print(diff)
m = isnan.astype(int)
n = np.sum(1-m)
rmse = np.sqrt(np.sum(diff**2)/float(n))
print('rmse =', rmse)


# In[965]:


model.summary()


# **spam data dataset으로 학습하기**

# In[966]:


ds = tf.data.Dataset.from_generator(
  lambda: dg_spam,
  output_types=(tf.float32, tf.float32),
  output_shapes=(
    dg_spam.shape,
    dg_spam.shape
    #[batch_size, train_generator.dim],
    #[batch_size, train_generator.dim],
  )
).repeat(-1).prefetch(10)


# In[967]:


it = iter(ds)
x,y = next(it)
x.shape, y.shape


# In[968]:


history = model.fit(ds, steps_per_epoch=10, epochs=200)


# **학습성능 측정(rsme)**

# In[948]:


model.evaluate(ds, steps=50)


# **학습 그래프**

# In[949]:


fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()
ax.plot(history.history['gen_loss'], label='gen_loss')
ax.plot(history.history['disc_loss'], label='disc_loss')
ax2.plot(history.history['rmse'], label='rmse', color='green')
#ax2.plot(history.history['val_loss'], label='val_loss', color='red')
#plt.legend(history.history.keys(), loc='upper right')
#ax.legend(loc='upper center')
ax.legend(loc='upper center')
ax2.legend(loc='upper right')
ax.set_xlabel("epochs")
ax.set_ylabel("loss")
ax2.set_ylabel("rmse")
plt.show()


# # 수질 GAIN 데이터

# **데이터 준비**

# In[969]:


def make_dataset_gain(self, data):
  dg = GainDataGenerator(
      df,
      input_width = self.input_width,
      label_width = self.label_width,
      batch_size = 128,
      normalize = False,
      miss_pattern = True,
      miss_rate = 0.15,
      fill_no = 2,
  )
  self.dg = dg
  ds = tf.data.Dataset.from_generator(
      lambda: dg,
      output_types=(tf.float32, tf.float32),
      output_shapes=(
        dg.shape,
        dg.shape
        #[batch_size, train_generator.dim],
        #[batch_size, train_generator.dim],
      )
  )
  return ds

WindowGenerator.make_dataset = make_dataset_gain


# In[970]:


train_df = df_all
val_df = df_all
test_df = df_all


# In[971]:


wide_window = WindowGenerator(
    input_width=24*3, label_width=24*3, shift=0,
    #label_columns=['T (degC)']
)


wide_window


# In[972]:


df[0]


# In[974]:


wide_window.plot(plot_col='총질소')
print('make_dataset_gain: dg.no = ', wide_window.dg.no)


# In[975]:


plt.figure(figsize=(9,10))
isnan = np.isnan(norm_data).astype(int)
data = isnan
n = data.shape[0]
seq_len = n//8
for i in range(8):
    plt.subplot(181+i)
    plt.imshow(data[i*seq_len:(i+1)*seq_len, 0:7], aspect='auto')
    plt.yticks([])
plt.show()


# In[976]:


plt.figure(figsize=(9,10))
n = wide_window.dg.data_m.shape[0]
train = n//8
for i in range(8):
    plt.subplot(181+i)
    plt.imshow(wide_window.dg.data_m[i*train:(i+1)*train, 0:7], aspect='auto')
    plt.yticks([])
#plt.imshow(wide_window.dg.data[0:100])
#plt.imshow(wide_window.dg.data_m[800:900], aspect='auto')
#print(wide_window.dg.data[0:50])
plt.show()


# ## 컴파일 및 학습

# In[653]:


val_performance = {}
performance = {}


# In[977]:


gain = GAIN(shape=wide_window.dg.shape[1:], gen_sigmoid=False)
gain.compile(loss=GAIN.RMSE_loss)


# In[978]:


#gain = GAIN_cnn(shape=wide_window.dg.shape[1:], gen_sigmoid=False, alpha=200.)
#gain.compile(loss=GAIN.RMSE_loss)


# In[979]:


MAX_EPOCHS = 2000

def compile_and_fit(model, window, patience=10):
  early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

  #model.compile(loss=tf.losses.MeanSquaredError(),
                #optimizer=tf.optimizers.Adam(),
                #metrics=[tf.metrics.MeanAbsoluteError()])
  model.compile(loss=GAIN.RMSE_loss)

  history = model.fit(window.train, epochs=MAX_EPOCHS,
                      validation_data=window.val,
                      callbacks=[early_stopping])
  return history


# In[980]:


history = compile_and_fit(gain, wide_window, patience=MAX_EPOCHS//5)


val_performance['Gain'] = gain.evaluate(wide_window.val)
performance['Gain'] = gain.evaluate(wide_window.test, verbose=0)


#early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
#                                                    patience=2,
#                                                    mode='min')
#gain.compile()


# **학습 loss history 출력**

# In[913]:


fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()
ax.plot(history.history['gen_loss'], label='gen_loss')
ax.plot(history.history['disc_loss'], label='disc_loss')
ax2.plot(history.history['rmse'], label='rmse', color='green')
ax2.plot(history.history['val_loss'], label='val_loss', color='red')
#plt.legend(history.history.keys(), loc='upper right')
#ax.legend(loc='upper center')
ax.legend(loc='upper center')
ax2.legend(loc='upper right')
ax.set_xlabel("epochs")
ax.set_ylabel("loss")
ax2.set_ylabel("rmse")
plt.show()


# 성능 측정

# In[914]:


gain.evaluate(wide_window.test.repeat(), steps=100)


# 샘플 prediction 출력

# In[915]:


wide_window.plot(gain, plot_col='클로로필-a')


# ## 학습데이터 테스트

# In[916]:


total_n = wide_window.dg.data.shape[0]
print(total_n)
unit_shape = wide_window.dg.shape[1:]
print(unit_shape)
dim = np.prod(wide_window.dg.shape[1:]).astype(int)
print(dim)
n = (total_n//dim)*dim
print(n)
x = wide_window.dg.data[0:n].copy()
y = wide_window.dg.data[0:n].copy()
m = wide_window.dg.data_m[0:n]
x[m == 0] = np.nan
print('x.shape =', x.shape)
x = x.reshape((-1,)+unit_shape)
y_true = y.reshape((-1,)+unit_shape)
print('x.shape =', x.shape)


# In[917]:


y_pred = gain.predict(x)


# In[918]:


y_pred = y_pred.reshape((n, 13))
x = x.reshape((n, 13))


# In[919]:


x.shape


# In[920]:


plt.figure()
plt.plot(x[:, 8])
plt.plot(y_pred[:, 8])
plt.show()


# ## 원본 데이터 테스트

# In[921]:


norm_df = pd.concat(df,axis=0)


# In[922]:


data = norm_df.to_numpy()
x = data[0:n].copy()
y_true = data[0:n].copy()
isnan = np.isnan(x)
x[isnan] = np.nan

total_n = wide_window.dg.data.shape[0]
print(total_n)
unit_shape = wide_window.dg.shape[1:]
print(unit_shape)
dim = np.prod(wide_window.dg.shape[1:]).astype(int)
print(dim)
n = (total_n//dim)*dim

print('x.shape =', x.shape)
x_reshape = x.reshape((-1,)+unit_shape)
print('x_reshape.shape =', x_reshape.shape)


# In[923]:


y_pred = gain.predict(x_reshape)


# In[924]:


y_pred = y_pred.reshape(y_true.shape)
y_pred.shape


# In[925]:


n = 8
plt.figure(figsize=(9,20))
for i in range(n):
    #plt.subplot('%d1%d'%(n,i))
    plt.subplot(811+i)
    plt.plot(x[:, i])
    plt.plot(y_pred[:, i])
plt.show()


# ## 연습 섹션

# In[78]:


it = iter(wide_window.val)
x,y = next(it)


# In[79]:


x.shape, y.shape


# In[80]:


history = gain.fit(wide_window.train, epochs=20,
                      validation_data=wide_window.val,
                      callbacks=[])


# In[81]:


it = iter(wide_window.val)
x,y = next(it)
x.shape, y.shape


# In[82]:


gain.predict(x)


# In[83]:


df[0].isna().astype(int).sum()


# In[84]:


date_time1 = pd.to_datetime(df_full[0].iloc[:, 0], format='%Y.%m.%d %H:%M')
date_time2 = pd.to_datetime(df_full[0].iloc[:, 0], format='%Y.%m.%d %H:%M')


# In[85]:


timestamp_s1 = date_time1.map(datetime.datetime.timestamp)
timestamp_s2 = date_time2.map(datetime.datetime.timestamp)


# In[86]:


day = 24*60*60
year = (365.2425)*day

df[0]['Day sin'] = np.sin(timestamp_s1 * (2 * np.pi / day))
df[0]['Day cos'] = np.cos(timestamp_s1 * (2 * np.pi / day))
df[0]['Year sin'] = np.sin(timestamp_s1 * (2 * np.pi / year))
df[0]['Year cos'] = np.cos(timestamp_s1 * (2 * np.pi / year))

df[1]['Day sin'] = np.sin(timestamp_s2 * (2 * np.pi / day))
df[1]['Day cos'] = np.cos(timestamp_s2 * (2 * np.pi / day))
df[1]['Year sin'] = np.sin(timestamp_s2 * (2 * np.pi / year))
df[1]['Year cos'] = np.cos(timestamp_s2 * (2 * np.pi / year))


# In[87]:


class CustomModel(keras.Model):
    def train_step(self, data):
        print(data[0].shape)
        # Unpack the data. Its structure depends on your model and
        # on what you pass to `fit()`.
        x, y = data

        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)  # Forward pass
            # Compute the loss value
            # (the loss function is configured in `compile()`)
            loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        # Update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)
        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}


# In[88]:


import numpy as np

# Construct and compile an instance of CustomModel
inputs = keras.Input(shape=(32,))
outputs = keras.layers.Dense(1)(inputs)
model = CustomModel(inputs, outputs)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Just use `fit` as usual
x = np.random.random((1000, 32))
y = np.random.random((1000, 1))
model.fit(x, y, epochs=3)


# In[89]:


ds = tf.data.Dataset.from_tensor_slices((x,y))


# In[90]:


ds.element_spec


# In[91]:


ds = ds.batch(5)
ds.element_spec


# In[109]:


df2


# In[92]:


model.fit(ds)


# # MNIST with data generator
# 
# https://towardsdatascience.com/keras-custom-data-generators-example-with-mnist-dataset-2a7a2d2b0360
# 

# In[93]:


import tensorflow as tf
import os
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import numpy as np
import math


# In[94]:


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


# In[95]:


class DataGenerator(tf.compat.v2.keras.utils.Sequence):
 
    def __init__(self, X_data , y_data, batch_size, dim, n_classes,
                 to_fit, shuffle = True):
        self.batch_size = batch_size
        self.X_data = X_data
        self.labels = y_data
        self.y_data = y_data
        self.to_fit = to_fit
        self.n_classes = n_classes
        self.dim = dim
        self.shuffle = shuffle
        self.n = 0
        self.list_IDs = np.arange(len(self.X_data))
        self.on_epoch_end()
    def __next__(self):
        # Get one batch of data
        data = self.__getitem__(self.n)
        # Batch index
        self.n += 1
        
        # If we have processed the entire dataset then
        if self.n >= self.__len__():
            self.on_epoch_end
            self.n = 0
        
        return data
    def __len__(self):
        # Return the number of batches of the dataset
        return math.ceil(len(self.indexes)/self.batch_size)
    def __getitem__(self, index):
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:
            (index+1)*self.batch_size]
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        
        X = self._generate_x(list_IDs_temp)
        
        if self.to_fit:
            y = self._generate_y(list_IDs_temp)
            return X, y
        else:
            return X
    def on_epoch_end(self):
        
        self.indexes = np.arange(len(self.X_data))
        
        if self.shuffle: 
            np.random.shuffle(self.indexes)
    def _generate_x(self, list_IDs_temp):
               
        X = np.empty((self.batch_size, *self.dim))
        
        for i, ID in enumerate(list_IDs_temp):
            
            X[i,] = self.X_data[ID]
            
            # Normalize data
            X = (X/255).astype('float32')
            
        return X[:,:,:, np.newaxis]
    def _generate_y(self, list_IDs_temp):
        
        y = np.empty(self.batch_size)
        
        for i, ID in enumerate(list_IDs_temp):
            
            y[i] = self.y_data[ID]
            
        return keras.utils.to_categorical(
                y,num_classes=self.n_classes)


# In[96]:


n_classes = 10
input_shape = (28, 28)
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(28, 28 , 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(n_classes, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])


# In[97]:


train_generator = DataGenerator(x_train, y_train, batch_size = 64,
                                dim = input_shape,
                                n_classes=10, 
                                to_fit=True, shuffle=True)
val_generator =  DataGenerator(x_test, y_test, batch_size=64, 
                               dim = input_shape, 
                               n_classes= n_classes, 
                               to_fit=True, shuffle=True)


# In[98]:


steps_per_epoch = len(train_generator)
validation_steps = len(val_generator)


# In[99]:


model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=1,
        validation_data=val_generator,
        validation_steps=validation_steps)


# In[100]:


it = iter(train_generator)


# In[101]:


x,y = next(it)


# In[102]:


x.shape


# In[103]:


y.shape


# ## MNIST with custom model

# In[104]:


n_classes = 10
input_shape = (28, 28, 1)
input_data = keras.layers.Input(shape=input_shape)
x = Conv2D(32, kernel_size=(3, 3),
                 activation='relu')(input_data)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Dropout(0.25)(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output_data = Dense(n_classes, activation='softmax')(x)
model = CustomModel(input_data, output_data)
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])


# In[105]:


model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=1,
        validation_data=val_generator,
        validation_steps=validation_steps)


# 결론: DataGenerator 만으로는 train_step에 input data의 shape에 None으로 들어간다.
# 
# ```py
#         X = keras.layers.Reshape((tf.reduce_sum(x.shape[1:]),))(x)
#         Y = keras.layers.Reshape((tf.reduce_sum(x.shape[1:]),))(y)
#         X = tf.reshape(x, shape=(x.shape[0], -1))
#         Y = tf.reshape(y, shape=(x.shape[0], -1)
# ```
# 
# 이런 함수들을 train_step 내에 사용할 수 없다

# # 한글 폰트

# In[106]:




import matplotlib
import matplotlib.font_manager

[f.fname for f in matplotlib.font_manager.fontManager.ttflist]


# In[107]:


get_ipython().system(' fc-list :lang=ko')


# In[108]:


import matplotlib
import matplotlib.font_manager as fm
fm.get_fontconfig_fonts()
font_location = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
#font_location = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# font_location = 'C:/Windows/Fonts/NanumGothic.ttf' # For Windows
fprop = fm.FontProperties(fname=font_location)


# In[109]:


fig = plt.figure()  
plt.plot((1,1), label='가-가가')  
plt.title('가가가',fontproperties=fprop)  
plt.legend(prop=fprop)  
plt.show()


# In[ ]:




