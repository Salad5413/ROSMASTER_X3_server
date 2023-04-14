import os
import signal
import subprocess
import time



command_to_execute = "roslaunch yahboomcar_laser laser_Warning.launch"

# Start the process with a new session
process = subprocess.Popen(command_to_execute, shell=True, preexec_fn=os.setsid)

# Run the process for a certain amount of time (e.g., 10 seconds)
time.sleep(20)

# Send the SIGINT signal (Ctrl+C) to the process group
os.killpg(os.getpgid(process.pid), signal.SIGINT)

# Wait for the process to finish and get the return code
return_code = process.wait()

print(f"Process terminated with return code {return_code}")
