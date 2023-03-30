import numpy as np

class NeuralNetwork:
    def __init__(self, layers, alpha=0.1):
        self.layers = layers
        self.alpha = alpha
        self.W = []
        self.initialize_weights()

    def initialize_weights(self):
        for i in range(0, len(self.layers) - 2):
            w = np.random.randn(self.layers[i] + 1, self.layers[i + 1] + 1)
            self.W.append(w / np.sqrt(self.layers[i]))

        w = np.random.randn(self.layers[-2] + 1, self.layers[-1])
        self.W.append(w / np.sqrt(self.layers[-2]))

    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x):
        return x * (1 - x)

    def fit(self, X, y, epochs=1000, batch_size=32):
        X = np.c_[X, np.ones((X.shape[0]))]
        for epoch in range(epochs):
            batch_indices = np.random.choice(X.shape[0], batch_size)
            X_batch = X[batch_indices]
            y_batch = y[batch_indices]

            for (x, target) in zip(X_batch, y_batch):
                self.feedforward(x)
                error = self.layers[-1] - target
                deltas = [error * self.sigmoid_deriv(self.layers[-1])]

                for i in range(len(self.layers) - 2, 0, -1):
                    delta = deltas[-1].dot(self.W[i].T)
                    delta = delta * self.sigmoid_deriv(self.layers[i])
                    deltas.append(delta)

                deltas = deltas[::-1]

                for i in range(len(self.W)):
                    layer = np.atleast_2d(self.layers[i])
                    delta = np.atleast_2d(deltas[i])
                    self.W[i] += -self.alpha * layer.T.dot(delta)

    def feedforward(self, x):
        self.layers = [x]

        for w in self.W:
            layer = self.sigmoid(np.dot(self.layers[-1], w))
            self.layers.append(layer)

        return self.layers[-1]

    def predict(self, X):
        X = np.c_[X, np.ones((X.shape[0]))]
        return self.feedforward(X).argmax(axis=1)
