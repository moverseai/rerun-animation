---
title: "Getting Started"
description: "Setup and install the rerun-animation package."
date: 2024-01-12 # used for ordering, most recent == first
layout: simple

cascade:
  showDate: false
  showAuthor: false
  showSummary: true
  invertPagination: true  
  showTableOfContents: true
---

{{< lead >}}
Setup and install the `rerun-animation` package.
{{< /lead >}}


## Installation

Install the package from PyPi using `pip`:

```bash
pip install rerun-animation
```

<div id="termynal" data-termynal data-ty-startDelay="600">
    <span data-ty="input" data-ty-prompt="~">pip install rerun-animation</span>
    <span data-ty data-ty-delay="250" data-ty-cursor="▋">Installing collected packages: rerun-animation...</span>
    <span data-ty="progress"></span>
    <span data-ty>Successfully installed rerun-animation</span>
</div>

The `rerun-animation` package is now almost ready for use.

## Deployment

While `*.bvh` files are straightforwardly available through this package after installing the plugin below, the parametric body animation files (e.g. `SMPL`/`SMPL-H`) require the deployment of their associated data files.

### Meshcapade / MPI Body Model Data

{{< alert "circle-info" >}}
**Important!** To be able to use body model files (`*.npz`) with this package, it is necessary to deploy their parameter files.
{{< /alert >}}

Download the respective body model files from:

- `SMPL`: https://smpl.is.tue.mpg.de/ 
- `SMPL-H`: https://mano.is.tue.mpg.de/

and place them under a common folder `PATH/TO/BODY/MODELS`.

Then, run:
```bash
rerun-animation-deploy --body_data_root `PATH/TO/BODY/MODELS`
```

<div id="termynal" data-termynal data-ty-startDelay="600">
    <span data-ty="input" data-ty-prompt="~">rerun-animation-deploy --body_data_root `PATH/TO/BODY/MODELS`</span>
    <span data-ty data-ty-delay="250" data-ty-cursor="▋">⚙    Preparing files from `PATH/TO/BODY/MODELS` ...</span>
    <span data-ty data-ty-delay="250" data-ty-cursor="▋"> 🟠    Processing `FILENAME1` ...</span>
    <span data-ty data-ty-delay="250" data-ty-cursor="▋"> 🟢    Done. Saving to ...</span>
    <span data-ty="progress"></span>
    <span data-ty>Installing the rerun-loader-animation plugin ...</span>
    <span data-ty="progress"></span>
</div>

Apart from deploying the necessary body model files, the previous step also installs the `rerun-loader-plugin` for animation data.

{{< alert "microsoft" >}}
**Important!** For Microsoft Windows it is necessary to install an executable with PyInstaller, which might take some time. For more details please see [rerun-sdk/external_data_loader](https://github.com/rerun-io/rerun/tree/main/examples/python/external_data_loader)
{{< /alert >}}


---