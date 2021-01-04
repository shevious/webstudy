#!/usr/bin/env python
# coding: utf-8

# In[705]:


get_ipython().run_line_magic('matplotlib', 'widget')


# In[3]:


import pandas as pd
import numpy as np
from glob import glob
import os
import datetime
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Input, Concatenate, Dot, Add, ReLU, Activation
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from tensorflow import keras


# In[701]:


# missing date 추가
folder = 'data'
#file_names = [['가평_2016.xlsx','가평_2017.xlsx','가평_2018.xlsx', '가평_2019.xlsx'], ['의암호_2016.xlsx','의암호_2017.xlsx','의암호_2018.xlsx', '의암호_2019.xlsx']]
file_name0 = '가평_2019.xlsx'
#file_name1 = '해평_2016.xlsx'
file_name1 = '도개_2019.xlsx'
#file_name1 = '의암호_2017.xlsx'

path = os.path.join(folder, file_name0)
df0 = pd.read_excel(path)
path = os.path.join(folder, file_name1)
df1 = pd.read_excel(path)
print(df0.shape)
print(df1.shape)

date_full = df0.iloc[:, 0]
fill = { col: np.nan for col in df1.columns}

j = 0
for i in range(len(date_full)):
    #print(i, date_full[i])
    #print(df1.iloc[j])
    #print(df1.iloc[j,0])
    while df1.iloc[j, 0][5:10] == '02.29':
        j += 1
    if df1.iloc[j, 0][5:] != date_full[i][5:]:
        print(i, date_full[i], j, df1.iloc[j,0])
        fill_date = df1.iloc[j,0][:5] + date_full[i][5:]
        #print(fill_date)
        fill[df1.columns[0]] = fill_date
        #print(fill)
        line = pd.DataFrame(fill, index=[j-0.5])
        df1 = df1.append(line, ignore_index=False)
        df1 = df1.sort_index().reset_index(drop=True)
    j += 1
print(i+1,j)
df1.to_excel(path, index=False)


# In[836]:


df1


# In[703]:


df1


# In[704]:


df0


# **한강 데이터 로딩**

# In[706]:


folder = 'data'
file_names = [['가평_2016.xlsx','가평_2017.xlsx','가평_2018.xlsx', '가평_2019.xlsx'], ['의암호_2016.xlsx','의암호_2017.xlsx','의암호_2018.xlsx', '의암호_2019.xlsx']]
#file_names = [['해평_2016.xlsx','해평_2017.xlsx','해평_2018.xlsx', '해평_2019.xlsx'], ['도개_2016.xlsx','도개_2017.xlsx','도개_2018.xlsx', '도개_2019.xlsx']]
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
    df.append(df_full[loc].iloc[:, [2,3,4,5,6,7,10]])
    date_time = pd.to_datetime(df_full[loc].iloc[:, 0], format='%Y.%m.%d %H:%M', utc=True)
    timestamp_s = date_time.map(datetime.datetime.timestamp)
    df[loc]['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df[loc]['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df[loc]['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df[loc]['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    df[loc] = df[loc].reset_index(drop=True)
        


# **낙동강 해평-도개**

# In[498]:


folder = 'data'
#file_names = [['가평_2016.xlsx','가평_2017.xlsx','가평_2018.xlsx', '가평_2019.xlsx'], ['의암호_2016.xlsx','의암호_2017.xlsx','의암호_2018.xlsx', '의암호_2019.xlsx']]
file_names = [['해평_2016.xlsx','해평_2017.xlsx','해평_2018.xlsx', '해평_2019.xlsx'], ['도개_2016.xlsx','도개_2017.xlsx','도개_2018.xlsx', '도개_2019.xlsx']]
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
    if loc == 0:
        df.append(df_full[loc].iloc[:, 2:9])
    else:
        df.append(df_full[loc].iloc[:, [2,3,4,5,6,7,10]])
    date_time = pd.to_datetime(df_full[loc].iloc[:, 0], format='%Y.%m.%d %H:%M', utc=True)
    timestamp_s = date_time.map(datetime.datetime.timestamp)
    df[loc]['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df[loc]['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df[loc]['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df[loc]['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    df[loc] = df[loc].reset_index(drop=True)
        


# In[707]:


df[0]


# In[708]:


df[1]


# In[710]:


# normalize data

df_all = pd.concat(df)
df_all

train_mean = df_all.mean()
train_std = df_all.std()
for i in range(len(file_names)):
    df[i] = (df[i]-train_mean)/train_std


# In[711]:


print(df_all.shape)


# In[712]:


train_mean, train_std


# In[713]:


df[0]


# In[714]:


train_df = df[0]
val_df = df[0]
test_df = df[0]


# In[715]:


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


# In[716]:


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


# In[717]:


import matplotlib
import matplotlib.font_manager as fm
fm.get_fontconfig_fonts()
font_location = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
#font_location = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# font_location = 'C:/Windows/Fonts/NanumGothic.ttf' # For Windows
fprop = fm.FontProperties(fname=font_location)


# In[718]:


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


# In[719]:


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


# **WindowGenerator 테스트**

# In[ ]:


w2 = WindowGenerator(input_width=6, label_width=1, shift=1,
                     label_columns=None)
w2


# In[ ]:


w1 = WindowGenerator(input_width=24, label_width=1, shift=1,
                     label_columns='수온')
w1


# In[ ]:


# Stack three slices, the length of the total window:
example_window = tf.stack([np.array(train_df[:w2.total_window_size]),
                           np.array(train_df[100:100+w2.total_window_size]),
                           np.array(train_df[200:200+w2.total_window_size])])


example_inputs, example_labels = w2.split_window(example_window)

print('All shapes are: (batch, time, features)')
print(f'Window shape: {example_window.shape}')
print(f'Inputs shape: {example_inputs.shape}')
print(f'labels shape: {example_labels.shape}')


# In[ ]:


w2.example = example_inputs, example_labels


# In[ ]:


w2.plot(plot_col='수온')


# **Window Generator trainset 정의**

# In[720]:


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


# In[721]:


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


# In[722]:


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


# In[723]:


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


# In[724]:


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


# In[725]:


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


# **miss_data 테스트**

# In[726]:


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

# In[727]:


norm_df = pd.concat(df,axis=0)
norm_data = norm_df.to_numpy()
MissData.save(norm_data, max_tseq = 24)


# In[728]:


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


# In[731]:


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
            #shift same as pd.shift(isany, fill_value=True)
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
        
            Y_mb = self.data[idx1:idx2].copy()
            X_mb = Y_mb.copy()
            M_mb = self.data_m[idx1:idx2]
            Z_mb = uniform_sampler(0, 0.01, shape=X_mb.shape)
            X_mb = M_mb*X_mb + (1-M_mb)*Z_mb
            #H_mb_temp = binary_sampler(self.hint_rate, shape=X_mb.shape)
            #H_mb = M_mb * H_mb_temp
            X_mb[M_mb == 0] = np.nan
            Y_mb[M_mb == 1] = np.nan
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


# In[730]:


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
        #imputed_data = tf.where(isnan, imputed_data, np.nan)
        imputed_data = tf.where(isnan, imputed_data, x)
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
        isnan = tf.math.is_nan(y_true)
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
        
        H = M * H_temp + 0.5*(1-H_temp)
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
    
    def save(self, save_dir='save'):
        if not os.path.exists(save_dir):
          os.makedirs(save_dir)
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        self.discriminator.save_weights(disc_savefile)
        self.generator.save_weights(gen_savefile)

    def load(self, save_dir='save'):
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        try:
          self.discriminator.load_weights(disc_savefile)
          self.generator.load_weights(gen_savefile)
          print('model weights loaded')
        except:
          print('model loadinng error')


# In[464]:


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
        #imputed_data = tf.where(isnan, imputed_data, np.nan)
        imputed_data = tf.where(isnan, imputed_data, x)
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
    
    def save(self, save_dir='save'):
        if not os.path.exists(save_dir):
          os.makedirs(save_dir)
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        self.discriminator.save_weights(disc_savefile)
        self.generator.save_weights(gen_savefile)

    def load(self, save_dir='save'):
        disc_savefile = os.path.join(save_dir, 'discriminator.h5')
        gen_savefile = os.path.join(save_dir, 'generator.h5')
        try:
          self.discriminator.load_weights(disc_savefile)
          self.generator.load_weights(gen_savefile)
          print('model weights loaded')
        except:
          print('model loadinng error')


# **GAIN 모델 test**

# In[420]:


gain = GAIN(shape=(2,7))
gain.compile(loss=GAIN.RMSE_loss)
#gain_cnn = GAIN_cnn(shape=(2,7))
#gain_cnn.compile(loss=GAIN.RMSE_loss)


# In[ ]:


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


# In[ ]:


gain.fit(x,y)
#gain_cnn.fit(x,y)


# ## spam data gain 학습 테스트

# In[732]:


df_spam = pd.read_csv('data/spam.csv')
dg_spam = GainDataGenerator([df_spam], batch_size=128, input_width=1, label_width=1)
it = iter(dg_spam)
x,y = next(it)
print(dg_spam.shape)
x.shape, y.shape


# In[745]:


model = GAIN(shape=dg_spam.shape[1:])
model.compile(loss=GAIN.RMSE_loss)


# In[ ]:


#model = GAIN_cnn(shape=dg_spam.shape[1:])
#model.compile(loss=GAIN.RMSE_loss)


# In[746]:


model.fit(dg_spam, batch_size=128, epochs=30)
#model.fit(x, y, batch_size=128)
#model.fit(dg_spam, batch_size=4601, epochs=1)


# In[ ]:


x = dg_spam.data.copy()
y = dg_spam.data.copy()
m = dg_spam.data_m
x[m == 0] = np.nan
y[m == 1] = np.nan
x = x.reshape(x.shape[0], 1, x.shape[1])
y = y.reshape(y.shape[0], 1, y.shape[1])
x.shape


#model.fit(x,y)


# In[ ]:


#model.load()


# **spam data rmse 측정**

# In[738]:


print(y.shape)
ret = model.evaluate(x, y)
print(ret)


# In[739]:


x_input = x[0:4601]
y_true = y[0:4601]
y_pred = model.predict(x_input)
#print(x_input)
#print(y_true)
#print(y_pred)
isnan = np.isnan(y_true)
diff = y_pred - y_true
diff[isnan] = 0.
#print(diff)
m = isnan.astype(int)
n = np.sum(1-m)
rmse = np.sqrt(np.sum(diff**2)/float(n))
print('rmse =', rmse)


# In[ ]:


model.summary()


# **spam data dataset으로 학습하기**

# In[747]:


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


# In[748]:


it = iter(ds)
x,y = next(it)
x.shape, y.shape


# In[749]:


history = model.fit(ds, steps_per_epoch=10, epochs=1000)


# **학습성능 측정(rsme)**

# In[750]:


model.evaluate(ds, steps=50)


# **학습 그래프**

# In[751]:


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

# In[828]:


def make_dataset_gain(self, data):
  dg = GainDataGenerator(
      df,
      input_width = self.input_width,
      label_width = self.label_width,
      batch_size = 128,
      normalize = False,
      miss_pattern = True,
      miss_rate = 0.15,
      fill_no = 3,
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


# In[753]:


train_df = df_all
val_df = df_all
test_df = df_all


# In[832]:


wide_window = WindowGenerator(
    input_width=24*5, label_width=24*5, shift=0,
    #label_columns=['T (degC)']
)

wide_window


# In[834]:


_ = wide_window.train


# In[835]:


wide_window.dg


# In[755]:


wide_window.example[0].shape


# **학습용 데이터 plotting**

# In[756]:


df[0]


# In[757]:


df[1]


# In[758]:


wide_window.plot(plot_col='클로로필-a')
print('make_dataset_gain: dg.no = ', wide_window.dg.no)


# In[759]:


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


# In[760]:


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

# In[761]:


val_performance = {}
performance = {}


# In[762]:


gain = GAIN(shape=wide_window.dg.shape[1:], gen_sigmoid=False)
gain.compile(loss=GAIN.RMSE_loss)


# In[542]:


#gain = GAIN_cnn(shape=wide_window.dg.shape[1:], gen_sigmoid=False, alpha=200.)
#gain.compile(loss=GAIN.RMSE_loss)


# In[763]:


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


# **모델 불러오기(사전 학습데이터)**

# In[580]:


#model.fit를 사용하지 않을 때에는 학습 데이터 로딩
gain.load(save_dir='save')


# **모델 학습**

# In[764]:


history = compile_and_fit(gain, wide_window, patience=MAX_EPOCHS//5)


val_performance['Gain'] = gain.evaluate(wide_window.val)
performance['Gain'] = gain.evaluate(wide_window.test, verbose=0)


#early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
#                                                    patience=2,
#                                                    mode='min')
#gain.compile()


# In[478]:


gain.save(save_dir='save')


# **학습 loss history 출력**

# In[765]:


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

# In[766]:


gain.evaluate(wide_window.test.repeat(), steps=100)


# 샘플 prediction 출력

# In[767]:


wide_window.plot(gain, plot_col='클로로필-a')


# ## 학습데이터 테스트

# In[ ]:


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
y[m == 1] = np.nan
print('x.shape =', x.shape)
x = x.reshape((-1,)+unit_shape)
y_true = y.reshape((-1,)+unit_shape)
print('x.shape =', x.shape)


# In[ ]:


y_pred = gain.predict(x)


# In[ ]:


y_pred = y_pred.reshape((n, 13))
x = x.reshape((n, 13))


# In[ ]:


x.shape


# In[ ]:


y_pred[~np.isnan(x)] = np.nan
plt.figure()
plt.plot(x[:, 8])
plt.plot(y_pred[:, 8])
plt.show()


# ## 원본 데이터 테스트

# **원본데이터 shape**
# ```py
# print(norm_df.shape)
# (70068,13)
# (rows, columns)
# ```
# 데이터 generator의 shape
# ```py
# print(wide_window.dg.shape)
# (128, 120, 13)
# (batch_size, input_width, column)
# ```
# ```py
# total_no = 70068
# dim = 120*13
# n = total_no//dim*dim
# x.shape
# (68640, 13)
# x.reshape( (-1, 120, 13) )
# ```

# In[ ]:





# In[768]:


norm_df = pd.concat(df,axis=0)


# In[769]:


data = norm_df.to_numpy()

total_n = wide_window.dg.data.shape[0]
print(total_n)
unit_shape = wide_window.dg.shape[1:]
print(unit_shape)
#dim = np.prod(wide_window.dg.shape[1:]).astype(int)
dim = wide_window.dg.shape[1]
print(dim)
n = (total_n//dim)*dim

x = data[0:n].copy()
y_true = data[0:n].copy()

#x = interpolate(x, max_gap=3)

print('x.shape =', x.shape)
x_reshape = x.reshape((-1,)+unit_shape)
print('x_reshape.shape =', x_reshape.shape)
isnan = np.isnan(x_reshape)
print(isnan.sum())
print('y_true.shape=', y_true.shape)
isnan = np.isnan(y_true)
print(isnan.sum())

x_remain = data[-wide_window.dg.shape[1]:].copy()
x_remain_reshape = x_remain.reshape((-1,)+unit_shape)
x_remain_reshape.shape


# In[770]:


# zero loss is normal because there is no ground truth in the real dataset
gain.evaluate(x_reshape, y_true.reshape((-1,)+unit_shape))


# In[771]:


y_pred = gain.predict(x_reshape)
y_remain_pred = gain.predict(x_remain_reshape)


# In[772]:


print(total_n)
print(n)
print(total_n-n)


# In[773]:


y_pred = y_pred.reshape(y_true.shape)
y_remain_pred = y_remain_pred.reshape(x_remain.shape)
print(y_pred.shape, y_remain_pred.shape)
y_pred = np.append(y_pred, y_remain_pred[-(total_n-n):], axis=0)
print(y_pred.shape)


# 그림용으로 nan 채우기

# In[774]:


y_pred[~np.isnan(data)] = np.nan


# In[775]:


n = 8
plt.figure(figsize=(9,20))
for i in range(n):
    #plt.subplot('%d1%d'%(n,i))
    plt.subplot(811+i)
    plt.plot(x[:, i])
    plt.plot(y_pred[:, i])
plt.show()


# In[776]:


total_n = wide_window.dg.data.shape[0]
print(total_n)
unit_shape = wide_window.dg.shape[1:]
print('unit_shape=', unit_shape)
time_seq = unit_shape[0]
print(time_seq)
n = (total_n//time_seq)*time_seq
print('n=', n)

gans = []
oris = []
for i in range(len(df)):
    x = df[i].to_numpy()
    total_n = x.shape[0]
    n = (total_n//time_seq)*time_seq
    x = x[0:n]
    x_block = x.reshape((-1,)+unit_shape)
    y = gain.predict(x_block)
    y_gan = y.reshape(x.shape)
    
    # cut off sin, cos data
    if (i > 0):
        x = x[:, :-4]
        y_gan = y_gan[:, :-4]
    gans.append(y_gan)
    oris.append(x)
print(x.shape)
print(y_gan.shape)


# In[777]:


# idx번째 데이터 출력
idx = 0
y_plt = gans[idx].copy()
y_plt[~np.isnan(oris[idx])] = np.nan
n = 8
plt.figure(figsize=(9,20))
for i in range(n):
    #plt.subplot('%d1%d'%(n,i))
    plt.subplot(811+i)
    plt.plot(oris[idx][:, i])
    plt.plot(y_plt[:, i])
plt.show()


# **self data 생성(가평)**

# In[ ]:


total_no = oris[0].shape[0]
train_no = int(total_no*0.7)

train_slice = slice(0, train_no)
val_slice = slice(train_no, None)
test_slice = slice(0, None)

train_df = pd.DataFrame(gans[0][train_slice])
val_df = pd.DataFrame(gans[0][val_slice])
test_df = pd.DataFrame(gans[0][test_slice])

train_ori_df = pd.DataFrame(oris[0][train_slice])
val_ori_df = pd.DataFrame(oris[0][val_slice])
test_ori_df = pd.DataFrame(oris[0][test_slice])

num_features = train_df.shape[1]
out_num_features = num_features


# **source-target data creation (target-가평, source-의암호)**

# In[778]:


ori = np.concatenate(oris, axis=1)
gan = np.concatenate(gans, axis=1)
print(oris[0].shape, gans[0].shape)
print(oris[1].shape, gans[1].shape)
print(ori.shape, gan.shape)

total_no = ori.shape[0]
train_no = int(total_no*0.7)

train_slice = slice(0, train_no)
val_slice = slice(train_no, None)
test_slice = slice(0, None)

train_df = pd.DataFrame(gan[train_slice])
val_df = pd.DataFrame(gan[val_slice])
test_df = pd.DataFrame(gan[test_slice])

train_ori_df = pd.DataFrame(ori[train_slice])
val_ori_df = pd.DataFrame(ori[val_slice])
test_ori_df = pd.DataFrame(ori[test_slice])

num_features = train_df.shape[1]
#out_num_features = oris[0].shape[1]-4
out_features = [6]
out_num_features = len(out_features)
out_num_features


# In[779]:


class WaterDataGenerator(keras.utils.Sequence):
    'Generates data for water'
    def __init__(self,
                 imputed_data,
                 ori_data = None,
                 batch_size=32,
                 input_width=24*7,
                 label_width=24*3,
                 shift=24*3,
                 skip_time = None,
                 shuffle = True,
                 out_features = None,
                 out_num_features = None,
                ):
        'Initialization'
        self.window_size = input_width+shift
        self.total_no = imputed_data.shape[0]
        self.data = imputed_data
        self.input_width = input_width
        self.label_width = label_width
        self.batch_size = batch_size
        self.input_shape = (batch_size, input_width, self.data.shape[1])
        self.out_num_features = out_num_features
        if out_features:
            self.out_features = out_features
        else:
            self.out_features = [i for i in range(out_num_features)]
        self.label_shape = (batch_size, label_width, self.out_num_features)
        if (skip_time):
            # TO-DO
            self.no = self.total_no - self.window_size
            self.data_idx = np.arange(0, self.no)
        else:
            self.no = self.total_no - self.window_size
            self.data_idx = np.arange(0, self.no)
            
        if shuffle:
            self.batch_idx = np.random.permutation(self.no)
        else:
            self.batch_idx = np.arange(0, self.no)
        self.batch_id = 0
        
        
    def __len__(self):
        'Denotes the number of batches per epoch'
        #return int(128/self.batch_size)
        #return 2
        return 1

    def __getitem__(self, index):
        'Generate one batch of data'
        #print('index =', index)
        #print('self.no =', self.no)
        #print('self.total_no =', self.total_no)
        #print('self.batch_id =', self.batch_id)
        # Sample batch
        label_width = self.label_width
        batch_idx = self.batch_idx
        
        x = np.empty((0, self.input_width, self.data.shape[1]))
        y = np.empty((0, self.label_width, self.out_num_features))
        for cnt in range(0, self.batch_size):
            i = self.batch_id
            self.batch_id += 1
            idx1 = self.data_idx[batch_idx[i]]
            idx2 = idx1 + self.input_width
            
            X = self.data[idx1:idx2]
            
            idx1 = self.data_idx[batch_idx[i]] + self.window_size - label_width
            idx2 = idx1 + label_width
            
            #Y = self.data[idx1:idx2,:,:out_num_features]
            Y = self.data.iloc[idx1:idx2, self.out_features]
            #print('Y.shape = ', Y.shape)
            #Y = Y.iloc[:,:out_num_features]
            
            self.batch_id %= self.no
            
            x = np.append(x, [X], axis = 0)
            y = np.append(y, [Y], axis = 0)
            
        return x, y
    
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        return


# In[780]:


def make_dataset_water(self, data):
  dg = WaterDataGenerator(
      data,
      batch_size = 128,
      input_width = self.input_width,
      label_width = self.label_width,
      shift = self.label_width,
      out_features = out_features,
      out_num_features = out_num_features,
  )
  #self.dg = dg
  ds = tf.data.Dataset.from_generator(
      lambda: dg,
      output_types=(tf.float32, tf.float32),
      output_shapes=(
        dg.input_shape,
        dg.label_shape
        #[batch_size, train_generator.dim],
        #[batch_size, train_generator.dim],
      )
  )
  return ds

WindowGenerator.make_dataset = make_dataset_water


# **WaterDataGenerator 테스트**

# In[341]:


wdg = WaterDataGenerator(train_df,
                         batch_size=128,
                         input_width = 24*7,
                         label_width = OUT_STEPS,
                         shift = OUT_STEPS,
                         out_num_features = out_num_features
                        )


# In[247]:


it = iter(wdg)


# In[248]:


x,y = next(it)
x.shape, y.shape


# **Water Dataset**

# In[781]:


def plot2(self, model=None, plot_col=0, max_subplots=3, plot_out_col=0):
  inputs, labels = self.example
  plt.figure(figsize=(10, 8))
  plot_col_index = self.column_indices[plot_col]
  plot_out_col_index = self.column_indices[plot_out_col]
  max_n = min(max_subplots, len(inputs))
  for n in range(max_n):
    plt.subplot(3, 1, n+1)
    plt.ylabel(f'{plot_col} [normed]', fontproperties=fprop)
    plt.plot(self.input_indices, inputs[n, :, plot_col_index],
             label='Inputs', marker='.', zorder=-10)

    if self.label_columns:
      label_col_index = self.label_columns_indices.get(plot_col, None)
      label_out_col_index = self.label_columns_indices.get(plot_out_col, None)
    else:
      label_col_index = plot_col_index
      label_out_col_index = plot_out_col_index

    if label_col_index is None:
      continue

    plt.plot(self.label_indices, labels[n, :, label_out_col_index],
                label='Labels', c='#2ca02c')
    if model is not None:
      predictions = model(inputs)
      plt.plot(self.label_indices, predictions[n, :, label_out_col_index],
                  marker=None, label='Predictions',
                  c='#ff7f0e')

    if n == 0:
      plt.legend()

  plt.xlabel('Time [h]')

WindowGenerator.plot2 = plot2


# In[782]:


OUT_STEPS = 24*5
multi_window = WindowGenerator(input_width=24*7,
                               label_width=OUT_STEPS,
                               shift=OUT_STEPS,
                               train_df=train_df,
                               val_df=val_df,
                               test_df=test_df,
                               )

multi_window.plot2(plot_col=out_features[0])
multi_window


# In[783]:


multi_window.plot2(plot_col=out_features[0])


# In[784]:


it = iter(multi_window.train)
x, y = next(it)
print(x.shape, y.shape)
#x, y = next(it#)


# **Baseline model**

# In[785]:


class MultiStepLastBaseline(tf.keras.Model):
  def call(self, inputs):
    #print(inputs[:, -1:, 0:1])
    #return tf.tile(inputs[:, -1:, :out_num_features], [1, OUT_STEPS, 1])
    return tf.tile(inputs[:, -1:, (out_features[0]):(out_features[0]+1)], [1, OUT_STEPS, 1])
    #return tf.tile(inputs[:, -1:, out_features[0]:(out_features[1]+1)], [1, OUT_STEPS, 1])

last_baseline = MultiStepLastBaseline()
last_baseline.compile(loss=tf.losses.MeanSquaredError(),
                      metrics=[tf.metrics.MeanAbsoluteError()])

#multi_val_performance = {}
#multi_performance = {}

multi_val_performance['Last'] = last_baseline.evaluate(multi_window.val.repeat(-1), steps=100)
multi_performance['Last'] = last_baseline.evaluate(multi_window.test.repeat(-1), verbose=0, steps=100)
print('val performance =', multi_val_performance['Last'])
print('test performance = ', multi_performance['Last'])
multi_window.plot2(last_baseline, plot_col=out_features[0], plot_out_col=0)


# **Water Data Generator test**

# In[67]:


wdg = WaterDataGenerator(
    train_df,
    batch_size = 32,
    input_width = 7,
    label_width = 3,
    shift = 3,
)


# In[ ]:


it = iter(wdg)
x, y = next(it)
x.shape, y.shape


# In[ ]:


last_baseline.evaluate(wdg)


# **학습**

# In[786]:


MAX_EPOCHS = 400

def compile_and_fit(model, window, patience=1000):
  early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

  model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError()])
  #model.compile(loss=GAIN.RMSE_loss)

  history = model.fit(window.train, epochs=MAX_EPOCHS,
                      validation_data=window.val,
                      callbacks=[early_stopping])
  return history


# In[787]:


import IPython
multi_linear_model = tf.keras.Sequential([
    # Take the last time-step.
    # Shape [batch, time, features] => [batch, 1, features]
    tf.keras.layers.Lambda(lambda x: x[:, -1:, :]),
    # Shape => [batch, 1, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*out_num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, out_num_features])
])

history = compile_and_fit(multi_linear_model, multi_window)

#IPython.display.clear_output()
multi_val_performance['Linear'] = multi_linear_model.evaluate(multi_window.val.repeat(-1), steps=100)
multi_performance['Linear'] = multi_linear_model.evaluate(multi_window.test.repeat(-1), verbose=0, steps=100)
#multi_window.plot(multi_linear_model, plot_col=0)
print('val performance =', multi_val_performance['Linear'])
print('test performance = ', multi_performance['Linear'])


# In[788]:


multi_performance['Linear'] = multi_linear_model.evaluate(multi_window.test.repeat(-1), verbose=0, steps=100)


# In[789]:


def plot_history(history):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(history.history['loss'], label='loss')
    ax.plot(history.history['mean_absolute_error'], label='mae')
    ax.plot(history.history['val_loss'], label='val_loss')
    ax.plot(history.history['val_mean_absolute_error'], label='val_mae')
    #plt.legend(history.history.keys(), loc='upper right')
    #ax.legend(loc='upper center')
    ax.legend()
    ax.set_xlabel("epochs")
    ax.set_ylabel("loss")
    plt.show()


# In[790]:


plot_history(history)


# In[176]:


multi_window._result=None


# In[791]:


multi_window.plot2(multi_linear_model, plot_col=out_features[0])


# **muti_step dense**

# In[792]:


multi_dense_model = tf.keras.Sequential([
    # Take the last time step.
    # Shape [batch, time, features] => [batch, 1, features]
    tf.keras.layers.Lambda(lambda x: x[:, -1:, :]),
    # Shape => [batch, 1, dense_units]
    #tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1024, activation='relu'),
    # Shape => [batch, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*out_num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, out_num_features])
])


# In[666]:


multi_dense_model = tf.keras.Sequential([
    # Take the last time step.
    # Shape [batch, time, features] => [batch, 1, features]
    tf.keras.layers.Flatten(),
    # Shape => [batch, 1, dense_units]
    #tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    # Shape => [batch, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*out_num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, out_num_features])
])


# In[793]:


history = compile_and_fit(multi_dense_model, multi_window)
multi_val_performance['Dense'] = multi_dense_model.evaluate(multi_window.val.repeat(-1), steps=100)
multi_performance['Dense'] = multi_dense_model.evaluate(multi_window.test.repeat(-1), verbose=1, steps=100)
print('val performance =', multi_val_performance['Dense'])
print('test performance = ', multi_performance['Dense'])


# In[794]:


plot_history(history)


# In[795]:


multi_window.plot2(multi_dense_model, plot_col=out_features[0])


# **Conv model**

# In[796]:


CONV_WIDTH = 7
CONV_LAYER_NO = 1
multi_conv_model = tf.keras.Sequential([
    # Shape [batch, time, features] => [batch, CONV_WIDTH, features]
    tf.keras.layers.Lambda(lambda x: x[:, -(CONV_WIDTH*CONV_LAYER_NO-CONV_LAYER_NO+1):, :]),
] + [
    # Shape => [batch, 1, conv_units]
    tf.keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)) for i in range(CONV_LAYER_NO)
] + [
    # Shape => [batch, 1,  out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*out_num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, out_num_features])
])


# In[ ]:


CONV_WIDTH = 3
CONV_LAYER_NO = 6
multi_conv_model = tf.keras.Sequential([
    # Shape [batch, time, features] => [batch, CONV_WIDTH, features]
    tf.keras.layers.Lambda(lambda x: x[:, -(CONV_WIDTH*CONV_LAYER_NO-CONV_LAYER_NO+1):, :]),
] + [
    # Shape => [batch, 1, conv_units]
    tf.keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)) for i in range(CONV_LAYER_NO)
] + [
    # Shape => [batch, 1,  out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
])


# In[ ]:


CONV_WIDTH = 11
CONV_LAYER_NO = 3
multi_conv_model = tf.keras.Sequential([
    # Shape [batch, time, features] => [batch, CONV_WIDTH, features]
    tf.keras.layers.Lambda(lambda x: x[:, -(CONV_WIDTH*CONV_LAYER_NO-CONV_LAYER_NO+1):, :]),
] + [
    # Shape => [batch, 1, conv_units]
    tf.keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)) for i in range(CONV_LAYER_NO)
] + [
    # Shape => [batch, 1,  out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
])


# In[ ]:





# In[ ]:


CONV_WIDTH = 11
#CONV_LAYER_NO = 3
multi_conv_model = tf.keras.Sequential([
    keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.MaxPooling1D(pool_size=2),
    keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.MaxPooling1D(pool_size=2),
    keras.layers.Conv1D(512, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.MaxPooling1D(pool_size=2),
    keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    #keras.layers.MaxPooling1D(pool_size=2),
    #keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    #keras.layers.MaxPooling1D(pool_size=2),
    #keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    #keras.layers.MaxPooling1D(pool_size=2),
    #keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.GlobalAveragePooling1D(),
    #keras.layers.Dropout(0.5),
    
    # Shape => [batch, 1,  out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
])


# In[ ]:


CONV_WIDTH = 11
#CONV_LAYER_NO = 3
multi_conv_model = tf.keras.Sequential([
    keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.Conv1D(256, strides=2, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.Conv1D(256, strides=2, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.Conv1D(512, strides=2, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.Conv1D(1024, strides=2, activation='relu', kernel_size=(CONV_WIDTH)),
    #keras.layers.MaxPooling1D(pool_size=2),
    #keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    #keras.layers.MaxPooling1D(pool_size=2),
    #keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    #keras.layers.MaxPooling1D(pool_size=2),
    #keras.layers.Conv1D(1024, activation='relu', kernel_size=(CONV_WIDTH)),
    keras.layers.GlobalAveragePooling1D(),
    #keras.layers.Dropout(0.5),
    
    # Shape => [batch, 1,  out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
])


# In[797]:


MAX_EPOCHS = 400
history = compile_and_fit(multi_conv_model, multi_window)

#IPython.display.clear_output()

multi_val_performance['Conv'] = multi_conv_model.evaluate(multi_window.val.repeat(-1), steps=100)
multi_performance['Conv'] = multi_conv_model.evaluate(multi_window.test.repeat(-1), steps=100, verbose=1)
print('val performance =', multi_val_performance['Conv'])
print('test performance = ', multi_performance['Conv'])


# In[816]:


multi_val_performance['Conv'] = multi_conv_model.evaluate(multi_window.val.repeat(-1), steps=100)
multi_performance['Conv'] = multi_conv_model.evaluate(multi_window.test.repeat(-1), steps=100, verbose=1)
print('val performance =', multi_val_performance['Conv'])
print('test performance = ', multi_performance['Conv'])


# In[799]:


plot_history(history)


# In[800]:


multi_window.plot2(multi_conv_model, plot_col=out_features[0])


# **RNN(lstm)**

# In[801]:


multi_lstm_model = tf.keras.Sequential([
    # Shape [batch, time, features] => [batch, lstm_units]
    # Adding more `lstm_units` just overfits more quickly.
    #tf.keras.layers.LSTM(32, return_sequences=False),
    tf.keras.layers.LSTM(128, return_sequences=False),
    # Shape => [batch, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*out_num_features,
                          kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, out_num_features])
])

history = compile_and_fit(multi_lstm_model, multi_window)

#IPython.display.clear_output()

multi_val_performance['LSTM'] = multi_lstm_model.evaluate(multi_window.val.repeat(-1), steps=100)
multi_performance['LSTM'] = multi_lstm_model.evaluate(multi_window.test.repeat(-1), steps=100, verbose=1)
print('val performance =', multi_val_performance['LSTM'])
print('test performance = ', multi_performance['LSTM'])


# In[803]:


plot_history(history)


# In[804]:


multi_window.plot2(multi_lstm_model, plot_col=out_features[0])


# **Autoregressive model**

# In[806]:


class FeedBack(tf.keras.Model):
  def __init__(self, units, out_steps):
    super().__init__()
    self.out_steps = out_steps
    self.units = units
    self.lstm_cell = tf.keras.layers.LSTMCell(units)
    # Also wrap the LSTMCell in an RNN to simplify the `warmup` method.
    self.lstm_rnn = tf.keras.layers.RNN(self.lstm_cell, return_state=True)
    self.dense = tf.keras.layers.Dense(num_features)
    
feedback_model = FeedBack(units=32, out_steps=OUT_STEPS)

def warmup(self, inputs):
  # inputs.shape => (batch, time, features)
  # x.shape => (batch, lstm_units)
  x, *state = self.lstm_rnn(inputs)
  #print('x =', x)

  # predictions.shape => (batch, features)
  prediction = self.dense(x)
  return prediction, state

FeedBack.warmup = warmup

prediction, state = feedback_model.warmup(multi_window.example[0])
prediction.shape

def call(self, inputs, training=None):
  # Use a TensorArray to capture dynamically unrolled outputs.
  predictions = []
  # Initialize the lstm state
  prediction, state = self.warmup(inputs)

  # Insert the first prediction
  predictions.append(prediction)

  # Run the rest of the prediction steps
  for n in range(1, self.out_steps):
    # Use the last prediction as input.
    x = prediction
    # Execute one lstm step.
    x, state = self.lstm_cell(x, states=state,
                              training=training)
    # Convert the lstm output to a prediction.
    prediction = self.dense(x)
    # Add the prediction to the output
    predictions.append(prediction)

  # predictions.shape => (time, batch, features)
  predictions = tf.stack(predictions)
  # predictions.shape => (batch, time, features)
  predictions = tf.transpose(predictions, [1, 0, 2])
  predictions = tf.keras.layers.Lambda(lambda x: x[:, :, out_features[0]:(out_features[0]+len(out_features))])(predictions)
  return predictions

FeedBack.call = call

print('Output shape (batch, time, features): ', feedback_model(multi_window.example[0]).shape)


# In[807]:


it = iter(multi_window.train)
x,y = next(it)
print(x.shape, y.shape)
pred = feedback_model.predict(x)
pred.shape


# In[808]:


history = compile_and_fit(feedback_model, multi_window)

#IPython.display.clear_output()

multi_val_performance['AR LSTM'] = feedback_model.evaluate(multi_window.val)
multi_performance['AR LSTM'] = feedback_model.evaluate(multi_window.test, verbose=0)

print('val performance =', multi_val_performance['AR LSTM'])
print('test performance = ', multi_performance['AR LSTM'])


# In[809]:


plot_history(history)


# In[810]:


multi_window.plot2(feedback_model, plot_col=out_features[0])


# **performance**

# In[817]:


x = np.arange(len(multi_performance))
width = 0.3


metric_name = 'mean_absolute_error'
metric_index = multi_conv_model.metrics_names.index('mean_absolute_error')
val_mae = [v[metric_index] for v in multi_val_performance.values()]
test_mae = [v[metric_index] for v in multi_performance.values()]

plt.figure()
plt.bar(x - 0.17, val_mae, width, label='Validation')
plt.bar(x + 0.17, test_mae, width, label='Test')
plt.xticks(ticks=x, labels=multi_performance.keys(),
           rotation=45)
plt.ylabel(f'MAE (average over all times and outputs)')
_ = plt.legend()
plt.show()


# ## 연습 섹션

# In[ ]:





# In[ ]:


it = iter(wide_window.val)
x,y = next(it)


# In[ ]:


x.shape, y.shape


# In[ ]:


history = gain.fit(wide_window.train, epochs=20,
                      validation_data=wide_window.val,
                      callbacks=[])


# In[ ]:


it = iter(wide_window.val)
x,y = next(it)
x.shape, y.shape


# In[ ]:


gain.predict(x)


# In[ ]:


df[0].isna().astype(int).sum()


# In[ ]:


date_time1 = pd.to_datetime(df_full[0].iloc[:, 0], format='%Y.%m.%d %H:%M')
date_time2 = pd.to_datetime(df_full[0].iloc[:, 0], format='%Y.%m.%d %H:%M')


# In[ ]:


timestamp_s1 = date_time1.map(datetime.datetime.timestamp)
timestamp_s2 = date_time2.map(datetime.datetime.timestamp)


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:


ds = tf.data.Dataset.from_tensor_slices((x,y))


# In[ ]:


ds.element_spec


# In[ ]:


ds = ds.batch(5)
ds.element_spec


# In[ ]:


df2


# In[ ]:


model.fit(ds)


# # MNIST with data generator
# 
# https://towardsdatascience.com/keras-custom-data-generators-example-with-mnist-dataset-2a7a2d2b0360
# 

# In[ ]:


import tensorflow as tf
import os
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import numpy as np
import math


# In[ ]:


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


# In[ ]:


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


# In[ ]:


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


# In[ ]:


train_generator = DataGenerator(x_train, y_train, batch_size = 64,
                                dim = input_shape,
                                n_classes=10, 
                                to_fit=True, shuffle=True)
val_generator =  DataGenerator(x_test, y_test, batch_size=64, 
                               dim = input_shape, 
                               n_classes= n_classes, 
                               to_fit=True, shuffle=True)


# In[ ]:


steps_per_epoch = len(train_generator)
validation_steps = len(val_generator)


# In[ ]:


model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=1,
        validation_data=val_generator,
        validation_steps=validation_steps)


# In[ ]:


it = iter(train_generator)


# In[ ]:


x,y = next(it)


# In[ ]:


x.shape


# In[ ]:


y.shape


# ## MNIST with custom model

# In[ ]:


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


# In[ ]:


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

# In[ ]:




import matplotlib
import matplotlib.font_manager

[f.fname for f in matplotlib.font_manager.fontManager.ttflist]


# In[ ]:


get_ipython().system(' fc-list :lang=ko')


# In[ ]:


import matplotlib
import matplotlib.font_manager as fm
fm.get_fontconfig_fonts()
font_location = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
#font_location = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
# font_location = 'C:/Windows/Fonts/NanumGothic.ttf' # For Windows
fprop = fm.FontProperties(fname=font_location)


# In[ ]:


fig = plt.figure()  
plt.plot((1,1), label='가-가가')  
plt.title('가가가',fontproperties=fprop)  
plt.legend(prop=fprop)  
plt.show()


# In[ ]:




