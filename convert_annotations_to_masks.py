import os
import json
import argparse
import numpy as np
import cv2

def parse_args():
    parser = argparse.ArgumentParser(description='Convert annotation JSON to mask images')
    parser.add_argument('--json', type=str, required=True, help='Path to annotation JSON file')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save mask images')
    parser.add_argument('--img_width', type=int, default=512, help='Width of mask image')
    parser.add_argument('--img_height', type=int, default=512, help='Height of mask image')
    parser.add_argument('--prefix', type=str, default='mask', help='Prefix for output mask files')
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.json, 'r') as f:
        annotations = json.load(f)

    # Create a single mask for all boxes in the file
    mask = np.zeros((args.img_height, args.img_width), dtype=np.uint8)
    for ann in annotations:
        box_min = ann['box_min']
        box_max = ann['box_max']
        # Convert float coordinates to int pixel indices
        x1, y1 = int(round(box_min['x'])), int(round(box_min['y']))
        x2, y2 = int(round(box_max['x'])), int(round(box_max['y']))
        # Clamp to image bounds
        x1, x2 = max(0, x1), min(args.img_width-1, x2)
        y1, y2 = max(0, y1), min(args.img_height-1, y2)
        mask[y1:y2+1, x1:x2+1] = 255  # 255 for mask

    out_path = os.path.join(args.output_dir, f"{args.prefix}.png")
    cv2.imwrite(out_path, mask)
    print(f"Saved mask to {out_path}")

if __name__ == '__main__':
    main() 