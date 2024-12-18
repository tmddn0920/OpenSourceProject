import random

# 운동 루틴 생성
def generate_routine(part):
    """운동 부위에 따라 루틴 생성"""
    exercises = {
        "어깨": [["사이드 레터럴 레이즈 머신(측면 스트레칭)"], ["밀리터리 프레스", "오버헤드 프레스"], ["덤벨 숄더 프레스", "아놀드 프레스"], ["프론트 레이즈", "업라이트 로우"], ["페이스 풀", "리버스 펙덱 플라이"]],
        "팔": [["바벨 컬"], ["해머 컬"], ["컨센트레이션 컬", "덤벨 컬"], ["트라이셉스 익스텐션", "케이블 푸쉬 다운"], ["덤벨 오버헤드 익스텐션", "덤벨 킥 백"]],
        "가슴": [["벤치 프레스", "덤벨 체스트 프레스"], ["인클라인 벤치 프레스", "덤벨 인클라인 체스트 프레스"], ["체스트 프레스 머신"], ["딥스"], ["케이블 플라이", "덤벨 플라이"]],
        "등": [["풀 다운", "풀업"], ["컨벤셔널 데드리프트", "루마니안 데드리프트"], ["티바 로우", "바벨 로우"], ["하이 로우", "케이블 로우"], ["렛 풀 다운"]],
        "하체": [["풀 스쿼트"], ["레그 프레스", "핵 스쿼트"], ["레그 컬"], ["레그 익스텐션", "런지"], ["이너 타이", "아웃 타이"]],
    }
    if part in exercises:
        return [random.choice(pair) for pair in exercises[part]]
    else:
        return []

def cardio_exercise():
    cardio_options = ["런닝머신 (30분)", "자전거 타기 (30분)", "천국의 계단 (15분)"]
    return random.choice(cardio_options)