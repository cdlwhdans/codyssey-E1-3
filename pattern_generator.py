from matrix import Matrix


class PatternGenerator:
    def generate_cross(self, size):
        if size <= 0 or size % 2 == 0:
            raise ValueError("패턴 크기는 1 이상의 홀수여야 합니다.")

        values = [[0.0] * size for _ in range(size)]
        center = size // 2

        for index in range(size):
            values[center][index] = 1.0
            values[index][center] = 1.0

        return Matrix(values)

    def generate_x(self, size):
        if size <= 0 or size % 2 == 0:
            raise ValueError("패턴 크기는 1 이상의 홀수여야 합니다.")

        values = [[0.0] * size for _ in range(size)]

        for index in range(size):
            values[index][index] = 1.0
            values[index][size - 1 - index] = 1.0

        return Matrix(values)