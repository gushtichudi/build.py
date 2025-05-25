# build.py
build.py is an experimental build system entirely written in Python.

it's partly inspired by tsoding's `nob`.

> [!WARNING]
> `build.py` is \_\_still\_\_ on constant development and as such,
> there are many features that are to be implemented in the future.
> this is yet very far from being an actual proper build system.

## usage
`build.py` is written to not depend on a motherlode of other Python files
(like my other (unfinished) [projects](https://www.github.com/gushtichudi/Barrels), please don't check the
rest of my GitHub).

to use `build.py` in a project, copy `build.py`, and write a `recipe.py` by `import`ing `build.py`.

a very small example is provided here.
```py
from build import Build

b = Build("program-name")

b.add_file(["main.c"])
b.add_compiler_arguments(["-static", "-nostdlib", "-ggdb"])

b.start_build()
```

more examples can be found in [examples](./examples/)

## bugs
  - (line 117): multiple file builds cannot be possible yet.
  - (line  87): when add_file()'s first parameter is put as a string, it will split the string into characters (lol)

## license
since this is not really a serious project of mine, i wouldn't fancy giving a license to this and as such, it's
basically in the Public Domain.
