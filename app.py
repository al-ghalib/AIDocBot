import gradio as gr
from brain_doctor import encode_image, analyze_image_with_query
from voice_patient import transcribe_with_groq
from voice_doctor import text_to_speech_with_elevenlabs
from config import VISION_MODEL

system_prompt = (
    "You have to act as a professional doctor, i know you are not but this is for learning purpose. "
    "What's in this image? Do you find anything wrong with it medically? "
    "If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in "
    "your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person. "
    "Do not say 'In the image I see' but say 'With what I see, I think you have ....'. "
    "Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor, "
    "Keep your answer concise (max 5 sentences). No preamble, start your answer right away please."
)

doctor_response_text = ""

def process_inputs(audio_filepath, image_filepath):
    global doctor_response_text

    transcription = transcribe_with_groq(audio_filepath)
    if not transcription:
        transcription = "Sorry, I couldn't transcribe the audio."

    if image_filepath:
        encoded_image = encode_image(image_filepath)
        if encoded_image:
            doctor_response_text = analyze_image_with_query(
                query=f"{system_prompt} {transcription}",
                encoded_image=encoded_image,
                model=VISION_MODEL
            )
        else:
            doctor_response_text = "Error: Couldn't process the image."
    else:
        doctor_response_text = "No image provided for analysis."

    audio_response_path = "doctor_response.mp3"
    text_to_speech_with_elevenlabs(input_text=doctor_response_text, output_filepath=audio_response_path)

    return transcription, audio_response_path, "✅ Analysis complete. Doctor's response is ready."

def get_doctor_response():
    return doctor_response_text

def reset_all():
    return "", None, "", ""

with gr.Blocks(theme=gr.themes.Base(), css="body { background-color: #f8f9fa; }") as app:
    gr.Markdown("<h1 style='text-align: center;'> 🩺 AI DocBot</h1>")
    gr.Markdown("<p style='text-align: center;'>Upload your voice and an image for a quick AI-based health assessment</p>")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak your symptoms")
            image_input = gr.Image(type="filepath", label="📷 Upload a skin/health image")
            diagnose_btn = gr.Button("🧠 Diagnose", variant="primary")
            clear_btn = gr.Button("♻️ Clear Inputs")

        with gr.Column():
            status_output = gr.Textbox(label="🛠️ System Status", interactive=False)
            stt_output = gr.Textbox(label="📝 Transcribed Speech")
            audio_output = gr.Audio(label="🔊 Doctor's Voice Response")

    with gr.Accordion("📄 Doctor's Notes (Click to Show)", open=False):
        doctor_notes_output = gr.Textbox(label="Doctor's Textual Opinion", interactive=False)
        show_notes_btn = gr.Button("Reveal Full Response")

    # Bind actions
    diagnose_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[stt_output, audio_output, status_output]
    )

    show_notes_btn.click(
        fn=get_doctor_response,
        outputs=[doctor_notes_output]
    )

    clear_btn.click(
        fn=reset_all,
        outputs=[stt_output, audio_output, status_output, doctor_notes_output]
    )

# Run
app.launch(debug=True)