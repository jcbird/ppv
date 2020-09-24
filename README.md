
# Table of Contents

1.  [Installation](#org20ed218)
    1.  [Requirements ](#orgd69c357)
2.  [Configuration and Data Files](#orgd5002b9)
3.  [Basic Usage](#org0d80a40)

Tools for dealing with SDSS-V plate files and plate runs.


<a id="org20ed218"></a>

# Installation

-   **Setup environment** (optional, but recommended)  
    If fulfilling the [Requirements](#org236f418) seems daunting and you run the conda package manager, you can set up a python environment that will happily install \`ppv\` with
    
        conda env create -f ppv_sdss_min.yml  # creates conda environment
        conda activate ppv  # activates conda environment
    
    and activate the environment with  
    `conda activate ppv`  
    Once you have activated your environment, proceed to clone and install!

-   **Clone this repository and install**  
    `git clone https://github.com/jcbird/ppv.git`  
    and, to install the \`ppv\` package  
    `python setup.py install`


<a id="orgd69c357"></a>

## Requirements <a id="org236f418"></a>

-   python (>3.5, 3.8 preferred) [if this frightens you, read on]
-   astropy
-   [pydl](https://github.com/jcbird/ppv.git) (development version)
    Package from Benjamin Weaver for dealing with yanny files.


<a id="orgd5002b9"></a>

# Configuration and Data Files

\`ppv\` interacts with a number of data files and needs to know their location on disk. This is accomplished through


<a id="org0d80a40"></a>

# Basic Usage

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

\*

