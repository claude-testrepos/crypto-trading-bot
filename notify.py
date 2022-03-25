"""Send a message to a Discord channel via webhook (DISCORD_WEBHOOK_URL)."""
import json
import os
import urllib.request


def notify(text: str) -> None:
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        return
    req = urllib.request.Request(
        url,
        data=json.dumps({"content": text}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "paper-bot"},
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except OSError as e:
        print(f"discord notify failed: {e}")
