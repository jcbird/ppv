
# Table of Contents

1.  [Installation](#org26a20b1)
2.  [Configuration and Data Files](#org050f07d)
    1.  [Copy `ppv_setup.ini` to home/.config and edit](#org525d270)
    2.  [Plate directory and PlugHoles files](#org4c37898)
3.  [Concepts](#orgaaf285e)
        1.  [Plate Summary](#orgbd0c26a)
        2.  [Plate](#org518da81)
        3.  [Field](#orge1c1186)
        4.  [Platerun](#org6ceba34)
        5.  [Targets](#orgd2a5023)
4.  [Basic Usage](#orgd9a6323)
5.  [FAQs](#org25d487a)
        1.  [I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.](#org37d08c1)
        2.  [I don&rsquo;t know the catalogIDs of the targets I want to check.](#orga4029df)
        3.  [Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.](#org72796f6)
6.  [TODOs](#org29f4ef5)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="org26a20b1"></a>

# Installation

-   **Setup environment** (optional, but recommended)   
    If fulfilling the [Requirements](#orgd03fe7f) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**
    
        git clone https://github.com/jcbird/ppv.git  # clone repository
        cd ppv
        python setup.py install  # install ==ppv== package

-   **Requirements** <a id="orgd03fe7f"></a>
    -   python (>3.5, 3.8 preferred) [if this frightens you, read on]
    -   astropy
    -   [pydl](https://github.com/jcbird/ppv.git) (development version)
        Package from Benjamin Weaver for dealing with yanny files.


<a id="org050f07d"></a>

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
<td class="org-left">/home/jquark/obsdata/plates</td>
<td class="org-left">absolute path to directory to store plate files</td>
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
-   plate<sub>dir</sub> does not need to exist. `ppv` will automatically create this directory if needed.


<a id="org525d270"></a>

## Copy `ppv_setup.ini` to home/.config and edit

You MUST edit the `ppv_setup.ini` and copy it to the `.config` directory in your home directory. Make this directory if necessary. Using a posix shell,

    mkdir ~/.config
    cd ppv
    cp ppv_setup.ini ~/.config

and edit accordingly.


<a id="org4c37898"></a>

## Plate directory and PlugHoles files

If you have an account at Utah and put the `ppv_setup.ini` file in your `$HOME/.config` directory, you are good to go! `ppv` will take of everything!


<a id="orgaaf285e"></a>

# Concepts

There are four basic objects in the `ppv` package: `Plate`, `Field`, `Platerun`, and `Targets`. There is also a convenient plate summmary table.


<a id="orgbd0c26a"></a>

### Plate Summary

Table accessible via `ppv.allplate_summary`. Each row corresponds to a single plate and contains, amongst other columns, the plate id, position of the plate center, the program name driving plate design, the corresponding field (name), and the platerun.


<a id="org518da81"></a>

### Plate

One to one correspondance with a plate. A `Plate` is identified by its unique plate id (an integer; e.g., 15004).


<a id="orge1c1186"></a>

### Field

A field is defined by a field name (a string; e.g., `AQM_001.85+26.44`) and represents one field of view on the sky. All plates belong to one field. All fields contain one or more plates.


<a id="org6ceba34"></a>

### Platerun

A platerun is definied by its name (a string; e.g., 2020.08.c.bhm-mwm). A platerun is a collection of fields (and thus plates) to be a drilled for a given observing run.


<a id="orgd2a5023"></a>

### Targets

The Targets class is a container for your targets of interest and interfaces with the Plate, Field, and Platerun objects.


<a id="orgd9a6323"></a>

# Basic Usage

See the [tutorial notebook](docs/PPV_tutorial.ipynb) in the `docs` directory.


<a id="org25d487a"></a>

# FAQs


<a id="org37d08c1"></a>

### I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.

If you plan on checking SDSS-V targeting, please sign up for a Utah account at
<https://wiki.sdss.org/display/DATA/Utah+Accounts>.  
PLEASE DO THIS!   
If there is a delay in getting an account for any reason, submit an issue with &ldquo;No Utah account&rdquo; as the title. I will send you a tarball with the correct files and directory structure.


<a id="orga4029df"></a>

### I don&rsquo;t know the catalogIDs of the targets I want to check.

Look at the tutorial notebook (under Targets) to see if downloading one of the carton targetDB files is helpful. If not, create an issue and I will help asap!


<a id="org72796f6"></a>

### Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.

Awesome, let&rsquo;s make it work. Submit an issue!


<a id="org29f4ef5"></a>

# TODOs

1.  Make functions to update platePlans summary.
2.  Sort targets and plugHoles tables by catalogID (after making sure that no info is lost in plugHoles files)
3.  Make it easy to get Gaia source IDs for all targets.
4.  Get documentation into ReadtheDocs format.
5.  Better Targets constuctor.
6.  Interface with five<sub>plates</sub> field files.
7.  Much more.

