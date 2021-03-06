# Lab 7 Learning rate and Evaluation
import tensorflow as tf
import random
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
# Check out https://www.tensorflow.org/get_started/mnist/beginners for
# more information about the mnist dataset
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

nb_classes = 10

W = tf.Variable(tf.zeros([784, nb_classes]))
b = tf.Variable(tf.zeros([nb_classes]))

# MNIST data image of shape 28 * 28 = 784
X = tf.placeholder(tf.float32, [None, 784])
# 0 - 9 digits recognition = 10 classes
Y = tf.placeholder(tf.float32, [None, nb_classes])

# Hypothesis (using softmax)
hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)

cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.).minimize(cost)

# Test model
is_correct = tf.equal(tf.arg_max(hypothesis, 1), tf.arg_max(Y, 1))
# Calculate accuracy
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

with tf.Session() as sess:
    # Initialize TensorFlow variables
    sess.run(tf.global_variables_initializer())

    # Training cycle
    for step in range(2001):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        c, _ = sess.run([cost, optimizer], feed_dict={
                        X: batch_xs, Y: batch_ys})
        if step % 100 == 0:
            print("Epoch: ", '%04d' % (step + 1),
                  "cost=", "{:.9f}".format(c))

    print("Learning finished")

    # Test the model using test sets
    print("Accuracy: ", accuracy.eval(session=sess, feed_dict={
          X: mnist.test.images, Y: mnist.test.labels}))

    # Get one and predict
    r = random.randint(0, mnist.test.num_examples - 1)
    print("Label: ", sess.run(tf.argmax(mnist.test.labels[r:r + 1], 1)))
    print("Prediction: ", sess.run(
        tf.argmax(hypothesis, 1), feed_dict={X: mnist.test.images[r:r + 1]}))

    plt.imshow(mnist.test.images[r:r + 1].
               reshape(28, 28), cmap='Greys', interpolation='nearest')
    plt.show()


'''
Epoch:  0001 cost= 2.302585363
Epoch:  0101 cost= 0.232252389
Epoch:  0201 cost= 0.263057202
Epoch:  0301 cost= 0.319312871
Epoch:  0401 cost= 0.572987258

...

Epoch:  1501 cost= 0.391383678
Epoch:  1601 cost= 0.251548856
Epoch:  1701 cost= 0.296876758
Epoch:  1801 cost= 0.209258422
Epoch:  1901 cost= 0.381276697
Epoch:  2001 cost= 0.432298064
Learning finished
Accuracy:  0.8865
'''
