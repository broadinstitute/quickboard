# Quickboard

#### *A simple Python package for creating quick, modular dashboards*


## Overview

Quickboard is a collection of Python classes and utilities for making scalable dashboards. Built on top of 
[Dash](https://github.com/plotly/dash) and [Plotly](https://github.com/plotly/plotly.py), Quickboard provides an assortment of tools and pre-made components to mix and match, 
achieving a balance between ease-of-use and customizability.

All visible Quickboard components are instances of `dash.html` objects, so you can fully customize them using knowledge 
of the `dash` package. As `plotly` has `plotly.express`, this package can be thought of an (unofficial) incarnation of 
an "express" version of `dash`, allowing you to quickly prototype a dashboard, while allowing for full customization 
using the usual `dash` API.

The following example was made using Quickboard.

![An example screenshot](https://github.com/broadinstitute/quickboard/raw/main/docs/images/README_example.jpg "All tabs are automatically scrollable!")

The Quickboard package contains three subpackages of interest for developing dashboards:
* base - the core components used to make the backbone of the dashboard,
* plugins - highly customizable add-ons to augment your other components,
* (DEPRECATED) textboxes - components for having dynamically updated text (to be removed in future version).

More details on using these can be found [below](#usage).

## Install Guide

To install, simply run
```
pip install quickboard
```
in your virtual environment.

## Usage

Once you have some datasets you'd like to visualize and present with a dashboard, you can start making
Quickboard components to achieve this purpose. Check out the [Component Gallery](docs/component_gallery.md) to see what
you can create with just a few lines of code.

Once you have a few components you'd like to put together into a larger app, or to take advantage of using tab-level
plugin interactions, you can use a few of the other Quickboard classes to achieve this. The general layout of a full 
Quickboard consists of:
* a **Quickboard** object to hold everything together;
* a (n optional) list of **BaseTab** objects to organize visuals into tabs;
* a **Sidebar** calibrated to hold different **plugins** based on the current tab.

Within each tab, we have
* various **ContentGrid** objects to display other components in a grid, with customizable column wrapping length;
* different **DynamicPanel** objects, materialized in the form of a **PlotPanel** or **DataPanel**, which house the
primary data displays, updatable via the sidebar plugins and other panel specific **ControlPlugin** objects.

Understanding how to compose and mix these components will allow for a huge variety in producible dashboards. For more
info on how to use them, check out the docstrings (e.g. `help(ContentGrid)`) or see the 
[Guided Example](https://github.com/broadinstitute/quickboard/blob/main/docs/beginner_example.md).
