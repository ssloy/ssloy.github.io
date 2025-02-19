# Assembly generation
## Introduction

This time we have reached a milestone: we will finally be generating assembly instead of python.
We covered working with the stack and registers, which cause the most problems for beginners in assembly, in the previous article, so this time there is very little left to do.
At this point, our compiler generates python code whose structure completely matches the desired assembly.
The only remaining task is to handle screen output, everything else is ready.

## Hello World, or printing strings to the screen

Most educational compilers choose MIPS assembly, but I don't like running code in an emulator, so I chose x86 GNU assembly, which comes with gcc, without much thought.
I can't say exactly why, but I wanted the 32-bit version.
For our purposes, it is not necessary to be an assembly guru, but we need to be able to write programs at the "Hello World" level.

Let's create a template that we will build upon.
Imagine we have a file [helloworld.s](assembly/helloworld.s) with the following content:

```asm linenums="1"
--8<-- "assembly/helloworld.s"
```

Then we can compile it using the `as` and `ld` commands as follows:

```
as --march=i386 --32 -o helloworld.o helloworld.s &&
ld -m elf_i386 helloworld.o -o helloworld &&
./helloworld
```

If everything went well, you should see a proud greeting on the screen.
Now let's understand what is happening there.
There are only two system calls — `sys_write` and `sys_exit`.
In C, the same thing could be written as follows:

```cpp
#include <sys/syscall.h>
#include <unistd.h>

int main(void) {
        syscall(SYS_write, 1, "hello world\n", 12);
        return 0;
}
```

If the stars align correctly, gcc will generate approximately the same assembly code.
For our needs, no other system calls are required; `write` and `exit` are more than enough, as the only interaction with the outside world in *wend* is screen output.

*Wend* does not perform any string operations, only printing constant strings to the screen, so my compiler creates a unique identifier for each string in the header just like for our hello world.
For printing boolean values, two constant strings `"true"` and `"false"` are used.
What about numbers? Well, here we need to do a bit of work.
I'm lazy and didn't want to deal with linking glibc and the like, so the luxury of `printf` is unavailable to me.
No problem, `sys_write` is more than enough!

## Printing decimal numbers

`sys_write` can print strings to the screen, so we need to learn how to convert numbers (I only have signed 32-bit numbers) to string representation.
For this, I rolled up my sleeves and wrote the function [`print_int32`](assembly/print_int32.s):


```asm linenums="1"
--8<-- "assembly/print_int32.s"
```


Reading someone else's assembly code is not easy, so let me provide the [python equivalent](assembly/print_int32.py) of our function:

```py linenums="1"
--8<-- "assembly/print_int32.py"
```

I am calling `write` only once, so we need to prepare a string buffer.
A 32-bit number will not require more than 11 characters, so I allocate 16 for the buffer (to align the stack to the edge of the machine word).
Then I convert the absolute value of the given number to a string, and finally attach a minus if the number was negative.

This way, we can print strings and numbers to the screen, and notably, without the headache of linking with some 32-bit version of libc on a 64-bit system.

This code allows to compile the `print` statement of our language, but in addition to that, it is handy for debugging.
GDB is for the faint-hearted; inserting print statements everywhere is our thing ;)

## Putting it all together
Well, that's about it.
Now, we take the python code generation template, and instead of outputting python's `print()`, we simply write `call print_int32`, and instead of `eax = eax * ebx`, we write `imull %ebx, %eax`.
Thus, we gradually translate python instructions into assembly, and we're done! No subtleties left, the long-awaited compiler is almost ready.
You can take [release v0.0.5](https://github.com/ssloy/tinycompiler/releases/tag/v0.0.5) and play with it.

The intermediate goal has been achieved: we have learned to compile our own language into real x86 GNU assembly.
At the moment, I am using the external library sly for parsing, but along the way, I found out that writing your own parser is not difficult at all.
And at the same time, we can tweak the grammar of the language to make it more pleasant!

The next two articles will be about how to create a lexer and parser yourself, [the ready code is already in the repository](https://github.com/ssloy/tinycompiler).

--8<-- "comments.html"
