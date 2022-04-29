#!/usr/bin/env python3

import os
import sys
import struct
import argparse

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert image color format from RGB888 to RGB565.')
    parser.add_argument('--input', required=True, type=str, help='input image path')
    parser.add_argument('--output', type=str, help='output image path')
    parser.add_argument('--endian', type=str, default="little", help='little or big endian', choices=["little", "big"])
    parser.add_argument('--show', help='preview image after output', action='store_true')
    return parser.parse_args()


def open_image(file_path: str) -> Image.Image:
    if not os.path.isfile(file_path):
        sys.exit(f"File not found in '{file_path}'!")
    try:
        return Image.open(file_path)
    except:
        sys.exit(f"Can't open image file '{file_path}'!")


def get_default_output_path(input_path: str) -> str:
    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    if "." in base_name:
        base_name = base_name[:base_name.rindex(".")]
    base_name += "_rgb565.bin"
    return dir_name + base_name


# 16 bits unsigned short -> width
# 16 bits unsigned short -> height
# 16 bits unsigned short -> pixel RGB_565 (from left to right, from top to bottom)
def convert_image_to_bin(img: Image.Image, output_path: str, little_endian: bool = True):
    if little_endian:
        struct_format = "<H"
    else:
        struct_format = ">H"
    pixels = img.load()
    with open(output_path, "wb") as f:
        width, height = img.size
        f.write(struct.pack(struct_format, width))
        f.write(struct.pack(struct_format, height))
        for h in range(height):
            for w in range(width):
                # noinspection PyUnresolvedReferences
                r, g, b = pixels[w, h][0], pixels[w, h][1], pixels[w, h][2]
                r, g, b = r >> 3, g >> 2, b >> 3
                p = r << 11 | g << 5 | b
                f.write(struct.pack(struct_format, p))


def show_image_from_bin(file_path: str, little_endian: bool = True):
    if little_endian:
        struct_format = "<H"
    else:
        struct_format = ">H"
    with open(file_path, "rb") as f:
        width = struct.unpack(struct_format, f.read(2))[0]
        height = struct.unpack(struct_format, f.read(2))[0]
        img = Image.new("RGB", (width, height))
        pixels = img.load()
        for h in range(height):
            for w in range(width):
                p = struct.unpack(struct_format, f.read(2))[0]
                r, g, b = (p & 0xF800) >> 11, (p & 0x7E0) >> 5, p & 0x1F
                r, g, b = r << 3, g << 2, b << 3
                # noinspection PyUnresolvedReferences
                pixels[w, h] = (r, g, b)
    img.show("RGB_565 to RGB_888")


def main():
    name_space = parse_args()
    input_image = open_image(name_space.input)
    output_path = name_space.output if name_space.output is not None else get_default_output_path(name_space.input)
    little_endian = True if name_space.endian == "little" else False
    print(f"Input: {name_space.input}")
    print(f"Output: {output_path}")
    print(f"Export endian: {'Little-Endian' if little_endian else 'Big-Endian'}")
    print(f"Input image mode: {input_image.mode}")
    print(f"Image size: w-{input_image.size[0]} * h-{input_image.size[1]}")
    if input_image.size[0] < 0 or input_image.size[0] > 65535:
        sys.exit("Image width should in [0, 65535]")
    elif input_image.size[1] < 0 or input_image.size[1] > 65535:
        sys.exit("Image height should in [0, 65535]")
    convert_image_to_bin(input_image, output_path, little_endian)
    print("\nConvert success!")
    if name_space.show:
        show_image_from_bin(output_path, little_endian)


if __name__ == '__main__':
    main()
