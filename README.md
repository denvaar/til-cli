## til-cli

A simple command-line interface to make it easy for me to publish new entries to my database of things that I learned. I tried to make the flow similar to how git commit/push works.

## Quick Overview

I've always wanted to keep track of things that I learn throughout the day while programming, but I never want to log in somewhere and write about it in the moment. I made this CLI so that I could just do it easily right from the terminal. How it works:

1. **wow I just learned something so great and new**
2. `til -p`
3. Now my editor of choice is open and I can write what I just learned.
4. After I save and exit the editor, a POST is made on a server where it gets published.
