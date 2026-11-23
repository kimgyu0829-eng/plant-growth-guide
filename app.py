import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="식물 성장 가이드", page_icon="🌱", layout="centered")
st.title("🌱 맞춤형 식물 성장 가이드")
st.write(
    "키우는 식물과 현재 관리 환경을 입력하면 권장 환경과 주의사항을 진단해 드립니다."
)

# 1. 식물별 권장환경 데이터 (리스트 구조로 구성)
# 각 항목 순서: [식물종, 권장 일조량, 권장 수분량(설명), 추천장소, 최소 권장 분사량(회), 최대 권장 분사량(회)]
plant_guides = [
    [
        "선인장",
        "많음",
        "적음 (하루 1~2회 가볍게)",
        "햇빛이 잘 드는 창가 / 베란다",
        1,
        2,
    ],
    [
        "사과나무",
        "많음",
        "보통 (하루 4~6회)",
        "야외 정원 / 햇빛 가득한 테라스",
        4,
        6,
    ],
    [
        "강낭콩",
        "보통",
        "많음 (하루 6~8회)",
        "통풍이 잘 되는 반양지 창가",
        6,
        8,
    ],
    [
        "몬스테라",
        "적음",
        "보통 (하루 3~5회)",
        "직사광선을 피한 거실 실내",
        3,
        5,
    ],
    [
        "바질",
        "많음",
        "많음 (하루 7~9회)",
        "주방 창가 / 햇빛 드는 베란다",
        7,
        9,
    ],
]


# 2. 현재 주의사항을 판단하는 함수 정의 (매개변수: 식물종, 하루 분사량, 일조량)
def check_plant_caution(plant_name, water_count, sunlight):
    cautions = []  # 주의사항을 담을 리스트
    target_plant = None

    # for 구문으로 리스트를 순회하며 선택한 식물(필요 일조량 등)을 찾을 때까지 탐색
    for plant in plant_guides:
        if plant[0] == plant_name:
            target_plant = plant
            break  # 식물을 찾으면 순회 종료

    if target_plant is not None:
        rec_sunlight = target_plant[1]  # 권장 일조량
        min_water = target_plant[4]  # 최소 권장 분사량
        max_water = target_plant[5]  # 최대 권장 분사량

        # 일조량 수준을 숫자로 변환하여 비교
        sun_level = {"적음": 1, "보통": 2, "많음": 3}

        # 조건문(if/elif)으로 일조량 비교
        if sun_level[sunlight] > sun_level[rec_sunlight]:
            cautions.append("일조량 감소 필요")
        elif sun_level[sunlight] < sun_level[rec_sunlight]:
            cautions.append("일조량 증가 필요")

        # 조건문(if/elif)으로 하루 물 분사량 기준 비교
        if water_count > max_water:
            cautions.append("분사량 줄이기 필요")
        elif water_count < min_water:
            cautions.append("분사량 상승 필요")

    # 주의사항이 없으면 정상 메시지, 있으면 쉼표(,)로 연결해 리턴
    if not cautions:
        return "현재 환경이 매우 적절합니다! (특이사항 없음)"
    else:
        return ", ".join(cautions)


st.divider()

# 3. 사용자 입력 UI 구성
# 식물종 리스트 추출
plant_names = [plant[0] for plant in plant_guides]
selected_plant = st.selectbox("1. 식물종을 선택하세요:", plant_names)

# 일조량 드롭다운 목록
selected_sunlight = st.selectbox(
    "2. 현재 일조량을 선택하세요:", ["많음", "보통", "적음"]
)

# 물 분사량 슬라이더 (하루 1~10회)
selected_water = st.slider(
    "3. 하루 물 분사량(횟수)을 선택하세요:", min_value=1, max_value=10, value=3
)

st.write("")  # 여백 추가

# 4. 버튼 클릭 시 결과 화면 출력
if st.button(
    "🔍 필요사항 및 주의사항 확인하기",
    type="primary",
    use_container_width=True,
):
    st.divider()

    # 텍스트 메시지로 제목 출력
    st.subheader(f"📋 {selected_plant} 키울 시 권장환경")

    # for 구문으로 해당 식물의 권장환경 데이터 찾기
    rec_info = None
    for plant in plant_guides:
        if plant[0] == selected_plant:
            rec_info = plant
            break

    # 테이블 표로 권장 일조량, 수분량, 추천장소 나타내기
    if rec_info:
        df = pd.DataFrame(
            {
                "권장 일조량": [rec_info[1]],
                "권장 수분량": [rec_info[2]],
                "추천 장소": [rec_info[3]],
            }
        )
        # 인덱스 번호(0)를 숨기고 깔끔한 표로 출력
        st.table(df.set_index("권장 일조량"))

    # 함수를 호출하여 현재 주의사항 리턴받기
    result_caution = check_plant_caution(
        selected_plant, selected_water, selected_sunlight
    )

    # 강조 수치(st.metric)로 현재 주의사항 출력
    st.metric(label="⚠️ 현재 주의사항", value=result_caution)
