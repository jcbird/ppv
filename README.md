
# Table of Contents

1.  [Installation](#org3981608)
2.  [Configuration and Data Files](#orgec0e892)
    1.  [Copy `ppv_setup.ini` to home/.config and edit](#org0bf7081)
    2.  [Plate directory and PlugHoles files](#orgd45a881)
3.  [Concepts](#orga93a175)
4.  [Basic Usage](#org0357f7b)
5.  [FAQs](#orge924146)
6.  [TODOs](#orgbbbba3c)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="org3981608"></a>

# Installation

-   **Setup environment** (optional, but recommended)   
    If fulfilling the [Requirements](#orga4b1982) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**
    
        git clone https://github.com/jcbird/ppv.git  # clone repository
        cd ppv
        python setup.py install  # install ==ppv== package

-   **Requirements** <a id="orga4b1982"></a>
    -   python (>3.5, 3.8 preferred) [if this frightens you, read on]
    -   astropy
    -   [pydl](https://github.com/jcbird/ppv.git) (development version)
        Package from Benjamin Weaver for dealing with yanny files.


<a id="orgec0e892"></a>

# Configuration and Data Files

`ppv` interacts with a number of data files and needs to know their location on disk. This is accomplished through the configuration file [ppv<sub>setup.ini</sub>](ppv_setup.ini). This setup file is short, but will grow in future releases.

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
<td class="org-left">plate<sub>dir</sub></td>
<td class="org-left">/home/jquark/obsdata/plates</td>
<td class="org-left">absolute path to directory to store plate files</td>
</tr>


<tr>
<td class="org-left">sdss<sub>org</sub></td>
<td class="org-left">username<sub>at</sub><sub>utah</sub></td>
<td class="org-left">username for sdss.org server at Utah</td>
</tr>
</tbody>
</table>

Notes:

-   file is ONLY read locally.
-   plate<sub>dir</sub> does not need to exist. `ppv` will automatically create this directory if needed.


<a id="org0bf7081"></a>

## Copy `ppv_setup.ini` to home/.config and edit

You MUST edit the `ppv_setup.ini` and copy it to the `.config` directory in your home directory. Make this directory if necessary. Using a posix shell,

    mkdir ~/.config
    cd ppv
    cp ppv_setup.ini ~/.config

and edit accordingly.


<a id="orgd45a881"></a>

## Plate directory and PlugHoles files

If you have an account at Utah and put the `ppv_setup.ini` file in your `$HOME/.config` directory, you are good to go! `ppv` will take of everything!


<a id="orga93a175"></a>

# Concepts


<a id="org0357f7b"></a>

# Basic Usage

See

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

~
~targets =

\#+BEGIN<sub>SRC</sub>

Check out the tutorial notebook (in the [Notebooks](notebooks/) directory) for more in depth information and examples.


<a id="orge924146"></a>

# FAQs

1.  I don&rsquo;t have an account at Utah and/or I can&rsquo;t get the plugHoles files.   
    If you plan to checking SDSS-V targeting long term, I strongly suggest you contact Joel Brownstein (check if there is a page somewhere) get access.   
    In the meantime, submit an issue above with &ldquo;No Utah account&rdquo; as the title. I will send you a tarball with the correct files and directory structure.
2.  Something doesn&rsquo;t work, I wish `ppv` did THIS, why does `ppv` do THIS, I want to do X with `ppv`, or I wish something in `ppv` had a different name.   
    Awesome, let&rsquo;s make it work. Submit an issue!


<a id="orgbbbba3c"></a>

# TODOs

1.  Make it easy to get Gaia source IDs for all targets.
2.  Much more.

