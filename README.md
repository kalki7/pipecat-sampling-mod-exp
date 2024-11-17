# Websocket Server

This is an example that shows how to use `WebsocketServerTransport` to communicate with a web client.

## Get started

```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env # and add your credentials
```
## Working Web Demo folder has the working demo, run the following in there
## Run the bot

```bash
python app.py
```

## Run the HTTP server

This will host the static web client:

```bash
python -m http.server
```

Then, visit `http://localhost:8000` in your browser to start a session.
