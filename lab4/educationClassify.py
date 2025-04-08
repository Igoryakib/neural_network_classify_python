import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import joblib
if __name__ == "__main__":
    INPUT_DIM = 4
    H_DIM = 10
    OUT_DIM = 3
    ALPHA = 0.0004
    NUM_EPOCHS = 400
    BATCH_SIZE = 50

    def relu(t): return np.maximum(t, 0)

    def relu_deriv(t): return (t >= 0).astype(float)

    def softmax(t):
        out = np.exp(t - np.max(t))  # стабілізація
        return out / np.sum(out)

    def softmax_batch(t):
        out = np.exp(t - np.max(t))
        return out / np.sum(out, axis=1, keepdims=True)

    def sparse_cross_entropy(z, y): return -np.log(z[0, y] + 1e-10) # запобіжник log0

    def sparse_cross_entropy_batch(z, y): return -np.log(np.array([z[j, y[j]] + 1e-10 for j in range(len(y))]))

    def to_full(y, num_classes):
        y_full = np.zeros((1, num_classes))
        y_full[0, y] = 1
        return y_full

    def to_full_batch(y, num_classes):
        y_full = np.zeros((len(y), num_classes))
        for j, yj in enumerate(y):
            y_full[j, yj] = 1
        return y_full

    df = pd.read_csv("shapes_dataset.csv")
    label_mapping = {"triangle": 0, "square": 1, "rectangle": 2}
    df["label"] = df["label"].map(label_mapping)

    X_raw = df[["num_lines", "avg_length", "perimeter", "max_length"]].values
    scaler = StandardScaler()
    X = scaler.fit_transform(X_raw)
    y = df["label"].values

    W1 = np.random.rand(INPUT_DIM, H_DIM)
    b1 = np.random.rand(1, H_DIM)
    W2 = np.random.rand(H_DIM, OUT_DIM)
    b2 = np.random.rand(1, OUT_DIM)

    W1 = (W1 - 0.5) * 2 * np.sqrt(1/INPUT_DIM)
    b1 = (b1 - 0.5) * 2 * np.sqrt(1/INPUT_DIM)
    W2 = (W2 - 0.5) * 2 * np.sqrt(1/H_DIM)
    b2 = (b2 - 0.5) * 2 * np.sqrt(1/H_DIM)

    loss_arr = []

    for ep in range(NUM_EPOCHS):
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        X = X[indices]
        y = y[indices]
        for i in range(len(X) // BATCH_SIZE):
            xb = X[i:i+BATCH_SIZE]
            yb = y[i:i+BATCH_SIZE]
            x = xb.copy()
            yt = np.array(yb)

            # Forward
            t1 = x @ W1 + b1
            h1 = relu(t1)
            t2 = h1 @ W2 + b2
            z = softmax_batch(t2)
            E = np.sum(sparse_cross_entropy_batch(z, yt))

            # Backward
            y_full = to_full_batch(yt, OUT_DIM)
            dE_dt2 = z - y_full
            dE_dW2 = h1.T @ dE_dt2
            dE_db2 = np.sum(dE_dt2, axis=0, keepdims=True)
            dE_dh1 = dE_dt2 @ W2.T
            dE_dt1 = dE_dh1 * relu_deriv(t1)
            dE_dW1 = x.T @ dE_dt1
            dE_db1 = np.sum(dE_dt1, axis=0, keepdims=True)

            
            W1 -= ALPHA * dE_dW1
            b1 -= ALPHA * dE_db1
            W2 -= ALPHA * dE_dW2
            b2 -= ALPHA * dE_db2
            
            loss_arr.append(E)
            
        # Вивід точності кожні 10 епох
        if ep % 10 == 0 or ep == NUM_EPOCHS - 1:
            correct = 0
            for j in range(len(X)):
                xj = X[j:j+1]
                yj = y[j]
                zj = softmax(relu(xj @ W1 + b1) @ W2 + b2)
                y_pred = np.argmax(zj)
                if y_pred == yj:
                    correct += 1
            acc = correct / len(X)
            print(f"Epoch {ep:03d}: Loss={E:.4f}, Accuracy={acc:.2f}")
    with open("weights.txt", "w") as f:
        np.savetxt("W1.txt", W1, delimiter=",")
        np.savetxt("b1.txt", b1, delimiter=",")
        np.savetxt("W2.txt", W2, delimiter=",")
        np.savetxt("b2.txt", b2, delimiter=",")
    joblib.dump(scaler, "scaler.pkl")
    plt.plot(loss_arr)
    plt.show()
