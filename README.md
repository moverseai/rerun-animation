#  A `rerun-sdk` plugin and tools for 3D animation

[![Python Version](https://img.shields.io/pypi/pyversions/rerun-animation.svg)](https://pypi.org/project/rerun-animation)
[![PyPI](https://img.shields.io/pypi/v/rerun-animation.svg)](https://pypi.org/project/rerun-animation)
![PyPI - Status](https://img.shields.io/pypi/status/rerun-animation)
[![PyPI - License](https://img.shields.io/pypi/l/rerun-animation)](https://github.com/moverseai/rerun-animation/blob/main/LICENSE)
[![Static Badge](https://img.shields.io/badge/docs-link-8A2BE2?style=flat&link=https%3A%2F%2Fmoverseai.github.io%2Frerun-animation%2F)](https://moverseai.github.io/rerun-animation/)
[![Discord](https://dcbadge.limes.pink/api/server/bQc7B6qSPd?style=flat)](https://discord.gg/bQc7B6qSPd)
<!-- [![Discord2](https://img.shields.io/badge/server-7289DA?logo=discord&logoColor=white&label=discord)](https://discord.gg/bQc7B6qSPd) -->
<!-- <a href="https://discord.gg/bQc7B6qSPd"><img src="https://img.shields.io/discord/1069970354937806970?logo=discord&logoColor=violet&label=discord" alt="Active Discord Server Users"/></a> -->

[![GitHub Release Date](https://img.shields.io/github/release-date/moverseai/rerun-animation)](https://github.com/moverseai/rerun-animation/releases)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/rerun-animation?style=plastic&logo=python&logoColor=magenta&color=magenta&link=https%3A%2F%2Fpypi.org%2Fproject%2Frerun-animation%2F)](https://pypi.org/project/rerun-animation/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ace5cb2d5105429da91010170445d4c6)](https://app.codacy.com/gh/moverseai/rerun-animation/dashboard)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<!-- [![CodeFactor](https://www.codefactor.io/repository/github/moverseai/rerun-animation/badge)](https://www.codefactor.io/repository/github/moverseai/rerun-animation) -->
<!-- [![Downloads](https://static.pepy.tech/badge/rerun-animation)](https://pepy.tech/project/rerun-animation) -->

[![Black Format](https://github.com/moverseai/rerun-animation/actions/workflows/black.yaml/badge.svg)](https://github.com/moverseai/rerun-animation/actions/workflows/black.yaml)
[![GitHub Pages](https://github.com/moverseai/rerun-animation/actions/workflows/gh-pages.yaml/badge.svg)](https://github.com/moverseai/rerun-animation/actions/workflows/gh-pages.yaml)
___

<!-- [![Downloads](https://static.pepy.tech/badge/rerun-animation/month)](https://pepy.tech/project/rerun-animation) -->


> ➿`rerun-animation` turns the [rerun-sdk](https://www.rerun.io) viewer to a `3D animation` viewer.

![intro](https://github.com/moverseai/rerun-animation/raw/main/docs/assets/gif/rerun_animation_amass_multi.gif)

## 📦 Features

With the `rerun-animation` ➿ package users can:
- `install` a [rerun-loader-plugin](https://rerun.io/blog/data-loaders) to drag-n-drop  `3D animation` files in the [`rerun-viewer`](https://rerun.io/docs/reference/viewer/overview).
- `execute` commands to log `3D animation` data to a [`rerun`](https://www.rerun.io) instance.

`rerun-animation`  supports the following types of `3D animation` data:
1. Biovision Hierarchy files (`*.bvh`)
2. Parametric Human Body parameter files (`*.npz`) from <a style="display: inline;" href="https://meshcapade.com/"><img src="https://meshcapade.com/images/meshcapade_logo_white.svg" width=120 style="display: inline;vertical-align:middle;horizontal-align:top;margin:0px 0px 5px 0px"></a> 

<!-- ☘️ 🌟 📣 💼 💾 👩‍💻 🎯 🥇 👑 💯 🏆 🎉 ⚡ 🔥 🐍 📌 📈 📝 🧩 📄 📖 🚀 📚 💡 🤝 🤍 💚 🧱 ⚙️ 🔗 ⭐ 📦 📰 🛠 🎁 ⏳ 🎓 👋 ✨ 🧮 ✅ 👀 -->

## 👩‍💻 Documentation

Up-to-date [documentation](https://moverseai.github.io/rerun-animation/docs/) is available online. 


## 💾 Installation

```sh
pip install rerun-animation
```

> [!WARNING]  
> `rerun-animation` has only been tested on Windows up to now, if you use another OS please submit your [feedback](#-get-involved) in case of errors.

### ⚒ Post-installation deployment

### `*.bvh` only
```sh
rerun-animation-deploy
```

### with `smpl(-h)` support

```sh
rerun-animation-deploy --body_data_root `PATH/TO/BODY/MODELS`
```

## ⏩ Quickstart

1. (_optional_) Select a visualization configuration
```sh
rerun-animation-config select CONFIG-NAME
```
2. Open the viewer
```sh
rerun-animation
```
3. Drag-n-drop a `*.bvh` or `*.npz` file

![quick-start](https://github.com/moverseai/rerun-animation/raw/main/docs/assets/gif/rerun_animation_quick_start.gif)


## 🤝 Get Involved

Feedback and contributions are welcome via GitHub ([issue](https://github.com/moverseai/rerun-animation/issues/new)/[PR](https://github.com/moverseai/rerun-animation/compare)) and [Discord](https://discord.gg/bQc7B6qSPd).
