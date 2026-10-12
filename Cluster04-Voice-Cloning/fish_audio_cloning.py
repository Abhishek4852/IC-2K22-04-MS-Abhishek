import os
import requests
from dotenv import load_dotenv


def get_validated_text(prompt="\nEnter the text you want the AI to speak:\n> "):
    """Validates user text input and re-prompts on invalid input."""
    while True:
        try:
            val = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            return None

        if not val or not any(c.isalnum() for c in val):
            print("❌ Invalid input! Please enter valid text.")
            continue

        return val


def get_validated_reference_id(prompt="\nEnter Voice Reference ID (press Enter for normal AI voice):\n> "):
    """Validates optional reference ID format and re-prompts on invalid input."""
    while True:
        try:
            val = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            return None

        # Empty means normal AI voice (valid)
        if not val:
            return ""

        # Validate reference ID: no spaces, alphanumeric with hyphens/underscores
        clean_id = val.replace("-", "").replace("_", "")
        if " " in val or not clean_id.isalnum():
            print("❌ Invalid input! Please enter a valid Voice Reference ID (or press Enter for normal AI voice).")
            continue

        return val


def main():

    print("=" * 60)
    print("FISH AUDIO - FREE S2.1 PRO TTS")
    print("=" * 60)

    # Load .env
    load_dotenv()

    api_key = os.getenv("FISH_API_KEY")

    if not api_key:
        print("\n❌ FISH_API_KEY not found.")
        print("Create .env file:")
        print("FISH_API_KEY=your_api_key")
        return

    # Get text with validation
    text = get_validated_text()
    if text is None:
        return

    # Optional reference voice with validation
    reference_id = get_validated_reference_id()
    if reference_id is None:
        return

    # API
    url = "https://api.fish.audio/v1/tts"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",

        # IMPORTANT
        "model": "s2.1-pro-free"
    }

    body = {
        "text": text,
        "format": "mp3"
    }

    # Add cloned voice if provided
    if reference_id:
        body["reference_id"] = reference_id

    try:

        print("\n[Processing] Sending request...")
        print("Model: s2.1-pro-free")

        response = requests.post(
            url,
            headers=headers,
            json=body
        )

        # Error handling
        if not response.ok:

            print("\n❌ API Error")
            print("Status:", response.status_code)
            print("Message:", response.text)

            return

        # Save audio
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(output_dir, "fish_audio_output.mp3")

        with open(output_file, "wb") as f:
            f.write(response.content)

        print("\n✅ SUCCESS!")
        print("Audio saved as:")
        print(output_file)

    except Exception as e:

        print("\n❌ Error:")
        print(e)


if __name__ == "__main__":
    main()