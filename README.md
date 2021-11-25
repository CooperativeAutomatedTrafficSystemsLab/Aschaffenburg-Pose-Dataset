# Aschaffenburg Pose Dataset (APD) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724486.svg)](https://doi.org/10.5281/zenodo.5724486)
This repository contains Python code for loading and filtering the Aschaffenburg Pose Dataset.
The dataset itself and a description can be found at **[Zenodo]**.
It contains trajectories as well as body poses of pedestrians and cyclists in road traffic
recorded in Aschaffenburg, Germany. It is appropriate for training and testing methods for
trajectory forecasting and intention prediction of vulnerable road users (VRUs) based on
the past trajectory and body poses.

[Zenodo]: https://doi.org/10.5281/zenodo.5724486

## Usage
First download the dataset **[here]** and unzip the file. The actual Python module for
loading and filtering the dataset can be found in the folder `APD`. In `examples` you
find the example of how to use the code (`plot_trajectories.py`). The example loads the
dataset from the provided path and plots the smoothed head trajectories in 2D from a bird's
eye view (the poses are not visualized here). The trajectories can be filtered by VRU type
and set using optional arguments:
```
Usage: python3 examples/plot_trajectories.py [-h] [-v VRU_TYPES] [-s SETS] path

Pipeline Arguments

positional arguments:
  path                  path to json files

optional arguments:
  -h, --help            show this help message and exit
  -v VRU_TYPES, --vru_types VRU_TYPES
                        select certain vru types for plotting ['ped', 'bike']
  -s SETS, --sets SETS  select certain sets for plotting ['train',
                        'validation', 'test']
```
[here]: https://doi.org/10.5281/zenodo.5724486
