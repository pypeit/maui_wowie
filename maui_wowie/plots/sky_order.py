"""
Plot the sky spectrum of one echelle order from PypeIt ``spec1d`` files.

The sky is PypeIt's sky model extracted in the boxcar aperture of the
target (``BOX_COUNTS_SKY``).  It is normalised by the exposure time and by
the number of pixels in the aperture, so the plotted quantity is the sky
in counts (electrons) per second per detector pixel.  Each science exposure
of the night is plotted separately, together with their mean.

The wavelengths are vacuum wavelengths in the observatory (topocentric)
frame: PypeIt's heliocentric correction is removed by dividing by the
``VEL_CORR`` factor, as is appropriate for sky emission.

By default the script plots order 53 of the UT 1997-05-09 observations of
Q1645+5520.

Usage::

    conda run -n pypeit14 python -m maui_wowie.plots.sky_order
"""
import os
import glob
import argparse

import numpy as np
from matplotlib import pyplot as plt

from pypeit import specobjs


# Default reduction folder: the UT 1997-05-09 night of Q1645+5520
REDUX_DIR = os.path.join('/Users/xavier/Astronomy/data/MauiWowie/HIRES',
                         '1997-05-09_Q1645+5520', 'keck_hires_orig_A')

# Defaults for the target and the echelle order
TARGET = 'Q1645+5520'
ORDER = 53

# Default output file
OUTFILE = 'sky_1997-05-09_Q1645+5520_order53.png'


def get_parser():
    """
    Construct the command-line argument parser.

    Returns:
        `argparse.ArgumentParser`_: The parser.
    """
    parser = argparse.ArgumentParser(
        description='Plot the sky spectrum of one echelle order.')
    parser.add_argument('--redux_dir', type=str, default=REDUX_DIR,
                        help='PypeIt reduction folder; the spec1d files are '
                             'read from its Science sub-folder.')
    parser.add_argument('--target', type=str, default=TARGET,
                        help='Target name, as in the spec1d file names.')
    parser.add_argument('--order', type=int, default=ORDER,
                        help='Echelle order to plot.')
    parser.add_argument('--date', type=str, default=None,
                        help='UT date for the plot label (YYYY-MM-DD).  '
                             'Default is taken from the spec1d header.')
    parser.add_argument('--outfile', type=str, default=OUTFILE,
                        help='Output figure file.  A relative path is '
                             'written to the reduction folder.')
    return parser


def load_sky(spec1d_file, order):
    """
    Load the boxcar sky spectrum of one echelle order from a ``spec1d`` file.

    Args:
        spec1d_file (:obj:`str`):
            PypeIt ``spec1d`` file.
        order (:obj:`int`):
            Echelle order.

    Returns:
        :obj:`tuple`: Four objects: (1) the topocentric vacuum wavelengths
        (Angstroms), (2) the sky in counts per second per pixel, (3) the
        good-pixel mask, and (4) the primary header of the file.  If the
        order was not extracted, all four are None.
    """
    sobjs = specobjs.SpecObjs.from_fitsfile(spec1d_file, chk_version=False)

    # Select the order; there is one object per order for this target
    indx = np.where(sobjs.ECH_ORDER == order)[0]
    if len(indx) == 0:
        return None, None, None, None
    sobj = sobjs[indx[0]]

    # Undo the heliocentric correction applied by PypeIt
    vel_corr = 1. if sobj.VEL_CORR is None else sobj.VEL_CORR
    wave = sobj.BOX_WAVE / vel_corr

    # Sky per second per pixel in the aperture
    exptime = sobjs.header['EXPTIME']
    npix = np.where(sobj.BOX_NPIX > 0, sobj.BOX_NPIX, np.nan)
    sky = sobj.BOX_COUNTS_SKY / npix / exptime

    # Good pixels: valid wavelengths and a populated aperture
    gpm = (wave > 0) & np.isfinite(sky)
    return wave, sky, gpm, sobjs.header


def main(args):
    """
    Make the figure.

    Args:
        args (`argparse.Namespace`_):
            Parsed command-line arguments; see :func:`get_parser`.
    """
    # Find the spec1d files of the target
    files = sorted(glob.glob(os.path.join(args.redux_dir, 'Science',
                                          f'spec1d_*-{args.target}_*.fits')))
    if len(files) == 0:
        raise FileNotFoundError(f'No spec1d files for {args.target} in '
                                f'{args.redux_dir}/Science')

    fig, ax = plt.subplots(figsize=(11, 5))

    # Plot each exposure
    waves, skies = [], []
    date = args.date
    for f in files:
        wave, sky, gpm, header = load_sky(f, args.order)
        if wave is None:
            print(f'Order {args.order} not extracted in {os.path.basename(f)}; '
                  'skipping.')
            continue
        # UT date for the label from the first file used
        if date is None:
            date = header['DATE-OBS'][:10]
        # Label each exposure by its KOA identifier and exposure time
        koaid = os.path.basename(f).split('_')[1].split('-')[0]
        label = f'{koaid} ({header["EXPTIME"]:.0f} s)'
        ax.plot(wave[gpm], sky[gpm], lw=0.6, alpha=0.7, label=label)
        waves.append(np.where(gpm, wave, np.nan))
        skies.append(np.where(gpm, sky, np.nan))

    if len(waves) == 0:
        raise ValueError(f'Order {args.order} was not extracted in any file.')

    # Mean of the exposures.  The wavelength solution and the trace are
    # nearly identical, so average pixel by pixel.
    mean_wave = np.nanmean(np.array(waves), axis=0)
    mean_sky = np.nanmean(np.array(skies), axis=0)
    ax.plot(mean_wave, mean_sky, color='k', lw=0.9,
            label=f'Mean of {len(skies)}')

    # Labels
    ax.set_xlabel(r'Vacuum wavelength, observatory frame ($\AA$)')
    ax.set_ylabel(r'Sky (e$^-$ s$^{-1}$ pixel$^{-1}$)')
    ax.set_title(f'Keck/HIRES  UT {date}  {args.target}  '
                 f'Echelle order {args.order}')
    ax.set_xlim(np.nanmin(mean_wave), np.nanmax(mean_wave))
    ax.legend(loc='upper left', fontsize='small')
    ax.minorticks_on()
    fig.tight_layout()

    # Write
    outfile = args.outfile if os.path.isabs(args.outfile) \
        else os.path.join(args.redux_dir, args.outfile)
    fig.savefig(outfile, dpi=200)
    plt.close(fig)
    print(f'Wrote: {outfile}')


if __name__ == '__main__':
    main(get_parser().parse_args())
