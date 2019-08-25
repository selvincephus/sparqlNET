import matplotlib.pyplot as plt

validation_loss = [1.8330, 1.5953,1.3162,1.2881,0.9410,
                   0.8255, 0.3212,0.2340,0.2450,
                   0.2112]
training_loss = [1.8628, 1.2020, 1.0405, 0.7784, 0.5566,0.3420, 0.2398, 0.2220, 0.1954, 0.1909]

train_curve, = plt.plot(training_loss, 'r', label="Training loss")
validation_curve, = plt.plot(validation_loss, 'g', label="Validation loss")

plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(handles=[train_curve, validation_curve])
plt.show()
