import argparse
import os.path as osp

import imageio
import tqdm

from ..utils import get_macro_block_size


def tovideo(in_file, inplace=False):
    stem, ext = osp.splitext(in_file)
    out_file = stem + "_tovideo" + ext

    reader = imageio.get_reader(in_file)
    meta_data = reader.get_meta_data()
    fps = meta_data["fps"]

    macro_block_size = get_macro_block_size(meta_data["size"])

    writer = imageio.get_writer(
        out_file, fps=fps, macro_block_size=macro_block_size
    )

    for i in tqdm.trange(reader.count_frames()):
        data = reader.get_data(i)
        writer.append_data(data)

    reader.close()
    writer.close()

    if inplace:
        raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("in_files", nargs="+", help="input video")
    parser.add_argument(
        "--inplace", "-i", action="store_true", help="operate in-place"
    )
    args = parser.parse_args()

    for in_file in args.in_files:
        tovideo(in_file, inplace=args.inplace)
