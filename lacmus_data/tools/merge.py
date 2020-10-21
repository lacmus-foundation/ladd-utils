from typing import List
import random
from lacmus_data.dataset import Annotation, Rectangle, LaddDataset, ImageIdType
import argparse

def merge_datasets(input_pathes: List[str], output_path: str, include_test: bool = False):
    output_dataset = LaddDataset(path=output_path)
    output_train_set: List[ImageIdType] = []
    output_test_set: List[ImageIdType] = []
    output_val_set: List[ImageIdType] = []
    output_id = -1

    for imput_path in input_pathes:
        imput_dataset = LaddDataset(path=imput_path)
        train_set, test_set, val_set = imput_dataset.train_test_val_ids()
        print(f'add {len(imput_dataset.ids())} of {imput_path}')
        
        for id in train_set:
            output_id = output_id + 1
            annotations = imput_dataset.annotations(id)
            output_dataset.add(
                image_id=f'{output_id}',
                source_image_path=imput_dataset.image_filename(id),
                annotations=annotations
            )
            output_train_set.append(f'{output_id}')

        for id in val_set:
            output_id = output_id + 1
            annotations = imput_dataset.annotations(id)
            output_dataset.add(
                image_id=f'{output_id}',
                source_image_path=imput_dataset.image_filename(id),
                annotations=annotations
            )
            output_val_set.append(f'{output_id}')
        
        if include_test:
            for id in test_set:
                output_id = output_id + 1
                annotations = imput_dataset.annotations(id)
                output_dataset.add(
                    image_id=f'{output_id}',
                    source_image_path=imput_dataset.image_filename(id),
                    annotations=annotations
                )
                output_test_set.append(f'{output_id}')
        
        if include_test:
            print(f'added {len(output_test_set)+len(output_val_set)+len(output_train_set)}')
        else:
            print(f'added {len(output_val_set)+len(output_train_set)}')
            output_test_set = output_val_set
    
    random.shuffle(output_train_set)
    random.shuffle(output_val_set)
    random.shuffle(output_test_set)
    output_dataset.write_image_sets(
        train_set=output_train_set,
        val_set=output_val_set,
        test_set=output_test_set)
    
    print(f'dataset {output_path} created with {len(output_dataset.ids())} items.')

def add_parser(subparser):
    parser = subparser.add_parser(
        "merge", help="merge lacmus deone datasets", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        help='list of imput pathes, e.g. -i path1 path2 path3 ',
        nargs='+',
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
        '--include_test',
        help='include tast images',
        action='store_true',
        required=False
    )
    parser.set_defaults(func=main)

def main(args):
    merge_datasets(
        input_pathes=args.input,
        output_path=args.output,
        include_test=args.include_test
    )
   


    
        
        

