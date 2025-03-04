import requests
import json

class ModelClient:
    def __init__(self):
        pass
    
    def score_text(self, text: str):
        try:
            res = requests.post('http://host.docker.internal:5200/score_text', json={"text_content": text}).json()
            return res
        except Exception as e:
            return {"error": repr(e)}


def run_program():
    pass
    
def test_program():
    pass

if __name__ == "__main__":
    run_program()