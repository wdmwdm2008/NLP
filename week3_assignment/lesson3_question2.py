from sklearn.datasets import load_boston
import random


def price(rm, k, b):
    return k * rm + b


def loss_one_order(y, y_hat):
    return sum([abs(y_i - y_hat_i) for y_i, y_hat_i in zip(y, y_hat)])/len(y)


def partial_k_one_order(x, y, y_hat):
    n = len(y)
    gradient = 0
    for (x_i, y_i, y_hat_i) in zip(x, y, y_hat):
        if y_i > y_hat_i:
            gradient -= x_i
        else:
            gradient += x_i
    return gradient / n


def partial_b_one_order(x, y, y_hat):
    n = len(y)
    gradient = 0
    for (y_i, y_hat_i) in zip(y, y_hat):
        if y_i > y_hat_i:
            gradient -= 1
        else:
            gradient += 1
    return gradient / n


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
        current_loss = loss_one_order(y, y_hat)
        if current_loss < min_loss:  # performance became better
            min_loss = current_loss

            if i % 50 == 0:
                print(
                    'When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b,
                                                                                               min_loss))
        current_k -= partial_k_one_order(x_rm, y, y_hat) * learning_rate
        current_b -= partial_b_one_order(x_rm, y, y_hat) * learning_rate
