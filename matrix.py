class Matrix:
    def __init__(self, values):
        self.values = values
        self._validate()

    @property
    def size(self):
        return len(self.values)

    def get(self, row, col):
        return self.values[row][col]

    def set(self, row, col, value):
        if not isinstance(value, (int, float)):
            raise ValueError("행렬에는 숫자만 저장할 수 있습니다.")
        self.values[row][col] = value

    def _validate(self):
        if not isinstance(self.values, list) or len(self.values) == 0:
            raise ValueError("행렬은 비어 있을 수 없습니다.")

        size = len(self.values)

        for row in self.values:
            if not isinstance(row, list) or len(row) != size:
                raise ValueError("행렬은 NxN 형태여야 합니다.")

            for value in row:
                if not isinstance(value, (int, float)):
                    raise ValueError("행렬에는 숫자만 저장할 수 있습니다.")