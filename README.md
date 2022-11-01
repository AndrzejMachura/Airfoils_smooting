# Airfoils smoothing

This script is using scipy splrep function to find the B-spline representation of 1-D curve. It is used to determine a smooth spline approximation of NACA airfoils. 

## How to use

1. Give file name in csv format with profile points. X-axis should be scaled to 1
2. Determine how many output points are wanted.
3. Give smoothing factor of profiles nose (number greater than 1).
4. Variable *border* is responsible for the length of the nose

## License 

You are free to use, modify and distribute the code as long as authorship is properly acknowledged.

## Exemplary airfoils

Exemplary airfoils are added to *spline*. All examples are taken from [Airfoil Tools](http://airfoiltools.com)
