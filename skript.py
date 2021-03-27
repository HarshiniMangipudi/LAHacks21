# { date +%H; echo 15; } | xargs -n 2 python3.7 skript.py
import argparse
import zmq

parser = argparse.ArgumentParser(description='Process hours')
parser.add_argument('hour', metavar='h', type=int, help='current hour')
parser.add_argument('min', metavar='m', type=int, help='current minute')
args = parser.parse_args()
currhr = args.hour
currmin = args.min
print(f"RECEIVED: {currhr} \tAS CURRENT HOUR")
print(f"RECEIVED: {currmin} \tAS CURRENT MINUTE")

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/server")
print("HI")
try:
    print("HI")
    socket.send_pyobj((currhr, currmin), flags=zmq.NOBLOCK)
except zmq.ZMError as e:
    print("HISDFSD")
    pass