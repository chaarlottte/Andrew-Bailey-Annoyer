import requests, random

class textgen():
    def __init__(self) -> None:
        self._prompts = [x.strip() for x in open(f"data/prompts.txt", "r", encoding="utf8").readlines()]
        pass

    def generate_text(self, name: str, max_rant_size: int) -> str:
        prompt = self._get_prompt(name=name)
        body = {
            "streamResponse": False,
            "prompt": {
                "text": prompt,
                "isContinuation": False
            },
            "startFromBeginning": False,
            "length": max_rant_size,
            "forceNoEnd": False,
            "topP": 0.9,
            "temperature": 1,
            "keywords": [
                "tranny",
                "dumb",
                "liberal",
                "libtard"
            ]
        }
        resp = requests.post("https://api.inferkit.com/v1/models/standard/generate?useDemoCredits=true", json=body)
        if resp.status_code == 200:
            if resp.json().get("data").get("text") is not None:
                return prompt + resp.json().get("data").get("text")
        return prompt

    def _get_prompt(self, name: str) -> str:
        prompt = random.choice(self._prompts)
        prompt = prompt.replace("<name>", name)
        return prompt

if __name__ == "__main__":
    ai = textgen()
    print(ai.generate_text(name="Joe Shmoe"))