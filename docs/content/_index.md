---
title: "rerun-animation :loop:" # :running: :runner: :running_woman: :nut_and_bolt: :moyai: :infinity: :wavy_dash: :curly_loop: :loop:
# https://gohugo.io/quick-reference/emojis/
description: "A python package that offers a rerun-sdk plugin and toolset to visualize 3D animation data."
---

{{< lead >}}
A `rerun-sdk` plugin & toolset to visualize 3D animation data.
{{< /lead >}}

<!-- TODO(badges)
https://shields.io/badges/discord
https://shields.io/badges/git-hub-release-date
https://shields.io/badges/py-pi-license
https://shields.io/badges/py-pi-status
-->

{{< button href="docs" target="_self" >}}
Get Started
{{< /button >}}

`rerun-animation` allows for quickly turning the installed <a style="display: inline;" href="https://www.rerun.io"><img src="https://rerun.io/logo.svg/" width=72 style="display: inline;"></a> viewer to a flexible `3D animation` viewer.

<!-- TODO: Once we add more funcs
A mini-framework

rerun-animation is more than a "plugin". It is a mini-framework developed with one goal in mind:

To enhance the `rerun-sdk` with supporting functionalities for working with 3D animation data.

For more information, see [Why this project?]()
-->

{{< alert >}}
**Warning!** The plugin is still in alpha but its functionality is not expected to change as it depends on `rerun-sdk` plugin system changes. 
Also, compatibility with specific `rerun-sdk` versions might be necessary because of this. 
Apart from integrating with `rerun-sdk` via the loader plugin, the `rerun-animation` package offers an additional configuration layer and extra tools. 
Once these have been stabilized and most bugs have been identified and solved, we will bump `rerun-animation` to a stable release.
{{< /alert >}}

## Features

With the `rerun-animation` {{< icon "python" >}} package users can:
- `install` a [rerun-loader-plugin](https://rerun.io/blog/data-loaders) to drag-n-drop  `3D animation` files in the [`rerun-viewer`](https://rerun.io/docs/reference/viewer/overview).
- `execute` commands to log `3D animation` data to a [`rerun`](https://www.rerun.io) instance.

`rerun-animation`  supports the following types of `3D animation` data:
1. Biovision Hierarchy files (`*.bvh`)
2. Parametric Human Body parameter files (`*.npz`) from <a style="display: inline;" href="https://meshcapade.com/"><img src="https://meshcapade.com/images/meshcapade_logo_white.svg" width=120 style="display: inline;vertical-align:middle;horizontal-align:top;margin:0px 0px 5px 0px"></a> 

<!--
<div class="flex px-4 py-2 mb-8 text-base rounded-md bg-primary-100 dark:bg-primary-900">
  <span class="flex items-center pe-3 text-primary-400">
    {{< icon "triangle-exclamation" >}}
  </span>
  <span class="flex items-center justify-between grow dark:text-neutral-300">
    <span class="prose dark:prose-invert">This is a demo of the <code id="layout">page</code> layout.</span>
    <button
      id="switch-layout-button"
      class="px-4 !text-neutral !no-underline rounded-md bg-primary-600 hover:!bg-primary-500 dark:bg-primary-800 dark:hover:!bg-primary-700"
    >
      Switch layout &orarr;
    </button>
  </span>
</div>
-->

<!-- {{< figure src="img/....png" class="m-auto mt-6 max-w-prose" >}} -->

<!--
Explore the [sample pages]({{< ref "" >}}) to get a feel for what Congo can do. If you like what you see, check out the project on [Github](https://github.com/jpanther/congo) or read the  to get started.
-->