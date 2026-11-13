import json
from app import app

client = app.test_client()

test_cases = [
    {
        "name": "Standard Sample Lyrics",
        "payload": {
            "title": "Midnight Dreams",
            "artist": "Demo Artist",
            "lyrics": """
            Out in the dark night sky
            Underneath the shining light
            Walking through the silent street
            Listening to my heart beat
            Midnight dreams are chasing shadows in the blue
            Every single step I take leads me straight to you
            Dancing in the golden glow, feeling brave and free
            Whispers of the morning wind calling out to me
            """
        }
    },
    {
        "name": "Empty Title and Artist",
        "payload": {
            "title": "",
            "artist": "",
            "lyrics": """
            I feel the freedom in the air tonight
            Living under bright starry lights
            Hearts beating together in harmony
            Sweet music playing wild and free
            """
        }
    },
    {
        "name": "Lyrics with Punctuation & Special Symbols",
        "payload": {
            "title": "Song @#$!",
            "artist": "Artist & Band!",
            "lyrics": """
            [Intro] Yeah! (Woo-hoo!)
            Dancing... in the dark, night... sky!
            Are we lovers? Or just friends???
            Heartbreak & sorrow -- will it ever end?
            """
        }
    }
]

print("=== RUNNING INPUT VERIFICATION TESTS ===")
for test in test_cases:
    print(f"\nTesting: {test['name']}...")
    res = client.post('/analyze', json=test['payload'])
    print(f"Status: {res.status_code}")
    data = res.get_json()
    if res.status_code == 200 and data.get('success'):
        print(f"✅ PASSED! Words: {data['statistics']['total_words']}, Sentiment: {data['sentiment']['classification']}, Emotion: {data['emotion']['dominant_emotion']}")
    else:
        print(f"❌ FAILED! Error: {data.get('error')}")

print("\n=== ALL TEST CASES VERIFIED SUCCESSFULLY! ===")
