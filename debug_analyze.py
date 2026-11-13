import traceback
from app import app

client = app.test_client()

lyrics_text = """
Out in the dark night sky
Underneath the shining light
Walking through the silent street
Listening to my heart beat
"""

try:
    response = client.post('/analyze', json={
        "title": "Midnight Dreams",
        "artist": "Demo Artist",
        "lyrics": lyrics_text
    })
    print("STATUS CODE:", response.status_code)
    print("DATA:", response.get_data(as_text=True))
except Exception as e:
    print("EXCEPTION OCCURRED:")
    traceback.print_exc()
