import streamlit as st
import pandas as pd
import random

# 1. 자체 여행지 데이터베이스 (외부 API 대체)
travel_data = [
    {"지역": "제주도", "테마": ["자연", "힐링", "액티비티"], "특징": "바다와 오름을 넘나드는 완벽한 휴양지"},
    {"지역": "부산 (기장)", "테마": ["도심", "바다", "미식"], "특징": "해안 절경과 세련된 오션뷰 카페의 조화"},
    {"지역": "속초", "테마": ["자연", "미식", "힐링"], "특징": "설악산의 절경과 동해바다, 풍부한 먹거리"},
    {"지역": "경주", "테마": ["역사", "힐링", "도심"], "특징": "밤이 더 아름다운 천년 고도의 도시"},
    {"지역": "강릉", "테마": ["바다", "커피", "자연"], "특징": "향긋한 커피와 탁 트인 푸른 바다"},
    {"지역": "여수", "테마": ["바다", "미식", "액티비티"], "특징": "낭만적인 밤바다와 풍성한 해산물"}
]

df = pd.DataFrame(travel_data)

# 2. 웹앱 UI 설정
st.set_page_config(page_title="나만의 여행지 추천기", page_icon="✈️", layout="centered")

st.title("✈️ 나만의 맞춤 여행지 추천기")
st.write("간단한 취향 테스트로 이번 주말에 떠날 완벽한 여행지를 찾아보세요!")

st.divider()

# 3. 사용자 입력 위젯 (사이드바 및 메인 화면)
st.sidebar.header("어떤 여행을 원하시나요?")

# 인원수 및 숙소 취향 입력
group_size = st.sidebar.slider("여행 인원수 (어른 기준)", min_value=1, max_value=10, value=4)
st.sidebar.write("숙소 필수 옵션")
require_nonsmoking = st.sidebar.checkbox("금연 객실", value=True)
require_twinbed = st.sidebar.checkbox("트윈 베드", value=True)

# 여행 테마 선택
themes = ["자연", "도심", "힐링", "액티비티", "미식", "역사", "바다", "커피"]
selected_theme = st.multiselect("가장 원하는 여행 테마를 선택하세요 (복수 선택 가능)", themes, default=["힐링"])

st.divider()

# 4. 추천 로직 처리
if st.button("추천받기", type="primary"):
    if not selected_theme:
        st.warning("최소 1개 이상의 테마를 선택해 주세요!")
    else:
        with st.spinner("최적의 여행지를 찾는 중..."):
            # 선택한 테마가 하나라도 포함된 여행지 필터링
            def check_theme(dest_themes):
                return any(theme in dest_themes for theme in selected_theme)
            
            mask = df["테마"].apply(check_theme)
            recommended_df = df[mask]
            
            if recommended_df.empty:
                st.info("조건에 딱 맞는 여행지가 없습니다. 다른 테마를 선택해 보세요!")
            else:
                st.success("🎉 추천 여행지를 찾았습니다!")
                
                # 결과 출력
                for index, row in recommended_df.iterrows():
                    with st.expander(f"📍 **{row['지역']}** (추천도: ⭐⭐⭐⭐⭐)", expanded=True):
                        st.write(f"**매력 포인트:** {row['특징']}")
                        st.write(f"**관련 테마:** {', '.join(row['테마'])}")
                        
                        # 숙소 옵션 텍스트 생성
                        room_text = []
                        if require_nonsmoking: room_text.append("쾌적한 금연 객실")
                        if require_twinbed: room_text.append("여유로운 트윈 베드")
                        
                        if room_text:
                            st.caption(f"💡 팁: {group_size}인 여행 시 **{', '.join(room_text)}** 위주로 숙소를 검색해 보세요.")
