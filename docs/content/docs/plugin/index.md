---
title: "Plugin"
description: "Drag-n-drop interface for the `rerun-sdk` viewer."
date: 2024-01-01 # used for ordering, most recent == first
layout: simple

cascade:
  showDate: false
  showAuthor: false
  showSummary: true
  invertPagination: true  
---

{{< lead >}}
Drag-n-drop interface for the `rerun-sdk` viewer.
{{< /lead >}}

<!-- ![Screenshots](feature.svg) -->

## The `rerun-viewer` for animation

1. (_optional_) Select a visualization configuration [see [here]({{< ref "config" >}}) for more details]
```sh
rerun-animation-config select CONFIG-NAME
```
2. Open the viewer
```sh
rerun-animation
```
3. Drag-n-drop a `*.bvh` or `*.npz` file

![quick-start](https://github.com/moverseai/rerun-animation/raw/main/docs/assets/gif/rerun_animation_quick_start.gif)

---