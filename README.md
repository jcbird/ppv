
# Table of Contents

1.  [Installation](#org19d0b59)
2.  [Configuration and Data Files](#org91029d8)
    1.  [Copy `ppv_setup.ini` to home/.config and edit](#org44087d6)
    2.  [Plate directory and PlugHoles files](#orgda8af53)
3.  [Concepts](#org9986207)
        1.  [Plate Summary](#orgd521dcc)
        2.  [Plate](#org1901dde)
        3.  [Field](#org20d329a)
        4.  [Platerun](#org4966542)
        5.  [Targets](#org2ac8720)
4.  [Basic Usage](#orgf99ed35)
5.  [FAQs](#org3318c97)
        1.  [I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.](#orgebe1042)
        2.  [Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.](#org4ee41da)
6.  [TODOs](#orge1d308b)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="org19d0b59"></a>

# Installation

-   **Setup environment** (optional, but recommended)   
    If fulfilling the [Requirements](#org98a14a6) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**
    
        git clone https://github.com/jcbird/ppv.git  # clone repository
        cd ppv
        python setup.py install  # install ==ppv== package

-   **Requirements** <a id="org98a14a6"></a>
    -   python (>3.5, 3.8 preferred) [if this frightens you, read on]
    -   astropy
    -   [pydl](https://github.com/jcbird/ppv.git) (development version)
        Package from Benjamin Weaver for dealing with yanny files.


<a id="org91029d8"></a>

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


<a id="org44087d6"></a>

## Copy `ppv_setup.ini` to home/.config and edit

You MUST edit the `ppv_setup.ini` and copy it to the `.config` directory in your home directory. Make this directory if necessary. Using a posix shell,

    mkdir ~/.config
    cd ppv
    cp ppv_setup.ini ~/.config

and edit accordingly.


<a id="orgda8af53"></a>

## Plate directory and PlugHoles files

If you have an account at Utah and put the `ppv_setup.ini` file in your `$HOME/.config` directory, you are good to go! `ppv` will take of everything!


<a id="org9986207"></a>

# Concepts

There are four basic objects in the `ppv` package: `Plate`, `Field`, `Platerun`, and `Targets`. There is also a convenient plate summmary table.


<a id="orgd521dcc"></a>

### Plate Summary

Table accessible via `ppv.allplate_summary`. Each row corresponds to a single plate and contains, amongst other columns, the plate id, position of the plate center, the program name driving plate design, the corresponding field (name), and the platerun.


<a id="org1901dde"></a>

### Plate

One to one correspondance with a plate. A `Plate` is identified by its unique plate id (an integer; e.g., 15004).


<a id="org20d329a"></a>

### Field

A field is defined by a field name (a string; e.g., `AQM_001.85+26.44`) and represents one field of view on the sky. All plates belong to one field. All fields contain one or more plates.


<a id="org4966542"></a>

### Platerun

A platerun is definied by its name (a string; e.g., 2020.08.c.bhm-mwm). A platerun is a collection of fields (and thus plates) to be a drilled for a given observing run.


<a id="org2ac8720"></a>

### Targets

The Targets class is a container for your targets of interest and interfaces with the Plate, Field, and Platerun objects.


<a id="orgf99ed35"></a>

# Basic Usage

See the [tutorial notebook](docs/PPV Tutorial.ipynb) in the `docs` directory.

Let&rsquo;s assume that you have a list of targets with numpy arrays `RA`, `Dec`, and `catalogIDs` representing the positions and catalogDB IDs, respecitively.
You want to know which of these stars **could** have been targeted within platerun `2020.08.c.bhm-mwm`.

You will need to constuct a \`Targets\` object to contain information about your targets and a \`Platerun\` object to interface with; e.g.,

\#+BEGIN<sub>SRC</sub> python
import ppv
targets = ppv.Targets(RA, Dec, catalogid=catalogIDs)
platerun = ppv.Platerun(&rsquo;2020.08.c.bhm-mwm&rsquo;)
\#+END<sub>SRC</sub> python

To get boolean mask (True/False array with the same shape as `catalogIDs`) of the available targets,  
`targets.available_in(platerun)`


<a id="org3318c97"></a>

# FAQs


<a id="orgebe1042"></a>

### I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.

If you plan to checking SDSS-V targeting long term, I strongly suggest you contact Joel Brownstein (check if there is a page somewhere) get access.   
In the meantime, submit an issue above with &ldquo;No Utah account&rdquo; as the title. I will send you a tarball with the correct files and directory structure.


<a id="org4ee41da"></a>

### Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.

Awesome, let&rsquo;s make it work. Submit an issue!


<a id="orge1d308b"></a>

# TODOs

1.  Make it easy to get Gaia source IDs for all targets.
2.  Get documentation into ReadtheDocs format.
3.  Make it so new plateruns don&rsquo;t require pulling the repository.
4.  Much more.

