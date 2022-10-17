
import numpy as np
import json
res = [False]*15
ans_org = """
여기에 적어주세요.
"""

try:
    if ans01 != ans_org and len(ans01) > 5:
        res[0] = ans01
except:
    pass

try:
    if ans02 != ans_org and len(ans02) > 5:
        res[1] = ans02
except:
    pass

try:
    if ans03 != ans_org and len(ans03) > 5:
        res[2] = ans03
except:
    pass

ans04_org = """
결과: 4주차 과제에서는 val_pos_accuracy가 0.000 이었다.
이유: ???????? 라고 생각한다.
"""

try:
    if ans04 != ans04_org and len(ans04) > 5:
        res[3] = ans04
except:
    pass

summary_list = []

try:
    ans05.summary(print_fn=lambda x: summary_list.append(x))
    summary_list = summary_list[4:-5] + summary_list[-3:-2]
    is_conv = False
    for line in summary_list:
        if 'Conv2D' in line:
            is_conv = True
            break
    if not is_conv:
        raise
    res[4] = '\n'.join(summary_list)
except:
    pass

# loss
try:
    if ans06 > 0.9:
        raise
    res[5] = float(ans06)
except:
    pass

#accuracy
try:
    if ans07 < 0.1:
        raise
    res[6] = float(ans07)
except:
    pass

try:
    if ans08 != ans_org and len(ans08) > 5:
        res[7] = ans08
except:
    pass

try:
    if abs(ans09-0.79853815) > 0.001:
        raise
    res[8] = float(ans09)
except:
    pass

try:
    if abs(ans10-79.03037965) > 0.001 and abs(ans10-385.45751572) > 0.001:
        raise
    res[9] = True
except:
    pass

box_answer = np.array(
[[36, 250, 79, 354], # bottle 이 부분을 수정하세요
 [ 160, 26, 371, 241], # tvmonitor 이 부분을 수정하세요
], dtype='float32')

try:
    if np.sum(np.abs(ans11 - box_answer)) > 0.001:
        raise
    res[10] = True
except:
    pass

try:
    if ans12 != ans_org and len(ans12) > 5:
        res[11] = ans12
except:
    pass

try:
    if ans13 != ans_org and len(ans13) > 5:
        res[12] = ans13
except:
    pass

try:
    if abs(ans14 - 0.9666666666666667) > 0.0001:
        raise
    res[13] = True
except:
    pass

try:
    if ans15 != ans_org:
        res[14] = ans15
    else:
        res[14] = ''
except:
    pass

resdict = {}
resdict['res'] = res
res_array = res.copy()
for i, r in enumerate(res_array):
    if type(r) == np.bool_ or type(r) == bool:
        res_array[i] = str(r)

false_array = np.array(['False']*23)
score = 0.
# 1번: 
wrong_cnt = (res_array[0:8] == false_array[0:8]).astype('int').sum()
score += (8 - wrong_cnt)/8.*50.
# 2번: 
wrong_cnt = (res_array[8:14] == false_array[8:14]).astype('int').sum()
score += (6 - wrong_cnt)/6.*50.

resdict['score'] = score

for i, r in enumerate(res):
    if type(r) == np.bool_:
        res[i] = bool(r)

with open('./result.json','w', encoding='UTF-8') as f:
    json.dump(resdict, f, indent=4, ensure_ascii=False)
