"""
Script to run ``pypeit_setup`` on a night of Keck/HIRES data and generate
the PypeIt reduction file(s).

``pypeit_setup`` is executed from within the data directory, with the raw
frames read from its ``lev0`` sub-folder (the structure written by
:mod:`maui_wowie.io.koa`).  By default the script processes the
UT 1997-05-09 observations of Q1645+5520.

Usage::

    conda run -n pypeit14 python -m maui_wowie.pypeit.run_setup
"""
import os
import argparse

from pypeit.scripts.setup import Setup


# Default data directory: the UT 1997-05-09 night of Q1645+5520
DATA_DIR = '/Users/xavier/Astronomy/data/MauiWowie/HIRES/1997-05-09_Q1645+5520'

# PypeIt spectrograph for the original (pre August 2004) HIRES detector
SPECTROGRAPH = 'keck_hires_orig'


def get_parser():
    """
    Construct the command-line argument parser.

    Returns:
        `argparse.ArgumentParser`_: The parser.
    """
    parser = argparse.ArgumentParser(
        description='Run pypeit_setup on a night of HIRES data.')
    parser.add_argument('--datadir', type=str, default=DATA_DIR,
                        help='Data directory for the night; the raw frames '
                             'are expected in its lev0 sub-folder.')
    parser.add_argument('--spectrograph', type=str, default=SPECTROGRAPH,
                        help='PypeIt spectrograph name.')
    parser.add_argument('--cfg_split', type=str, default='all',
                        help='Configurations to write PypeIt files for; '
                             'passed to pypeit_setup -c.')
    parser.add_argument('--no_overwrite', default=False, action='store_true',
                        help='Do not overwrite existing pypeit_setup output.')
    return parser


def main(args):
    """
    Run ``pypeit_setup`` from within the data directory.

    Args:
        args (`argparse.Namespace`_):
            Parsed command-line arguments; see :func:`get_parser`.
    """
    # Check the inputs
    rawdir = os.path.join(args.datadir, 'lev0')
    if not os.path.isdir(rawdir):
        raise FileNotFoundError(f'No raw data directory: {rawdir}')

    # Build the equivalent of the pypeit_setup command line.  The root is
    # given relative to the data directory so that the paths are portable.
    command = ['-s', args.spectrograph,
               '-r', 'lev0',
               '-c', args.cfg_split]
    if not args.no_overwrite:
        command += ['-o']
    print(f'cd {args.datadir}')
    print('pypeit_setup ' + ' '.join(command))

    # pypeit_setup writes its output to the current working directory
    cwd = os.getcwd()
    os.chdir(args.datadir)
    try:
        Setup.main(Setup.parse_args(command))
    finally:
        # Always return to where we started
        os.chdir(cwd)


if __name__ == '__main__':
    main(get_parser().parse_args())
