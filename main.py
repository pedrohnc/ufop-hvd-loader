import os

from data import load_data, reshape
from utils import shape

BASE_DIR = '/media/share/datasets/lupulo/ufop-hvd/'
RESHAPED_DIR = '/media/share/datasets/lupulo/ufop-hvd-reshaped/'


def main():
    # Resizes the images if they don't already exist
    if not os.path.isdir(RESHAPED_DIR + 'train'):
        reshape(BASE_DIR + 'train', RESHAPED_DIR + 'train', shape=(300, 300))
    if not os.path.isdir(RESHAPED_DIR + 'validation'):
        reshape(BASE_DIR + 'validation', RESHAPED_DIR + 'validation', shape=(300, 300))
    if not os.path.isdir(RESHAPED_DIR + 'test'):
        reshape(BASE_DIR + 'test', RESHAPED_DIR + 'test', shape=(300, 300))

    # Reads the images and labels
    x_train, y_train, labels_train = load_data(RESHAPED_DIR + 'train', use_numpy_array=False)
    x_validation, y_validation, labels_validation = load_data(RESHAPED_DIR + 'validation')
    x_test, y_test, labels_test = load_data(RESHAPED_DIR + 'test')

    # Prints type and shape
    print('x_train')
    print('type:', type(x_train))
    print('shape:', shape(x_train))
    print()

    print('y_train')
    print('type:', type(y_train))
    print('shape:', shape(y_train))
    print()

    print('x_validation')
    print('type:', type(x_validation))
    print('shape:', shape(x_validation))
    print()

    print('y_validation')
    print('type:', type(y_validation))
    print('shape:', shape(y_validation))
    print()

    print('x_test')
    print('type:', type(x_test))
    print('shape:', shape(x_test))
    print()

    print('y_test')
    print('type:', type(y_test))
    print('shape:', shape(y_test))
    print()

    # Prints the first pixel of the first training image
    print('x_train[0]:')
    print(x_train[0][0][0])
    print()

    # Prints one-hot-encoding example
    print('y_train[0]:')
    print(y_train[0])
    print()

    # Prints label example
    print('labels_train[0]:')
    print(labels_train[0])

    exit(0)


if __name__ == "__main__":
    main()
