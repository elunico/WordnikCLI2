# WordnikCLI2
A re-implementation of most of my WordnikCLI project to address some issues

The original program was a simple command-line tool for getting definitions for English words. I made it as sort of an
inspiration to man pages. I thought of it like man pages for English words.

I was unsatisfied with how I wrote the original version and it had some issues that I could not work out because
of the nature of how the program was put together. I took on a rewrite and ended up simplifying parts of it greatly
as well as eliminating the issues it had.

The entire program was not, however, rewritten, as of yet. `define.py` was copied from the original project as the issues
were entirely around the `Screen` and `BufferedScreen` classes. `define.py` was modified to work with the new `Screen` class. I cleaned up `define.py` enough that I do not think it needs to be rewritten. Similarly, `web.py` is a small file and was taken as is, but types were added.

## Notes
 * This program uses BeautifulSoup, the Wordnik API (currently does scraping, but API use will be used in the future), requests (for python) to give simple definitions for English words on the command line.

 * You can customize the colors of the interface by modifying colors.json as you please

## Examples

`./define.py happy`

![Alt Text](/images/define-happy.png "A screenshot of the program showing the prompt for define happy")
![Alt Text](/images/defs-happy-1.png "A screenshot of the program showing definitions of happy")
![Alt Text](/images/defs-happy-3.png "A screenshot of the program showing definitions of happy")

`./define.py alabaster`

![Alt Text](/images/define-alabaster.png "A screenshot of the program showing the prompt for define alabaster")
![Alt Text](/images/defs-alabaster-1.png "A screenshot of the program showing definitions of alabaster")

`./define.py akshun`

![Alt Text](/images/define-akshun.png "A screenshot of the program showing the prompt for define a non-existent word")
![Alt Text](/images/defs-akshun-1.png "A screenshot of the program showing definitions of a non-existent word")
