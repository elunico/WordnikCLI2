# WordnikCLI2
A reimplementation of most of my WordnikCLI project to address some issues

The original program was a simple command-line tool for getting definitions for English words. I made it as sort of an
inspiration to man pages. I thought of it like man pages for English words.

I was unsatisfied with how I wrote the original version and it had some issues that I could not work out because
of the nature of how the program was put together. I took on a rewrite and ended up simplifying parts of it greatly
as well as eliminitating the issues it had.

The entire program was not, however, rewritten, as of yet. `define.py` was copied from the original project as the issues
were entirely around the `Screen` and `BufferedScreen` classes. `define.py` was modified to work with the new `Screen` class. I may
rewrite `define.py` soon but for now it works as is.... sort of.

## Issues
While I did resolve all the issues the original version was having, I unfortunately introduced a new one which is that
color does not work. I am working on a fix for this but that is still TBD.

## Notes
This program uses BeautifulSoup, the Wordnik API (currently does scraping, but API use will be used in the future), requests (for python) to give simple definitions for English words on the command line.
