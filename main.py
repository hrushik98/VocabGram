



from instagrapi import Client
from instagrapi.types import Location, Media, UserShort
import openai
openai.api_key = ""

system_content = """I'm making an instagram bot that will post vocabulary words that many people dont know, but our aim is to improve their lexicon. You
have to return the content in this format only: 
Word: <word-here>
Meaning: <meaning-here> (keep it short, 5 words max)
Example: <usage-of-the-word-in-a-short-one-line-sentence> (keep it short)

Here is an example for you:
Word: Halcyon
Meaning: (adj.) denoting a period of time in the past that was idyllically happy and peaceful.
Example: the halcyon days of the mid 1980s, when profits were soaring"""


m1 = [{"role": "system", "content": f"{system_content}"}]
result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens = 100,
    temperature =0.8,
    messages=m1)
response = result["choices"][0]['message']['content']
print(response)

import re

text = f"""{response}"""

# Define a pattern to match "Word:", "Meaning:", and "Example:" followed by the text
pattern = r"(Word|Meaning|Example):\s(.+)$"

# Find all matches in the text
matches = re.findall(pattern, text, re.MULTILINE)

# Create a dictionary to store the extracted data
data = {}
for match in matches:
    key, value = match
    data[key] = value

# Append the values to a list
result_list = [data["Word"], data["Meaning"], data["Example"]]

print(result_list)

from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

# Input your data
word_name = f"{result_list[0]}"
meaning = f"""{result_list[1]}"""
example_sentence = f"""{result_list[2]}"""

# Create a square image
image_size = (1080, 1080)  # Instagram post aspect ratio is 1:1 (square)
new = Image.new('RGB', image_size, (221, 228, 232))  # Light blue-gray background

# Define custom fonts and font sizes for each text
word_font = ImageFont.truetype("SEASRN__.ttf", 50)  # Replace "Font1.ttf" with the actual font path and size
meaning_font = ImageFont.truetype("JosefinSans-SemiBoldItalic.ttf", 23)  # Replace "Font2.ttf" with the actual font path and size
example_font = ImageFont.truetype("Roboto-BoldItalic.ttf",21)  # Replace "Font3.ttf" with the actual font path and size

# Prepare the drawing context
d = ImageDraw.Draw(new)

# Set text color
text_color = (0, 0, 0)  # Black

# Calculate the center position for each text
center_x = image_size[0] // 2

# Calculate vertical positions for each text
word_height = word_font.getsize(word_name)[1]
meaning_height = meaning_font.getsize( meaning)[1]
example_height = example_font.getsize( example_sentence)[1]

# Calculate vertical spacing
vertical_spacing = 40

# Calculate positions to center the text within the image
word_position = (center_x - word_font.getsize(word_name)[0] // 2, (image_size[1] - (word_height + meaning_height + example_height + 2 * vertical_spacing)) // 2)
meaning_position = (center_x - meaning_font.getsize("Meaning: " + meaning)[0] // 2, word_position[1] + word_height + vertical_spacing)
example_position = (center_x - example_font.getsize("Example: " + example_sentence)[0] // 2, meaning_position[1] + meaning_height + vertical_spacing)

# Add a color gradient background
gradient = [(222, 184, 135), (255, 239, 184)]  # Gradient from light brown to light yellow

for y in range(image_size[1]):
    r = int(gradient[0][0] + (gradient[1][0] - gradient[0][0]) * y / image_size[1])
    g = int(gradient[0][1] + (gradient[1][1] - gradient[0][1]) * y / image_size[1])
    b = int(gradient[0][2] + (gradient[1][2] - gradient[0][2]) * y / image_size[1])
    for x in range(image_size[0]):
        new.putpixel((x, y), (r, g, b))

# Add the sentences to the image with the adjusted fonts and centered positions
d.text(word_position, word_name, fill=text_color, font=word_font)
d.text(meaning_position, "Meaning: " + meaning, fill=text_color, font=meaning_font)
d.text(example_position, "Example: " + example_sentence, fill=text_color, font=example_font)

# Display the image
new.save("image.jpg")

username = ""
password = ""

cl = Client()
cl.login(username, password)

media = cl.photo_upload(
    path = "image.jpg",
    caption = f"""
    Word: {result_list[0]}
    Meaning: {result_list[1]}
    Example usage: {result_list[2]}
    """
    
)
import datetime

now = datetime.datetime.now()
print("Posted on", now.strftime("%Y-%m-%d %H:%M:%S"))
import os
os.remove("image.png")
