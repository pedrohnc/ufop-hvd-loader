import fnmatch
import os
import random as rd
from collections import Sequence
from typing import List

import numpy
import numpy as np


def get_file_name(file_path):
    return os.path.basename(file_path)


def get_path(file_path):
    return os.path.dirname(file_path)


def count_images(dir, exclude=None, include=None):
    return count_files(dir, get_image_extensions(), exclude=exclude, include=include)


def count_labels(dir, exclude=None, include=None):
    return count_files(dir, get_label_extensions(), exclude=exclude, include=include)


def count_files(dir, extensions=None, exclude=None, include=None):
    if not extensions:
        return sum([len(files) for r, d, files in os.walk(dir)])
    if type(extensions) is not list:
        extensions = [extensions]
    file_names = [file_names for _, _, file_names in os.walk(dir)]
    file_names = list(np.concatenate(file_names))
    file_names = list(map(lambda x: x.lower(), file_names))
    if exclude is not None:
        if type(exclude) is not list:
            exclude = [exclude]
        for ex in exclude:
            file_names = [file_name for file_name in file_names if ex not in file_name]
    if include is not None:
        if type(include) is not list:
            include = [include]
        for inc in include:
            file_names = [file_name for file_name in file_names if inc in file_name]
    num_files = 0
    for extension in extensions:
        num_files += len(fnmatch.filter(file_names, '*.' + extension))
    return num_files


def get_image_extensions():
    return ['jpg', 'jpeg', 'png']


def get_image_file_names(dir, random=None, exclude=None, include=None):
    file_names = get_file_names(dir, random, exclude, include)
    return list(filter(is_image, file_names))


def get_label_file_names(dir, random=None, exclude=None, include=None):
    file_names = get_file_names(dir, random, exclude, include)
    return list(filter(is_label, file_names))


def get_file_names(dir, random=None, exclude=None, include=None, starts_with=None, ends_with=None, recursive=True):
    if recursive:
        file_names = [file_names for _, _, file_names in os.walk(dir)]
        file_names = list(np.concatenate(file_names))
    else:
        file_names = []
        for file_name in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file_name)):
                file_names.append(file_name)
    if exclude is not None:
        if type(exclude) is not list:
            exclude = [exclude]
        for ex in exclude:
            file_names = [file_name for file_name in file_names if ex not in file_name]
    if include is not None:
        if type(include) is not list:
            include = [include]
        for inc in include:
            file_names = [file_name for file_name in file_names if inc in file_name]
    if starts_with is not None:
        file_names = [file_name for file_name in file_names if file_name.startswith(starts_with)]
    if ends_with is not None:
        file_names = [file_name for file_name in file_names if file_name.endswith(ends_with)]
    if random is not None:
        num_samples = int(random * len(file_names))
        file_names = rd.sample(file_names, k=num_samples)
    return file_names


def is_image(file_name):
    return get_file_extension(file_name).lower() in get_image_extensions()


def is_label(file_name):
    return get_file_extension(file_name).lower() in get_label_extensions()


def is_json(file_name):
    return get_file_extension(file_name).lower() == 'json'


def is_xml(file_name):
    return get_file_extension(file_name).lower() == 'xml'


def get_file_prefix(file_name):
    return split_file_name(file_name)[0]


def get_file_extension(file_name):
    return split_file_name(file_name)[1]


def get_label_extensions():
    return ['txt', 'csv', 'json', 'xml']


def split_file_name(file_name):
    file_names = file_name.rsplit('.', 1)
    if len(file_names) < 2:
        raise Exception('Invalid filename:', file_name)
    return file_names


def shape(lst):
    if isinstance(lst, List):
        return len(lst), lst[0].shape[0], lst[0].shape[1], lst[0].shape[2]
    elif isinstance(lst, numpy.ndarray):
        return lst.shape
    return None
