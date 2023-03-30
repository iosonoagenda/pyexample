import numpy as np
from scipy.spatial.distance import pdist, squareform

class AgglomerativeClustering:
    def __init__(self, n_clusters=2, linkage='ward'):
        self.n_clusters = n_clusters
        self.linkage = linkage

    def fit(self, X):
        self.n_samples, self.n_features = X.shape
        self.labels_ = np.zeros(self.n_samples)
        self.distances_ = squareform(pdist(X, metric='euclidean'))

        for i in range(self.n_samples):
            self.labels_[i] = i

        self.n_labels_ = self.n_samples
        self.current_label_ = self.n_samples

        while(self.n_labels_ > self.n_clusters):
            idx = np.argmin(self.distances_)
            i, j = np.unravel_index(idx, (self.n_labels_, self.n_labels_))
            self.merge(i, j)
            self.n_labels_ -= 1

        return self

    def merge(self, i, j):
        indices = np.arange(self.n_labels_)
        indices = np.delete(indices, [i, j])
        new_label = self.current_label_

        if self.linkage == 'single':
            new_distances = np.maximum(self.distances_[i, indices], self.distances_[j, indices])
        elif self.linkage == 'complete':
            new_distances = np.minimum(self.distances_[i, indices], self.distances_[j, indices])
        else:
            new_distances = (self.distances_[i, indices] + self.distances_[j, indices]) / 2

        self.distances_ = new_distances
        self.labels_[self.labels_ == i] = new_label
        self.labels_[self.labels_ == j] = new_label
        self.current_label_ += 1

        return self

    def predict(self, X):
        distances = np.zeros((X.shape[0], self.n_labels_))

        for i in range(self.n_labels_):
            mask = self.labels_ == i
            centroid = X[mask].mean(axis=0)
            distances[:, i] = np.linalg.norm(X - centroid, axis=1)

        return np.argmin(distances, axis=1)
