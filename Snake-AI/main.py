from game import *
from training_data import generate_training_data
from keras.models import Sequential
from keras.layers import Dense
import pygame

pygame.init()
display = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
clock = pygame.time.Clock()

"""
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN ->button_direction = 2
UP -> button_direction = 3
"""
training_data_x, training_data_y = generate_training_data(display, clock)

model = Sequential()
model.add(Dense(9, input_dim=7))
model.add(Dense(15, activation="relu"))
model.add(Dense(3, activation="softmax"))
model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
model.fit(
    (np.array(training_data_x).reshape(-1, 7)),
    (np.array(training_data_y).reshape(-1, 3)),
    batch_size=256,
    epochs=3,
)

model.save_weights("model.h5")

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
