# CH01 파이썬 실습 (book1/ch01)

## 1. 목적
- 리스트(scores) 데이터를 사용해 평균/최댓값/최솟값/개수를 계산하는 연습

## 2. 실행 환경
- Python: 3.x
- 라이브러리: numpy

## 3. 설치/실행 방법
### (1) 가상환경 활성화 (이미 되어있다면 생략)
- Windows (cmd)
  - .venv\Scripts\Activate.ps1

### (2) 필요한 패키지 설치
- pip install numpy

### (3) 실행
- python ch01ex01.py

## 4. 파일 설명
- ch01ex01.py: scores 리스트를 기반으로 통계값(개수/평균/최대/최소) 출력

## 5. 입력 데이터
- scores = [70, 75, 80, 85, 90, 95]

## 6. 출력 예시
- 데이터 개수: 6
- 평균: 82.5
- 최댓값: 95
- 최솟값: 70

## 7. 메모
- numpy 사용 함수: np.mean, np.max, np.min
