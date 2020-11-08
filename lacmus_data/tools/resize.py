from typing import List
import random
from lacmus_data.dataset import Annotation, Rectangle, LaddDataset, ImageIdType
import argparse
import cv2
import shutil

def compute_resize_scale(image_shape, min_side=800, max_side=1333):
    """ Compute an image scale such that the image size is constrained to min_side and max_side.
    Args
        min_side: The image's min side will be equal to min_side after resizing.
        max_side: If after resizing the image's max side is above max_side, resize until the max side is equal to max_side.
    Returns
        A resizing scale.
    """
    (rows, cols, _) = image_shape

    smallest_side = min(rows, cols)

    # rescale the image so the smallest side is min_side
    scale = min_side / smallest_side

    # check if the largest side is now greater than max_side, which can happen
    # when images have a large aspect ratio
    largest_side = max(rows, cols)
    if largest_side * scale > max_side:
        scale = max_side / largest_side

    return scale


def resize_image(img, min_side=800, max_side=1333):
    """ Resize an image such that the size is constrained to min_side and max_side.
    Args
        min_side: The image's min side will be equal to min_side after resizing.
        max_side: If after resizing the image's max side is above max_side, resize until the max side is equal to max_side.
    Returns
        A resized image.
    """
    # compute scale to resize the image
    scale = compute_resize_scale(img.shape, min_side=min_side, max_side=max_side)

    # resize the image with the computed scale
    img = cv2.resize(img, None, fx=scale, fy=scale)

    return img, scale

def resize(input_path: str, output_path: str,
        min_side: int, max_side: int) -> None:
    imput_dataset = LaddDataset(path=input_path)
    output_dataset = LaddDataset(path=output_path)
    ids = imput_dataset.ids()
    
    for id in ids:
        annotations = imput_dataset.annotations(id)
        img = cv2.imread(imput_dataset.image_filename(id))
        img, scale = resize_image(img, min_side=min_side, max_side=max_side)
        scaled_annotations = []

        for annotation in annotations:
            scaled_annotation = Annotation(
                label=annotation.label,
                bbox=Rectangle(
                    xmin=int(annotation.bbox.xmin * scale),
                    ymin=int(annotation.bbox.ymin * scale),
                    xmax=int(annotation.bbox.xmax * scale),
                    ymax=int(annotation.bbox.ymax * scale),
                )
            )
            scaled_annotations.append(scaled_annotation)

        output_dataset.images_dir().mkdir(parents=True, exist_ok=True)
        image_filename = output_dataset.image_filename(id)
        cv2.imwrite(image_filename, img)
        
        output_dataset.add(
                image_id=f'{id}',
                source_image_path=image_filename,
                annotations=scaled_annotations
            )

    train_set, test_set, val_set = imput_dataset.train_test_val_ids()
    output_dataset.write_image_sets(
        train_set=train_set,
        val_set=val_set,
        test_set=test_set)
    print(f"resized {len(ids)} items!")

def add_parser(subparser):
    parser = subparser.add_parser(
        "resize", help="resize images and annotations at lacmus deone dataset", formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
        '--min_side',
        help='min image side (default 2100)',
        type=int,
        default=2100,
        required=False
    )
    parser.add_argument(
        '--max_side',
        help='max image side (default 2100)',
        type=int,
        default=2100,
        required=False
    )
    parser.set_defaults(func=main)

def main(args):
    resize(
        input_path=args.input,
        output_path=args.output,
        min_side=args.min_side,
        max_side=args.max_side
    )