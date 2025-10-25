---
title: Addition
---

# Addition and numerical errors

In this chapter, we will be working with signed floating point numbers, so I add the last bit we need to get a `Float8` class.
If you have read previous two chapters, you know that this class has integer `e` and `m` members (standing for exponent and mantissa).
Here I add `s` member that can take either `1` or `-1` value.

This triplet represents the real number that can be computed as `s * m * 2**(e-4)` (line 17 of the following listing):

??? example "float8.py"
    ```py linenums="1" hl_lines="20-25"
    --8<-- "add/float8a.py"
    ```


## Rounding

The IEEE754 standard defines a number of rounding modes but the default rounding mode is the *round-to-nearest-even-on-ties* (RNE) mode.
Here is an illustration of RNE rounding mode with our 8-bit floating point representation:

![](add/rounding.svg)

The real number 4.65 is rounded to its only nearest `Float8` neighbor 4.75,
however there are two nearest `Float8` values (4.75 and 5.0) equidistant to the real number 4.875.
In this case, RNE mode specifies that 4.875 should round to 5.0 because the bit representation of 5.0 (`0b01100100`) is an even number when interpreted as an integer.
Similarly, the real number 5.125 rounds to 5.0 and 5.375 rounds to 5.5.

## Addition

## Numerical errors

The result of arithmetic operations in floating point experiences rounding error when it cannot be exactly represented.
While modern hardware and libraries produce correctly rounded results for arithmetic operations,
this rounding error can get amplified with a series of operations because the intermediate result must be rounded.
When working with finite precision, numerical errors should be carefully addressed.

### Catastrophic cancellation

### Summation


--8<-- "comments.html"
