# Getting started

## Goals

This repository will be used to explore the "Maui Wowie" signal pursued by
Steve Vogt.  We will examine the data behind the claimed signal, assess how
robust it is, and share the analysis and diagnostics with the community.

## Prompts

1. Read this file.  Execute the 1st task under "Claude/CLAUDE.md file"
2. Read this file.  Execute the 1st task under "Claude/Skills"
3. Read this file.  Execute the 1st task under "Claude/Settings"
4. Read this file.  Execute the 1st task under "Basic start up"

## Claude

### CLAUDE.md file

1. Examine all of the current files in the repository.  Then generate a basic
   CLAUDE.md file for this project.  Have it indicate:

    - I will perform git commands.  Read-only git (status, diff, log, show,
      branch) is fine; anything that changes repository state is mine to run.
    - If you do any calculation, generate it as a python script and write it to
      disk so that I can add it to the Repository.
    - If you need to run Python, use the "pypeit14" conda environment.
    - Related repositories on disk:
        - `/Users/xavier/Projects/PypeIt/first-hires-exoplanet` (and its data
          in `/Users/xavier/Projects/PypeIt/first-hires-exoplanet-data`) —
          sibling Keck/HIRES radial-velocity work; reuse its conventions and
          code where they apply.
        - `/Users/xavier/Projects/PypeIt/PypeIt` and
          `/Users/xavier/Projects/PypeIt/PypeIt-development-suite` — consult
          them for HIRES reduction behavior rather than guessing.
    - Read `prompts/` before acting, and do only the numbered task you were
      pointed at.
    - Log your work in the Logs section of the relevant prompt doc.

### Skills

1. Copy over the skills/ files from the IOPtics repository
   (`/Users/xavier/Oceanography/python/IOPtics/.claude/skills`) into
   `.claude/skills/` here.  That is `critical-partner` and `grill-me`.

### Settings

1. Generate a `.claude/settings.json` for the project that allows you to run
   most bash commands and run Python (use the "pypeit14" conda environment).
   Start from `/Users/xavier/Projects/PypeIt/first-hires-exoplanet/.claude/settings.json`
   (itself derived from IOPtics and already on `pypeit14`).  Copy the policy,
   not any accumulated path-specific allow entries.  Keep the deny list, in
   particular `git push` / `git commit` / `git reset` / `git rebase`, so the
   permission system enforces the git rule above.

## Basic start up

1. Generate the basic files that one needs for a Python GitHub repository, e.g.
   a file for dependencies.  Examine the other Repositories in
   `Projects/PypeIt` (especially `first-hires-exoplanet`) and
   `Oceanography/python` to see how I tend to organize things.  The package
   directory should be `maui_wowie`.  Log your work in the Logs section.

### Report

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs
