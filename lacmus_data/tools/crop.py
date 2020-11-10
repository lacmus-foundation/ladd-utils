from lacmus_data.cropper import DatasetGridCropper, ImageGridCropper
from lacmus_data.dataset import LaddDataset
import os
import argparse
import tqdm

def run_crop(source_path: str,
             target_path: str,
             image_width: int,
             image_height: int,
             overlap_width: int,
             overlap_height: int,
             min_cropped_bbox_square: int) -> None:
    """Разрезание изображений из датасета и формирование нового датасета (формат Pascal VOC)"""
    cropper = DatasetGridCropper(
        source_dataset=LaddDataset(path=source_path),
        target_dataset=LaddDataset(path=target_path),
        image_cropper=ImageGridCropper(
            window_w=image_width,
            window_h=image_height,
            overlap_w=overlap_width,
            overlap_h=overlap_height,
            min_cropped_bbox_square=min_cropped_bbox_square
        ),
        iter_callback=tqdm.tqdm
    )
    cropper.generate_dataset(prob=0.5)

def add_parser(subparser):
    parser = subparser.add_parser(
        "crop", help="crop lacmus deone dataset", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        help='input path',
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
        '--crop-width',
        help='crop width (default 800)',
        type=int,
        required=False,
        default=800
    )
    parser.add_argument(
        '--crop-height',
        help='crop height (default 800)',
        type=int,
        required=False,
        default=800
    )
    parser.add_argument(
        '--overlap-width',
        help='overlap width (default 125)',
        type=int,
        required=False,
        default=125
    )
    parser.add_argument(
        '--overlap-height',
        help='overlap height (default 125)',
        type=int,
        required=False,
        default=125
    )
    parser.add_argument(
        '--min-cropped-bbox-square',
        help='minimum area of ​​the new bbox in relation to the original (default 0.8)',
        type=float,
        required=False,
        default=0.8
    )
    parser.set_defaults(func=main)

def main(args):
    assert os.path.exists(args.input), f'imput path dose not exists {args.input}' 
    run_crop(
        source_path=args.input,
        target_path=args.output,
        image_width=args.crop_width,
        image_height=args.crop_height,
        overlap_width=args.overlap_width,
        overlap_height=args.overlap_height,
        min_cropped_bbox_square=args.min_cropped_bbox_square
    )