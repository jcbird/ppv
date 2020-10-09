
# Table of Contents

1.  [Installation](#org642288a)
2.  [Configuration and Data Files](#orgd33bf07)
    1.  [Copy `ppv_setup.ini` to ~/.config and edit](#org83ae075)
    2.  [`five_plates` functionality](#org0a66b5d)
    3.  [Plate directory and PlugHoles files](#org68bdc22)
        1.  [run `ppv.ppv.update_platefiles()` to ensure the latest versions of all plate files.](#orga112a91)
3.  [Breaking Changes (PLEASE READ)](#orgb825fff)
4.  [Concepts](#org1a42d67)
    1.  [Plate Summary](#org942c269)
    2.  [Plate](#org608f842)
    3.  [Field](#orgd1bf58a)
    4.  [Platerun](#org92d8d68)
    5.  [Targets](#org8f715b1)
5.  [Basic Usage](#org3da2f2e)
    1.  [See the tutorial notebook in the `docs` directory.](#orga8a3cfc)
    2.  [Specific example notebook with 2020.10.a.mwm-bhm plate run](#orgf1ad5ef)
6.  [FAQs](#orgd8b4a92)
        1.  [I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.](#org6c80bcf)
        2.  [I don&rsquo;t know the catalogIDs of the targets I want to check.](#org0c6c07d)
        3.  [Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.](#org0f0bc08)
7.  [TODOs](#org7027b87)
    1.  [DONE](#org7f216b0)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="org642288a"></a>

# Installation

-   **Setup environment** (optional, but recommended)   
    If fulfilling the [Requirements](#org637ccf5) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**
    
        git clone https://github.com/jcbird/ppv.git  # clone repository
        cd ppv
        python setup.py install  # install ==ppv== package

-   **Requirements** <a id="org637ccf5"></a>
    -   python (>3.5, 3.8 preferred) [if this frightens you, read on]
    -   astropy
    -   pexpect (this is a dependency of ipython)
    -   [pydl](https://github.com/jcbird/ppv.git) (development version)
        Package from Benjamin Weaver for dealing with yanny files.


<a id="orgd33bf07"></a>

# Configuration and Data Files

`ppv` interacts with a number of data files and needs to know their location on disk. This is accomplished through the configuration file [`ppv_setup.ini`](ppv_setup.ini). This setup file is short, but will grow in future releases.

The contents of `ppv_setup.ini`

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">parameter</th>
<th scope="col" class="org-left">default value</th>
<th scope="col" class="org-left">description</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left"><code>plate_dir</code></td>
<td class="org-left"><code>/home/user/path/to/platedir</code></td>
<td class="org-left">absolute path to directory to store plate files</td>
</tr>


<tr>
<td class="org-left"><code>fiveplates_dir</code></td>
<td class="org-left"><code>/home/user/path/to/five_plates/plateruns</code></td>
<td class="org-left">absolute path to plateruns directory inside <code>five_plates</code> repo</td>
</tr>


<tr>
<td class="org-left"><code>sdss_org</code></td>
<td class="org-left"><code>username_at_utah</code></td>
<td class="org-left">username for sdss.org server at Utah</td>
</tr>
</tbody>
</table>

Notes:

-   file is ONLY read locally.
-   `plate_dir` does not need to exist. `ppv` will automatically create this directory if needed.


<a id="org83ae075"></a>

## Copy `ppv_setup.ini` to ~/.config and edit

You MUST edit the `ppv_setup.ini` and copy it to the `.config` directory in your home directory. Make this directory if necessary. Using a posix shell,

    mkdir ~/.config
    cd ppv
    cp ppv_setup.ini ~/.config

and edit accordingly.


<a id="org0a66b5d"></a>

## `five_plates` functionality

[`https://github.com/sdss/five_plates/tree/master/python`](file:///home/jquark/projects/sdss5/ppv/~five_plates~) produces the input files for the plate design code. `ppv` can interact with these &ldquo;field files&rdquo; as well.

-   You **MUST** clone the `five_plates` to the local machine running `ppv` AND edit your `ppv_setup.ini` file to point to the `plateruns` directory inside the repository. Be sure to perform  a `git pull` when necessary to get the latest plateruns files.
-   See the [`five_plates` tutorial notebook](docs/PPV_fiveplates.ipynb)  in the `docs` directory for an example of this.


<a id="org68bdc22"></a>

## Plate directory and PlugHoles files

If you have an account at Utah and put the `ppv_setup.ini` file in your `$HOME/.config` directory, you are good to go! `ppv` will take of everything!


<a id="orga112a91"></a>

### run `ppv.ppv.update_platefiles()` to ensure the latest versions of all plate files.

See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory for an example of this.


<a id="orgb825fff"></a>

# Breaking Changes (PLEASE READ)

In the interest of speed, `ppv` is following the, &ldquo;break early and often&rdquo; maxim. Inevitably, some changes will need to occur that are not backward-compatible. Apologies for the lack of a deprecation warning! Note that the tutorial notebooks in the `docs` folder are always updated to the latest syntax. With the hope that this section stays very short, the following breaking changes need to be accounted for:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Since version or commit</td>
<td class="org-left">Change</td>
</tr>


<tr>
<td class="org-left"><code>v0.3</code></td>
<td class="org-left">list of available plateruns are now accessible via <code>ppv.ppv.available_plateruns()</code></td>
</tr>


<tr>
<td class="org-left"><code>v0.3</code></td>
<td class="org-left">summary table of all plates now accessible via <code>ppv.ppv.allplate_summary</code></td>
</tr>


<tr>
<td class="org-left"><code>v0.35</code></td>
<td class="org-left"><code>ppv.targets.Targets</code>   constructor now just takes table and, optionally, column names</td>
</tr>
</tbody>
</table>


<a id="org1a42d67"></a>

# Concepts

There are four basic objects in the `ppv` package: `Plate`, `Field`, `Platerun`, and `Targets`. There is also a convenient plate summary table.


<a id="org942c269"></a>

## Plate Summary

Table accessible via `ppv.ppv.allplate_summary`. Each row corresponds to a single plate and contains, amongst other columns, the plate id, position of the plate center, the program name driving plate design, the corresponding field (name), and the platerun.


<a id="org608f842"></a>

## Plate

One to one correspondence with a plate. A `Plate` is identified by its unique plate id (an integer; e.g., 15004).


<a id="orgd1bf58a"></a>

## Field

A field is defined by a field name (a string; e.g., `AQM_001.85+26.44`) and represents one field of view on the sky. All plates belong to one field. All fields contain one or more plates.


<a id="org92d8d68"></a>

## Platerun

A platerun is defined by its name (a string; e.g., 2020.08.c.bhm-mwm). A platerun is a collection of fields (and thus plates) to be a drilled for a given observing run.


<a id="org8f715b1"></a>

## Targets

The Targets class is a container for your targets of interest and interfaces with the Plate, Field, and Platerun objects.


<a id="org3da2f2e"></a>

# Basic Usage


<a id="orga8a3cfc"></a>

## See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory.


<a id="orgf1ad5ef"></a>

## Specific example [notebook with 2020.10.a.mwm-bhm plate run](docs/platerun_2020_10_a_mwm_bhm_example.ipynb)


<a id="orgd8b4a92"></a>

# FAQs


<a id="org6c80bcf"></a>

### I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.

If you plan on checking SDSS-V targeting, please sign up for a Utah account at
<https://wiki.sdss.org/display/DATA/Utah+Accounts>.  
PLEASE DO THIS!   
If there is a delay in getting an account for any reason, submit an issue with &ldquo;No Utah account&rdquo; as the title. I will send you a tarball with the correct files and directory structure.


<a id="org0c6c07d"></a>

### I don&rsquo;t know the catalogIDs of the targets I want to check.

Look at the tutorial notebook (under Targets) to see if downloading one of the carton targetDB files is helpful. If not, create an issue and I will help asap!


<a id="org0f0bc08"></a>

### Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.

Awesome, let&rsquo;s make it work. Submit an issue!


<a id="org7027b87"></a>

# TODOs

1.  Sort targets and plugHoles tables by catalogID (after making sure that no info is lost in plugHoles files)
2.  Make it easy to get Gaia source IDs for all targets.
3.  Get documentation into ReadtheDocs format.
4.  Better Targets constructor.


<a id="org7f216b0"></a>

## DONE

1.  Make functions to update platePlans summary.
2.  Interface with five<sub>plates</sub> field files.

