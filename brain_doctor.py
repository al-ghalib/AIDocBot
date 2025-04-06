import base64
from groq import Groq
from config import GROQ_API_KEY


def encode_image(image_filepath):
    try:
        with open(image_filepath, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    except Exception as e:
        print(f"Image encoding error: {e}")
        return None


def analyze_image_with_query(query, model, encoded_image):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            }
        ]
        chat_completion = client.chat.completions.create(messages=messages, model=model)
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"AI Doctor couldn't analyze the image: {e}"
