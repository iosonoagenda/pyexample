import numpy as np

def calculate_correlation_matrix(data):
    # Calcola la matrice di correlazione per un insieme di dati
    # Input:
    # - data: un array numpy bidimensionale
    # Output:
    # - La matrice di correlazione come un array numpy bidimensionale

    # Calcola la media per ogni colonna
    col_means = np.mean(data, axis=0)

    # Sottrae la media dalla matrice di dati
    data_centered = data - col_means

    # Calcola la deviazione standard per ogni colonna
    col_stds = np.std(data_centered, axis=0)

    # Divide ogni colonna per la deviazione standard
    data_normalized = data_centered / col_stds

    # Calcola la matrice di correlazione
    correlation_matrix = np.dot(data_normalized.T, data_normalized) / data.shape[0]

    return correlation_matrix

# Genera un insieme di dati casuali con 3 variabili e 1000 osservazioni
data = np.random.normal(size=(1000, 3))

# Calcola la matrice di correlazione per l'insieme di dati
correlation_matrix = calculate_correlation_matrix(data)

# Stampa la matrice di correlazione
print(correlation_matrix)
