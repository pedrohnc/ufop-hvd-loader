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

```python
def reshape(dataset_path, destiny_path, shape=None, max_dim=None, verbose=1):
    ...


def load_data(datasets_path, shape=(300, 300), rescale=1. / 255, seed=None, file_name_pattern=None, shuffle=True,
              verbose=1, use_numpy_array=True):
    ...
```
