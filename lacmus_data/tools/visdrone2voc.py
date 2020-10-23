from typing import List
import random
from lacmus_data.dataset import Annotation, Rectangle, LaddDataset, ImageIdType
import argparse
import os

# regions(0)
# pedestrian(1) -> Pedestrian
# people(2)     -> Pedestrian
# bicycle(3)
# car(4)
# van(5)
# truck(6)
# tricycle(7)
# awning-tricycle(8)
# bus(9)
# motor(10)
# others(11)
labels = {
    1: "Pedestrian",
    2: "Pedestrian"
}

def visdrone2voc(input_path: str, output_path: str, labels: dict):
    train_annotations_dir = os.path.join(input_path, 'train', 'annotations')
    train_inages_dir = os.path.join(input_path, 'train', 'images')
    val_annotations_dir = os.path.join(input_path, 'val', 'annotations')
    val_inages_dir = os.path.join(input_path, 'val', 'images')
    
    output_dataset = LaddDataset(path=output_path)
    output_train_set: List[ImageIdType] = []
    output_test_set: List[ImageIdType] = []
    output_val_set: List[ImageIdType] = []
    output_id = -1

    fnames = os.listdir(train_annotations_dir)
    train_ids = []
    for name in fnames:
        train_ids.append(name.replace('.txt', ''))
    
    for id in train_ids:
        lines = open(os.path.join(train_annotations_dir, f'{id}.txt'), 'r').readlines()
        annotations = []

        for line in lines:
            # <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
            words = line.split(',')
            xmin = int(words[0])
            ymin = int(words[1])
            xmax = xmin + int(words[2])
            ymax = ymin + int(words[3])
            object_category = int(words[5])
            if object_category not in labels.keys():
                continue

            label = labels[object_category]

            annotation = Annotation(
                label=label,
                bbox=Rectangle(
                    xmin=xmin,
                    ymin=ymin,
                    xmax=xmax,
                    ymax=ymax,
                )
            )

            annotations.append(annotation)
        
        output_id = output_id + 1
        output_dataset.add(
            image_id=f'{output_id}',
            source_image_path=os.path.join(train_inages_dir, f'{id}.jpg'),
            annotations=annotations
        )
        output_train_set.append(f'{output_id}')
    
    fnames = os.listdir(val_annotations_dir)
    train_ids = []
    for name in fnames:
        train_ids.append(name.replace('.txt', ''))
    
    for id in train_ids:
        lines = open(os.path.join(val_annotations_dir, f'{id}.txt'), 'r').readlines()
        annotations = []

        for line in lines:
            # <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
            words = line.split(',')
            xmin = int(words[0])
            ymin = int(words[1])
            xmax = xmin + int(words[2])
            ymax = ymin + int(words[3])
            object_category = int(words[5])
            if object_category not in labels.keys():
                continue

            label = labels[object_category]

            annotation = Annotation(
                label=label,
                bbox=Rectangle(
                    xmin=xmin,
                    ymin=ymin,
                    xmax=xmax,
                    ymax=ymax,
                )
            )

            annotations.append(annotation)
        
        output_id = output_id + 1
        output_dataset.add(
            image_id=f'{output_id}',
            source_image_path=os.path.join(val_inages_dir, f'{id}.jpg'),
            annotations=annotations
        )
        output_val_set.append(f'{output_id}')
    
    output_test_set = output_val_set
    random.shuffle(output_train_set)
    random.shuffle(output_val_set)
    output_dataset.write_image_sets(
        train_set=output_train_set,
        val_set=output_val_set,
        test_set=output_test_set)
    
    print(f'dataset {output_path} created with {len(output_dataset.ids())} items.')


def add_parser(subparser):
    parser = subparser.add_parser(
        "visdrone2voc", help="convert visdrone to lacmus voc format", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        help='imput path',
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        help='save path',
        type=str,
        required=True
    )
    parser.set_defaults(func=main)

def main(args):
    visdrone2voc(
        input_path=args.input,
        output_path=args.output,
        labels=labels
    )


