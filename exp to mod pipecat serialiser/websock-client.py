import asyncio
import websockets
import json

# Define the WebSocket server URL
WEBSOCKET_SERVER_URL = "ws://127.0.0.1:5000"  # Replace with your server URL

# Define the JSON payload
payload = {
    "type": "media",
    "ucid": "111XXXXXXXX71",
    "data": {
        "samples": [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        "bitsPerSample": 16,
        "sampleRate": 8000,
        "channelCount": 1,
        "numberOfFrames": 80,
        "type": "data"
    }
}

async def send_data():
    # Establish the WebSocket connection
    async with websockets.connect(WEBSOCKET_SERVER_URL) as websocket:
        # Send the JSON payload
        # await websocket.send(json.dumps(payload))
        # print("Data sent to server.")

        # Wait for a response (if needed)
        response = await websocket.recv()
        print("Response from server:", response)

# Run the WebSocket client
asyncio.run(send_data())
