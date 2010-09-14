# FrameNet in Python

I'm now maintaining [Patrick Ye](http://ww2.cs.mu.oz.au/~jingy/)'s Python library for accessing [FrameNet](http://framenet.icsi.berkeley.edu/) data. This version works with FrameNet version 1.3.

## Getting Started

First you must obtain and install the FrameNet XML files, which are free for non-commerical and require an application.  Then, you can obtain the Python Library and run:

    python setup.py build
    sudo python setup.py install

Second, you should set your `FRAMENET_HOME` environment variable to point to where you installed and uncompressed FrameNet's XML files.  (Alternatively you can edit the `FRAMENET_PATH` constant in `framenet/settings.py`).

Then you can test your installation by running `python test/importer.py` or opening a Python shell and typing:

    import framenet
    fn = framenet.FrameNet()

The first time you instantiate the **FrameNet** class, it will parse *all* of the XML files and save pickle objects.   This takes a while, so go have a coffee or celebrate your next birthday.  You should see:

    Loading the frames ... Framenet not initialized, doing it now
    Loading xml for frames ...

# Common Functions


## FrameNet.lookupLexicalUnit(text, part_of_speech)

You can look up frames by the **lexical units** (e.g., words) and their parts of speech.  For example:

    buy = fn.lookupLexicalUnit('buy','v')

## FrameNet.lookupFrame(frame)

    commerce_frame = fn.lookupFrame('Commerce_buy')



