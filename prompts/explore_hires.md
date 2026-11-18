# Explore HIRES data

## Goals

Begin our assessment of the Maui Wowie signal by exploring HIRES data.
We are aiming eventually to:

- Develop a sky spectrum from existing HIRES data which is not the signal of interest
- Develop an algorithm to identify the Maui Wowie signal 
- Search a set of HIRES spectra for the Maui Wowie signal

We will begin by examining a few example spectra where the Maui Wowie signal is clearly present.

## Context

Place any data that you download into the `/Users/xavier/Astronomy/data/MauiWowie/HIRES` folder
Make sub-folders for each individual target.  Name by date and object name.

## Code

If you write code for any of the analysis (likely), use Python and 
put the files in `maui_wowie/explore`.

Follow these guidelines:
- Use the same style and code flow as the code in the PypeIt repository.
- Use inline comments to explain the code.
- Place imports at the top of modules
- Include detailed doc strings

Use the `conda` environment `pypeit14` when you need to run any code
or install packages.

## Prompts

### Q1645+5520

1. One of the first examples found was from UT 1997-May-09 for the quasar Q1645+5520.
And then again on UT 1997-May-29.
In echelle order 53.  The observers were Wal Sargent and Limin Lu.  Please search the 
Keck Observatory Archive (KOA) for these data.  
Do not download it yet.
If you have any questions, put them in the `Q&A/Q1645+5520` section below.
Log your work in the Logs section below.
Use Fable if you can.

2. I have answered your first round of questions in the Q&A section below.
Download the data from KOA.  If it is helpful, install the `pykoa` package
on the conda environment `pypeit14`.  Add it to an `environment.yml` file.
I ask that you create Python scripts to download the data.  Put them in the 
`maui_wowie/io` folder.
The next step will be to reduce the data with PypeIt.
If you have any questions, put them in the `Q&A/Q1645+5520` section below.
Log your work in the Logs section below.
Use Fable if you can.

## Q&A

### Q1645+5520

Questions from Claude (prompt #1, 2026-11-18):

1. **Which setup holds order 53?** I estimate order 53 is centred near 6700 A
   (from m x lambda ~ 3.55e5 A; my estimate, not checked against an arc).
   KOA's `waveblue`/`wavered` keywords for these frames do not reach that
   (2795-4368 A on May 09; 3520-5000 and 3470-4980 A on May 29), but they are
   also inconsistent with the order-blocking filters (e.g. 3892-5463 A behind
   og530), so I do not trust them. On May 29 there are two echelle settings
   (ECHANGL -0.746 and +0.795). Do you know which one shows the signal, or
   should I take both?
>A. Let us start with the May 09 data.  We would then take the May 29 data with 
an echelle setting closest to May 09.
2. **Adjacent nights.** Q1645+5520 was also observed on UT 1997-May-10
   (4 exposures, same program C47H) and UT 1997-May-28 (5 exposures, C48H).
   Include them in the download?
>A. No, these 2 nights are enough for now.
3. **Calibrations.** Download the full night (40 files for May 09, 80 for
   May 29) or only the frames matching the Q1645+5520 setups (science, arcs,
   flats, biases/darks, standard stars)?
>A. Only the frames matching the Q1645+5520 setup.
4. **Folder names.** I plan to use `1997-05-09_Q1645+5520` and
   `1997-05-29_Q1645+5520` under `/Users/xavier/Astronomy/data/MauiWowie/HIRES`.
   OK?
>A. Yes, that is ok.

## Logs

### Q1645+5520

#### 2026-11-18 -- Prompt #1: KOA search (no data downloaded)

Method: queried the KOA TAP service (`https://koa.ipac.caltech.edu/TAP/sync`,
table `koa_hires`) with `date_obs = to_date('YYYY-MM-DD','YYYY-MM-DD')` for the
two nights, plus a positional box search (RA 251.6-251.9, Dec 55.2-55.3) over
all dates. `pykoa` is not installed, so I used `curl`. Only metadata was
retrieved; no FITS files were downloaded.

Result: both nights are in KOA. All frames are 1x2 binned (`binning` = "1,2"),
slit width 0.861 arcsec, original single-CCD HIRES detector.

**UT 1997-05-09** -- program C47H, PI W. Sargent, observer keyword "lu";
40 files in total for the night. Q1645+5520 frames, decker C1, filter kv408,
ECHANGL -0.432, XDANGL 0.003:

| KOAID | UT | Type | Exp (s) | Airmass |
|---|---|---|---|---|
| HI.19970509.40564.fits | 11:16:04 | object | 3000 | 1.24 |
| HI.19970509.43673.fits | 12:07:53 | ThAr | 1 | 1.23 |
| HI.19970509.43849.fits | 12:10:49 | object | 2500 | 1.23 |
| HI.19970509.46467.fits | 12:54:27 | ThAr | 1 | 1.25 |
| HI.19970509.46585.fits | 12:56:25 | object | 2700 | 1.25 |
| HI.19970509.49385.fits | 13:43:05 | ThAr | 1 | 1.31 |
| HI.19970509.49499.fits | 13:44:59 | object | 2700 | 1.32 |
| HI.19970509.52330.fits | 14:32:10 | ThAr | 1 | 1.43 |

Total science exposure 10,900 s. Matching calibrations the same night:
4 quartz flats (00:00-00:06 UT, HI.19970509.00053/00184/00281/00379),
4 zero-second "darks" typed as bias (00:34-00:38 UT, taken in the other
setup), and standards SAO 31165 (HI.19970509.52473) and BD+28 4211
(HI.19970509.52723) in the same setup. The only arcs in this setup are the
four interleaved with the science frames.

**UT 1997-05-29** -- program C48H, PI L. Lu, observers Lu/Sargent/Boksenberg;
80 files in total for the night. Q1645+5520 frames, decker C2, filter gg475,
in two echelle settings:

| KOAID | UT | Type | Exp (s) | Airmass | ECHANGL | XDANGL |
|---|---|---|---|---|---|---|
| HI.19970529.33931.fits | 09:25:31 | object | 3000 | 1.27 | -0.746 | 0.888 |
| HI.19970529.37050.fits | 10:17:30 | ThAr | 1 | 1.23 | -0.746 | 0.888 |
| HI.19970529.37194.fits | 10:19:54 | object | 3000 | 1.23 | -0.746 | 0.888 |
| HI.19970529.40292.fits | 11:11:32 | ThAr | 1 | 1.23 | -0.746 | 0.888 |
| HI.19970529.40448.fits | 11:14:08 | object | 3000 | 1.23 | -0.746 | 0.888 |
| HI.19970529.43574.fits | 12:06:14 | ThAr | 1 | 1.28 | -0.746 | 0.888 |
| HI.19970529.44512.fits | 12:21:52 | object | 3000 | 1.31 | +0.795 | 0.797 |
| HI.19970529.47626.fits | 13:13:46 | ThAr | 1 | 1.43 | +0.795 | 0.790 |
| HI.19970529.47806.fits | 13:16:46 | object | 4000 | 1.44 | +0.795 | 0.798 |
| HI.19970529.51902.fits | 14:25:02 | ThAr | 1 | 1.73 | +0.795 | 0.798 |

Total science exposure 16,000 s (9000 s + 7000 s). Matching afternoon
calibrations exist for both settings (02:05-02:29 UT: 2 ThAr + 4 quartz
each), plus 1-s darks (01:57-02:02 UT) and standards Feige 67
(HI.19970529.21193 and .21660, one per setting), SAO 66336
(HI.19970529.43831) and SAO 31165 (HI.19970529.52133). The afternoon
calibration frames carry the previous night's observer keyword
("Boesgaard/Stephens") but the C48H program ID.

Other things found:

- The positional search returned Q1645+5520 exposures on two further nights:
  UT 1997-05-10 (4 science, C1/kv408, ECHANGL +0.405; C47H) and UT 1997-05-28
  (5 science, C1/kv408, ECHANGL -0.170/-0.185; C48H, observer keyword
  "Boesgaard/Stephens"). Later HIRES frames at this position (2001, 2007;
  PI Tytler) are labelled 1646+5514 / q1646.
- KOA's `waveblue`/`wavered` values look unreliable for these 1997 frames
  (see Q&A item 1), so I could not confirm from metadata alone which setup
  contains order 53.
- KOA returned empty `filesize_mb` for these files, so I have no download
  size estimate.
- Several frames have the original filename `hires0000.fits` or a repeated
  number (`ofname`), so the KOAID is the only reliable identifier.
#### 2026-11-18 -- Prompt #2: KOA download

Setup: installed `pykoa` 1.7.2 (with its dependencies `bs4`, `xmltodict`) in
the `pypeit14` conda environment with `pip`, and created `environment.yml`
at the top of the repository listing it. PypeIt is not listed there because
`pypeit14` uses an editable install of the PypeIt `develop` branch.

Code (in `maui_wowie/io`):

- `koa.py` -- `query_night` (KOA metadata for one UT date), `select_setup`
  (frames matching the setup of a target's science exposures, plus
  biases/darks), `download` (raw frames via `pykoa`).
- `download_q1645.py` -- the script for this target. Run with
  `conda run -n pypeit14 python -m maui_wowie.io.download_q1645`
  (`--dry_run` lists the selection without downloading).

Selection rule: a frame is kept if it has the same decker, order-blocking
filter and binning as the Q1645+5520 science exposures, with echelle and
cross-disperser angles within 0.01 deg; bias and dark frames with the same
binning are kept regardless of setup. For May 29 the script takes the
setting whose echelle angle is closest to May 09 (-0.432): that is
ECHANGL -0.746 (the other is +0.795).

Result: 37 raw frames downloaded, all open cleanly with `astropy`
(single extension, 1024 x 2303, uint16). `pykoa` puts the files in a `lev0`
sub-folder. Each night's folder also holds `koa_night.tbl` (metadata for
the whole night) and `download_list.tbl` (the frames downloaded).

| Folder (under `.../MauiWowie/HIRES`) | Files | Size | Contents |
|---|---|---|---|
| `1997-05-09_Q1645+5520/lev0` | 18 | 82 MB | 4 science, 4 ThAr, 4 quartz flats, 4 biases, 2 standards (SAO 31165, BD+28 4211) |
| `1997-05-29_Q1645+5520/lev0` | 19 | 86 MB | 3 science, 5 ThAr, 4 quartz flats, 4 darks (1 s), 1 odd frame, 2 standards (Feige 67, SAO 66336) |

Things to know before the reduction:

- **The two nights are not the same setup.** May 09 is decker C1 / kv408 /
  XDANGL 0.003 with header `XDISPERS` = "0"; May 29 is decker C2 / gg475 /
  XDANGL 0.888 with `XDISPERS` = "UV". Only the echelle angle is "close"
  (-0.432 vs -0.746), so the wavelength coverage and the position of
  order 53 will differ between the nights.
- May 09 has no arc from the afternoon in the science setup; the only arcs
  are the four taken between the science exposures. The four biases were
  taken while the instrument was in a different setup (C2 / og530).
- May 29: `HI.19970529.18796.fits` is typed `arclamp` by KOA but its OBJECT
  keyword is "quartz" (1 s, 05:13 UT). It needs a look before it is used
  as either. The "darks" that night are 1-s exposures, not zero-second
  biases.
- These are original-detector frames (Tektronix 2048, single amplifier),
  so the PypeIt spectrograph is `keck_hires_orig`, which exists in the
  installed `develop` branch. I have not run it on these data.
