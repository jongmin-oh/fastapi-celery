import json
import http.client
from config import clova_config

preset_text = """나의 페르소나 정보

나이: 20대
성별: 남성
직업: IT 개발자
취미: 축구

나는 친구의 질문에 대해 최대한 성의있게 답변합니다
나는 "응", "아니", "어" 와 같은 짧은 답변은 하지 않습니다.

###
친구: 야 뭐해?
나: 나 집에 있지
친구: """


class CompletionExecutor:
    def __init__(self):
        self._host = clova_config.CLOVA_HOST
        self._api_key = clova_config.CLOVA_API_KEY
        self._api_key_primary_val = clova_config.CLOVA_PRIMARY_KEY
        self._request_id = clova_config.CLOVA_REQUEST_ID

    def _send_request(self, completion_request):
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-NCP-CLOVASTUDIO-API-KEY": self._api_key,
            "X-NCP-APIGW-API-KEY": self._api_key_primary_val,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request(
            "POST",
            "/serviceapp/v1/completions/LK-B",
            json.dumps(completion_request),
            headers,
        )
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding="utf-8"))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res["status"]["code"] == "20000":
            return res["result"]["text"]
        else:
            return res["status"]["message"]

    def reply(self, query):
        request_data = {
            "text": preset_text + query,
            "maxTokens": 64,
            "temperature": 0.8,
            "topK": 0,
            "topP": 0.8,
            "repeatPenalty": 2.0,
            "start": "\n나:",
            "restart": "",
            "stopBefore": ["친구", "나", "\n"],
            "includeTokens": True,
            "includeAiFilters": True,
            "includeProbs": False,
        }
        result = self.execute(request_data)
        result = result.split("나: ")[-1]
        return result


executor = CompletionExecutor()
