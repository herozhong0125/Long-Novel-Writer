import ollama

MODEL = "qwen2.5:14b-instruct-q4_0"

def generate_text(prompt):
    try:
        full_response = ""
        for chunk in ollama.generate(model=MODEL, prompt=prompt, stream=True):
            if chunk.get('response') is not None:
                full_response += chunk['response']
                yield chunk['response']
        return full_response
    except Exception as e:
        print(f"Error generating text: {e}")
        return None

def generate_text_sync(prompt):
    try:
        response = ollama.generate(model=MODEL, prompt=prompt)
        return response['response']
    except Exception as e:
        print(f"Error generating text: {e}")
        return None