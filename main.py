import streamlit as st
import pandas as pd
from collections import defaultdict

# --- 초기 설정 ---
st.set_page_config(page_title="게임 장르 추천", layout="wide")

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    # 이미지 없는 CSV 파일을 사용합니다.
    df = pd.read_csv('games.csv')
    return df

games_df = load_data()

# --- 질문 및 로직 데이터 ---
questions = {
    1: ("새로운 게임을 시작할 때, 가장 먼저 무엇에 끌리시나요?", 
           {"몰입감 높은 스토리와 세계관": "스토리", "빠른 액션과 타격감": "액션성", "고민이 필요한 전략과 퍼즐": "전략성", "다른 사람들과의 상호작용": "사교성"}),
    2: ("게임 플레이 중 가장 큰 만족을 느낄 때는 언제인가요?", 
           {"강력한 보스를 쓰러뜨렸을 때": "액션성", "나만의 공간이나 캐릭터를 꾸밀 때": "창의성", "복잡한 문제를 해결했을 때": "전략성", "팀원과 협력하여 승리했을 때": "사교성"}),
    3: ("선호하는 게임의 진행 속도는 어떤가요?", 
           {"빠르고 숨 쉴 틈 없는 전개": "액션성", "내 페이스대로 즐기는 여유로운 플레이": "창의성", "신중한 계획이 요구되는 턴(Turn) 방식": "전략성", "예측 불가능하고 매번 다른 경험": "모험성"}),
    4: ("게임에서 실패(죽음 등)했을 때 어떤 감정을 느끼나요?", 
           {"성장의 밑거름! 더 강해져서 돌아온다": "액션성", "괜찮아, 다른 걸 하면 돼": "창의성", "패배 원인을 분석하고 다음 수를 생각한다": "전략성", "아쉽지만, 팀원들과 다음을 기약한다": "사교성"}),
    5: ("게임에서 가장 중요하게 생각하는 요소는 무엇인가요?", 
           {"매력적인 캐릭터와 감동적인 서사": "스토리", "정교한 컨트롤과 즉각적인 피드백": "액션성", "자원 관리와 효율적인 성장": "전략성", "다른 플레이어와의 경쟁 또는 협력": "사교성"}),
    6: ("어떤 종류의 도전을 즐기시나요?", 
           {"강력한 적들과의 전투": "액션성", "창의력을 발휘하는 건설과 제작": "창의성", "두뇌를 자극하는 퍼즐과 수수께끼": "전략성", "예측불허의 상황과 생존 경쟁": "모험성"}),
    7: ("게임의 스토리를 즐기는 방식은 어떤가요?", 
           {"주인공이 되어 스토리를 직접 이끌어간다": "스토리", "한 편의 영화나 소설처럼 감상한다": "스토리", "스토리보다는 게임의 규칙과 시스템이 더 재밌다": "전략성", "다른 플레이어들과 함께 만들어가는 이야기": "사교성"}),
    8: ("선호하는 게임의 비주얼 스타일은 무엇인가요?", 
           {"현실적인 그래픽과 분위기": "모험성", "개성 있는 아트 스타일과 판타지 세계": "스토리", "정보가 명확하게 보이는 깔끔한 인터페이스": "전략성", "다양한 코스튬과 꾸미기 요소": "창의성"}),
    9: ("얼마나 많은 시간을 하나의 게임에 투자하는 편인가요?", 
           {"수백 시간 이상 깊게 파고드는 편": "전략성", "엔딩을 보고 다른 게임을 찾아보는 편": "스토리", "짧은 시간 동안 가볍게 즐기는 편": "액션성", "커뮤니티 활동까지 하며 계속 즐기는 편": "사교성"}),
    10: ("다음 중 가장 흥미로운 활동은 무엇인가요?", 
           {"미지의 세계를 탐험하고 비밀을 밝히는 것": "모험성", "최고의 장비를 맞추고 캐릭터를 성장시키는 것": "액션성", "나만의 제국이나 도시를 건설하고 운영하는 것": "전략성", "랭킹을 올리거나 길드 활동을 하는 것": "사교성"}),
}

trait_to_genre = {
    '스토리': ('RPG', "당신은 매력적인 서사와 깊이 있는 세계관에 몰입하는 것을 즐기는 이야기꾼입니다."),
    '액션성': ('Action', "당신은 즉각적인 반응과 정교한 컨트롤로 역동적인 플레이를 즐기는 해결사입니다."),
    '전략성': ('Strategy', "당신은 신중한 계획과 효율적인 판단으로 도전을 해결하는 지략가입니다."),
    '사교성': ('Multiplayer', "당신은 다른 사람들과 함께 경쟁하거나 협력하며 즐거움을 느끼는 커뮤니케이터입니다."),
    '창의성': ('Simulation', "당신은 자신만의 것을 만들고 꾸미며 자유로운 플레이를 즐기는 아티스트입니다."),
    '모험성': ('Adventure', "당신은 새로운 세계를 탐험하고 예상치 못한 상황을 즐기는 탐험가입니다.")
}

# --- 세션 상태 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'traits' not in st.session_state:
    st.session_state.traits = defaultdict(int)

# --- 페이지별 함수 정의 ---
def home_page():
    st.title('🎯 나의 핵심 게임 장르 찾기')
    st.write('총 10개의 질문에 답하고, 당신의 플레이 성향에 딱 맞는 핵심 장르와 게임을 추천받으세요!')
    if st.button('테스트 시작하기', type="primary"):
        st.session_state.page = 1
        st.rerun()

def question_page(q_num):
    question, options = questions[q_num]
    st.subheader(f"Question {q_num}/{len(questions)}")
    st.header(question)
    
    st.markdown("""
    <style>div.stButton > button { height: 50px; width: 100%; margin: 5px 0; }</style>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, (option, trait) in enumerate(options.items()):
        col = cols[i % 2]
        if col.button(option, key=f"q{q_num}_{i}"):
            st.session_state.answers[q_num] = trait
            if q_num == len(questions):
                st.session_state.page = 'result'
            else:
                st.session_state.page = q_num + 1
            st.rerun()

def result_page():
    for trait in st.session_state.answers.values():
        st.session_state.traits[trait] += 1
    
    if not st.session_state.traits:
        st.warning("분석 결과가 없습니다. 테스트를 다시 시작해주세요.")
        if st.button("처음으로 돌아가기"):
            reset()
        return

    top_trait = max(st.session_state.traits, key=st.session_state.traits.get)
    recommended_genre, description = trait_to_genre[top_trait]

    st.title("✨ 당신의 게임 성향 분석 결과")
    st.header(f'당신의 핵심 성향은 "{top_trait}" 입니다!')
    st.write(description)
    st.success(f"### 🎯 추천 핵심 장르: **{recommended_genre}**")

    st.subheader("📊 당신의 게임 성향 프로필")
    traits_df = pd.DataFrame(list(st.session_state.traits.items()), columns=['성향', '점수']).set_index('성향')
    st.bar_chart(traits_df)

    st.subheader("🎮 추천 게임 목록")
    
    def get_relevance_score(genres_str):
        genres = genres_str.split(';')
        if recommended_genre in genres:
            return len(genres) - genres.index(recommended_genre)
        return 0

    games_df['relevance'] = games_df['genres'].apply(get_relevance_score)
    recommended_games = games_df[games_df['relevance'] > 0].sort_values(by='relevance', ascending=False).head(5)

    if recommended_games.empty:
        st.info('아쉽지만 현재 데이터에 추천할 만한 게임이 없네요.')
    else:
        for _, row in recommended_games.iterrows():
            # 이미지 관련 코드 제거, 텍스트만 출력
            st.markdown(f"#### {row['title']}")
            st.markdown(f"**장르**: {row['genres'].replace(';', ', ')}")
            st.divider()

    if st.button("테스트 다시하기"):
        reset()

def reset():
    st.session_state.page = 'home'
    st.session_state.answers = {}
    st.session_state.traits = defaultdict(int)
    st.rerun()

# --- 메인 로직: 페이지 전환 ---
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'result':
    result_page()
else:
    question_page(st.session_state.page)
