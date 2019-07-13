from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import random


def price(rm, k, b):
    return k * rm + b


def draw_rm_and_price():
    plt.scatter(x[:, 5], y)


def loss(y, y_hat):
    return sum((y_i - y_hat_i) ** 2 for y_i, y_hat_i in zip(list(y), list(y_hat))) / len(list(y))


def random_choose_method():
    trying_times = 2000
    min_loss = float('inf')

    for i in range(trying_times):
        k = random.random() * 200 - 100
        b = random.random() * 200 - 100
        price_by_random_k_and_b = [price(r, k, b) for r in x_rm]

        current_loss = loss(y, price_by_random_k_and_b)
        if current_loss < min_loss:
            min_loss = current_loss
            print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, k, b, min_loss))


def direction_adjusting_method():
    directions = [
        (+1, +1),
        (+1, -1),
        (-1, +1),
        (-1, -1),
    ]
    trying_times2 = 1000
    best_value = float('inf')
    best_k = random.random() * 200 - 100
    best_b = random.random() * 200 - 100
    next_direction = random.choice(directions)
    scalar = 0.1

    for i in range(trying_times2):
        k_direction, b_direction = next_direction
        current_k = best_k + k_direction * scalar
        current_b = best_b + b_direction * scalar
        x_rm = x[:, 5]
        y_k_and_b = loss(y, [price(rm, current_k, current_b) for rm in x_rm])

        if y_k_and_b < best_value:
            best_value = y_k_and_b
            best_k, best_b = current_k, current_b
            print('when time is {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, best_value))
        else:
            next_direction = random.choice(directions)


if __name__=='__main__':

    data = load_boston()
    x, y = data['data'], data['target']
    x_rm = x[:, 5]

    # 1) Random Choose Method to get optimal k and b
    random_choose_method()

    # 2) Random Choose Method to get optimal k and b
    direction_adjusting_method()

