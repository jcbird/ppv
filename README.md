
# Table of Contents

1.  [Installation](#org09e7c68)
2.  [Configuration and Data Files](#org07cbf7c)
    1.  [Copy `ppv_setup.ini` to ~/.config and edit](#org4af761d)
    2.  [`five_plates` functionality](#orgebee548)
    3.  [Plate directory and PlugHoles files](#orge3335e7)
        1.  [run `ppv.ppv.update_platefiles()` to ensure the latest versions of all plate files.](#org4f69f52)
3.  [Concepts](#org8a12d1d)
    1.  [Plate Summary](#orgd6b7f70)
    2.  [Plate](#orgbb9cdd9)
    3.  [Field](#org808862d)
    4.  [Platerun](#orgc325d80)
    5.  [Targets](#org5d3ec58)
4.  [Breaking Changes (READ)](#org665b1ab)
5.  [Bsic Usage](#org2c33410)
6.  [FAQs](#org2b0bebc)
        1.  [I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.](#org7ae165a)
        2.  [I don&rsquo;t know the catalogIDs of the targets I want to check.](#org35dc942)
        3.  [Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.](#org526d467)
7.  [TODOs](#org90f53f1)
    1.  [DONE](#org9a96a03)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="org09e7c68"></a>

# Installation

-   **Setup environment** (optional, but recommended)   
    If fulfilling the [Requirements](#orgc943cb2) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**
    
        git clone https://github.com/jcbird/ppv.git  # clone repository
        cd ppv
        python setup.py install  # install ==ppv== package

-   **Requirements** <a id="orgc943cb2"></a>
    -   python (>3.5, 3.8 preferred) [if this frightens you, read on]
    -   astropy
    -   pexpect (this is a dependency of ipython)
    -   [pydl](https://github.com/jcbird/ppv.git) (development version)
        Package from Benjamin Weaver for dealing with yanny files.


<a id="org07cbf7c"></a>

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


<a id="org4af761d"></a>

## Copy `ppv_setup.ini` to ~/.config and edit

You MUST edit the `ppv_setup.ini` and copy it to the `.config` directory in your home directory. Make this directory if necessary. Using a posix shell,

    mkdir ~/.config
    cd ppv
    cp ppv_setup.ini ~/.config

and edit accordingly.


<a id="orgebee548"></a>

## `five_plates` functionality

[`https://github.com/sdss/five_plates/tree/master/python`](file:///home/jquark/projects/sdss5/ppv/~five_plates~) produces the input files for the plate design code. `ppv` can interact with these &ldquo;field files&rdquo; as well.

-   You **MUST** clone the `five_plates` to the local machine running `ppv` AND edit your `ppv_setup.ini` file to point to the `plateruns` directory inside the repository. Be sure to perform  a `git pull` when necessary to get the latest plateruns files.
-   See the [`five_plates` tutorial notebook](docs/PPV_fiveplates.ipynb)  in the `docs` directory for an example of this.


<a id="orge3335e7"></a>

## Plate directory and PlugHoles files

If you have an account at Utah and put the `ppv_setup.ini` file in your `$HOME/.config` directory, you are good to go! `ppv` will take of everything!


<a id="org4f69f52"></a>

### run `ppv.ppv.update_platefiles()` to ensure the latest versions of all plate files.

See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory for an example of this.


<a id="org8a12d1d"></a>

# Concepts

There are four basic objects in the `ppv` package: `Plate`, `Field`, `Platerun`, and `Targets`. There is also a convenient plate summary table.


<a id="orgd6b7f70"></a>

## Plate Summary

Table accessible via `ppv.ppv.allplate_summary`. Each row corresponds to a single plate and contains, amongst other columns, the plate id, position of the plate center, the program name driving plate design, the corresponding field (name), and the platerun.


<a id="orgbb9cdd9"></a>

## Plate

One to one correspondence with a plate. A `Plate` is identified by its unique plate id (an integer; e.g., 15004).


<a id="org808862d"></a>

## Field

A field is defined by a field name (a string; e.g., `AQM_001.85+26.44`) and represents one field of view on the sky. All plates belong to one field. All fields contain one or more plates.


<a id="orgc325d80"></a>

## Platerun

A platerun is defined by its name (a string; e.g., 2020.08.c.bhm-mwm). A platerun is a collection of fields (and thus plates) to be a drilled for a given observing run.


<a id="org5d3ec58"></a>

## Targets

The Targets class is a container for your targets of interest and interfaces with the Plate, Field, and Platerun objects.


<a id="org665b1ab"></a>

# Breaking Changes (READ)

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
</tbody>
</table>


<a id="org2c33410"></a>

# Bsic Usage

See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory.


<a id="org2b0bebc"></a>

# FAQs


<a id="org7ae165a"></a>

### I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.

If you plan on checking SDSS-V targeting, please sign up for a Utah account at
<https://wiki.sdss.org/display/DATA/Utah+Accounts>.  
PLEASE DO THIS!   
If there is a delay in getting an account for any reason, submit an issue with &ldquo;No Utah account&rdquo; as the title. I will send you a tarball with the correct files and directory structure.


<a id="org35dc942"></a>

### I don&rsquo;t know the catalogIDs of the targets I want to check.

Look at the tutorial notebook (under Targets) to see if downloading one of the carton targetDB files is helpful. If not, create an issue and I will help asap!


<a id="org526d467"></a>

### Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.

Awesome, let&rsquo;s make it work. Submit an issue!


<a id="org90f53f1"></a>

# TODOs

1.  Sort targets and plugHoles tables by catalogID (after making sure that no info is lost in plugHoles files)
2.  Make it easy to get Gaia source IDs for all targets.
3.  Get documentation into ReadtheDocs format.
4.  Better Targets constructor.


<a id="org9a96a03"></a>

## DONE

1.  Make functions to update platePlans summary.
2.  Interface with five<sub>plates</sub> field files.

