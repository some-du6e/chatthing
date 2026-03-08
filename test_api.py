import requests
import json

api_key = "sk-hc-v1-d2bc97fbbf6b4bf6a9667f9f4294592a74b052008df6469e9516d6e6bb5506c3"

response = requests.post(
    "https://ai.hackclub.com/proxy/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "qwen/qwen3-32b",
        "messages": [
            {"role": "user", "content": "Write a very long and detailed story about a space exploration mission. Make it at least 3000 words with lots of descriptions and dialogue."}
        ],
        "stream": True,
    },
    stream=True,
)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("Streaming response:")
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8') if isinstance(line, bytes) else line
            if line.startswith('data: '):
                data_str = line[6:]  # Remove 'data: ' prefix
                if data_str == '[DONE]':
                    break
                try:
                    data = json.loads(data_str)
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            print(content, end='', flush=True)
                except json.JSONDecodeError:
                    pass
    print("\n--- Stream complete ---")
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")
