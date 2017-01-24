#!/usr/bin/python
__author__ = 'Sergey Syrota'

# implements text based communication with home's RS-485 bus.
# Only one of these worked should be started to avoid collisions on the bus

import gearman
import serial
import daemon
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', help='Serial port path', default='/dev/ttyUSB0')
parser.add_argument('--speed', help='Baud rate for serial port', default=115200)
parser.add_argument('--timeout', help='How long (seconds) to wait for reply after sending a command to device',
                    required=False, default=2)
parser.add_argument('--gearman',
                    help='Gearman host to connect to (host:port)',
                    default='localhost:4730',
                    required=False)
args = parser.parse_args()


# sends a string to the bus, and returns the reply
def task_listener_rs485(gearman_worker, gearman_job):
    rs485 = serial.Serial(args.port, args.speed, timeout=args.timeout)
    rs485.write(gearman_job.data)
    res = rs485.readline()
    rs485.close()
    return res


gm_worker = gearman.GearmanWorker([args.gearman])
# gm_worker.set_client_id is optional
gm_worker.set_client_id('rs485-worker')
gm_worker.register_task('rs485', task_listener_rs485)

#Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
with daemon.DaemonContext():
    gm_worker.work()
