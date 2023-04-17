import sys, os
import signal
import subprocess
import ctypes
from Rosmaster_Lib import Rosmaster
import asyncio
import websockets

def run_command(command_to_execute):
    process = subprocess.Popen(command_to_execute, shell=True, preexec_fn=os.setsid)
    return process

def stop_command(process):
    if process:
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        return_code = process.wait()
        print(f"Process terminated with return code {return_code}")

# Create the Rosmaster object bot
bot = Rosmaster()

def calculate_motion(degree):
    if -5 < degree < 5:
        return 0.0
    else:
        return max(min(degree / 40.0 * 0.3, 0.3), -0.3)

processes = {
    "following": None,
    "avoiding": None,
    "guard": None,
}

async def process_messages(websocket, path):
    await websocket.send("Connected")

    async for message in websocket:
        if message == "start_following":
            processes["following"] = run_command("roslaunch yahboomcar_laser laser_Tracker.launch")
        elif message == "stop_following":
            stop_command(processes["following"])
            processes["following"] = None
        elif message == "start_avoiding":
            processes["avoiding"] = run_command("roslaunch yahboomcar_laser laser_Avoidance.launch")
        elif message == "stop_avoiding":
            stop_command(processes["avoiding"])
            processes["avoiding"] = None
        elif message == "start_guard":
            processes["guard"] = run_command("roslaunch yahboomcar_laser laser_Warning.launch")
        elif message == "stop_guard":
            stop_command(processes["guard"])
            processes["guard"] = None
        else:
            degree_lr, degree_fb = map(int, message.split(','))
            x = -calculate_motion(degree_fb)
            y = -calculate_motion(degree_lr)
            z = 0.0

            print(x,y)
            bot.set_car_motion(x, y, z)

start_server = websockets.serve(process_messages, "0.0.0.0", sys.argv[1])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
