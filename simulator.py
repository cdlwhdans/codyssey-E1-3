from matrix import Matrix
from npu import NPU
from data_loader import DataLoader


'''
def _print_user_input_result(self, score_a, score_b, average_time, result):
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"평균 MAC 연산 시간: {average_time:.6f} ms")

    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {self.npu.epsilon})")
    else:
        print(f"판정: {result}")'''

class Simulator:
    def __init__(self, data_path="data.json"):
        self.npu = NPU()
        self.data_loader = DataLoader(data_path)

    def run(self):
        print("=== Mini NPU Simulator ===")
        print()
        print("[모드 선택]")
        print()
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")

        while True:
            try:
                choice = int(input("선택: "))

                if choice not in (1, 2):
                    print("1 또는 2를 입력해주세요.")
                    continue
                break

            except ValueError:
                print("유효한 숫자를 입력해주세요.")

        if choice == 1:
            self._run_user_input_mode()
        elif choice == 2:
            self._run_json_mode()


        
    def _run_user_input_mode(self):
        self._print_section("[1] 필터 로드")
        filter_a = self._input_matrix("필터 A", 3)
        filter_b = self._input_matrix("필터 B", 3)

        self._print_section("[2] 패턴 입력")
        pattern = self._input_matrix("패턴", 3)


        score_a, score_b, result = self.npu.classify(pattern, filter_a, filter_b, "A", "B")
        average_time = self.npu.measure_average_time(pattern, filter_a)

        self._print_section("[3] MAC 결과")
        self._print_user_input_result(score_a, score_b, average_time, result)
            

    def _input_matrix(self, name, size):
        print(f"{name} ({size}줄 입력, 공백 구분)")
        matrix = []

        while len(matrix) < size:
            try:
                row = list(map(float, input().split()))

                if len(row) != size:
                    print(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")
                    continue

                matrix.append(row)

            except ValueError:
                print("입력 형식 오류: 숫자만 입력하세요.")
        print()
        return Matrix(matrix)

    def _run_json_mode(self):
        pass


    def _print_section(self, title):
        print("\n#---------------------------------------")
        print(f"# {title}")
        print("#---------------------------------------")
       
    def _print_user_input_result(self, score_a, score_b, average_time, result):
        print(f"A 점수: {score_a:.10f}")
        print(f"B 점수: {score_b:.10f}")
        print(f"연산 시간(평균/10회): {average_time:.3f} ms")
        if result == "UNDECIDED":
            print(f"판정: 판정 불가 (|A-B| < {self.npu.epsilon})\n")
        else:
            print(f"판정: {result}\n")


    def _print_json_result(self, score_cross, score_x, result, expected):
        pass

    def _print_performance(self, results):
        pass

    def _print_summary(self, total, passed, failures):
        pass