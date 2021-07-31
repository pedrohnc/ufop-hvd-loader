import json
import os.path
import xml.etree.ElementTree as ET
from json import JSONDecoder

from constant import CLASS_TO_INT, LABELS
from utils import get_file_name, get_path, is_json, is_xml


class Label:

    def __init__(self, label_id=None, label_name=None, label_description=None, main_bounding_box=None,
                 bounding_boxes=None, height=None, width=None, img_file_name=None, label_file_name=None):
        super().__init__()
        self.label_id = label_id
        self.label_name = label_name
        self.label_description = label_description
        self.main_bounding_box = main_bounding_box
        self.bounding_boxes = bounding_boxes
        self.height = height
        self.width = width
        self.img_file_name = img_file_name
        self.label_file_name = label_file_name

    def encode(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def decode(self, label_json):
        label_dict = JSONDecoder().decode(label_json)
        self.label_id = label_dict['label_id']
        self.label_name = label_dict['label_name']
        self.label_description = label_dict['label_description']
        self.height = label_dict['height']
        self.width = label_dict['width']
        self.img_file_name = label_dict['img_file_name']
        self.label_file_name = label_dict['label_file_name']
        if 'main_bounding_box' in label_dict:
            self.main_bounding_box = label_dict['main_bounding_box']
        else:
            self.main_bounding_box = None
        if 'bounding_boxes' in label_dict:
            self.bounding_boxes = label_dict['bounding_boxes']
        else:
            self.bounding_boxes = None
        return self

    def __str__(self) -> str:
        return 'label_id: ' + str(self.label_id) \
               + '\nlabel_name: ' + str(self.label_name) \
               + '\nlabel_description: ' + str(self.label_description) \
               + '\nmain_bounding_box: ' + str(self.main_bounding_box) \
               + '\nbounding_boxes: ' + str(self.bounding_boxes) \
               + '\nheight: ' + str(self.height) \
               + '\nwidth: ' + str(self.width) \
               + '\nimg_file_name: ' + str(self.img_file_name) \
               + '\nlabel_file_name: ' + str(self.label_file_name)


class LabelUtils:

    @staticmethod
    def save(file_name, label):
        with open(file_name, 'w') as file:
            label_json = label.encode()
            file.write(label_json)

    @staticmethod
    def load(file_name) -> Label:
        if is_json(file_name):
            return LabelUtils.load_json(file_name)
        elif is_xml(file_name):
            return LabelUtils.load_xml(file_name)

    @staticmethod
    def load_json(file_name) -> Label:
        try:
            with open(file_name) as json_file:
                return json.load(json_file, cls=Label)
        except:
            pass

    @staticmethod
    def load_xml(xml_file_name) -> Label:
        tree = ET.parse(xml_file_name)
        root = tree.getroot()
        file_name = root.find('filename').text
        img_file_name = os.path.join(get_path(xml_file_name), get_file_name(file_name))
        width = int(root.find('size')[0].text)
        height = int(root.find('size')[1].text)
        label_name = None
        label_id = None
        label_description = None
        main_bounding_box = None
        bounding_boxes = []
        for member in root.findall('object'):
            if not label_name:
                label_name = member[0].text
                label_id = CLASS_TO_INT[label_name]
                label_description = LABELS[label_id]
            x_min = float(int(member[4][0].text)) / float(width)
            y_min = float(int(member[4][1].text)) / float(height)
            x_max = float(int(member[4][2].text)) / float(width)
            y_max = float(int(member[4][3].text)) / float(height)
            bounding_box = [x_min, y_min, x_max, y_max]
            bounding_boxes.append(bounding_box)
            if main_bounding_box is None:
                main_bounding_box = 0
            elif LabelUtils.area(bounding_box) > LabelUtils.area(bounding_boxes[main_bounding_box]):
                main_bounding_box = len(bounding_boxes) - 1
        return Label(label_id=label_id, label_name=label_name, label_description=label_description,
                     main_bounding_box=main_bounding_box,
                     bounding_boxes=bounding_boxes, height=height, width=width, img_file_name=img_file_name,
                     label_file_name=xml_file_name)

    @staticmethod
    def area(bounding_box: []):
        if bounding_box is None:
            return None
        x_min, y_min, x_max, y_max = bounding_box
        return (x_max - x_min) * (y_max - y_min)
