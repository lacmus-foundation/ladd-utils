from typing import List
import random
from lacmus_data.dataset import LaddDataset, ImageIdType, AnnotationFileReader
import argparse 
import os

def create(input_path: str, output_path: str, initial_index: int):
    output_dataset = LaddDataset(path=output_path)
    output_ids: List[ImageIdType] = []
    output_id = initial_index - 1

    for d in os.listdir(input_path):
        if not os.path.isdir(os.path.join(input_path, d)):
            continue
        for f in os.listdir(os.path.join(input_path, d)):
            filename = os.path.join(input_path, d, f)
            
            if not os.path.isfile(filename):
                continue
            if not '.xml' in f:
                continue

            output_id = output_id + 1
            reader = AnnotationFileReader(filename)
            annotations = reader.read_annotations()
            source_image_path = filename.replace('.xml', '.jpg')
            if not os.path.exists(source_image_path):
                real_source_image_path = source_image_path.replace('.jpg', '.JPG')
                if os.path.exists(real_source_image_path):
                    os.rename(real_source_image_path, source_image_path)
                else:
                    print(f"{source_image_path} is skipped!")
                    continue

            output_dataset.add(
                image_id=f'{output_id}',
                source_image_path=source_image_path,
                annotations=annotations
            )
            output_ids.append(f'{output_id}')
    

    train_count = int(len(output_ids) * 0.8)
    random.shuffle(output_ids)
    train_set = output_ids[:train_count]
    val_set = output_ids[train_count:]
    test_set = val_set
    output_dataset.write_image_sets(
        train_set=train_set,
        val_set=val_set,
        test_set=test_set
    )
    print(f"created {train_count} items!")

def add_parser(subparser):
    parser = subparser.add_parser(
        "create", help="create lacmus deone dataset from lablimg annotation", formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
    parser.add_argument(
        '--initial_index',
        help='initial index (default 0)',
        type=int,
        default=0,
        required=False
    )
    parser.set_defaults(func=main)

def main(args):
    create(
        input_path=args.input,
        output_path=args.output,
        initial_index=args.initial_index
    )