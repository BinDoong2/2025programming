import streamlit as st
import pandas as pd
from collections import defaultdict

@st.cache_data
def load_data():
    df = pd.read_csv('games.csv')
    return df

games_df = load_data()

st.title('🧐 게임 성향 테스트 기반 추천')
st.write('몇 가지 질문에 답해주시면, 당신의 게임 성향에 맞는 장르와 게임을 추천해 드립니다!')

st.subheader('1. 게임의 진행 속도는 어떤 것을 선호하시나요?')
q1 = st.radio('q1', ('빠른 속도감과 액션', '느긋하고 차분한 플레이', '상황에 따라 다름'), label_visibility="collapsed")

st.subheader('2. 스토리는 얼마나 중요한가요?')
q2 = st.radio('q2', ('스토리가 가장 중요해요', '게임 플레이가 더 중요해요', '스토리는 거의 신경 쓰지 않아요'), label_visibility="collapsed")

st.subheader('3. 누구와 함께 플레이하는 것을 즐기시나요?')
q3 = st.radio('q3', ('혼자서 몰입하는 플레이', '친구들과 협동하는 플레이', '다른 플레이어와 경쟁하는 플레이'), label_visibility="collapsed")

st.subheader('4. 어떤 테마나 세계관을 좋아하시나요?')
q4 = st.radio('q4', ('판타지나 마법의 세계', '공상 과학(SF) 또는 우주', '현실 기반 또는 가까운 미래'), label_visibility="collapsed")

if st.button('결과 보기'):
    genre_scores = defaultdict(int)

    if q1 == '빠른 속도감과 액션':
        for genre in ['Action', 'Shooter', 'Roguelike', 'MOBA', 'Battle Royale']: genre_scores[genre] += 2
    elif q1 == '느긋하고 차분한 플레이':
        for genre in ['Simulation', 'Farming', 'Puzzle', 'Life Sim', 'Building']: genre_scores[genre] += 2
    else:
        for genre in genre_scores.keys(): genre_scores[genre] += 0.5

    if q2 == '스토리가 가장 중요해요':
        for genre in ['RPG', 'Story Rich', 'Adventure', 'Metroidvania']: genre_scores[genre] += 2
    elif q2 == '게임 플레이가 더 중요해요':
        for genre in ['Action', 'Shooter', 'Strategy', 'Roguelike', 'Platformer']: genre_scores[genre] += 1
    else:
        for genre in ['Party', 'Roguelike', 'Sandbox', 'MOBA']: genre_scores[genre] += 1

    if q3 == '혼자서 몰입하는 플레이':
        for genre in ['RPG', 'Simulation', 'Story Rich', 'Indie', 'Platformer', 'Sandbox']: genre_scores[genre] += 2
    elif q3 == '친구들과 협동하는 플레이':
        for genre in ['MOBA', 'Team-based', 'Party', 'Survival']: genre_scores[genre] += 2
    else:
        for genre in ['Shooter', 'MOBA', 'Battle Royale', 'Strategy']: genre_scores[genre] += 2

    if q4 == '판타지나 마법의 세계':
        for genre in ['RPG', 'Dark Fantasy', 'Adventure', 'MOBA']: genre_scores[genre] += 2
    elif q4 == '공상 과학(SF) 또는 우주':
        for genre in ['Sci-Fi', 'Shooter']: genre_scores[genre] += 2
    else:
        for genre in ['Simulation', 'Crime', 'Western', 'Tactical']: genre_scores[genre] += 2

    sorted_genres = sorted(genre_scores.items(), key=lambda item: item[1], reverse=True)
    top_genres = [genre for genre, score in sorted_genres if score > 0][:3]

    st.subheader('📈 당신의 게임 성향 분석 결과')
    if not top_genres:
        st.warning('추천할 만한 장르를 찾지 못했습니다. 다른 답변을 시도해 보세요.')
    else:
        st.write(f"당신은 **{', '.join(top_genres)}** 장르를 선호하는 성향을 가지고 있습니다!")
        recommended_games = games_df[games_df['genres'].apply(lambda x: any(g in x for g in top_genres))]
        st.subheader('🎯 추천 게임 목록')
        if recommended_games.empty:
            st.info('아쉽지만 현재 데이터에 추천할 만한 게임이 없네요.')
        else:
            for index, row in recommended_games.head(5).iterrows():
                st.markdown(f"**{row['title']}** (장르: {row['genres']})")
