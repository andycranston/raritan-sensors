# Raritan sensor utilities using the Python JSON-RPC API

Here are some utilities for managing sensors attached to
a Raritan intelligent PDU.  The PDU must be running a recent
version of the Xerus firmware, say at least 3.3.x or higher.

## movesensorslot.py

This utility moves a sensor from one 'slot' to another slot.  One use
for this is when you have several  racks with the same number and type of sensors positioned in identical places on the rack.
In order to keep things simple you want each sensor to have the same slot number across all the racks so, for example, the temperature sensor at the back of the rack is always in slot 4.

By using the `movesensorslot.py` utility you can move any sensors not in the expected slot to the correct slot.

See this document for more information:

(README-movesensorslot.md)

## settempthresholds.py

This utility changes the temperature thresholds on all temperature sensors
on a PDU to the thresholds specified.  The thresholds changed are:

+ Lower critical
+ Lower warning
+ Upper warning
+ Upper critical

This is useful if you have many temperature sensors and need to make
a bulk change to the thresholds.  For example equipment in a rack may
have been improved in a way that allows them to run perfectly safely a
few degrees hotter so you could use the `settempthresholds.py` utility
to set slightly higher thresholds.

See this document for more information:

(README-settempthresholds.md)

-----------------------------------------------------------

end of README.md
