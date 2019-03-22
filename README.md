# TSP Subroute Finder

This is a Python 3.7 script to look for subroutes in Excel Solver solutions to 
the Travelling Salesman's Problem

## Usage

The `tsp.py` file interprets a route in the form of

	(A,B) (B,C) (C,D) [...] (X,Y) (Y,Z) (Z,X)
	
where A, B ... Z are location IDs. **Note that spaces are only present between parentheses!**

The route can be either copied to script input (by invoking `tsp.py` without arguments) or read from a textfile (by invoking `tsp.py` with a single argument, the filename)

- Input the string manually: `python tsp.py`
- Read the route string from file `python tsp.py FILENAME`

The script `generate_route.py` can be used to generate sample data of any length and with any number of subroutes. This route is outputted both to stdout and to a `route.txt` file.
