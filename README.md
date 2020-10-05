
# Table of Contents

1.  [Installation](#orgb5a44eb)
2.  [Configuration and Data Files](#org1fae1cc)
    1.  [Copy `ppv_setup.ini` to ~/.config and edit](#org7795398)
    2.  [`five_plates` functionality](#org7776ba7)
    3.  [Plate directory and PlugHoles files](#orgdbcc1a2)
        1.  [run `ppv.ppv.update_platefiles()` to ensure the latest versions of all plate files.](#org05dae28)
3.  [Concepts](#orge3297cb)
        1.  [Plate Summary](#orgebfa645)
        2.  [Plate](#org250806c)
        3.  [Field](#orgeee0cec)
        4.  [Platerun](#org9f73b8e)
        5.  [Targets](#org6dcd111)
4.  [Basic Usage](#org1fe9e55)
5.  [FAQs](#org11260c0)
        1.  [I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.](#org4657662)
        2.  [I don&rsquo;t know the catalogIDs of the targets I want to check.](#orga7327fd)
        3.  [Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.](#orgc053ee5)
6.  [TODOs](#org7d64860)
    1.  [DONE](#orgafcd68f)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="orgb5a44eb"></a>

# Installation

-   **Setup environment** (optional, but recommended)   
    If fulfilling the [Requirements](#org75d013f) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**
    
        git clone https://github.com/jcbird/ppv.git  # clone repository
        cd ppv
        python setup.py install  # install ==ppv== package

-   **Requirements** <a id="org75d013f"></a>
    -   python (>3.5, 3.8 preferred) [if this frightens you, read on]
    -   astropy
    -   pexpect (this is a dependency of ipython)
    -   [pydl](https://github.com/jcbird/ppv.git) (development version)
        Package from Benjamin Weaver for dealing with yanny files.


<a id="org1fae1cc"></a>

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


<a id="org7795398"></a>

## Copy `ppv_setup.ini` to ~/.config and edit

You MUST edit the `ppv_setup.ini` and copy it to the `.config` directory in your home directory. Make this directory if necessary. Using a posix shell,

    mkdir ~/.config
    cd ppv
    cp ppv_setup.ini ~/.config

and edit accordingly.


<a id="org7776ba7"></a>

## `five_plates` functionality

[`https://github.com/sdss/five_plates/tree/master/python`](file:///home/jquark/projects/sdss5/ppv/~five_plates~) produces the input files for the plate design code. `ppv` can interact with these &ldquo;field files&rdquo; as well.

-   You **MUST** clone the `five_plates` to the local machine running `ppv` AND edit your `ppv_setup.ini` file to point to the `plateruns` directory inside the repository. Be sure to perform  a `git pull` when necessary to get the latest plateruns files.
-   See the [`five_plates` tutorial notebook](docs/PPV_fiveplates.ipynb)  in the `docs` directory for an example of this.


<a id="orgdbcc1a2"></a>

## Plate directory and PlugHoles files

If you have an account at Utah and put the `ppv_setup.ini` file in your `$HOME/.config` directory, you are good to go! `ppv` will take of everything!


<a id="org05dae28"></a>

### run `ppv.ppv.update_platefiles()` to ensure the latest versions of all plate files.

See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory for an example of this.


<a id="orge3297cb"></a>

# Concepts

There are four basic objects in the `ppv` package: `Plate`, `Field`, `Platerun`, and `Targets`. There is also a convenient plate summmary table.


<a id="orgebfa645"></a>

### Plate Summary

Table accessible via `ppv.allplate_summary`. Each row corresponds to a single plate and contains, amongst other columns, the plate id, position of the plate center, the program name driving plate design, the corresponding field (name), and the platerun.


<a id="org250806c"></a>

### Plate

One to one correspondance with a plate. A `Plate` is identified by its unique plate id (an integer; e.g., 15004).


<a id="orgeee0cec"></a>

### Field

A field is defined by a field name (a string; e.g., `AQM_001.85+26.44`) and represents one field of view on the sky. All plates belong to one field. All fields contain one or more plates.


<a id="org9f73b8e"></a>

### Platerun

A platerun is definied by its name (a string; e.g., 2020.08.c.bhm-mwm). A platerun is a collection of fields (and thus plates) to be a drilled for a given observing run.


<a id="org6dcd111"></a>

### Targets

The Targets class is a container for your targets of interest and interfaces with the Plate, Field, and Platerun objects.


<a id="org1fe9e55"></a>

# Basic Usage

See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory.


<a id="org11260c0"></a>

# FAQs


<a id="org4657662"></a>

### I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.

If you plan on checking SDSS-V targeting, please sign up for a Utah account at
<https://wiki.sdss.org/display/DATA/Utah+Accounts>.  
PLEASE DO THIS!   
If there is a delay in getting an account for any reason, submit an issue with &ldquo;No Utah account&rdquo; as the title. I will send you a tarball with the correct files and directory structure.


<a id="orga7327fd"></a>

### I don&rsquo;t know the catalogIDs of the targets I want to check.

Look at the tutorial notebook (under Targets) to see if downloading one of the carton targetDB files is helpful. If not, create an issue and I will help asap!


<a id="orgc053ee5"></a>

### Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.

Awesome, let&rsquo;s make it work. Submit an issue!


<a id="org7d64860"></a>

# TODOs

1.  Sort targets and plugHoles tables by catalogID (after making sure that no info is lost in plugHoles files)
2.  Make it easy to get Gaia source IDs for all targets.
3.  Get documentation into ReadtheDocs format.
4.  Better Targets constuctor.


<a id="orgafcd68f"></a>

## DONE

1.  Make functions to update platePlans summary.
2.  Interface with five<sub>plates</sub> field files.

