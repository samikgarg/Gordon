from cartesia import Cartesia
import os
import subprocess
import ffmpeg
import ssl
import certifi

def speak_transcript(transcript):

    print("***************")
    print(str(os.environ.get("CARTESIA_API_KEY")))
    client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    model_id = "sonic-english"

    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 44100,
    }

    ws = client.tts.websocket()

    # Open afile to write the raw PCM audio bytes to
    with open("sonic.pcm", "wb") as f:
        # Generate and stream audio
        for output in ws.send(
            model_id=model_id,
            transcript=transcript,
            voice_id=voice_id,
            stream=True,
            output_format=output_format,
        ):
            buffer = output["audio"]  # buffer contains raw PCM audio bytes
            f.write(buffer)

    # Close the connection to release resources
    ws.close()

    # Convert the raw PCM bytes to a WAV file
    ffmpeg.input("sonic.pcm", format="f32le").output("sonic.wav").run()

    # Play the file
    subprocess.run(["ffplay", "-autoexit", "-nodisp", "sonic.wav"])

    # Clean up temporary files
    os.remove("sonic.pcm")
    os.remove("sonic.wav")