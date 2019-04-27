# SW Enhance

This is a project for writing custom optimization tools for Summoners War.  The goal of this project is to have many of the functions of the Rune Optimizer, but be able to customize it.  On the other hand, this project will probably never have a GUI and is not designed to be able to be used without modification in general.  The Rune Optimizer is already an excellent tool for general use.  It is in its very early days and comes with no warranties or guarantees (or even tests at this point).

## Features

### Current Features

* Import data from SWEX json file
* Search for runes to reapp
* For grinds in inventory, find runes (that don't need to be reapped) that can use them

### Coming Features

* Search for how to use gems in inventory

## Usage

### Prerequisites

You need a Python 3 environment and the SW Exporter.

### Running

First use the SWEX to get your profile information.

Then modify `SWEnhance.py` to have the correct path to the JSON file.

Then run 
```bash
python SWEnhance.py
```

You will get a list of your grinds and the runes that can be improved by them.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This project would not be possible without Xzandro's sw-exporter and Rune Optimizer.  Parsing the data would have been long and tedious without the work coming before this project.
