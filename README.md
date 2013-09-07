GameMonkey Lint
=======

[GameMonkey](http://gmscript.com) lint plugin for [Sublime Text 3](http://www.sublimetext.com/3).

Basically, **GameMonkey Lint** listens to when you save a GameMonkey file (.gm) in Sublime Text. When the file is saved, it compiles the file immediately; if the compilation fails, it instantly jumps to the errorneous line.

You can see the exact compile error if you open the Sublime Text console.

Currently works only on PC


Installation
---
You can install **GameMonkey Lint** by going to your packages directory and cloning this repro. 

*Step 1 - Go to Package Directory*

![Packages Dir](http://i.imgur.com/jxQeGdQ.png)


*Step 2 - Clone gm-lint into this directory*

![Directory](http://i.imgur.com/H5zhPHV.png)


Now, it should work. Note tha gm-lint uses an executable, so if you are using cygwin or whatever for git, there might be some issues with file permissions on executable, in that case, you might need to change the permission on the **GmByteCodeGen.exe**
