class MiniNPU:
    def __init__(self, epsilon=1e-9):
        self.epsilon = epsilon

    def calculate_mac(self, pattern, filter_):
        pass

    def compare_scores(self, score_a, score_b):
        pass

    def classify(self, pattern, filter_a, filter_b,
                 label_a="A", label_b="B"):
        pass

    def measure_average_time(self, pattern, filter_, repeat=10):
        pass