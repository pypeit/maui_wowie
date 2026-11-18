"""
Script to download the Keck/HIRES observations of Q1645+5520 taken on
UT 1997-05-09 and UT 1997-05-29 from the Keck Observatory Archive (KOA).

Only the frames matching the instrument setup of the Q1645+5520 science
exposures are downloaded (science, arcs, flats, standards, biases/darks).
The UT 1997-05-09 night has a single setup.  The UT 1997-05-29 night has
two; the one with the echelle angle closest to UT 1997-05-09 is selected.

Usage::

    conda run -n pypeit14 python -m maui_wowie.io.download_q1645
"""
import os
import argparse

import numpy as np

from maui_wowie.io import koa


# Root directory for the HIRES data of this project
DATA_ROOT = '/Users/xavier/Astronomy/data/MauiWowie/HIRES'

# Name of the target, as used for the output folders
TARGET = 'Q1645+5520'

# UT dates of the observations.  The first is the reference night: its
# echelle angle is used to choose the setup on the nights that follow.
DATES = ['1997-05-09', '1997-05-29']


def get_parser():
    """
    Construct the command-line argument parser.

    Returns:
        `argparse.ArgumentParser`_: The parser.
    """
    parser = argparse.ArgumentParser(
        description='Download the HIRES data of Q1645+5520 from KOA.')
    parser.add_argument('--root', type=str, default=DATA_ROOT,
                        help='Root directory for the downloaded data.')
    parser.add_argument('--dry_run', default=False, action='store_true',
                        help='Query KOA and list the selected frames, but '
                             'do not download them.')
    return parser


def main(args):
    """
    Query KOA, select the frames in the Q1645+5520 setups and download them.

    Args:
        args (`argparse.Namespace`_):
            Parsed command-line arguments; see :func:`get_parser`.

    Returns:
        :obj:`int`: 0 if every selected frame is on disk (or for a dry
        run), 1 otherwise.
    """
    ref_echangl = None
    status = 0
    for date in DATES:
        # One folder per night, named by date and object
        outdir = os.path.join(args.root, f'{date}_{TARGET}')

        # Metadata for every HIRES frame taken that night
        night = koa.query_night(date, os.path.join(outdir, 'koa_night.tbl'))

        # Restrict to the setup of the science exposures
        selected = koa.select_setup(night, TARGET, echangl=ref_echangl)

        # The first night sets the reference echelle angle
        is_sci = selected['koaimtyp'] == 'object'
        sci_names = [koa.normalize_name(n) for n in selected['targname']]
        is_sci &= np.array(sci_names) == koa.normalize_name(TARGET)
        if ref_echangl is None:
            ref_echangl = float(np.median(selected['echangl'][is_sci]))

        print(f'UT {date}: selected {len(selected)} of {len(night)} frames '
              f'({np.sum(is_sci)} science exposures of {TARGET})')
        koa.summarize(selected)

        if args.dry_run:
            continue

        # Download and report anything that did not arrive
        missing = koa.download(selected, outdir)
        if len(missing) > 0:
            status = 1
            print(f'UT {date}: {len(missing)} frames are missing:')
            for path in missing:
                print(f'    {path}')
        else:
            print(f'UT {date}: all {len(selected)} frames are in '
                  f'{os.path.join(outdir, "lev0")}')
    return status


if __name__ == '__main__':
    raise SystemExit(main(get_parser().parse_args()))
