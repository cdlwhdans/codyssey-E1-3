import json

class DataLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.validate_schema(data)

        return data

    def validate_schema(self, data):
        if not isinstance(data, dict):
            raise ValueError("JSON의 최상위 데이터는 객체여야 합니다.")

        if "filters" not in data:
            raise ValueError("filters 데이터가 없습니다.")

        if "patterns" not in data:
            raise ValueError("patterns 데이터가 없습니다.")

        if not isinstance(data["filters"], dict):
            raise ValueError("filters는 객체 형태여야 합니다.")

        if not isinstance(data["patterns"], dict):
            raise ValueError("patterns는 객체 형태여야 합니다.")

    def extract_size(self, key):
        parts = key.split("_")

        if len(parts) < 2 or parts[0] != "size":
            raise ValueError(f"잘못된 패턴 키입니다: {key}")

        try:
            return int(parts[1])
        except ValueError:
            raise ValueError(f"크기를 추출할 수 없습니다: {key}")

    def normalize_label(self, label):
        if label in ("+", "cross", "Cross"):
            return "Cross"

        if label in ("x", "X"):
            return "X"

        raise ValueError(f"알 수 없는 라벨입니다: {label}")