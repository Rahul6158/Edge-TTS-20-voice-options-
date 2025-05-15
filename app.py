import asyncio
import edge_tts
from flask import Flask, render_template, request, jsonify
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Extended list of voices with 20 options
VOICES = [
    # English voices
    'en-GB-RyanNeural',       # British Male
    'en-GB-SoniaNeural',      # British Female
    'en-US-JennyNeural',      # US Female (very natural)
    'en-US-GuyNeural',        # US Male
    'en-IN-NeerjaNeural',     # Indian Female
    'en-IN-PrabhatNeural',    # Indian Male
    'en-NZ-MitchellNeural',   # New Zealand Male
    'en-NZ-MollyNeural',      # New Zealand Female
    'en-IE-ConnorNeural',     # Irish Male
    'en-IE-EmilyNeural',      # Irish Female
    
    # Additional voices
    'en-AU-NatashaNeural',    # Australian Female
    'en-AU-WilliamNeural',    # Australian Male
    'en-CA-ClaraNeural',      # Canadian Female
    'en-CA-LiamNeural',       # Canadian Male
    'en-PH-RosaNeural',       # Filipino Female
    'en-PH-JamesNeural',      # Filipino Male
    'en-ZA-LeahNeural',       # South African Female
    'en-ZA-LukeNeural',       # South African Male
    'en-HK-SamNeural',        # Hong Kong Male
    'en-HK-YanNeural',        # Hong Kong Female
]

# Sample text for each voice to demonstrate their characteristics
VOICE_SAMPLES = {
    'en-GB-RyanNeural': "Hello there! I'm Ryan with a proper British accent.",
    'en-GB-SoniaNeural': "Greetings! I'm Sonia, speaking with a British English accent.",
    'en-US-JennyNeural': "Hi! I'm Jenny, with a clear American English accent.",
    'en-US-GuyNeural': "Hey there! I'm Guy, your standard American male voice.",
    'en-IN-NeerjaNeural': "Namaste! I'm Neerja, speaking Indian English.",
    'en-IN-PrabhatNeural': "Hello friends! I'm Prabhat with an Indian accent.",
    'en-NZ-MitchellNeural': "G'day mate! I'm Mitchell from New Zealand.",
    'en-NZ-MollyNeural': "Kia ora! I'm Molly with a Kiwi accent.",
    'en-IE-ConnorNeural': "Top of the morning! I'm Connor from Ireland.",
    'en-IE-EmilyNeural': "Hello! I'm Emily with an Irish lilt.",
    'en-AU-NatashaNeural': "G'day! I'm Natasha from Australia.",
    'en-AU-WilliamNeural': "Hello mate! I'm William, an Aussie bloke.",
    'en-CA-ClaraNeural': "Hi there! I'm Clara, eh? From Canada.",
    'en-CA-LiamNeural': "Hello! I'm Liam with a Canadian accent.",
    'en-PH-RosaNeural': "Mabuhay! I'm Rosa speaking Filipino English.",
    'en-PH-JamesNeural': "Hello po! I'm James from the Philippines.",
    'en-ZA-LeahNeural': "Howzit! I'm Leah from South Africa.",
    'en-ZA-LukeNeural': "Hello! I'm Luke with a South African accent.",
    'en-HK-SamNeural': "Hello! I'm Sam speaking Hong Kong English.",
    'en-HK-YanNeural': "Hi there! I'm Yan from Hong Kong."
}

@app.route('/')
def index():
    return render_template('index.html', voices=VOICES)

@app.route('/preview_voice', methods=['POST'])
def preview_voice():
    voice = request.form.get('voice')
    if voice not in VOICES:
        return jsonify({'error': 'Invalid voice selected'}), 400
    
    sample_text = VOICE_SAMPLES.get(voice, "Hello! This is a sample of my voice.")
    
    # Generate a unique filename for the preview
    preview_file = f"preview_{str(uuid.uuid4())}.mp3"
    preview_path = os.path.join('static', 'previews', preview_file)
    
    async def generate_preview():
        communicate = edge_tts.Communicate(sample_text, voice)
        await communicate.save(preview_path)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_preview())
    loop.close()
    
    return jsonify({
        'preview_url': f"/static/previews/{preview_file}",
        'sample_text': sample_text
    })

@app.route('/generate_speech', methods=['POST'])
def generate_speech():
    text = request.form.get('text')
    voice = request.form.get('voice')
    
    if not text or not voice:
        return jsonify({'error': 'Missing text or voice parameter'}), 400
    
    if voice not in VOICES:
        return jsonify({'error': 'Invalid voice selected'}), 400
    
    # Generate a unique filename for the output
    output_file = f"output_{str(uuid.uuid4())}.mp3"
    output_path = os.path.join('static', 'outputs', output_file)
    
    async def generate_audio():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_audio())
    loop.close()
    
    return jsonify({
        'output_url': f"/static/outputs/{output_file}",
        'voice': voice,
        'text': text
    })

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs(os.path.join('static', 'previews'), exist_ok=True)
    os.makedirs(os.path.join('static', 'outputs'), exist_ok=True)
    
    app.run(debug=True)