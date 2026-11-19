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

3. We are going to reduce the May 09 data with PypeIt.  Let us first create
the PypeIt file with a call to `pypeit_setup`.  Run that from the data directory:
`Astronomy/data/MauiWowie/HIRES/1997-05-09_Q1645+5520`.  For repetativlity, create
a Python script to do this and place it in the `maui_wowie/pypeit` folder.
If you have any questions, put them in the `Q&A/Q1645+5520` section below.
Log your work in the Logs section below.
Use Fable if you can.

4. I have answered your questions in the Q&A section below.  
And I have modified the PypeIt code to recognise `IMAGETYP = 'bias'` as a bias/dark.
Rerun `pypeit_setup` and report the results.
Log your work in the Logs section below.
Use Fable if you can.

5. Ok, now proceed to reduce the data with PypeIt.  Run `run_pypeit` from the 
data directory:
`Astronomy/data/MauiWowie/HIRES/1997-05-09_Q1645+5520`.
Create a Python script to do this and place it in the `maui_wowie/pypeit` folder.
I have commented out the SAO 31165 frame in the PypeIt file.
We will want to avoid files like this in the future too.  Ideally via your 
pypeit scripts.
If you have any questions, put them in the `Q&A/Q1645+5520` section below.
Log your work in the Logs section below.
Use Fable if you can.

6.  Please read my answers to your last round of questions below.
Then, I wish for you to generate a figure showing the sky spectrum for Order 53,
flux vs. wavelength, for the May 09 data.  Label it with the date, object name,
and order.  As always, do so by creating a Python script and placing it in the `maui_wowie/plots` folder.
Log your work in the Logs section below.
Use Opus 5.5 if you can.

7. 

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

Questions from Claude (prompt #3, 2026-11-18):

5. **Bias frames are not recognised by PypeIt.** The four zero-second frames
   from May 09 have `IMAGETYP = 'bias'`, but for pre-1998 data
   `keck_hires_orig` only recognises `IMAGETYP = 'dark'` as a bias/dark
   (the `RED97` branch of `compound_meta` in `keck_hires.py`). They were
   left untyped and commented out, so Setup A has no bias frames. Options:
   (a) reduce with overscan subtraction only, (b) I add the four frames to
   the PypeIt file as `bias` from the script, or (c) add a `"bias"` case to
   PypeIt itself. Which do you prefer?
>A. I have modified the PypeIt code to recognise `IMAGETYP = 'bias'` as a bias/dark.
6. **SAO 31165 is typed `science`.** This 15-s exposure
   (`HI.19970509.52473.fits`) is not in PypeIt's standard-star archive, so
   it was typed as science. Should it stay, be dropped, or be retyped?
>A. We do not need to use a standard star for our analysis.  Ignore it

Questions from Claude (prompt #5, 2026-11-18):

7. **The flats are too bright in the red orders.** The 3-s quartz flats
   peak at ~61,500 ADU in order 53 (median 49,200). They never reach the
   ADC limit of 65,535, but they are above PypeIt's non-linearity limit for
   this detector (0.7 x 65,535 = 45,874 ADU), and `run_pypeit` crashes on
   order 53 by default. To get a reduction I set
   `[calibrations][[flatfield]] saturated_slits = continue`, which means
   orders 53 and 52 are **not flat-fielded** (and much of orders 54-57 has
   the pixel flat set to 1). Is that acceptable for the Maui Wowie search,
   or do you want to raise the `nonlinear` fraction for `keck_hires_orig`
   in PypeIt (it is hard-coded in the detector definition, so it cannot be
   set from the PypeIt file)? I do not know how linear this CCD is above
   46,000 ADU.
>A. Flat fielding won't affect the signal we are interested in.  It is ok 
8. **BD+28 4211.** It is still in the PypeIt file as `standard` and was
   reduced (about 30 s of the run). `run_setup.py` has a `--drop_standards`
   option that comments it out; should that be the default?
>A. Yes, make that the default
9. **Output location.** As requested `run_pypeit` runs from the data
   directory, so `Calibrations/`, `Science/` and `QA/` are in
   `1997-05-09_Q1645+5520/` and not in `keck_hires_orig_A/`. OK to keep
   this convention for other nights?
>A. I would prefer the outputs be in the `keck_hires_orig_A` folder.  Please
modify the script and also move the outputs for this object accordingly.

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

#### 2026-11-18 -- Prompt #3: `pypeit_setup` for May 09

Code: `maui_wowie/pypeit/run_setup.py`. It changes into the data directory
and calls PypeIt's `Setup` script class with the equivalent of

    cd /Users/xavier/Astronomy/data/MauiWowie/HIRES/1997-05-09_Q1645+5520
    pypeit_setup -s keck_hires_orig -r lev0 -c all -o

Run with `conda run -n pypeit14 python -m maui_wowie.pypeit.run_setup`
(options: `--datadir`, `--spectrograph`, `--cfg_split`, `--no_overwrite`).
PypeIt version 3.0.1.dev2+g42ef90446 (`develop` branch).

Result: `pypeit_setup` ran without error and found two configurations.
Output in the data directory:

- `keck_hires_orig_A/keck_hires_orig_A.pypeit` (and `.calib`) -- the
  Q1645+5520 setup: `RED97`, decker C1, kv408, echangle -0.432,
  xdangle 0.0025, binning 1,2. 14 frames, all in calibration group 0:
  4 `arc,tilt`, 4 `pixelflat,illumflat,trace`, 4 `science` (Q1645+5520),
  1 `science` (SAO 31165) and 1 `standard` (BD+28 4211).
- `keck_hires_orig_B/keck_hires_orig_B.pypeit` (and `.calib`) -- only the
  four zero-second frames, untyped and commented out. This file is not
  usable; it exists because those frames were taken in a different setup
  (C2 / og530) and were not recognised as biases (see Q&A item 5).
- `pypeit_setup_20261118-1648.log`.

Notes:

- The PypeIt file has no `[rdx]` parameters beyond the spectrograph; I did
  not edit it by hand.
- PypeIt labels the cross-disperser `RED97` for all data before 1998,
  whatever the `XDISPERS` header says.
- The science frames carry B1950 coordinates in their headers
  (`EQUINOX = 1950.0`, RA 16:45:52.92, Dec +55:20:04.3), and PypeIt copies
  them unchanged into the `ra`/`dec` columns (251.4705, 55.3345). The
  J2000 position from KOA is 251.730, 55.247. This matters for
  standard-star matching, and slightly for the heliocentric correction.
- PypeIt warned that some frames qualified as both science and standard;
  it resolved them by coordinate match to its standard archive, which is
  why BD+28 4211 is `standard` and SAO 31165 is `science`.

#### 2026-11-18 -- Prompt #4: rerun `pypeit_setup` for May 09 (bias fix)

Reran `conda run -n pypeit14 python -m maui_wowie.pypeit.run_setup`
(no change to the script). PypeIt is the local `orig-hires-fixes` branch
with the uncommitted edit to `pypeit/spectrographs/keck_hires.py` that adds
a `"bias"` case to the `RED97` branch (version string still
3.0.1.dev2+g42ef90446).

Result: `pypeit_setup` ran without error and now finds **one**
configuration; all 18 frames are typed. Output in the data directory:

- `keck_hires_orig_A/keck_hires_orig_A.pypeit` (and `.calib`) -- Setup A:
  `RED97`, decker C1, kv408, echangle -0.432, xdangle 0.0025, binning 1,2.
  18 frames, all in calibration group 0:

  | Frame type | N | Frames |
  |---|---|---|
  | `arc,tilt` | 4 | HI.19970509.43673 / 46467 / 49385 / 52330 (ThAr, 1 s) |
  | `bias` | 4 | HI.19970509.02050 / 02145 / 02239 / 02332 (0 s) |
  | `pixelflat,illumflat,trace` | 4 | HI.19970509.00053 / 00184 / 00281 / 00379 (quartz, 3 s) |
  | `science` | 4 | HI.19970509.40564 / 43849 / 46585 / 49499 (Q1645+5520; 3000, 2500, 2700, 2700 s) |
  | `science` | 1 | HI.19970509.52473 (SAO 31165, 15 s) |
  | `standard` | 1 | HI.19970509.52723 (BD+28 4211, 300 s) |

- `pypeit_setup_20261118-1700.log`.
- There is no `keck_hires_orig_B` any more: the biases are excluded from
  the configuration matching and are attached to Setup A.

Notes:

- The four biases keep their own header values in the table (decker C2,
  og530, echangle 0.191, xdangle 1.345). They are in Setup A only because
  PypeIt ignores bias/dark frames when defining configurations.
- SAO 31165 is still typed `science` and BD+28 4211 `standard`. Per Q&A
  item 6 they are to be ignored, but I did not edit the PypeIt file; both
  rows need to be commented out (or removed) before `run_pypeit`,
  otherwise PypeIt will reduce them.
- Same warning as before about frames qualifying as both science and
  standard; nothing else of note in the log.
- The `ra`/`dec` columns are still the B1950 header values (see the
  prompt #3 log).

#### 2026-11-18 -- Prompt #5: `run_pypeit` for May 09

Code (in `maui_wowie/pypeit`):

- `run_reduce.py` (new) -- changes into the data directory and calls
  PypeIt's `RunPypeIt` script class with the equivalent of
  `run_pypeit keck_hires_orig_A/keck_hires_orig_A.pypeit -o`. Run with
  `conda run -n pypeit14 python -m maui_wowie.pypeit.run_reduce`
  (options: `--datadir`, `--spectrograph`, `--setup`, `--calib_only`,
  `--redo_calibs`, `--no_overwrite`).
- `run_setup.py` (changed) -- after `pypeit_setup` it now comments out, in
  the PypeIt file, every `science` frame whose target is not `--target`
  (default `Q1645+5520`; `all` keeps everything). This reproduces your
  hand edit: only `HI.19970509.52473.fits` (SAO 31165) is commented out.
  `--drop_standards` also comments out `standard` frames (off by default).
  It also passes a parameter block to `pypeit_setup -p` (`--param_file`).
- `keck_hires_orig.par` (new) -- that parameter block; currently only
  `[calibrations][[flatfield]] saturated_slits = continue`.

I reran `run_setup` twice (regenerating the PypeIt file, same content as
your edited version plus the parameter block) and `run_reduce` twice.

First run: **crashed** in the flat-field step after ~2 min --
"Only 44.66% of the pixels on slit 911 are not saturated". Slit 911 is
echelle order 53. Median / peak counts of the quartz flat along the order
centres (ADU, one flat): order 78: 5,400 / 8,600; order 60: 31,800 /
39,300; order 57: 40,800 / 49,800; order 54: 47,300 / 58,500; order 53:
49,200 / 61,500; order 52: 49,800 / 61,400. Nothing is at 65,535 apart
from 1-2 pixels per frame; the limit being hit is PypeIt's non-linearity
threshold (45,874 ADU). See Q&A item 7.

Second run, with `saturated_slits = continue`: **completed** in 4 min 54 s
without error. Products in the data directory:

- `Calibrations/` -- Bias, Arc, Tiltimg, Edges, Slits, WaveCalib, Tilts,
  Flat (all `_A_0_DET01`).
- `Science/` -- `spec2d` and `spec1d` (+ `.txt`) for the four Q1645+5520
  exposures and for BD+28 4211.
- `QA/` -- `MF_A.html` and one HTML page per exposure.
- `keck_hires_orig_A/keck_hires_orig_A.log` -- the PypeIt log.

Results:

- 28 orders traced: 78 (blue, ~4559 A centre) to 51 (red). m x lambda =
  3.556e5 A, so the estimate in Q&A item 1 holds.
- **Order 53 covers 6658.7-6756.0 A** and was extracted (optimal) in all
  four science exposures, median S/N per pixel 5.7-6.3. Its arc solution
  is the best of all orders (RMS 0.058 pix).
- Wavelength calibration: RMS 0.06-0.19 pix for orders 78-52; 2D fit RMS
  0.11 A x order. Order 51 (at the detector edge) failed the
  cross-correlation and was refit with RMS 0.48 pix -- not to be trusted.
- Quasar S/N per pixel per exposure: ~0 at order 78, 1-3 for orders 76-60,
  6-8 for orders 57-52. Object FWHM 2.4-2.9 binned spatial pixels,
  i.e. 1.05-1.2 arcsec (`opt_fwhm`).
- Orders with no extraction because the global sky fit was rejected (just
  over 80% of pixels masked): order 51 in exposures 40564, 43849 and
  46585; orders 68 and 57 in exposure 43849.
- Flat field: orders 53 and 52 were skipped (not flat-fielded). PypeIt
  also warned of "unrealistically high or low values" in the flat model
  for orders 54 (18,069 pix), 55 (13,828), 56 (8,701), 51 (8,903), and a
  few hundred pixels in orders 57 and 64.

Not done: I have not looked at the QA plots or the 2D images, so I have
not checked the sky subtraction in order 53 or looked for the Maui Wowie
signal. Note that PypeIt's sky model will subtract any emission that
fills the slit; the sky model is kept in the `spec2d` files.

#### 2026-11-19 -- Prompt #6: sky spectrum of order 53 (May 09)

Changes following the Q&A answers:

- **Standards dropped by default** (item 8): `run_setup.py` now comments
  out `standard` frames unless `--keep_standards` is given (the old
  `--drop_standards` option is gone). Rerunning it commented out both
  HI.19970509.52473 (SAO 31165) and HI.19970509.52723 (BD+28 4211).
- **Outputs in `keck_hires_orig_A`** (item 9): `run_reduce.py` now passes
  `-r <datadir>/keck_hires_orig_A` to `run_pypeit`. I moved the existing
  `Calibrations/`, `Science/` and `QA/` folders there with `mv`. The
  `.calib` file was regenerated by `run_setup` and now points to
  `keck_hires_orig_A/Calibrations`.

Re-reduction: I reran `run_reduce` to check the new path. Calibrations were
reused from the moved folder, as intended. But the new `spec1d` files had
**every order twice** (54 objects instead of 27, and the two copies
differed). That is a PypeIt bug: when a `spec1d` file already exists,
`SpecObjs.write_to_fits` keeps the objects of the detectors not being
reduced. It identifies these by comparing `DET` with `rdx.detnum`, but
`keck_hires_orig` sets `detnum = 1` (an int) while the file stores
`'DET01'`, so the old objects are never removed. I did not change PypeIt.
Instead, `run_reduce.py` now deletes existing `Science/spec1d_*` files
before an overwriting run. A third run then gave clean files (27
orders, as in prompt #5). That step also deleted the stale BD+28 4211
`spec1d`; its old `spec2d` is still in `Science/`.

Plot code: `maui_wowie/plots/sky_order.py`. Run with
`conda run -n pypeit14 python -m maui_wowie.plots.sky_order`
(options: `--redux_dir`, `--target`, `--order`, `--date`, `--outfile`).
Output:
`.../1997-05-09_Q1645+5520/keck_hires_orig_A/sky_1997-05-09_Q1645+5520_order53.png`.

What is plotted: PypeIt's sky model extracted in the boxcar aperture of the
quasar (`BOX_COUNTS_SKY`), divided by the exposure time and the number of
aperture pixels (`BOX_NPIX`), i.e. e-/s/pixel. Each of the four exposures
is plotted, plus their pixel-by-pixel mean. Wavelengths are vacuum, with
PypeIt's heliocentric correction removed (divided by `VEL_CORR`) to put
them in the observatory frame. Order 53 spans 6658.7-6756.0 A. The flux
is not calibrated, and order 53 is not flat-fielded (Q&A item 7).

What the figure shows:

- Continuum ~0.002-0.003 e-/s/pix in all four exposures, rising to ~0.007
  at the blue end of the order (below ~6665 A; probably the edge of the
  order, not checked).
- A group of emission lines at 6715-6720 A that are **present only in the
  last exposure** (HI.19970509.49499, 13:45 UT). Peaks (e-/s/pix, 49499
  vs. the other three): 6716.6 A: 0.100 vs <=0.003; 6719.4 A: 0.030 vs
  <=0.004; 6715.3 A: 0.019 vs <=0.003. There are weaker features at
  ~6714 A and ~6718 A.
- A line at 6733.4-6733.8 A that varies too: 0.020 in HI.19970509.46585,
  0.0095 in 49499, 0.0056 in 40564, and close to continuum in 43849.
- Weak features at ~6737-6742 A in several exposures.

A steady night-sky line should appear in all four exposures at a similar
strength, so the 6715-6720 A group and the 6733.5 A line do not behave
like ordinary sky emission. I have not checked whether they fill the slit,
or whether they appear in the 2D frames or in neighbouring orders. Because
of the one exposure, the mean is dominated by 49499 at 6715-6720 A.

Note: the heliocentric correction PypeIt applied (and that I removed) used
the B1950 header coordinates (see prompt #3 log). It cancels out here
because the same factor is divided back out.
