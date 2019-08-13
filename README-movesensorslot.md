# The movesensorslot.py utility

This utility moves a sensor on a Raritan intelligent PDU from one slot
to another.

This is a YouTube video showing the `movesensorslot.py` utility in
action:

[Moving Raritan sensors from one slot to another](https://www.youtube.com/watch?v=wy-pl4CY48s)

You need to specify on the command line the `--host` argument and give
the name or IP address of the PDU.  The next two command line arguments
are the sensor slot number to move and the slot number to move to.
For example:

```
python movesensorslot.py --host px2study 2 4
```

will move the sensor currently in slot 2 to slot 4 on the PDU called
`px2study`.

NB: depending on your environment you may need to use:

```
python3 movesensorslot.py --host px2study 2 4
```

as the `movesensorslot.py` utility is a Python 3 script.

Also you will need to set an environment variable to contain the password
for the `admin` user on the PDU.  By default the `movesensorslot.py`
utility will look for an environment variable called `PW`.  For example
if the `admin` password is still the factory default `raritan` then at
the Windows command prompt you would type:

```
set PW=raritan
```

On UNIX/Linux you would type:

```
PW=raritan
export PW
```

Make sure no one is looking over your shoulder when you do this and
do not leave your computer unattended once you have set the `PW`
environment variable!

For a better way to set environment variables with passwords you may want to look at:

[Set Windows/UNIX/Linux environment variables with a password but keep the password hidden](https://github.com/andycranston/setpw)

If you want to use a different user name to login to the PDU use the
`--user` argument as follows:

```
python movesensorslot.py --host px2study --user localadm 2 4
```

which will try and login as user `localadm`.

If you want to use a different environment variable with the password use
the `--envvar` argument as follows:

```
python movesensorslot.py --host px2study --envvar RARITANPASS 2 4
```

which will use the environment variable `RARITANPASS`.

All this can be combined as:

```
python movesensorslot.py --host px2study --user localadm --envvar RARITANPASS 2 4
```

The script does some basic error checking like checking the first
slot number does contain a sensor and the second slot number is empty.
This prevents a sensor for being accidently overwritten.

If you have two sensor slots you want to swap you will need to move
the first sensor to a free slot, then move the second sensor to the
first slot position and finally move the sensor now in the free slot
to the actual second slot.  An example makes this clearer.  Say I want
to swap the two sensors in slot 2 and 6.  I know that slot 32 is free.
I can do this by running the movesensorslot.py utility three times:

```
python movesensorslot.py --host px2study 2 32
python movesensorslot.py --host px2study 6 2
python movesensorslot.py --host px2study 32 6
```

---------------------------------------------------------------------

End of README-movesensorslot.md




