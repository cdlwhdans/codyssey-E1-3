from matrix import Matrix
from npu import NPU
from data_loader import DataLoader

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
        self._print_section("[1] 필터 입력")
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
        try:
            data = self.data_loader.load()
        except (OSError, ValueError, KeyError) as error:
            print(f"data.json 로드 실패: {error}")
            return

        filters = data["filters"]
        patterns = data["patterns"]

        self._print_section("[1] 필터 로드")

        loaded_filters = {}
        filter_errors = {}

        for filter_key, filter_data in filters.items():
            try:
                if not isinstance(filter_data, dict):
                    raise ValueError("필터 데이터는 객체 형태여야 합니다.")

                normalized_filters = {}

                for raw_label, values in filter_data.items():
                    label = self.data_loader.normalize_label(raw_label)
                    normalized_filters[label] = Matrix(values)

                if "Cross" not in normalized_filters or "X" not in normalized_filters:
                    raise ValueError("Cross와 X 필터가 모두 필요합니다.")

                size = self.data_loader.extract_size(filter_key)

                cross_filter = normalized_filters["Cross"]
                x_filter = normalized_filters["X"]

                if cross_filter.size != size or x_filter.size != size:
                    raise ValueError(f"필터 크기가 키에 명시된 {size}x{size} 크기와 일치하지 않습니다.")

                loaded_filters[filter_key] = normalized_filters

                print(f"✓ {filter_key} 필터 로드 완료 (Cross, X)")

            except (ValueError, TypeError) as error:
                filter_errors[filter_key] = str(error)
                print(f"✗ {filter_key} 필터 로드 실패: {error}")

        self._print_section("[2] 패턴 분석 (라벨 정규화 적용)")

        total = 0
        passed = 0
        failures = []

        for key, case in patterns.items():
            total += 1

            print(f"--- {key} ---")

            try:
                if not isinstance(case, dict):
                    raise ValueError("패턴 데이터는 객체 형태여야 합니다.")

                if "input" not in case:
                    raise ValueError("input 데이터가 없습니다.")

                if "expected" not in case:
                    raise ValueError("expected 데이터가 없습니다.")

                size = self.data_loader.extract_size(key)
                filter_key = f"size_{size}"

                if filter_key in filter_errors:
                    raise ValueError(f"{filter_key} 필터 오류: {filter_errors[filter_key]}")

                if filter_key not in loaded_filters:
                    raise ValueError(f"{filter_key} 필터를 찾을 수 없습니다.")

                pattern = Matrix(case["input"])

                if pattern.size != size:
                    raise ValueError(f"패턴 크기가 키에 명시된 {size}x{size} 크기와 일치하지 않습니다.")

                cross_filter = loaded_filters[filter_key]["Cross"]
                x_filter = loaded_filters[filter_key]["X"]

                expected = self.data_loader.normalize_label(case["expected"])

                score_cross, score_x, result = self.npu.classify(pattern, cross_filter, x_filter, "Cross", "X")

                self._print_json_result(score_cross, score_x, result, expected)

                if result == expected:
                    passed += 1

                else:
                    if result == "UNDECIDED":
                        failures.append(f"{key}: 동점(UNDECIDED) 처리 규칙에 따라 FAIL")
                    else:
                        failures.append(f"{key}: 판정 {result}, expected {expected}로 FAIL")

            except (ValueError, KeyError, TypeError) as error:
                failures.append(f"{key}: {error}")
                print(f"FAIL: {error}")

            print()

        self._print_section("[3] 성능 분석 (평균/10회)")

        performance_results = []

        for size in (3, 5, 13, 25):
            pattern = Matrix([[1.0] * size for _ in range(size)])
            filter_ = Matrix([[1.0] * size for _ in range(size)])

            normal_time = self.npu.measure_average_time(pattern, filter_)

            pattern_flat = pattern.flatten()
            filter_flat = filter_.flatten()

            flat_time = self.npu.measure_average_time_flat(pattern_flat, filter_flat)

            performance_results.append((size, normal_time, flat_time))

        self._print_performance(performance_results)

        self._print_section("[4] 결과 요약")
        self._print_summary(total, passed, failures)


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
        status = "PASS" if result == expected else "FAIL"

        print(f"Cross 점수: {score_cross:.10f}")
        print(f"X 점수: {score_x:.10f}")
        print(f"판정: {result} | expected: {expected} | {status}")

    def _print_performance(self, results):
        print("크기       평균 시간(ms)    최적화 후(ms)     연산 횟수")
        print("-------------------------------------------------------")

        for size, average_time, flat_time in results:
            size_text = f"{size}x{size}"
            operation_count = size ** 2

            print(f"{size_text:<10} {average_time:>12.6f} {flat_time:>16.6f} {operation_count:>13}")

    def _print_summary(self, total, passed, failures):
        print(f"총 테스트: {total}개")
        print(f"통과: {passed}개")
        print(f"실패: {len(failures)}개")

        if failures:
            print("실패 케이스:")

            for failure in failures:
                print(f"- {failure}")