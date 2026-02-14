import whisper

# Load model
model = whisper.load_model("base")

# Audio file
audio_path = "audio/sample.ogg"

# Transcribe
result = model.transcribe(audio_path)

# Save raw text
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Transcript saved to transcript.txt")
