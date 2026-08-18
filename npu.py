import time

class MiniNPU:
    def __init__(self, epsilon=1e-9):
        self.epsilon = epsilon

    def calculate_mac(self, pattern, filter_):
        if pattern.size != filter_.size:
            raise ValueError("패턴과 필터의 크기가 일치해야 합니다.")

        result = 0

        for row in range(pattern.size):
            for col in range(pattern.size):
                result += pattern.get(row, col) * filter_.get(row, col)

        return result

    def compare_scores(self, score_a, score_b):
        diff = score_a - score_b

        if abs(diff) < self.epsilon:
            return 0
        
        return diff


    def classify(self, pattern, filter_a, filter_b, label_a, label_b):
        score_a = self.calculate_mac(pattern, filter_a)
        score_b = self.calculate_mac(pattern, filter_b)

        result = self.compare_scores(score_a, score_b)

        if result == 0:
            return "UNDECIDED"
        elif result > 0:
            return label_a
        return label_b

    def measure_average_time(self, pattern, filter_, repeat=10):
        total_time = 0

        for _ in range(repeat):
            start = time.perf_counter()
            self.calculate_mac(pattern, filter_)
            end = time.perf_counter()

            total_time += (end - start)

        average_time = total_time / repeat * 1000

        return average_time