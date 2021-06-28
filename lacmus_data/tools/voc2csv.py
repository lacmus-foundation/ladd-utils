from typing import List
import random
from lacmus_data.dataset import Annotation, Rectangle, LaddDataset, ImageIdType
import argparse
import os

def sort(items: List[str]) -> List[int]:
    int_items = map(lambda x: int(x), items)
    sorted_items = sorted(int_items)
    result = map(lambda x: str(x), sorted_items)
    return result

def merge_datasets(input_path: str, output_path: str):
    input_dataset = LaddDataset(path=input_path)
    train_set, test_set, val_set = input_dataset.train_test_val_ids()
    print(f'load daa with {len(train_set)} train images, {len(test_set)} test images, {len(val_set)} val images')
    ouutput_rows = [
        'image_filename,xmin,ymin,xmax,ymax\n'
    ]
    for id in sort(train_set):
        annotations = input_dataset.annotations(str(id))
        image_filename = os.path.basename(input_dataset.image_filename(id))

        for annotation in annotations:
            xmin = annotation.bbox.xmin
            xmax = annotation.bbox.xmax
            ymin = annotation.bbox.ymin
            ymax = annotation.bbox.ymax
            row = f'{image_filename},{xmin},{ymin},{xmax},{ymax}\n'
            ouutput_rows.append(row)
    open(os.path.join(output_path, 'train.csv'), 'w').writelines(ouutput_rows)

    ouutput_rows = [
        'image_filename,xmin,ymin,xmax,ymax\n'
    ]

    for id in sort(val_set):
        annotations = input_dataset.annotations(id)
        image_filename = os.path.basename(input_dataset.image_filename(id))

        for annotation in annotations:
            xmin = annotation.bbox.xmin
            xmax = annotation.bbox.xmax
            ymin = annotation.bbox.ymin
            ymax = annotation.bbox.ymax
            row = f'{image_filename},{xmin},{ymin},{xmax},{ymax}\n'
            ouutput_rows.append(row)
    open(os.path.join(output_path, 'val.csv'), 'w').writelines(ouutput_rows)

    ouutput_rows = [
        'image_filename,xmin,ymin,xmax,ymax\n'
    ]    
    for id in sort(test_set):
        annotations = input_dataset.annotations(id)
        image_filename = os.path.basename(input_dataset.image_filename(id))

        for annotation in annotations:
            xmin = annotation.bbox.xmin
            xmax = annotation.bbox.xmax
            ymin = annotation.bbox.ymin
            ymax = annotation.bbox.ymax
            row = f'{image_filename},{xmin},{ymin},{xmax},{ymax}\n'
            ouutput_rows.append(row)
    open(os.path.join(output_path, 'test.csv'), 'w').writelines(ouutput_rows)
        
    

def add_parser(subparser):
    parser = subparser.add_parser(
        "voc2csv", help="convert voc to csv format", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        help='imput path',
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        help='output path',
        type=str,
        required=True
    )
    parser.set_defaults(func=main)

def main(args):
    merge_datasets(
        input_path=args.input,
        output_path=args.output
    )
   


    
        
        

