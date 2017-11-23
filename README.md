## til-cli

A simple command-line interface to make it easy for me to publish new entries to my database of things that I learned. I tried to make the flow similar to how git commit/push works.

## Quick Overview

I've always wanted to keep track of things that I learn throughout the day while programming, but I never want to log in somewhere and write about it in the moment. I made this CLI so that I could just do it easily right from the terminal. How it works:

1. *Wow, I just learned something so great and new...*
2. `til -p`
3. Now my editor of choice is open and I can write what I just learned.
4. After I save and exit the editor, a POST is made on a server where it gets published.

## Development Environment Setup

Create a virtual environment and install the required packages, which are found in `package.txt`.

```
pip install -r requirements.txt
```

You can use Pyinstaller to create an executable for distribution:

```
pyinstaller --onefile client.py --name til
```

## Download & Installation

Download the latest release [here](https://github.com/denvaar/til-cli/releases)


