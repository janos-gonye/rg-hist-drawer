import argparse
import os

from rg_hist import draw_rg_hist


def constrast_strech_value(arg):
    try:
        v = float(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if v < 0 or v > 1:
        raise argparse.ArgumentTypeError("Argument must be <= 1 and >= 0")
    return v


def positive_or_zero(arg):
    try:
        v = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if v < 0:
        raise argparse.ArgumentTypeError("Must be >= 0")
    return v


def get_argparser():
    description = "Script to generate an rg histogram of an image"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'input',
        help="Image from which to generate the rg histogram")
    parser.add_argument(
        "-o", "--output",
        default=None, type=str,
        help="Output path. Default is '<input>_hist.ext'.")
    parser.add_argument(
        "-min", "--contrast-stretch-min",
        default=0.0, type=constrast_strech_value,
        help=(
            "Get rid of X%% of the darkest pixels when performing "
            "contrast streching on the histogram. Default is '0.0'."
        ))
    parser.add_argument(
        "-max", "--contrast-stretch-max",
        default=0.9975, type=constrast_strech_value,
        help=(
            "Keep X%% of the less bright pixels when performing "
            "contrast streching on the histogram. Default is '0.9975'."
        ))
    parser.add_argument(
        "-s", "--size",
        default=2048, type=positive_or_zero,
        help="Size of the output image. Default is '2048'.")
    parser.add_argument(
        "-b", "--blur",
        default=0, type=positive_or_zero,
        help="Size of the blur applied on the output image. Default is '0'.")
    return parser


def default_output(path_in):
    filename, ext = os.path.basename(path_in).split(".")
    head, _ = os.path.split(path_in)
    return os.path.join(head, f"{filename}_hist.{ext}")


def main():
    parser = get_argparser()
    args = parser.parse_args()

    if args.output is None:
        path_out = default_output(args.input)

    draw_rg_hist(
        path_in=args.input, path_out=path_out,
        a1=args.contrast_stretch_min, a2=args.contrast_stretch_max,
        size=args.size, blur=args.blur)
    print(f"rg histogram: {path_out}")


if __name__ == '__main__':
    main()
