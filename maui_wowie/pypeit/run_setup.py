"""
Script to run ``pypeit_setup`` on a night of Keck/HIRES data and generate
the PypeIt reduction file(s).

``pypeit_setup`` is executed from within the data directory, with the raw
frames read from its ``lev0`` sub-folder (the structure written by
:mod:`maui_wowie.io.koa`).  By default the script processes the
UT 1997-05-09 observations of Q1645+5520.

After ``pypeit_setup`` has run, the PypeIt file(s) are edited to comment out
the ``science`` frames that are not of the requested target (e.g. bright
stars that PypeIt does not recognise as standards), so that ``run_pypeit``
does not reduce them.  The standard-star frames are commented out too,
unless ``--keep_standards`` is given.

Usage::

    conda run -n pypeit14 python -m maui_wowie.pypeit.run_setup
"""
import os
import glob
import argparse

from pypeit.scripts.setup import Setup


# Default data directory: the UT 1997-05-09 night of Q1645+5520
DATA_DIR = '/Users/xavier/Astronomy/data/MauiWowie/HIRES/1997-05-09_Q1645+5520'

# PypeIt spectrograph for the original (pre August 2004) HIRES detector
SPECTROGRAPH = 'keck_hires_orig'

# Default file with parameters to add to the PypeIt file(s)
PARAM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'keck_hires_orig.par')

# Default science target; science frames of any other target are commented out
TARGET = 'Q1645+5520'


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
    parser.add_argument('--param_file', type=str, default=PARAM_FILE,
                        help='File with a block of PypeIt parameters to add '
                             'to the PypeIt file(s); passed to '
                             'pypeit_setup -p.  Use "none" to add nothing.')
    parser.add_argument('--target', type=str, default=TARGET,
                        help='Name of the science target.  Science frames of '
                             'any other target are commented out of the '
                             'PypeIt file.  Use "all" to keep every frame.')
    parser.add_argument('--keep_standards', dest='drop_standards',
                        default=True, action='store_false',
                        help='Keep the standard-star frames.  By default '
                             'they are commented out of the PypeIt file.')
    parser.add_argument('--no_overwrite', default=False, action='store_true',
                        help='Do not overwrite existing pypeit_setup output.')
    return parser


def normalize_target(name):
    """
    Put a target name in a standard form for comparison.

    Args:
        name (:obj:`str`):
            Target name, e.g. from the ``target`` column of a PypeIt file.

    Returns:
        :obj:`str`: The name in lower case with all white space removed.
    """
    return ''.join(name.split()).lower()


def comment_frames(pypeit_file, target, drop_standards=False):
    """
    Comment out the unwanted frames in the data block of a PypeIt file.

    A frame is commented out if its frame type includes ``science`` and its
    target is not ``target``.  This removes, e.g., bright stars observed in
    the science setup that are not in the PypeIt standard-star archive and
    are therefore typed as ``science``.  Optionally, the ``standard`` frames
    are commented out too.  Calibration frames are never touched.

    The file is edited as text (and in place) so that the remainder of the
    file is preserved exactly as written by ``pypeit_setup``.

    Args:
        pypeit_file (:obj:`str`):
            Path to the PypeIt file; overwritten if any frame is commented.
        target (:obj:`str`):
            Name of the science target to keep.  The comparison ignores
            case and white space.
        drop_standards (:obj:`bool`, optional):
            If True, also comment out the frames typed as ``standard``.

    Returns:
        :obj:`list`: Names of the files that were commented out.
    """
    with open(pypeit_file, 'r') as f:
        lines = f.readlines()

    # Find the data block
    stripped = [line.strip() for line in lines]
    start = stripped.index('data read')
    end = stripped.index('data end')

    # The table header is the first line of the block with column
    # delimiters; the path line(s) come before it
    header = next(i for i in range(start+1, end) if '|' in lines[i])
    columns = [col.strip() for col in lines[header].split('|')]
    ifile = columns.index('filename')
    itype = columns.index('frametype')
    itarget = columns.index('target')

    # Work through the table rows
    commented = []
    for i in range(header+1, end):
        # Skip rows that are blank or already commented out
        if len(stripped[i]) == 0 or stripped[i].startswith('#'):
            continue
        row = [col.strip() for col in lines[i].split('|')]
        frametypes = row[itype].split(',')
        # Science frames of another target
        other = 'science' in frametypes \
            and normalize_target(row[itarget]) != normalize_target(target)
        # Standard stars, if requested
        standard = drop_standards and 'standard' in frametypes
        if other or standard:
            lines[i] = '#' + lines[i]
            commented.append(row[ifile])

    # Only rewrite the file if something changed
    if len(commented) > 0:
        with open(pypeit_file, 'w') as f:
            f.writelines(lines)
    return commented


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
    if args.param_file.lower() != 'none':
        # Reduction parameters to include in the PypeIt file(s)
        if not os.path.isfile(args.param_file):
            raise FileNotFoundError(f'No parameter file: {args.param_file}')
        command += ['-p', os.path.abspath(args.param_file)]
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

    # Comment out the frames we do not want to reduce
    if args.target.lower() == 'all':
        return
    pypeit_files = sorted(glob.glob(
        os.path.join(args.datadir, f'{args.spectrograph}_*', '*.pypeit')))
    for pypeit_file in pypeit_files:
        commented = comment_frames(pypeit_file, args.target,
                                   drop_standards=args.drop_standards)
        print(f'{pypeit_file}: commented out {len(commented)} frame(s)')
        for filename in commented:
            print(f'    {filename}')


if __name__ == '__main__':
    main(get_parser().parse_args())
