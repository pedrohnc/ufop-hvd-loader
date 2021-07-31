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
