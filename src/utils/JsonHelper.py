import json


class JsonHelper:

    @staticmethod
    def str2dict(data: str) -> dict:
        first_pos_curly_bracket = data.find('{')
        data = data[first_pos_curly_bracket:]
        return json.loads(data)

    @staticmethod
    def dict2json(data: dict) -> str:
        return json.dumps(data)

    @staticmethod
    def is_json(data: str) -> bool:
        try:
            json.loads(data)
        except ValueError as e:
            return False
        return True
