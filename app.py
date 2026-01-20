import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts


DISCLAIMER = """
⚠️ Medical Disclaimer  
This AI Doctor provides educational guidance only.  
It is NOT a substitute for a real doctor.
"""


SYSTEM_PROMPT = """
You are an experienced medical doctor.

RULES:
- NEVER greet the user
- NEVER ask "how can I help"
- Give direct medical guidance
- Be calm, clear, and responsible
"""


def process_inputs(audio, text, image, language):
    try:
        # 1️⃣ Get user text
        if audio:
            user_text = transcribe_with_groq(audio)
        elif text and text.strip():
            user_text = text.strip()
        else:
            return "", "Please speak or type your symptoms.", None

        # 2️⃣ Language control (FIXED)
        if language != "Auto":
            language_instruction = f"Reply ONLY in {language} language."
        else:
            language_instruction = "Reply in the SAME language as the user."

        # 3️⃣ Build prompt
        prompt = f"""
{SYSTEM_PROMPT}

{language_instruction}

Patient symptoms:
{user_text}

Provide medical guidance.
"""

        # 4️⃣ Vision / text analysis
        if image:
            encoded = encode_image(image)
            doctor_reply = analyze_image_with_query(prompt, encoded)
        else:
            doctor_reply = analyze_image_with_query(prompt, None)

        # 5️⃣ Text to speech
        audio_out = text_to_speech_with_gtts(doctor_reply)

        return user_text, doctor_reply, audio_out

    except Exception as e:
        return "Error", str(e), None


# ================= UI =================

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown(DISCLAIMER)
    gr.Markdown("## 🩺 AI Doctor with Vision and Voice")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎙️ Record Your Voice (optional)"
            )

            text_input = gr.Textbox(
                label="✍️ Type Your Symptoms (optional)",
                placeholder="e.g. yennodu skin epdi iruku / mujhe pimples ho rahe hain"
            )

            image_input = gr.Image(
                type="filepath",
                label="🖼️ Upload Medical Image (optional)"
            )

            language = gr.Dropdown(
                choices=[
                    "Auto",
                    "English",
                    "Tamil",
                    "Urdu",
                    "Hindi",
                    "Malayalam",
                    "Arabic"
                ],
                value="Auto",
                label="🌐 Select Language"
            )

        with gr.Column():
            speech_text = gr.Textbox(label="🗣️ Speech / Text Input")
            doctor_text = gr.Textbox(label="🧑‍⚕️ Doctor Response", lines=8)
            doctor_audio = gr.Audio(label="🔊 Doctor Voice Response", autoplay=True)

    btn = gr.Button("🩺 Analyze")

    btn.click(
        process_inputs,
        inputs=[audio_input, text_input, image_input, language],
        outputs=[speech_text, doctor_text, doctor_audio],
        queue=True
    )

app.launch()

