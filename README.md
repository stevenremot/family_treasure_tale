# The Family's treasure tale

Entry in [PyWeek #19](http://www.pyweek.org/19/)

URL: http://pyweek.org/e/family_treasure

Team: The Family's treasure tale

Members: Alexandre Kazmierowski, Steven Rémot

License: GPL v3, see LICENSE.txt

## Running the game

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

```sh
    python run_game.py
```

## How to play the game

You are the spirit of the room. The family living in your house got a
treasure, and hide it inside a "safe" place. Unfortunately, a burglar
decides to visit this house tonight.

As the spirit of the room, you can move some objects, and event change
the room's position in the house when no-one is inside. Do your best
to protect the treasure !

When you can interact with an object, the cursor's shape changes. If
clicking does not trigger anything, this means this could be done
later (or sooner) in the game.

## Development notes

Creating a source distribution with:

```sh
   python setup.py sdist
```

You can generate a Windows standalone executable using
[Pyinstaller](http://www.pyinstaller.org). Change the path in
`family_treasure.spec`, or follow the instructions in the developer
guide to create a new one.

Upload files to PyWeek with:

```sh
   python pyweek_upload.py
```

Upload to the Python Package Index with:

```sh
   python setup.py register
   python setup.py sdist upload
```

## Sounds attributions

- Window sound from Iwan "qubodup" [http://qubodup.net](http;//qubodup.net)
- Wind sound from Lanea Zimmerman
- THe other sounds belong to the public domain
