from sklearn.datasets import load_boston
import random


def price(rm, k, b):
    return k * rm + b


def loss(y, y_hat):
    return sum([(y_i - y_hat_i) ** 2 for y_i, y_hat_i in zip(y, y_hat)])/len(y)


def partial_k(x, y, y_hat):
    return -2 * sum([(y_i - y_hat_i) * x_i for (y_i, y_hat_i, x_i) in zip(y, y_hat, x)]) / len(y)


def partial_b(x, y, y_hat):
    return -2 * sum([(y_i - y_hat_i) for (y_i, y_hat_i) in zip(y, y_hat)]) / len(y)


if __name__ == '__main__':
    data = load_boston()
    x, y = data['data'], data['target']
    x_rm = x[:, 5]

    trying_times = 2000
    learning_rate = 0.01
    min_loss = float('inf')
    current_k = random.random() - 200 + 100
    current_b = random.random() - 200 + 100

    for i in range(trying_times):
        y_hat = [price(rm, current_k, current_b) for rm in x_rm]
        current_loss = loss(y, y_hat)
        if current_loss < min_loss:  # performance became better
            min_loss = current_loss

            if i % 50 == 0:
                print(
                    'When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b,
                                                                                               min_loss))
        current_k -= partial_k(x_rm, y, y_hat) * learning_rate
        current_b -= partial_b(x_rm, y, y_hat) * learning_rate
