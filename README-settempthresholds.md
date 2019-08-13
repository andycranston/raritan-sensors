# The settempthresholds.py utility

This utility sets the threshold values of all temperatore sensors on
a Raritan intelligent PDU.

This is a YouTube video showing the `settempthresholds.py` utility in
action:

[Setting Raritan PDU temperature sensor thresholds](https://youtu.be/N91bIJLmNAE)

You need to specify on the command line the `--host` argument and
give the name or IP address of the PDU.  You also need to specify the
`--temps` argument and give the four threshold values separated by commas.
For example:

```
python settempthresholds.py --host px2study --temps 15,18,22,25
```

will set the thresholds of all temperature sensors on PDU `px2study`
to 15,18,22 and 25.  Specifically:

+ The lower critical temperature will be set to 15
+ The lower warning temperature will be set to 18
+ The upper warning temperature will be set to 22
+ The upper critical temperature will be set to 25

NB: depending on your environment you may need to use:

```
python3 settempthresholds.py --host px2study --temps 15,18,22,25
```

as the `settempthresholds.py` utility is a Python 3 script.

Also you will need to set an environment variable to contain the password
for the `admin` user on the PDU.  By default the `settempthresholds.py`
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

For a better way to set environment variables with passwords you may
want to look at:

[Set Windows/UNIX/Linux environment variables with a password but keep the password hidden](https://github.com/andycranston/setpw)

If you want to use a different user name to login to the PDU use the
`--user` argument as follows:

```
python settempthresholds.py --host px2study --user localadm --temps 15,18,22,25
```

which will try and login as user `localadm`.

If you want to use a different environment variable with the password use
the `--envvar` argument as follows:

```
python settempthresholds.py --host px2study --envvar RARITANPASS --temps 15,18,22,25
```

which will use the environment variable `RARITANPASS`.

All this can be combined as:

```
python settempthresholds.py --host px2study --user localadm --envvar RARITANPASS --temps 15,18,22,25
```

The script will look at every sensor 'slot' on the PDU and when it
finds a temperature sensor it will change the thresholds.  If it
encounters a problem trying to change the thresholds the script will
give up.  The logic here is that if it cannot change the thresholds
on a temperature sensor it is likely it will not be able to change any
remaining temperature sensors for the same reason.

Here are some reasons why the script might not be able to change the
thresholds on a temperature sensor:

+ A threshold value is out of range (too high or too low)
+ Thresholds are too close together (e.g. 15,18,22.1,22.4 will not work)

---------------------------------------------------------------------

End of README-settempthresholds.md
