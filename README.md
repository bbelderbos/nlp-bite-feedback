# NLP on Bite exercise data

This script loads all Bite reviews and uses `[textblob](https://textblob.readthedocs.io/en/dev/)` to see which Bites have the most negative vs. raving reviews.

It's a great example of using a library that abstracts all (NLP) complexity away and got me results fast!

## Setup

Run `make setup` to make a virtual environment and install the dependencies.

## Example

Output of running `python script.py`:

```
$ python script.py
bite id | # comments | avg sentiment score
    442 |          1 | -0.5833333333333333
    142 |          3 | -0.38675925925925925
    286 |          3 | -0.2138227513227513
    145 |          4 | -0.16699305555555555
    276 |          3 | -0.16435185185185186
    260 |          6 | -0.1388888888888889

[output trucanted]

    412 |          2 | 0.7375
    140 |          2 | 0.75
    229 |          3 | 0.7533333333333333
```

To read reviews for one Bite:

- Positive:

```
$ python script.py 229
  0.6 | Nice one.
 0.75 | Nice Bite! Learned (once again) to always, always, always proof-read my code.
 0.91 | I've always struggled with loops, so this was very good practice.
 ```
- Negative:

```
$ python script.py 276
-0.25 | It was only difficult because I forgot why we were defining.
-0.15 | I'm not sure if I'm missing something on this one.  the multiply_numbers function didn't require a and b to be passed in to it when it was defined.  It can still multiply a and b.
-0.09 | If you are already going to have a function defined in the starting code it would be less confusing if you already had the multiply_numbers(a, b): filled in. As there is no way to get output from the built in editor, it is hard to troubleshoot that the variables in the function are missing.
```
