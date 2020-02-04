
data=open('./gdrive/My Drive/SKCC/2_텍스트/ml_6_spacing_train.csv')
rdr = csv.reader(data)
total=[]
y=[]
s=[]
for ol in rdr:
    line=ol[0]
    s.append(line)
    word=[]
    for w in line:
        vec=[0]*26
        vec[(ord(w)-97)]=1
        word+=vec
    for i in range(16-len(line)):
        word+=[0]*26
    ans=[0]*16
    if ol[3]=="":
        ans[len(ol[1])-1]=1
    else:
        ans[len(ol[1])-1]=1
        ans[len(ol[1])+len(ol[2])-1]=1
    total.append(word)
    y.append(ans)
total.pop(0)
y.pop(0)
print(y)
####신경망 학습###
import tensorflow as tf
import numpy as np
 
# [꼬리(tail), 짖음(bark), 다리갯수(legs), 크기(size(cm))]
x_data = np.array(total)
y_data = np.array(y)
#########
# 신경망 모델 구성
######
X = tf.placeholder(tf.float32, shape=[None, 26*16])
Y = tf.placeholder(tf.float32, shape=[None, 16])
W1 = tf.Variable(tf.random_uniform([26*16, 26*16], -1., 1.))
 
# b1은 편향(bias)이며, 첫 번째 히든 레이어의 뉴런 갯수입니다. 
b1 = tf.Variable(tf.zeros([26*16]))
 
# 신경망의 히든 레이어에 가중치 W1과 편향 b1을 적용합니다
L1 = tf.nn.relu(tf.add(tf.matmul(X, W1), b1))
 
 
W2 = tf.Variable(tf.random_normal([26*16,20*10]))
b2 = tf.Variable(tf.zeros([200]))
L2 = tf.nn.relu(tf.add(tf.matmul(L1, W2), b2))
 
W3 = tf.Variable(tf.random_normal([200, 150]))
b3 = tf.Variable(tf.zeros([150]))
L3 = tf.nn.relu(tf.add(tf.matmul(L2, W3), b3))
 
W4 = tf.Variable(tf.random_normal([150, 100]))
b4 = tf.Variable(tf.zeros([100]))
L4 = tf.nn.relu(tf.add(tf.matmul(L3, W4), b4))
 
W5 = tf.Variable(tf.random_normal([100 , 16]))
b5 = tf.Variable(tf.zeros([16]))
L5 = tf.nn.relu(tf.add(tf.matmul(L4, W5), b5))
 
W6 = tf.Variable(tf.random_normal([16, 16]))
b6 = tf.Variable(tf.zeros([16]))
model = tf.add(tf.matmul(L5, W6), b6)
cost = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y, logits=model))
 
optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
train_op = optimizer.minimize(cost)
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
 
for step in range(10000):
    sess.run(train_op, feed_dict={X: x_data, Y: y_data})
prediction = tf.argmax(model, 1)
target = tf.argmax(Y, 1)
print('예측값:', sess.run(prediction, feed_dict={X: x_data}))
print('실제값:', sess.run(target, feed_dict={Y: y_data}))
 
is_correct = tf.equal(prediction, target)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print('정확도: %.2f' % sess.run(accuracy * 100, feed_dict={X: x_data, Y: y_data}))
sess.close()
