import streamlit as st

# 1. 종목 리스트 저장
events = ["매디신볼", "왕복달리기", "제자리 멀리뛰기", "윗몸말아올리기", "유연성"]

# 2. 성별 및 종목별 상위권/중위권 기준표 (입시체육 일반 기준 예시 - 필요시 숫자 수정)
standards = {
    "남자": {
        "매디신볼": {"상": 13.0, "중": 10.0, "단위": "m"},
        "왕복달리기": {"상": 25.0, "중": 20.0, "단위": "회"},
        "제자리 멀리뛰기": {"상": 270.0, "중": 240.0, "단위": "cm"},
        "윗몸말아올리기": {"상": 70.0, "중": 50.0, "단위": "회"},
        "유연성": {"상": 25.0, "중": 15.0, "단위": "cm"}
    },
    "여자": {
        "매디신볼": {"상": 9.0, "중": 7.0, "단위": "m"},
        "왕복달리기": {"상": 22.0, "중": 18.0, "단위": "회"},
        "제자리 멀리뛰기": {"상": 220.0, "중": 195.0, "단위": "cm"},
        "윗몸말아올리기": {"상": 60.0, "중": 40.0, "단위": "회"},
        "유연성": {"상": 28.0, "중": 18.0, "단위": "cm"}
    }
}

# 3. 성별, 종목, 기록을 매개변수로 받는 판독 함수
def evaluate_record(gender, selected_event, user_record):
    # for 구문을 사용하여 리스트에서 일치하는 종목 탐색
    for event in events:
        if event == selected_event:
            std = standards[gender][event]
            high_cut = std["상"]
            mid_cut = std["중"]
            unit = std["단위"]
            
            # 조건문을 통한 상/중/하 판별
            if user_record >= high_cut:
                grade = "상"
                diff = 0
            elif user_record >= mid_cut:
                grade = "중"
                diff = round(high_cut - user_record, 2)
            else:
                grade = "하"
                diff = round(high_cut - user_record, 2)
                
            return grade, diff, unit

# 4. Streamlit 화면 구성
st.title("🏃‍♂️ 입시체육 종목별 수준 판독 시스템")
st.write("성별과 종목을 선택하고 본인의 기록을 입력한 뒤 판독하기 버튼을 눌러주세요.")

# 성별 선택 버튼 (가로 배치)
gender = st.radio("성별 선택", ["남자", "여자"], horizontal=True)

# 종목 선택
selected_event = st.selectbox("종목 선택", events)
current_unit = standards[gender][selected_event]["단위"]

# 기록 입력 받기
step_val = 1.0 if current_unit == "회" else 0.1
format_str = "%.0f" if current_unit == "회" else "%.1f"

user_record = st.number_input(
    f"기록 입력 ({current_unit})", 
    min_value=-50.0, 
    max_value=500.0, 
    value=0.0, 
    step=step_val,
    format=format_str
)

# 판독하기 버튼 및 결과 출력
if st.button("판독하기"):
    grade, diff, unit = evaluate_record(gender, selected_event, user_record)
    
    # '회' 단위일 때는 소수점(.0) 제거
    if unit == "회":
        diff = int(diff)
        
    # 기본 결과 문구
    result_msg = f"**{selected_event}** 중 **{grade}위** 기록입니다."
    
    # 중, 하위 기록일 경우 추가 문구 생성
    if grade in ["중", "하"]:
        result_msg += f"\n\n상위 기록까지 **{diff}{unit}** 남았습니다."
        st.warning(result_msg)
    else:
        st.success(result_msg)
