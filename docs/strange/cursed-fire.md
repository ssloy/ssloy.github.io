# Cursed fire or `#define` black magic

![](cursed-fire/define.png)

Have you ever wondered whether it is possible to write fully functional code using only the `#define` directive in C?
It's well-known that the C++ templates are Turing complete, developers even write [ray tracers](https://github.com/tcbrindle/raytracer.hpp) that do all evaluations at compile time (instead of runtime).
What about the C preprocessor? As it turns out, the question is a bit more complex than one might think.
Let us try to figure it out. There won't be any ray tracer, but you'll see quite a bit of cursed code.

First of all, why do I raise the question? If you find old-school computer graphics boring, you can skip the next section.

## The most mundane fire, non-cursed yet

In fact, recently I promised to write a simple, yet quite [rich compiler for the *wend* language](../../compiler/) that I just invented over the weekend.
Although it's easy to code, it's harder to *describe*.
A good description needs vibrant examples.
I'm allergic to code examples like calculating Fibonacci numbers.
For crying out loud! Since *wend* is pretty primitive, I need examples that are simple yet still impressive.
Suddenly, remembered the old demoscene!
Let us say, I want a bonfire animation.

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire6.mp4" type="video/mp4"></source></video>

It's not all that difficult.
I can't run graphics mode, but my terminal supports the `\033[` escape sequence, so a single `print` instruction is enough to draw the fire!
By the way, I have heard that the Windows terminal also supports the ANSI escape sequences, but I haven't checked it myself.
The technology being sorted out, all that's left to do is write the code.
Since I am only half-crazy, I'll write it first in C, and then translate it (manually) into the *wend* language.
Indeed, my compiler is good, but C offers a greater variety of tools.
In addition to that, my compiler isn't bug-free, and I'm too lazy to chase the issues out.
Of course, it happened to me to come across the GCC bugs, but they're rare and almost extinct.
Let us see how to create such a fire animation, and then we'll get back to the preprocessor and the black magic.
This is what the starting point looks like:

??? example "The starting point"
    ```cpp hl_lines="48-51" linenums="1"
    --8<-- "cursed-fire/fire0.c"
    ```

First, I define the dimensions of my terminal (80x25), then define the 256-color palette array and the `fire` buffer that actually contains the picture of the (future) bonfire.
Then, in the infinite `for(;;)` loop, I render the buffer, where I fill randomly selected pixels with white color.
We obtain quite an expected result:

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire0.mp4" type="video/mp4"></source></video>

The white pixels will be sparks of flame.
The sparks cool down pretty quickly while heating the surroundings.
It's easy to simulate: at each new frame, we just blur the picture from the previous frame.
All the code changes will occur inside the block marked as `// rendering body`, and each time I'll highlight the lines that change.
You can find the final code in [my compiler repository](https://github.com/ssloy/tinycompiler/tree/main/test-programs/gfx).

The simplest way to blur a picture is to compute the average value of each pixel in relation to its neighboring pixels.
Virtually all implementations I come across require creating a copy of the entire buffer.
Check it on [Wikipedia](https://en.wikipedia.org/wiki/Box_blur) for an example.
However, such filters are separable in coordinates, so the blur can be obtained
by two separate [motion blur filters](https://en.wikipedia.org/wiki/Motion_blur): one horizontal and the other one vertical.
Let us start with the vertical one (lines 60-62):

??? example "Vertical motion blur"
    ```cpp hl_lines="60-62" linenums="1"
    --8<-- "cursed-fire/fire1.c"
    ```

A three-element ring buffer is all we need: no more copies of the screen buffer.
The code gives the following animation (I slowed down the video a bit to make it clearer):

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire1.mp4" type="video/mp4"></source></video>

Let us add the horizontal motion blur (lines 63-64), thus making it a box blur:

??? example "Box blur"
    ```cpp hl_lines="60-64" linenums="1"
    --8<-- "cursed-fire/fire2.c"
    ```
<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire2.mp4" type="video/mp4"></source></video>

The heat from a single pixel quickly spreads out quickly, so it becomes nearly invisible in my palette.
On the first iteration, the white pixel is surrounded by eight black pixels; on the second, all nine pixels have a value of 255/9 = 28, and so on:

```
iteration 1    iteration 2     iteration 3
              0  0  0  0 0    3  6  9  6 3
 0  0  0      0 28 28 28 0    6 12 18 12 6
 0 255 0      0 28 28 28 0    9 18 28 18 9
 0  0  0      0 28 28 28 0    6 12 18 12 6
              0  0  0  0 0    3  6  9  6 3
```

Here, I scattered sparks all over the screen, but in reality, the heat is coming directly from the fire.
Let us fix the code a bit to allow fire pixels to be generated on the bottom line only (lines 66-70):

??? example "Fire bed"
    ```cpp hl_lines="66-70" linenums="1"
    --8<-- "cursed-fire/fire3.c"
    ```

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire3.mp4" type="video/mp4"></source></video>

The air does not randomly ignite anymore, even if the animation becomes less interesting.
In fact, we forgot about convection!
Let us just scroll the previous frame up one line at each step (lines 60-63):

??? example "Convection"
    ```cpp hl_lines="60-62" linenums="1"
    --8<-- "cursed-fire/fire4.c"
    ```

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire4.mp4" type="video/mp4"></source></video>


That looks much more like it!
But our campfire should have embers: sparks usually don't come out of nowhere.
Let us paint the ember bed a permanent color (and thus add heat) to the bottom line of the picture (lines 74-75):

??? example "Ember bed"
    ```cpp hl_lines="74-75" linenums="1"
    --8<-- "cursed-fire/fire5.c"
    ```

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire5.mp4" type="video/mp4"></source></video>

That's almost it, but we have too much heat, don't you think?
Let us add a cooling effect as a final touch (lines 70-72):

??? example "Cooling"
    ```cpp hl_lines="70-72" linenums="1"
    --8<-- "cursed-fire/fire6.c"
    ```

<video width="320" autoplay="" loop="" muted="" controls=""><source src="fire6.mp4" type="video/mp4"></source></video>


Well, that's it, I am happy with the result.
The mundane, non-cursed flame is lit.
I guess we're ready to start translating the code to *wend*, right?
Get ready a machina just around the corner, deus ex parked it for me.

## Deus ex machina
The attentive reader might have noticed that in this demo, I have used the `fire[]` buffer to render the animation,
but my *wend* language doesn't have arrays!
It is impossible to compute colors for each pixel independently, because the heat dissipation (and convection, too) requires knowledge of the state of neighboring pixels.
No worries, *wend* has functions.
Let us imagine that I need an 8-element array.
We can emulate it using eight different variables and two functions, the getter/setter pair:

```cpp
uint8_t fire0, fire1, fire2, fire3, fire4, fire5, fire6, fire7;

uint8_t get_fire(int i) {
    if (i==0) return fire0;
    if (i==1) return fire1;
    if (i==2) return fire2;
    if (i==3) return fire3;
    if (i==4) return fire4;
    if (i==5) return fire5;
    if (i==6) return fire6;
    if (i==7) return fire7;
}

void set_fire(int i, uint8_t v) {
  [...]
}
```

I omit the setter function because it's structurally similar to the getter.
The code seems trivial, but I have just made a linked list instead of an array.
To get to the 2'000th element, I'll have to do 2'000 comparisons.
It does not really matter, but I dislike it.
We can use a dichotomy to convert linear complexity to logarithmic.

```cpp
uint8_t get_fire(int i) {
    if (i<4) {
        if (i<2) {
            if (i<1) {
                return fire0;
            } else {
                return fire1;
            }
        } else {
            if (i<3) {
                return fire2;
            } else {
                return fire3;
            }
        }
    } else {
        if (i<6) {
            if (i<5) {
                return fire4;
            } else {
                return fire5;
            }
        } else {
            if (i<7) {
                return fire6;
            } else {
                return fire7;
            }
        }
    }
}
```

That's better.
This very code pushes me to write the article.
My terminal is 80x25, so I need 2'000 memory cells.
2'048 is very close to 2'000, and it's an exact power of two.
So, I get a minimal overhead and don't have to puzzle over about boundary conditions — I can just write a fully-balanced binary search tree.

I could have taken any programming language and generated the right text line.
However, I don't know why, but I decided to write a simple `#define` switch in the source code of fire.
This `#define` might switch between a base array and an emulated array: it would have been an easy way to make sure I didn't mess up anywhere.

I have asked myself: can this function be created using the C preprocessor?
To do that, I'd have to write a recursive `#define`.
Is it possible to do this, and if so, how? Of course, I started googling the question.
And I accidentally stumbled upon a [curious thread](https://cplusplus.com/forum/general/9036/) on cplusplus.com, I have even screenshoted it.

??? quote "Screenshot"
    ![](cursed-fire/forum.png)

Someone asked the same question I did. In response, he was told three times that the `#define` recursion was impossible. Mwahaha!
Keep in mind that I'm not the smartest person in the room.
I just found the [right URL](https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms) on Stack Overflow and only tried to sum up what I have learned.

## How C preprocessor works, or why macros aren't functions

Let us dig into how the C preprocessor works.
In the above code (bonfire), we have already encountered the `#define WIDTH 80`.
This is quite a standard case to define constants.

By the way, don't do this in C++, `constexpr` is a better option!
Define macros have many unpleasant moments, which can be removed with `constexpr`.
When the lexer encounters the `WIDTH` token, it replaces it with 80 before running the compiler.
Macros can also look function-like.
For example, the famous `#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))` macro.
Note: don't do it like that! In the third decade of the 21st century, I don't see any reason to continue using code from the 70s.

The "execution," or rather the expansion of macro commands, is purely textual.
The preprocessor doesn't understand the C language.
So, if you give it `MIN(habracadabra, circ][(beg+++))`, it'll happily convert it to `(((habracadabra) < (circ][(beg+++))) ? (habracadabra) : (circ][(beg+++)`! Check it yourself with `gcc -E source.c`.

When we want to use a function-like macro command, and we see the similar syntax, most programmers assume that it behaves like a function too.
It is tempting to think that first we evaluate the arguments and then pass them to the body of the parent macro command.
Nope.
The preprocessor isn't the C language, and macros don't behave that way, and the `MIN(habracadabra, circ][(beg+++))` example is proof of that.

Let me list macro expansion rules in the order in which they're executed:

* casting to string (there's no the `#` operator in the article);
* substituting arguments for parameter names (without expanding the tokens);
* token concatenation (there are numerous `##` operators in the article);
* expanding parameter tokens;
* rescanning and expanding the result.

## These are dark times, or the time has come for the black magic

Let us check the simplest example of tail recursion (in C):
```
void recursion(int d) {
    printf("%d ", d);
    if (d!=0) recursion(d - 1);
}
```

If we call `recursion(3)`, we'll see `3 2 1 0` in the terminal.
We need to learn how to do something like that using macros only.
OK, let us go through the ingredients one by one, starting with the simplest and working our way up.
We need to know:

* how to decrement;
* how to do conditional branching;
* how to test a numeric value for zero;
* how to make a recursive call.

### Decrement
Let us start with the first item, how to decrement.
The preprocessor is pretty dumb, it just does find-and-replace in the source code.
This may be annoying, but it also allows you to manipulate parts of expressions if you want to, so, it makes a certain sense.
The preprocessor doesn't know anything about arithmetics.
It just makes text substitutions, making things a bit tricky.
Let us make the first try:

```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define DEC(n) n - 1

DEC(3)
'
3 - 1
```

For better readability, I am running GCC directly from the command line, so you can see both the source code and the preprocessor output side-by-side.
So, the `DEC(3)` macro command doesn't expand into the desired constant, `2`, but rather into the `3-1` expression.
It is not a problem if we are creative enough. Here comes the token concatenation:


```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define DEC(n) DEC_##n
#define DEC_0 0
#define DEC_1 0
#define DEC_2 1
#define DEC_3 2

DEC(3)
DEC(DEC(3))
'
2
DEC_DEC(3)
```

Upon expansion of `DEC(3)`, the `DEC_` and `3` tokens are merged, and a new `DEC_3` token is generated, and this one expands to `2`.
Just what we needed!
There is one problem, though: the trick doesn't work with `DEC(DEC(3))`.
Why is that? Let us check the rules of macro expansion.
Concatenation occurs prior to parameters expansion, so the code actually doesn't do what it looks like at first glance:
we merge the `DEC_` token with the non-expanded text of the `DEC(3)` parameter, and that's where it stops working.
No biggies, it's not too hard to help here: we can defer the concatenation by pushing it one level deeper:


```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define CONCAT(a,b) a##b

#define DEC(n) CONCAT(DEC_,n)
#define DEC_0 0
#define DEC_1 0
#define DEC_2 1
#define DEC_3 2

DEC(3)
DEC(DEC(3))
DEC(DEC(DEC(3)))
'
2
1
0
```

I declare `CONCAT`, the macro command to merge two tokens, and all problems disappear: decrement operates fine using numeric constants, not expressions.
Note: I can't decrement, for example, 4 in this code.
It's fair to ask whether it is reasonable to define a macro command for each numeric value.
Short answer: forget about reason when programming only with lexer without a parser!
The detailed answer: in this case, the decrement is based on the depth of recursion.
It seldom goes over a dozen or two levels.

### Conditional branching

So, we have learned the most important thing: now we can create new tokens by merging, and we can use these tokens as names for other macro commands!
In such a case, branching is a piece of cake.
Let us take a look at the following code:

```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define CONCAT(a,b) a##b

#define IF_ELSE(b) CONCAT(IF_,b)
#define IF_0(i) ELSE_0
#define IF_1(i) i ELSE_1
#define ELSE_0(e) e
#define ELSE_1(e)

IF_ELSE(1)(then body)(else body)
IF_ELSE(0)(then body)(else body)
'
then body
else body
```

`IF_ELSE` is a macro command that takes only 0 or 1 as an argument and generates either the `IF_0` token or the `IF_1` token using trivial concatenation.
`IF_0` is a command that generates the `ELSE_0` token, and discarding its own arguments along the way.
`ELSE_0` is just an identity map.
Let us follow the whole chain of expanding `IF_ELSE(0)(then body)(else body)`:

```cpp
IF_ELSE(0)(then body)(else body)
IF_0(then body)(else body)
ELSE_0(else body)
(else body)
```

The expansion with the 1 as argument is pretty similar.

### Check for zero

Now you, seasoned metaprogrammers, won't be scared of a simple null check :)

```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define SECOND(a, b, ...) b
#define TEST(...) SECOND(__VA_ARGS__, 0)
#define ISZERO(n) TEST(ISZERO_ ## n)
#define ISZERO_0 TRASH, 1

ISZERO(0)
ISZERO(3)
'
1
0
```

Let us get into it.
When we expand `ISZERO(n)`, the first thing we do (again, look at the expansion rule order) is concatenation.
In this example, I expand `ISZERO(0)` and `ISZERO(3)` macros.
Let us follow the expansion path for `ISZERO(3)` first.
`ISZERO_3` is expanded to `TEST(ISZERO_3)`, which, in its turn, is expanded to `SECOND(ISZERO_3, 0)`, and it terminates in `0` constant,
since `SECOND(a, b, ...)` is a variadic macro returning its second parameter.

Now let us follow the expansion path for `ISZERO(0)`.
It turns out that it is expanded to `TEST(ISZERO_0)`, where `ISZERO_0` is the name of an already existing macro command!
Then it expands to a list of `SECOND(TRASH,1,0)`, and finally to `1`.

This is the key idea: to get something with a comma to the arguments of `SECOND`, we should pass zero to the `ISZERO` command.

### Recursion

If you have defeated the zero test, it means that only the sky is the limit for you.
Let us make the last step.

It's very important to know that all substitutions in macros happen during the lexing phase **PRIOR** to parsing.
The general idea is that it's up to the parser to handle recursions (hello, Turing completeness in templates).
The creators of the C lexer made significant efforts **to prevent recursive calls**.
This is necessary to avoid infinite loops during macro expansion.
Let us take a look at the following piece of code:

```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define FOO F BAR
#define BAR B FOO

FOO
BAR
'
F B FOO
B F BAR
```

It works like this: the preprocessor knows which macros it expands.
If it detects one of the macros again at the expanding stage, it [paints it blue](https://en.wikipedia.org/wiki/Painted_blue) and leaves it as it is.
Let us suppose we want to expand the `FOO` token.
The preprocessor enters the "expanding `FOO`" state, processes the `F` token.
However, when it expands the `BAR` macro, it encounters the `FOO` token again and immediately paints it blue, thus banning further expansion.
It's pretty much the same story when we expand the `BAR` macro, and, therefore, instead of infinite recursion we obtain just one iteration.

Now let us add few parentheses:
```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define FOO() F BAR
#define BAR() B FOO

FOO()()()()()()()()()
'
F B F B F B F B F BAR
```

Interesting and curious.
What happened? Something pretty interesting happened: we expanded the `FOO` macro command to a command with parameters.
Let us go through two levels of recursion:

```cpp hl_lines="3"
FOO()()()()()()()()()
F BAR()()()()()()()()
F B FOO()()()()()()() <- here FOO is not painted blue!
```

When we encounter `FOO` for the second time, the lexer does not recognize it because the lexer generated the `FOO` token **without parameters**.
That is the end of the `FOO` handling.
Then the lexer rescans the string, detects the brackets, and calls `FOO` for the second time.
And then a third time.
A fourth time.
I am feeling lucky!
Let me remind you that a direct call to `FOO()` inside `BAR` doesn't work.
We should stop the context of an expanding macro command **before** we encounter the same macro command token with parameters.
And, as it turns out, it's not a hard thing to do.
First, let us add an empty macro command, `EMPTY()`:

```cpp
ssloy@home:~$ gcc -P -E - <<<'
#define EMPTY()
#define FOO() F BAR EMPTY() ()
#define BAR() B FOO EMPTY() ()

FOO()

#define EVAL(x) x
EVAL(FOO())
EVAL(EVAL(FOO()))
EVAL(EVAL(EVAL(FOO())))
EVAL(EVAL(EVAL(EVAL(FOO()))))
'
F BAR ()
F B FOO ()
F B F BAR ()
F B F B FOO ()
F B F B F BAR ()
```

Now, upon expansion of `FOO()`, the lexer creates the `F` token and the `BAR` token that don't match the name of the `BAR()` macro command.
Then the lexer handles the empty token and leaves the brackets `()` as is.
That's it, the `FOO()` context is finished, and nothing has been painted blue.
However, `FOO()` expands to a rather boring `F BAR ()`, just like before.
What do we get? Look further down the code.
I define the identity macro command `#define EVAL(x) x`, and the `EVAL(FOO())` recursion becomes much more interesting.
Let us follow the whole chain (refresh your memory of the expansion rules, especially the last one):

```cpp
EVAL(FOO()) <- start EVAL context
FOO()       <- at this stage, we start expansion of the EVAL parameters
F BAR ()    <- the single EVAL parameter is expanded
F B FOO ()  <- RESCAN after EVAL parameters have been expanded!</code></pre>
```

Well, that's about it.
After wrapping it up in two `EVAL`s, we're done here.
In general, we need about as many `EVAL` wrappers as there are levels of recursion.
This can be provided with just a few lines of code.

Let us put it all together.
Here is the reference C program that we want to mimick with `#define` recursion:

```cpp
ssloy@home:~$ gcc -xc - <<<'
#include <stdio.h>
void foo(int d) {
    printf("%d ", d);
    if (d!=0) foo(d - 1);
}
int main() {
    foo(3);
    return 0;
}
' && ./a.out
3 2 1 0 ssloy@home:~$
```

No problem at all, we can do that! Here are just copy-pasted code snippets we saw before.
We have to be careful with another level of delay on line 28.
The `BAR` token is generated inside the branching instruction, so we need to wait for one more iteration of `EVAL` to ensure that `BAR` isn't painted blue.

```cpp hl_lines="28" linenums="1"
ssloy@home:~$ gcc -xc - <<<'
#include <stdio.h>

#define CONCAT(a,b) a##b

#define DEC(n) CONCAT(DEC_,n)
#define DEC_0 0
#define DEC_1 0
#define DEC_2 1
#define DEC_3 2

#define IF_ELSE(b) CONCAT(IF_,b)
#define IF_0(i) ELSE_0
#define IF_1(i) i ELSE_1
#define ELSE_0(e) e
#define ELSE_1(e)

#define SECOND(a, b, ...) b
#define TEST(...) SECOND(__VA_ARGS__, 0)
#define ISZERO(n) TEST(ISZERO_ ## n)
#define ISZERO_0 TRASH, 1

#define EMPTY()
#define FOO(d) \
    printf("%d ", d); \
    IF_ELSE(ISZERO(d)) \
    ( ) \
    ( BAR EMPTY EMPTY() () (DEC(d)) )
#define BAR(d) FOO EMPTY() (d)

#define EVAL(x)  EVAL1(EVAL1(EVAL1(x)))
#define EVAL1(x) EVAL2(EVAL2(EVAL2(x)))
#define EVAL2(x) EVAL3(EVAL3(EVAL3(x)))
#define EVAL3(x) x

int main() {
    EVAL(FOO(3))
    return 0;
}
' && ./a.out
3 2 1 0 ssloy@home:~$
```
## Cursed fire

Here is the complete source file for the cursed fire.

??? example "Cursed fire"
    ```cpp hl_lines="80-88" linenums="1"
    --8<-- "cursed-fire/fire_cursed.c"
    ```
As I promised, the entire frame buffer is stored in separate variables; there are no arrays!
If you look at the lines 80-88, for example (highlighted in the code), those generate the variables.
By running `gcc -E` on the source file, this portion generates the 2048 variables just as expected:

??? example "Preprocessed variables"
    ```cpp linenums="1"
    --8<-- "cursed-fire/fire_cursed_variables.c"
    ```


## Is the C preprocessor Turing complete?
The term "Turing complete" most often means that any real general-purpose computer or computer language can approximately simulate the computational aspects of any other real general-purpose computer or computer language.
No real system can have infinite memory, but if we neglect the memory limitation, most programming languages are otherwise Turing complete.
Not only the preprocessor memory is limited, but also the number of token rescanning levels (which we set with `EVAL`).
However, it's just a form of memory limitation, so the preprocessor is quite Turing complete.

After I wrote this article, I have found another link to a [project](https://github.com/Hirrolot/metalang99),
where devs have created a full-blown programming metalanguage on `#define` macros.
Unfortunately, it's too complex for the introduction to the b1ack magic of the C preprocessor.
Above tricks might still go into prod, but metalang99's tricks - I doubt it :)

## Bonus level

Modern optimizing compilers may be the most complex and impressive creation of humanity in the field of software engineering.
However, they are not magic.
An ordinary human brain will tell in a few seconds what the below very trivial code should be compiled into, but GCC will need many exabytes of memory and many years to give the answer.

??? example "GCC memory bomb"
    ```cpp
    #define X1(x) X2(x)+X2(x)
    #define X2(x) X3(x)+X3(x)
    #define X3(x) X4(x)+X4(x)
    #define X4(x) X5(x)+X5(x)
    #define X5(x) X6(x)+X6(x)
    #define X6(x) X7(x)+X7(x)
    #define X7(x) X8(x)+X8(x)
    #define X8(x) X9(x)+X9(x)
    #define X9(x) X10(x)+X10(x)
    #define X10(x) X11(x)+X11(x)
    #define X11(x) X12(x)+X12(x)
    #define X12(x) X13(x)+X13(x)
    #define X13(x) X14(x)+X14(x)
    #define X14(x) X15(x)+X15(x)
    #define X15(x) X16(x)+X16(x)
    #define X16(x) X17(x)+X17(x)
    #define X17(x) X18(x)+X18(x)
    #define X18(x) X19(x)+X19(x)
    #define X19(x) X20(x)+X20(x)
    #define X20(x) X21(x)+X21(x)
    #define X21(x) X22(x)+X22(x)
    #define X22(x) X23(x)+X23(x)
    #define X23(x) X24(x)+X24(x)
    #define X24(x) X25(x)+X25(x)
    #define X25(x) X26(x)+X26(x)
    #define X26(x) X27(x)+X27(x)
    #define X27(x) X28(x)+X28(x)
    #define X28(x) X29(x)+X29(x)
    #define X29(x) X30(x)+X30(x)
    #define X30(x) X31(x)+X31(x)
    #define X31(x) X32(x)+X32(x)
    #define X32(x) X33(x)+X33(x)
    #define X33(x) X34(x)+X34(x)
    #define X34(x) X35(x)+X35(x)
    #define X35(x) X36(x)+X36(x)
    #define X36(x) X37(x)+X37(x)
    #define X37(x) X38(x)+X38(x)
    #define X38(x) X39(x)+X39(x)
    #define X39(x) X40(x)+X40(x)
    #define X40(x) X41(x)+X41(x)
    #define X41(x) X42(x)+X42(x)
    #define X42(x) X43(x)+X43(x)
    #define X43(x) X44(x)+X44(x)
    #define X44(x) X45(x)+X45(x)
    #define X45(x) X46(x)+X46(x)
    #define X46(x) X47(x)+X47(x)
    #define X47(x) X48(x)+X48(x)
    #define X48(x) X49(x)+X49(x)
    #define X49(x) X50(x)+X50(x)
    #define X50(x) X51(x)+X51(x)
    #define X51(x) X52(x)+X52(x)
    #define X52(x) X53(x)+X53(x)
    #define X53(x) X54(x)+X54(x)
    #define X54(x) X55(x)+X55(x)
    #define X55(x) X56(x)+X56(x)
    #define X56(x) X57(x)+X57(x)
    #define X57(x) X58(x)+X58(x)
    #define X58(x) X59(x)+X59(x)
    #define X59(x) X60(x)+X60(x)
    #define X60(x) X61(x)+X61(x)
    #define X61(x) X62(x)+X62(x)
    #define X62(x) X63(x)+X63(x)
    #define X63(x) X64(x)+X64(x)
    #define X64(x) x+x

    int main() {
      return X1(0);
    }
    ```

