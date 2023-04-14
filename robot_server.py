from Rosmaster_Lib import Rosmaster
# Create the Rosmaster object bot
bot = Rosmaster()

import asyncio
import websockets
import nest_asyncios

nest_asyncio.apply()  # Apply nested asyncio patch

def calculate_motion(degree):
    if -5 < degree < 5:
        return 0.0
    else:
        return max(min(degree / 40.0 * 0.3, 0.3), -0.3)

async def process_messages(websocket, path):
    # Send a confirmation message to the iOS app
    await websocket.send("Connected")

    async for message in websocket:
        degree_lr, degree_fb = map(int, message.split(','))
        #print(f"Degree LR: {degree_lr}, Degree FB: {degree_fb}")

        x = -calculate_motion(degree_fb)
        y = calculate_motion(degree_lr)
        z = 0.0

        #print(x, y)
        bot.set_car_motion(x, y, z)

start_server = websockets.serve(process_messages, "0.0.0.0", 7003)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
