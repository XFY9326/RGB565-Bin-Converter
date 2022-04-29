# RGB565-Bin-Converter

Convert image from rgb_888 to rgb_565 binary file

## Requirements

- Python 3
- Pillow

## Usage

Install dependenices:

```shell
pip3 install Pillow
```

Run python script:

```
usage: main.py [-h] --input INPUT [--output OUTPUT] [--endian {little,big}] [--show]

Convert image color format from RGB888 to RGB565.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         input image path
  --output OUTPUT       output image path
  --endian {little,big}
                        little or big endian
  --show                preview image after output

```

## Output file format

| Bits              | Type           | Description                                            |
|-------------------|----------------|--------------------------------------------------------|
| 16                | unsigned short | width                                                  |
| 16                | unsigned short | height                                                 |
| 16\*width\*height | unsigned short | pixel RGB_565 (from left to right, from top to bottom) |
