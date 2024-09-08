---
title: "Getting Started"
description: "Setup and install the `rerun-animation` package."
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

{{< icon "list" >}} Install the package from PyPi using `pip`:

```bash
pip install rerun-animation
```

<div id="termynal" data-termynal data-ty-startDelay="600">
    <span data-ty="input" data-ty-prompt="~">pip install rerun-animation</span>
    <span data-ty data-ty-delay="250" data-ty-cursor="▋">Installing collected packages: rerun-animation...</span>
    <span data-ty="progress"></span>
    <span data-ty>Successfully installed rerun-animation</span>
</div>

{{< icon "check" >}} The `rerun-animation` package is now installed & almost ready to use.

## Deployment

{{< icon "list" >}} After installing the package, the next step is to deploy the `rerun-loader-plugin` by running:

```bash
rerun-animation-deploy
```

<div id="termynal" data-termynal data-ty-startDelay="600">
    <span data-ty="input" data-ty-prompt="~">rerun-animation-deploy</span>    
    <span data-ty>Installing the rerun-loader-animation plugin ...</span>
    <span data-ty="progress"></span>
</div>

{{< icon "check" >}} Support for `*.bvh` files is straightforwardly available through this barebone deployment. [`rerun` [transforms]({{< ref "plugin" >}}) to a `bvh-viewer`]

{{< icon "xmark" >}} However, support for the parametric body animation files (e.g. `SMPL`/`SMPL-H`) requires the deployment of their associated data files.

{{< alert "circle-info" >}}
In the case that support for parametric body model files is not needed, the **missing file warnings** can be safely ignored.
{{< /alert >}}

### Meshcapade / MPI Body Model Data

{{< alert "circle-info" >}}
**Important!** To be able to use body model files (`*.npz`) with this package, it is necessary to deploy their parameter files.
{{< /alert >}}

{{< icon "list" >}}
Download the currently supported body model files and place them under a common folder `PATH/TO/BODY/MODELS`:

- `SMPL`: https://smpl.is.tue.mpg.de/ 
- `SMPL-H`: https://mano.is.tue.mpg.de/

{{< icon "list" >}}Then, run the deployment with the `body_data_root` argument pointing to `PATH/TO/BODY/MODELS`:

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

{{< icon "check" >}} The `rerun-loader-plugin` now supports custom `*.npz` files containing parametric body model parameters.

{{< alert "microsoft" >}}
**Important!** For Microsoft Windows it is necessary to install an executable with [PyInstaller](https://pyinstaller.org/en/stable/), which might take some time. For more details please see [rerun-sdk/external_data_loader](https://github.com/rerun-io/rerun/tree/main/examples/python/external_data_loader)
{{< /alert >}}

## Next

See how to select a visualization [configuration]({{< ref "config" >}}), or just [drag-n-drop]({{< ref "plugin" >}}) a file into the `rerun-viewer`.


---