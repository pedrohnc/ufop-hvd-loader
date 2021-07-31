import os

import cv2
import numpy as np

from constant import CLASS_TO_INT
from utils import count_labels, get_label_file_names, get_file_name, get_file_prefix


def reshape(dataset_path, destiny_path, shape=None, max_dim=None, verbose=1):
    from label import LabelUtils
    if dataset_path is None:
        raise Exception('Dataset Path not informed.')
    if destiny_path is None:
        raise Exception('Destiny Path not informed.')
    if shape is None and max_dim is None:
        raise Exception('Shape or max_dim must be informed.')
    if not os.path.isdir(destiny_path):
        os.makedirs(destiny_path)
    if verbose > 0:
        print('Reshaping imagens in path:', dataset_path)
    num_files = count_labels(dataset_path)
    if verbose > 0:
        print(num_files, 'images found.')
    index = 0
    label_file_names = get_label_file_names(os.path.join(dataset_path))
    for label_file_name in label_file_names:
        label = LabelUtils.load(os.path.join(dataset_path, label_file_name))
        img = cv2.imread(label.img_file_name)
        if shape:
            img_reshaped = cv2.resize(img, shape, interpolation=cv2.INTER_AREA)
            label.width = shape[0]
            label.height = shape[1]
        else:
            h, w, _ = img.shape
            bigger_dim = max(h, w)
            if bigger_dim <= max_dim:
                img_reshaped = img
            else:
                perc = max_dim / bigger_dim
                new_h = int(h * perc)
                new_w = int(w * perc)
                img_reshaped = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                label.width = new_w
                label.height = new_h
        img_reshaped_file_name = get_file_name(label.img_file_name)
        img_reshaped_file_path = os.path.join(destiny_path, img_reshaped_file_name)
        cv2.imwrite(img_reshaped_file_path, img_reshaped)
        label.img_file_name = img_reshaped_file_path
        new_label_file_name = get_file_name(label.label_file_name)
        new_label_file_name = get_file_prefix(new_label_file_name) + '.json'
        new_label_file_path = os.path.join(destiny_path, new_label_file_name)
        label.label_file_name = new_label_file_path
        LabelUtils.save(new_label_file_path, label)
        del img
        index += 1
        if verbose > 0:
            if index % 10 == 0:
                perc = str((index * 100) // num_files)
                print(perc + '% completed...')
    if verbose > 0:
        print('100% completed.')
        print()


def load_data(datasets_path, shape=(300, 300), rescale=1. / 255, seed=None, file_name_pattern=None, shuffle=True,
              verbose=1, use_numpy_array=True):
    from utils import get_label_file_names
    from label import LabelUtils
    from utils import count_labels
    if datasets_path is None:
        raise Exception('Dataset Path not informed.')
    if type(datasets_path) != list:
        datasets_path = [datasets_path]
    if file_name_pattern:
        print('file_name_pattern:', file_name_pattern)
    num_files = 0
    if verbose > 0:
        print('Loading imagens in path:', datasets_path)
    for dataset_path in datasets_path:
        num_files += count_labels(dataset_path, include=file_name_pattern)
    if verbose > 0:
        print(num_files, 'images found.')
    labels = []
    x = []
    y = np.zeros(num_files, dtype=int)
    index = 0
    for dataset_path in datasets_path:
        label_file_names = get_label_file_names(os.path.join(dataset_path), include=file_name_pattern)
        for label_file_name in label_file_names:
            label = LabelUtils.load(os.path.join(dataset_path, label_file_name))
            img = cv2.imread(label.img_file_name)
            img_reshaped = cv2.resize(img, shape, interpolation=cv2.INTER_AREA)
            del img
            if rescale is not None:
                img_reshaped = img_reshaped * rescale
            x.append(img_reshaped)
            label.width = shape[0]
            label.height = shape[1]
            labels.append(label)
            y[index] = label.label_id
            index += 1
            if verbose > 0:
                if index % 10 == 0:
                    perc = str((index * 100) // num_files)
                    print(perc + '% completed...')
    y = np.eye(len(CLASS_TO_INT))[y]
    indexes = np.arange(num_files)
    if seed is not None:
        np.random.seed(seed)
    if shuffle:
        np.random.shuffle(indexes)
    if use_numpy_array:
        if verbose > 0:
            print('Generating numpy array...')
        try:
            x = np.array(x, dtype=object)
        except:
            # Process finished with exit code 137 (interrupted by signal 9: SIGKILL)
            print('Insufficient memory to generate numpy array.')
            print('Try to use param \'use_numpy_array=False\'.')
            exit(0)
    labels = np.array(labels)
    if use_numpy_array:
        x = x[indexes]
    else:
        x = [x[i] for i in indexes]
    y = y[indexes]
    labels = labels[indexes]
    if verbose > 0:
        print('100% completed.')
        print()
    return x, y, labels
