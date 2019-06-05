import matplotlib.pyplot as plt

validation_loss = [2.073276786544655, 1.7760467139329281,1.2400173825106071,0.7650948015714103,0.17130059347748358,
                   0.10600187977362915, 0.05806053814554663,0.03756621126183696,0.03701257627244324,
                   0.028082659580958572]
training_loss = [1.7425, 1.0693, 0.4956, 0.1821, 0.1057, 0.0575, 0.0367, 0.0251, 0.0264, 0.0188]

train_curve, = plt.plot(training_loss, 'r', label="Training loss")
validation_curve, = plt.plot(validation_loss, 'g', label="Validation loss")

plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(handles=[train_curve, validation_curve])
plt.show()
