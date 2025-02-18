---
title: Afterword
---

# A compiler in a week-end: afterword
This project was (and still is!) a tremendous fun for me.
I have learned quite a few things during the journey that ought to take just one week-end.
It took much, much longer.
I mean, the core compiler was made in one week-end (from Friday Jan 12 to Sunday Jan 14, 2024), you can check the commit history.
But it went sideways:

* I accidentally learned [C preprocessor black magic](../strange/cursed-fire.md).
* I programmed my own lexer and my own parser even if it was not initially planned.
* I dived into the bottomless pit of [optimizing compilers](https://github.com/ssloy/tinyoptimizer/), and I am not sure to make it to the surface ever again.
* I met new people.
* And I have spent weeks if not months on test programs.

Have you ever wondered [how to compute trigonometric functions](https://github.com/ssloy/tinycompiler/blob/main/test-programs/nontrivial/trig-hp12c.wend) when you do not have access to any math library
and you have only integer variables?

??? example "int sin24(int x)"
    ```cpp
    // sin(x) = x * (1 + x^2 * (0.00761 * x^2 - 0.16605))
    // this formula works pretty well in the range [-pi/2, +pi/2]
    int sin24(int x) {
        int sign;
        if x>0 { sign = 1; } else { sign = -1; x = -x; }    //
        while x>+79060768 { x = x - 105414357; }            // reduce the argument to the acceptable range
        if x>26353589 { return sign*sin24(52707179 - x); }  //
        return sign*(x/4096)*((16777216 + (((x/4096)*(x/4096))/4096)*((((x/4096)*(x/4096))/131 - 2785856)/4096))/4096);
    }
    ```

Have you tried to emulate bitwise operations (not/and/or/xor) using only [integer arithmetics](https://github.com/ssloy/tinycompiler/blob/main/test-programs/nontrivial/bitwise.wend)?
??? example "int and(int a, int b)"
    ```cpp
    int and(int a, int b) {
        int result;
        int pow;

        result = 0;
        if (a<0 && b<0) {
            result = -2147483648;
        }
        if (a<0) {
            a = a + 2147483648;
        }
        if (b<0) {
            b = b + 2147483648;
        }
        pow = 1;
        while a>0 || b>0 {
            if a % 2 == 1 && b % 2 == 1 {
                result = result + pow;
            }
            a = a / 2;
            b = b / 2;
            pow = pow * 2;
        }
        return result;
    }
    ```

Have you tried to program a [zero-player breakout game](https://github.com/ssloy/tinycompiler/blob/main/test-programs/gfx/breakout.wend) without having arrays?

<video width="320" autoplay="" loop="" muted="" controls=""><source src="../home/breakout.mp4" type="video/mp4"></source></video>


Stay tuned, have fun!


