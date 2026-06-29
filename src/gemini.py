import os
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_answer(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

# def stream_answer(prompt):

#     response = client.models.generate_content_stream(
#         model="gemini-2.5-flash",
#         contents=prompt,
#     )

#     for chunk in response:

#         if chunk.text:

#             yield chunk.text

# def stream_answer(prompt):

#     response = client.models.generate_content_stream(
#         model="gemini-2.5-flash",
#         contents=prompt,
#     )

#     for chunk in response:

#         print(repr(chunk.text))

#         if chunk.text:

#             yield chunk.text

def stream_answer(prompt):

    text = """
# Process

A **process** is a running program.

## Characteristics

- Process ID
- Memory Image
- CPU Context
- File Descriptors

### Example

```cpp
int main() {
    return 0;
}
```
"""

    for ch in text:

        yield ch

        time.sleep(0.01)