# ufop-hvd-loader
Python application for loading images and labels from the UFOP Hop Varieties Dataset.

## Dataset
The dataset is available at the link below:

http://www.decom.ufop.br/csilab/databases/

## Dependencies
To run this application you need the numpy and opencv packages, which can be installed with the following command:
```sh
pip install numpy opencv-python
```

## Main Files
This section contains the description of the main files and methods of the project.
### data.py
This file contains methods **reshape** and **load_data**.

The method **reshape** is responsible for resizing the images and saving them in a new file. Although images can be read directly without prior resizing, this is not recommended due to performance issues. It must receive an output shape parameter in the format (width, height), the path with the original images and the destination path. It returns nothing.

The **load_data** reads the image and its labels from one or more directories. If it hasn't already been done, it can receive a shape parameter to resize the images. The return consists of a list (or a numpy array) of all pixel-mapped images assuming values from 0 to 1 in each channel, a list of the corresponding class of each image in one-hot-encoding format, and a list of labels of type **Label** (which will be described later). If when trying to load the images you get the error `Process finished with exit code 137 (interrupted by signal 9: SIGKILL)`, it may be due to excessive use of memory to generate the numpy array. In that case, you can use the parameter `use_numpy_array=False` to mitigate it.

```python
def reshape(dataset_path, destiny_path, shape=None, max_dim=None, verbose=1):
    ...


def load_data(datasets_path, shape=(300, 300), rescale=1. / 255, seed=None, file_name_pattern=None, shuffle=True,
              verbose=1, use_numpy_array=True):
    ...
    return x, y, labels
```
### label.py
This file contains **Label** and **LabelUtils** classes.

The **Label** class favors the manipulation of bounding boxes since, unlike the Pascal VOC format, they are already normalized (many frameworks prefer this way). In addition, it also reports the index of the largest bounding box (main_boundin_box).

The **LabelUtils** class can be used to save and load xml and json format files.

```python
class Label:

    def __init__(self, label_id=None, label_name=None, label_description=None, main_bounding_box=None,
                 bounding_boxes=None, height=None, width=None, img_file_name=None, label_file_name=None):
        ...
        
class LabelUtils:

    ...
                 
```
## Usage Example

The **main.py** file contains an example of using the application, where the images are resized (only the first time it is run). Then they are read with their labels. Finally, the program prints some information such as the type and shape of each output and an sample of an image, an one-hot-encoding and a label. The second and later runs will be faster than the first, as you won't need to resize the images again.

```python
# Prints type and shape
x_train
type: <class 'list'>
shape: (1128, 300, 300, 3)

y_train
type: <class 'numpy.ndarray'>
shape: (1128, 12)

x_validation
type: <class 'numpy.ndarray'>
shape: (232, 300, 300, 3)

y_validation
type: <class 'numpy.ndarray'>
shape: (232, 12)

x_test
type: <class 'numpy.ndarray'>
shape: (232, 300, 300, 3)

y_test
type: <class 'numpy.ndarray'>
shape: (232, 12)

# Prints the first pixel of the first training image
x_train[0][0][0]:
[0.97254902 0.78431373 0.50196078]

# Prints one-hot-encoding example
y_train[0]:
[0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

# Prints label example
labels_train[0]:
label_id: 2
label_name: sorachi_ace
label_description: Sorachi Ace
main_bounding_box: 0
bounding_boxes: [[0.12003968253968254, 0.31473214285714285, 0.8485449735449735, 0.9590773809523809]]
height: 300
width: 300
img_file_name: /media/share/datasets/lupulo/ufop-hvd-reshaped/train/sorachi_ace_l2_11.jpg
label_file_name: /media/share/datasets/lupulo/ufop-hvd-reshaped/train/sorachi_ace_l2_11.json
```
