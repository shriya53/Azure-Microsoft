import whisper

# Load whisper model
model = whisper.load_model("base")

# Audio file path
audio_path = "audio/sample.ogg"


# Transcribe audio
result = model.transcribe(audio_path)

# Print text
print("\n--- TRANSCRIBED TEXT ---\n")
print(result["text"])
