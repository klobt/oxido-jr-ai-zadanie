#!/usr/bin/env python3
from openai import OpenAI
import sys
import json
import os

OUTPUT_PATH = 'article.html'

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    print("No environment variable OPENAI_API_KEY defined.", file=sys.stderr)
    exit(1)

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} ARTICLE_TEXT_FILE", file=sys.stderr)
    exit(1)

input_path = sys.argv[1]


client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def htmlize(text):
    prompt = f"""
    Turn the following article in text form into HTML. Put formatting (headings, etc.) in the appropriate places. Put images where you think they'd be appropriate. Each image should have exactly the string "image_placeholder.jpg" in the `src` attribute and for the `alt` attribute I want you to generate a prompt that can be used to generate an image. Each image should be followed by `div` tag with a Polish description of the image.

    The article is as follows:
    {text}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You're a HTML generator. You generate only HTML5 output that can be put INSIDE the document body with no CSS or Javascript. Output only HTML with not quotes around it. The resulting message will be treated as a HTML by a machine. Keep that in mind.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    if len(chat_completion.choices) == 0:
        return None

    return chat_completion.choices[0].message.content.strip()

try:
    input_file = open(input_path, 'r')
except Exception:
    print(f"Failed to open '{input_path}'.", file=sys.stderr)
    exit(1)
else:
    input_text = input_file.read()
    input_file.close()

output_html = htmlize(input_text)

try:
    output_file = open(OUTPUT_PATH, 'w')
except Exception:
    print(f"Failed to open '{OUTPUT_PATH}'.", file=sys.stderr)
    exit(1)
else:
    output_text = output_file.write(output_html)
    output_file.close()
