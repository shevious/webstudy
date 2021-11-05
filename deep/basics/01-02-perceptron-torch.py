import torch
x_train = torch.FloatTensor([[1, -1], [-1, 1]])
#x_train = torch.FloatTensor([[1, -1], [-0.9, 0.9]])

y_train = torch.FloatTensor([1, -1])

# weights 초기값
W = torch.FloatTensor([-1, 1])
b = 0

# learning rate
lr = 0.1

epochs = 4

print('batch_size: 1')
for epoch in range(epochs):
    for batch in range(2):
        # batch에서 한개씩 데이터를 꺼내옴
        x = x_train[batch]
        y = y_train[batch]

        # 추론 값을 hypothesis라고도 부름
        hypothesis = torch.sign(torch.matmul(W,x) + b)

        # 손실 함수(참고용)
        cost = ((hypothesis - y) ** 2)/2

        # gradient 계산
        gradient_W = (hypothesis - y) * x
        gradient_b = (hypothesis - y)

        # weights의 갱신
        W -= lr * gradient_W
        b -= lr * gradient_b

    print('epoch %i: '%epoch, W, b)

# weights 초기값
W = torch.FloatTensor([-1, 1])
b = 0

print('batch_size: 2')
for epoch in range(epochs):
    # 추론 값을 hypothesis라고도 부름
    hypothesis = torch.sign(torch.matmul(W, torch.transpose(x_train, 0, 1)) + b)
    #print(torch.matmul(W, torch.transpose(x_train, 0, 1)) + b)

    # 손실 함수(참고용)
    cost = torch.sum(((hypothesis - y_train) ** 2)/2)

    # gradient 계산
    gradient_W = torch.matmul(hypothesis - y_train, torch.transpose(x_train, 0, 1))
    gradient_b = torch.sum(hypothesis - y_train)

    # weights의 갱신
    W -= lr * gradient_W
    b -= lr * gradient_b
    print('epoch %i: '%epoch, W, b)

