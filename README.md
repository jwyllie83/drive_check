# drive_check

`drive_check` is a quick tool I wrote when I couldn't find anything that quite met my needs for verifying that a hard drive had a finishing wipe applied property to it.  Most hard drive tools, like [dban](https://sourceforge.net/projects/dban/), will finish with a zero-byte wipe over the whole drive.  This can verify that, indeed, all of the bytes are zeroed out that are readalbe.

# Warning

So, *this won't verify that your drive can't have data pulled off of it, even if wiped with all zeroes!* I know there are lots of papers out there about reading data off of a drive when the bytes are overwritten.  Your comfort-level using a tool to wipe your drive and then giving it to a stranger is personal and will vary depending on lots of factors, including but not limited to the actual data your drive was holding.  This just verifies that it's been zero'd out.  Furthermore, I didn't do any _serious_ functional testing, just the usual basic stuff.

# Requirements

`drive_check` requires the following non-standard Python modules:

* `tqdm` for a progress bar, [available on pypi](https://pypi.python.org/pypi/tqdm)

# Using drive_check

Running:

    drive_check -h

will show you all of the options.
