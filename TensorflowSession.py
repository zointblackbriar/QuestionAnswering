import tensorflow as tf

helloParam = tf.constant('Hello Tensorflow')

sess = tf.Session()

print(sess.run(helloParam))