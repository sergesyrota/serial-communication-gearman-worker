# Half duplex communication daemon

This daemon facilitates serial communication over half duplex serial port. When multiple processes cannot talk to the port,
and one master with multiple slaves are deployed, this ensures you have only one thread that is making a request on serial
port or reading a reply from that port.

# Gearman

In this solution, Gearman is used to handle commands and communication between worker and server. Implementation only
covers the worker part. This has "exclusive" right to go to serial port, while all other applications need to queue
their commands in gearman and wait for reply.

# Requirements

 - Python with modules:
  - serial
  - gearman
  - daemon
 - Gearman

# Installation

Copy `serial-worker.py` to your folder of choice (e.g. /usr/bin). `chmod +x` the file.

See `contrib` folder for init scripts. This will ensure worker will start with system boot. If using local gearman, make
sure to specify dependency for gearman process, where supported.
