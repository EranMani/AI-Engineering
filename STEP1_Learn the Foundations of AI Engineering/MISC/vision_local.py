import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# encoder helper
def encode_image(image_path):
    """Reads a file and converts it to a base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

    
image_path = r"C:\Users\eranm\Desktop\image.jpeg"
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {
                    "type": "image_url",
                    "image_url": {
                        # We inject the base64 string here
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
)

print("\nAI Description:")
print(response.choices[0].message.content)