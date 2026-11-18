"""
Methods to query the Keck Observatory Archive (KOA) for HIRES data and
download the raw frames that match the instrument setup of a science target.

.. include:: ../include/links.rst
"""
import os

import numpy as np

from astropy.table import Table

from pykoa.koa import Koa


# Columns retrieved from the ``koa_hires`` table.  ``instrume`` and
# ``filehand`` are required by :func:`pykoa.koa.Koa.download`.
KOA_COLUMNS = ['koaid', 'instrume', 'ofname', 'targname', 'object', 'ra',
               'dec', 'date_obs', 'ut', 'elaptime', 'koaimtyp', 'observer',
               'progpi', 'progid', 'deckname', 'slitwidt', 'echangl',
               'xdangl', 'fil1name', 'lfilname', 'binning', 'airmass',
               'filehand']

# KOA image types that are setup independent
SETUP_INDEPENDENT_TYPES = ['bias', 'dark']


def normalize_name(name):
    """
    Normalize a target name for comparison.

    White space is removed and the name is converted to lower case so that,
    e.g., ``'Q 1645+5520'`` and ``'q1645+5520'`` compare as equal.

    Args:
        name (:obj:`str`):
            Target name.

    Returns:
        :obj:`str`: The normalized name.
    """
    return ''.join(str(name).split()).lower()


def query_night(date, outfile, overwrite=False):
    """
    Query KOA for the metadata of all HIRES frames taken on one UT date.

    Args:
        date (:obj:`str`):
            UT date of the observations, formatted as ``YYYY-MM-DD``.
        outfile (:obj:`str`):
            Path for the IPAC-format metadata table written by KOA.
        overwrite (:obj:`bool`, optional):
            If True, repeat the query even if ``outfile`` already exists.

    Returns:
        `astropy.table.Table`_: Metadata for every HIRES frame of the night,
        sorted by ``koaid``.
    """
    if overwrite or not os.path.isfile(outfile):
        # Make sure the output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(outfile)), exist_ok=True)
        # date_obs is an Oracle DATE column, so the string must be converted
        query = f"select {', '.join(KOA_COLUMNS)} from koa_hires " \
                f"where date_obs = to_date('{date}','YYYY-MM-DD') " \
                f"order by koaid"
        Koa.query_adql(query, outfile, overwrite=True, format='ipac')

    # Read it back
    tbl = Table.read(outfile, format='ascii.ipac')
    if len(tbl) == 0:
        raise ValueError(f'KOA returned no HIRES frames for UT {date}.')
    return tbl


def select_setup(tbl, target, echangl=None, ang_tol=0.01):
    """
    Select the frames of a night that match the setup of a science target.

    The setup is defined by the decker, the order-blocking filter, the
    echelle angle, the cross-disperser angle and the binning of the science
    exposures of ``target``.  The selection returns every frame taken in
    that setup (science, arcs, flats, standard stars) and all of the bias
    and dark frames with the same binning.

    Args:
        tbl (`astropy.table.Table`_):
            Metadata for the night; see :func:`query_night`.
        target (:obj:`str`):
            Name of the science target.  Compared to the ``targname``
            column after normalizing both with :func:`normalize_name`.
        echangl (:obj:`float`, optional):
            Reference echelle angle (deg).  If the target was observed with
            more than one setup, the one with the echelle angle closest to
            this value is selected.  If None, the target must have been
            observed with a single setup.
        ang_tol (:obj:`float`, optional):
            Tolerance (deg) on the echelle and cross-disperser angles when
            matching frames to the science setup.

    Returns:
        `astropy.table.Table`_: The selected rows of ``tbl``.
    """
    # Identify the science exposures of the target
    names = np.array([normalize_name(name) for name in tbl['targname']])
    is_sci = (names == normalize_name(target)) & (tbl['koaimtyp'] == 'object')
    if not np.any(is_sci):
        raise ValueError(f'No science exposures of {target} in the table.')

    # Group the science exposures by echelle angle to find the setups
    sci_ech = np.asarray(tbl['echangl'][is_sci], dtype=float)
    setups = []
    for ech in sci_ech:
        if not any(abs(ech - _ech) < ang_tol for _ech in setups):
            setups.append(ech)

    # Choose the setup
    if len(setups) > 1 and echangl is None:
        raise ValueError(f'{target} was observed with {len(setups)} echelle '
                         f'angles ({setups}); provide echangl to choose one.')
    ech0 = setups[0] if echangl is None \
        else setups[np.argmin(np.abs(np.array(setups) - echangl))]

    # Use the first science exposure in that setup as the reference
    ref = tbl[is_sci][np.abs(sci_ech - ech0) < ang_tol][0]

    # Frames taken with the same setup
    same_bin = tbl['binning'] == ref['binning']
    in_setup = (tbl['deckname'] == ref['deckname']) \
        & (tbl['fil1name'] == ref['fil1name']) \
        & (np.abs(tbl['echangl'] - ref['echangl']) < ang_tol) \
        & (np.abs(tbl['xdangl'] - ref['xdangl']) < ang_tol) \
        & same_bin

    # Bias and dark frames do not depend on the optical setup
    is_bias = np.isin(tbl['koaimtyp'], SETUP_INDEPENDENT_TYPES) & same_bin

    return tbl[in_setup | is_bias]


def download(tbl, outdir, metafile=None):
    """
    Download the raw (level 0) frames listed in a metadata table from KOA.

    The files are written to ``outdir/lev0``, which is the directory
    structure imposed by :func:`pykoa.koa.Koa.download`.  Files already on
    disk are skipped by `pykoa`_.

    Args:
        tbl (`astropy.table.Table`_):
            Metadata of the frames to download; must include the
            ``instrume`` and ``filehand`` columns.
        outdir (:obj:`str`):
            Output directory.
        metafile (:obj:`str`, optional):
            Path for the IPAC-format table listing the downloaded frames.
            If None, ``outdir/download_list.tbl`` is used.

    Returns:
        :obj:`list`: Paths of the frames expected on disk that are missing
        after the download; empty if the download was complete.
    """
    os.makedirs(outdir, exist_ok=True)
    if metafile is None:
        metafile = os.path.join(outdir, 'download_list.tbl')

    # pykoa works from a metadata file on disk
    tbl.write(metafile, format='ascii.ipac', overwrite=True)

    # Raw frames only; no KOA-associated calibrations or level 1 products
    Koa.download(metafile, 'ipac', outdir, lev0file=1, calibfile=0,
                 lev1file=0)

    # Check that everything arrived
    expected = [os.path.join(outdir, 'lev0', koaid) for koaid in tbl['koaid']]
    return [path for path in expected if not os.path.isfile(path)]


def summarize(tbl):
    """
    Print a one-line-per-frame summary of a metadata table.

    Args:
        tbl (`astropy.table.Table`_):
            Metadata table; see :func:`query_night`.
    """
    columns = ['koaid', 'targname', 'object', 'ut', 'elaptime', 'koaimtyp',
               'deckname', 'fil1name', 'echangl', 'xdangl']
    tbl[columns].pprint_all()

