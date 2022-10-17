
import numpy as np
import json
res = [False]*23
try:
    tmp = np.array([[0.1,0.2,0.3,0.4],
              [0.5,0.6,0.7,0.8],
              [0.9,1. ,1.1,1.2],
              [1.3,1.4,1.5,1.6]], dtype='float32')
    res[0] = (tmp == ans01.astype('float32')).all()
except:
    pass
 
try:
    tmp = np.array([[3. , 3.2, 3.4],
                    [3.8, 4. , 4.2]], dtype='float32')
    res[1] = (tmp == ans02.astype('float32')).all()
except:
    pass

try:
    res[2] = (ans03 >= 51) and (ans03 <= 53)
except:
    pass

try:
    res[3] = (ans04 >= 420) and (ans04 <= 422)
except:
    pass

try:
    tmp = np.array([[17., 23.,  9.],
                    [39., 53., 27.]], dtype='float32')
    if (tmp == ans05.astype('float32')).all():
        res[4] = True
except:
    pass

try:
    tmp = np.array(
      [[17., 39.],
       [23., 53.],
       [ 9., 27.]]
    , dtype='float32')
    if (tmp == ans05.astype('float32')).all():
        res[4] = True
except:
    pass

try:
    tmp = np.array(
      [[[17., 23.,  9.]],
       [[39., 53., 27.]]]
    , dtype='float32')
    if (tmp == ans05.astype('float32')).all():
        res[4] = True
except:
    pass

try:
    tmp = np.array([[  1.2,   0. , -12. ],
                    [  0. ,   1.2, -23. ]], dtype='float32')
    tmp = np.abs(tmp-ans06).mean()
    res[5] = tmp < 3.0
except:
    pass

try:
    tmp = np.array([[ 6.123234e-17, -1.000000e+00,  2.000000e+02],
       [ 1.000000e+00,  6.123234e-17,  0.000000e+00]], dtype='float32')
    tmp = np.abs(tmp - ans07).mean()
    res[6] = tmp < 0.1
except:
    pass

try:
    tmp = np.array([[ -1.,   0., 200.],
       [  0.,   1.,   0.]], dtype='float32')
    tmp = np.abs(tmp - ans08).mean()
    res[7] = (tmp < 0.2)
except:
    pass

try:
    res[8] = ans09
except:
    pass

try:
    res[9] = ans10
except:
    pass

try:
    tmp = len(ans11)
    if tmp > 5 or tmp == 0:
        raise
    tmp1 = np.array([512]*tmp)
    tmp2 = np.array(ans11)
    tmp = tmp1 - tmp2
    res[10] = (tmp >= 0).all()
except:
    pass

try:
    if len(ans12) > 14:
        res[11] = True
except:
    pass

try:
    res[12] = (ans13 > 0) and (ans13 < 0.2)
except:
    pass

#batch_size
try:
    res[13] = (ans14 > 0) and (ans14 <= 256)
except:
    pass

# epoch
try:
    res[14] = (ans15 > 5) and (ans15 < 10000)
except:
    pass

# val_loss
try:
    res[15] = (ans16 < 0.9)
except:
    pass

ans18_org = """
tf.reduce_all의 역할은 무엇인지, axis=1은 무엇을 의미하는 지 간단히 요약해 봅시다.
"""

ans19_org = """
tf.reduce_mean은 코드에서 어떤 역할을 하는지, 간단히 요약해 봅시다. 
"""

ans20_org = """
최종 출력층의 activation=None인 이유 
"""

ans21_org = """
random seed의 사용 이유 
"""

# val_accuracy
try:
    res[16] = (ans17 > 0.8)
except:
    pass

try:
    if ans18 != ans18_org:
        res[17] = ans18
except:
    pass
try:
    if ans19 != ans19_org:
        res[18] = ans19
except:
    pass

try:
    if ans20 != ans20_org:
        res[19] = ans20
except:
    pass

try:
    if ans21 != ans21_org:
        res[20] = ans21
except:
    pass

#convval
try:
    res[21] = np.abs(ans22-0.6013072) < 0.001
except:
    pass

try:
    res[22] = ans23
except:
    pass
resdict = {}
resdict['res'] = res
res_array = np.array(res, dtype='str')
false_array = np.array(['False']*23)
score = 0.
# 1번: 
wrong_cnt = (res_array[0:2] == false_array[0:2]).astype('int').sum()
score += (2 - wrong_cnt)/2.*20.
# 2번: 
wrong_cnt = (res_array[2:5] == false_array[2:5]).astype('int').sum()
score += (3 - wrong_cnt)/3.*20.
# 3번: 
wrong_cnt = (res_array[5:10] == false_array[5:10]).astype('int').sum()
score += (5 - wrong_cnt)/5.*20.
# 4번: 
wrong_cnt = (res_array[10:21] == false_array[10:21]).astype('int').sum()
score += (11 - wrong_cnt)/11.*20.
# 5번: 
wrong_cnt = (res_array[21:22] == false_array[21:22]).astype('int').sum()
score += (1 - wrong_cnt)/1.*20.

#wrong_cnt = (res_array == false_array).astype('int').sum()
#score = (23 - wrong_cnt)/23.*100.
resdict['score'] = score

for i, r in enumerate(res):
    if type(r) == np.bool_:
        res[i] = bool(r)

with open('./result.json','w', encoding='UTF-8') as f:
    json.dump(resdict, f, indent=4, ensure_ascii=False)
