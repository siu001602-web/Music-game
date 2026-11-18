import base64
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Star Trail - Rhythm Game",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        body {
            background-color: #0e1117;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

song1_music = "music/Screen_Recording_20261117_180140_YouTube_17112026.m4a"
song1_img = "Image/SmartSelect_20261117_234657_YouTube.jpg"

song2_music = "music/Screen_Recording_20261118_013745_YouTube_18112026.m4a"
song2_img = "Image/SmartSelect_20261118_014123_YouTube.jpg"

song3_music = "music/Screen_Recording_20261118_180535_YouTube_18112026.m4a"
song3_img = "Image/SmartSelect_20261118_180837_YouTube.jpg"

mashiro_img_path = "Character/SmartSelect_20261118_202345_NAVER.jpg"
maro_img_path = "Character/SmartSelect_20261118_202541_NAVER.jpg"
huya_img_path = "Character/SmartSelect_20261118_174228_NAVER.jpg"
yuni_img_path = "Character/SmartSelect_20261118_003411_NAVER.jpg"
arunyang_img_path = "Character/SmartSelect_20261118_010700_NAVER.jpg"
baku_img_path = "Character/SmartSelect_20261118_174346_NAVER.jpg"

mashiro_voice_path = "voice/Screen_Recording_20261118_202921_YouTube_18112026.m4a"
yuni_voice_path = "voice/Screen_Recording_20261118_004242_YouTube_18112026.m4a"
huya_voice_path = "voice/Screen_Recording_20261118_175438_YouTube_18112026.m4a"

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

audio1_base64 = get_base64(song1_music)
image1_base64 = get_base64(song1_img)
audio2_base64 = get_base64(song2_music)
image2_base64 = get_base64(song2_img)
audio3_base64 = get_base64(song3_music)
image3_base64 = get_base64(song3_img)

mashiro_base64 = get_base64(mashiro_img_path)
maro_base64 = get_base64(maro_img_path)
huya_base64 = get_base64(huya_img_path)
yuni_base64 = get_base64(yuni_img_path)
arunyang_base64 = get_base64(arunyang_img_path)
baku_base64 = get_base64(baku_img_path)

mashiro_voice_base64 = get_base64(mashiro_voice_path)
yuni_voice_base64 = get_base64(yuni_voice_path)
huya_voice_base64 = get_base64(huya_voice_path)

# 사이드바 악보 및 난이도 선택 설정
st.sidebar.title("🎵 악보 및 게임 설정")
selected_song_title = st.sidebar.selectbox(
    "플레이할 악보 선택",
    ["Star Trail", "삐질게", "별자리가 될 수 있다면"]
)

selected_diff_label = st.sidebar.selectbox(
    "난이도 선택",
    ["쉬움 (Easy)", "보통 (Normal)", "하드 (Hard)", "익스퍼트 (Expert)"]
)

song_map = {
    "Star Trail": {"id": "startrail", "audio": audio1_base64, "thumb": image1_base64, "duration": 225},
    "삐질게": {"id": "bbijilge", "audio": audio2_base64, "thumb": image2_base64, "duration": 144},
    "별자리가 될 수 있다면": {"id": "constellation", "audio": audio3_base64, "thumb": image3_base64, "duration": 255}
}

diff_map = {
    "쉬움 (Easy)": "easy",
    "보통 (Normal)": "normal",
    "하드 (Hard)": "hard",
    "익스퍼트 (Expert)": "expert"
}

current_song = song_map[selected_song_title]
current_diff_key = diff_map[selected_diff_label]

rhythm_game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {
    box-sizing: border-box;
    touch-action: manipulation;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    user-select: none;
  }
  html, body {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    background-color: #0e1117;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  #app-wrapper {
    position: relative;
    width: 100%;
    max-width: 480px;
    height: 100vh;
    max-height: 840px;
    background-color: #0e1117;
    border-left: 2px solid #30363d;
    border-right: 2px solid #30363d;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.15);
    overflow: hidden;
  }

  #menu-screen {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    background: linear-gradient(rgba(14, 17, 23, 0.94), rgba(14, 17, 23, 0.94)), url('data:image/jpeg;base64,{current_song["thumb"]}');
    background-size: cover;
    background-position: center;
    padding: 14px;
    text-align: center;
  }

  #play-screen {
    width: 100%;
    height: 100%;
    display: none;
    position: relative;
    background-color: #161b22;
  }

  canvas {
    width: 100%;
    height: 100%;
    display: block;
    background: linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('data:image/jpeg;base64,{current_song["thumb"]}');
    background-size: cover;
    background-position: center;
    touch-action: none;
  }

  .nav-tabs {
    display: flex; gap: 3px; width: 100%;
    background: rgba(22, 27, 34, 0.9); padding: 5px;
    border-radius: 12px; border: 1px solid #30363d; margin-bottom: 8px;
  }
  .nav-tab {
    flex: 1; padding: 6px 0; font-size: 10px; font-weight: bold;
    color: #8b949e; background: transparent; border: none; border-radius: 8px; cursor: pointer;
  }
  .nav-tab.active { color: #0e1117; background: #00f2fe; box-shadow: 0 2px 10px rgba(0, 242, 254, 0.3); }

  .tab-content { width: 100%; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow-y: auto; }

  .section-title { font-size: 11px; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }

  .unit-slots { display: flex; gap: 8px; margin-bottom: 8px; width: 100%; }
  .unit-slot {
    flex: 1; background: #161b22; border: 2px dashed #30363d; border-radius: 12px;
    height: 105px; display: flex; flex-direction: column; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.2s; position: relative; padding: 6px; text-align: center;
  }
  .unit-slot.filled { border-style: solid; }
  .unit-slot.filled.star-5 { border-color: #facc15; box-shadow: 0 0 8px rgba(250, 204, 21, 0.3); }
  .unit-slot.filled.star-4 { border-color: #c084fc; box-shadow: 0 0 8px rgba(192, 132, 252, 0.3); }
  
  .plus-icon { font-size: 26px; color: #8b949e; font-weight: bold; margin-bottom: 2px; }
  .slot-img { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; margin-bottom: 2px; border: 2px solid currentColor; }

  #char-select-modal {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(14, 17, 23, 0.96); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 30; padding: 20px;
  }
  .char-select-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; margin-bottom: 14px; max-height: 360px; overflow-y: auto; }
  .char-option-card {
    background: #161b22; border: 2px solid #30363d; border-radius: 12px; padding: 10px;
    display: flex; flex-direction: column; align-items: center; cursor: pointer; text-align: center;
  }
  .char-option-card.owned { border-color: #00f2fe; }

  .prep-skill-card {
    background: rgba(255, 121, 198, 0.1); border: 1px solid #ff79c6; border-radius: 8px;
    padding: 8px 10px; margin-bottom: 8px; font-size: 11px; width: 100%; text-align: left;
  }

  .action-btn {
    padding: 10px 24px; font-size: 14px; font-weight: bold; color: #0e1117; background: #00f2fe;
    border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
  }

  .stats-box {
    background: rgba(255, 255, 255, 0.08); border: 1px solid #30363d; border-radius: 10px;
    padding: 8px 14px; margin: 2px 0 8px 0; width: 100%; text-align: left; font-size: 11px; line-height: 1.4;
  }
  .controls-hint { margin-top: 6px; font-size: 10px; color: #8b949e; }

  .gacha-box {
    background: #161b22; border: 2px solid #30363d; border-radius: 14px; padding: 16px;
    width: 100%; display: flex; flex-direction: column; align-items: center; gap: 10px;
  }
  .gacha-btn-group { display: flex; gap: 10px; width: 100%; }
  .gacha-btn { flex: 1; padding: 10px; font-size: 13px; font-weight: bold; border: none; border-radius: 20px; cursor: pointer; }
  .gacha-btn.single { background: #21262d; color: #00f2fe; border: 1px solid #00f2fe; }
  .gacha-btn.multi { background: #00f2fe; color: #0e1117; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); }

  #gacha-result-modal {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(14, 17, 23, 0.95); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 25; padding: 20px;
  }

  .skill-popup {
    position: absolute; right: 55px;
    display: flex; align-items: center; gap: 8px; background: rgba(0, 242, 254, 0.25);
    border: 2px solid #00f2fe; border-radius: 30px; padding: 4px 12px 4px 4px; z-index: 20;
    opacity: 0; transform: translateY(-10px); transition: all 0.3s ease; pointer-events: none;
  }
  .skill-popup.show { opacity: 1; transform: translateY(0); }
  .skill-popup img { width: 30px; height: 30px; border-radius: 50%; object-fit: cover; }

  #mashiro-popup { top: 12px; border-color: #facc15; background: rgba(250, 204, 21, 0.25); }
  #fever-popup { top: 56px; border-color: #ff79c6; background: rgba(255, 121, 198, 0.25); }

  #giveup-btn {
    position: absolute; top: 12px; right: 12px; width: 36px; height: 36px;
    background: rgba(255, 75, 75, 0.2); border: 2px solid #ff4b4b; border-radius: 50%;
    color: #ff4b4b; font-size: 16px; font-weight: bold; display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 25; transition: all 0.2s;
  }

  #hp-bar-container {
    position: absolute; top: 12px; left: 18px; width: 140px;
    background: rgba(14, 17, 23, 0.85); border: 2px solid #30363d; border-radius: 10px;
    padding: 4px 8px; display: flex; flex-direction: column; gap: 2px; z-index: 20;
  }
  .hp-gauge-bg { width: 100%; height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; }
  .hp-gauge-fill { width: 100%; height: 100%; background: #4ade80; transition: width 0.1s linear; }

  #skill-gauges-wrapper {
    position: absolute; bottom: 12px; right: 12px;
    display: flex; flex-direction: column; gap: 6px; z-index: 20;
  }
  .skill-bar-box {
    background: rgba(14, 17, 23, 0.85); border: 2px solid #30363d; border-radius: 12px;
    padding: 5px 10px; display: none; flex-direction: column; align-items: center; gap: 2px;
  }
  .gauge-bg { width: 95px; height: 6px; background: #21262d; border-radius: 4px; overflow: hidden; }
  .gauge-fill { width: 0%; height: 100%; transition: width 0.1s linear; }

  .mission-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 10px;
    width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;
  }
</style>
</head>
<body>

<audio id="game-bgm" preload="auto">
  <source src="data:audio/mp4;base64,{current_song['audio']}" type="audio/mp4">
</audio>
<audio id="mashiro-voice" preload="auto">
  <source src="data:audio/mp4;base64,{mashiro_voice_base64}" type="audio/mp4">
</audio>

<div id="app-wrapper">

  <div id="menu-screen">
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 4px;">
      <h1 id="main-title" style="margin: 0; color: #00f2fe; font-size: 16px;">🎵 {selected_song_title}</h1>
      <div style="background: #161b22; border: 1px solid #facc15; border-radius: 12px; padding: 3px 10px; font-size: 12px; font-weight: bold; color: #facc15;">
        ⭐ 스텔라: <span id="stella-count">100</span>개
      </div>
    </div>
    
    <div class="nav-tabs">
      <button class="nav-tab active" data-tab="songs">🎸 유니트/시작</button>
      <button class="nav-tab" data-tab="gacha">🎁 뽑기</button>
      <button class="nav-tab" data-tab="characters">👤 도감</button>
      <button class="nav-tab" data-tab="missions">📋 임무</button>
      <button class="nav-tab" data-tab="settings">💾 데이터</button>
    </div>

    <div id="tab-songs" class="tab-content">
      <div id="stats-container" class="stats-box" style="display: none;"></div>

      <div style="width: 100%; display: flex; flex-direction: column; align-items: center; padding: 4px;">
        <div class="section-title" style="align-self: flex-start;">출전 유니트 편성 (캐릭터 2명)</div>
        <div class="unit-slots">
          <div id="slot-1" class="unit-slot" onclick="openCharSelector(0)">
            <div class="plus-icon">+</div>
            <div style="font-size: 10px; color: #8b949e;">슬롯 1</div>
          </div>
          <div id="slot-2" class="unit-slot" onclick="openCharSelector(1)">
            <div class="plus-icon">+</div>
            <div style="font-size: 10px; color: #8b949e;">슬롯 2</div>
          </div>
        </div>

        <div id="synergy-card" class="prep-skill-card" style="opacity: 0.5;">
          <div style="font-weight: bold; color: #8b949e; margin-bottom: 2px;">✨ 활성화된 시너지 없음</div>
          <div style="font-size: 10px; color: #8b949e;">• [네네코 마시로 + 마로] 편성 시 [냥냥 집사의 특급 후원] 발동!</div>
        </div>

        <div style="background: rgba(0, 242, 254, 0.08); border: 1px solid #00f2fe; border-radius: 10px; padding: 8px 12px; margin-bottom: 6px; font-size: 11px; width: 100%; text-align: left;">
          <div style="font-weight: bold; color: #00f2fe;">🏆 선택 곡: {selected_song_title} ({selected_diff_label})</div>
          <div style="color: #8b949e; font-size: 10px; margin-top: 2px;">사이드바에서 악보 및 난이도를 변경할 수 있습니다.</div>
        </div>
      </div>

      <button id="start-btn" class="action-btn" style="margin-top: 4px;">라이브 시작하기</button>

      <div class="controls-hint">
        🎹 노트: <b>[D] [F] [J] [K]</b> | 슬라이드: <b>[←][→]</b> 또는 <b>[A][L]</b>
      </div>
    </div>

    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="gacha-box">
        <div style="font-size: 32px;">🌟</div>
        <div style="font-size: 15px; font-weight: bold; color: #00f2fe;">스타 스카우트 (캐릭터 뽑기)</div>
        <div style="font-size: 11px; color: #8b949e; text-align: center; line-height: 1.4;">
          • ⭐⭐⭐⭐⭐ 5성 픽업 (시로, 후야, 유니)<br>
          • ⭐⭐⭐⭐ 4성 픽업 (마로, 아르냥, 바쿠)
        </div>
        <div style="font-size: 12px; color: #facc15; font-weight: bold; margin: 4px 0;">소모 재화: 1회당 스텔라 10개</div>
        <div class="gacha-btn-group">
          <button id="gacha-1-btn" class="gacha-btn single">1회 스카우트 (10개)</button>
          <button id="gacha-10-btn" class="gacha-btn multi">10회 스카우트 (100개)</button>
        </div>
      </div>
    </div>

    <div id="tab-characters" class="tab-content" style="display: none;">
      <div class="section-title">보유 캐릭터 도감</div>
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; width: 100%; margin-top: 4px;">
        <div id="char-card-mashiro" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-mashiro-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-mashiro-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">네네코 마시로</div>
        </div>
        <div id="char-card-huya" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-huya-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-huya-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">사키하네 후야</div>
        </div>
        <div id="char-card-yuni" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-yuni-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-yuni-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">아야츠노 유니</div>
        </div>
        <div id="char-card-maro" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-maro-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-maro-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">마로</div>
        </div>
        <div id="char-card-arunyang" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-arunyang-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-arunyang-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">아르냥</div>
        </div>
        <div id="char-card-baku" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-baku-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-baku-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">바쿠</div>
        </div>
      </div>
    </div>

    <div id="tab-missions" class="tab-content" style="display: none; align-items: flex-start; padding: 4px;">
      <div class="section-title">출석 체크</div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;">
          <b>📅 일일 출석 보상</b><br><span style="color: #8b949e; font-size: 10px;">스텔라 30개 수령</span>
        </div>
        <button id="attendance-btn" onclick="claimAttendance()" style="padding: 6px 12px; font-size: 11px; font-weight: bold; background: #00f2fe; color: #0e1117; border: none; border-radius: 12px; cursor: pointer;">수령하기</button>
      </div>
    </div>

    <div id="tab-settings" class="tab-content" style="display: none; align-items: center; justify-content: center; padding: 10px;">
      <div class="gacha-box">
        <div style="font-size: 24px;">💾</div>
        <div style="font-size: 14px; font-weight: bold; color: #00f2fe;">게임 데이터 관리</div>
        <button onclick="resetGameData()" style="background: transparent; color: #ff4b4b; border: 1px solid #ff4b4b; border-radius: 10px; padding: 6px; font-size: 11px; font-weight: bold; cursor: pointer; width: 100%;">데이터 초기화</button>
      </div>
    </div>
  </div>

  <div id="play-screen">
    <canvas id="gameCanvas" width="480" height="720"></canvas>
    <button id="giveup-btn" onclick="requestGiveUp()" title="중도포기">✕</button>

    <div id="hp-bar-container">
      <div style="display: flex; justify-content: space-between; font-size: 9px; font-weight: bold; color: #4ade80;">
        <span>❤️ HP</span>
        <span id="hp-text">100 / 100</span>
      </div>
      <div class="hp-gauge-bg"><div id="hp-fill" class="hp-gauge-fill"></div></div>
    </div>

    <div id="mashiro-popup" class="skill-popup">
      <img src="data:image/jpeg;base64,{mashiro_base64}">
      <span style="font-size: 11px; font-weight: bold; color: #facc15;">[반갑쟈나~] 발동!</span>
    </div>

    <div id="fever-popup" class="skill-popup">
      <span style="font-size: 11px; font-weight: bold; color: #ff79c6;">🐾 [냥냥 피버] 충전 25% UP!</span>
    </div>

    <div id="skill-gauges-wrapper">
      <div id="mashiro-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #facc15;">🐾 [반갑쟈나~]</div>
        <div class="gauge-bg"><div id="mashiro-gauge-fill" class="gauge-fill" style="background: #facc15;"></div></div>
        <div id="mashiro-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div>
      </div>
    </div>
  </div>

  <div id="char-select-modal">
    <div style="font-size: 15px; font-weight: bold; color: #00f2fe; margin-bottom: 10px;">👤 편성할 캐릭터 선택</div>
    <div class="char-select-grid" id="char-select-list"></div>
    <button id="modal-close-btn" style="padding: 6px 20px; font-size: 12px; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 20px; cursor: pointer;">닫기</button>
  </div>

  <div id="gacha-result-modal">
    <div style="font-size: 16px; font-weight: bold; color: #facc15; margin-bottom: 10px;">🎁 뽑기 결과</div>
    <div id="gacha-result-list" style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-bottom: 15px;"></div>
    <button id="gacha-close-btn" class="action-btn">확인</button>
  </div>
</div>

<script>
const menuScreen = document.getElementById('menu-screen');
const playScreen = document.getElementById('play-screen');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const mainTitle = document.getElementById('main-title');
const statsContainer = document.getElementById('stats-container');
const gameBgm = document.getElementById('game-bgm');
const hpFill = document.getElementById('hp-fill');
const hpText = document.getElementById('hp-text');

const mashiroVoice = document.getElementById('mashiro-voice');
const mashiroPopup = document.getElementById('mashiro-popup');
const feverPopup = document.getElementById('fever-popup');
const mashiroSkillBar = document.getElementById('mashiro-skill-bar');
const mashiroGaugeFill = document.getElementById('mashiro-gauge-fill');
const mashiroSkillStatus = document.getElementById('mashiro-skill-status');

const stellaCountEl = document.getElementById('stella-count');
const gacha1Btn = document.getElementById('gacha-1-btn');
const gacha10Btn = document.getElementById('gacha-10-btn');
const gachaModal = document.getElementById('gacha-result-modal');
const gachaResultList = document.getElementById('gacha-result-list');
const gachaCloseBtn = document.getElementById('gacha-close-btn');

const charSelectModal = document.getElementById('char-select-modal');
const charSelectList = document.getElementById('char-select-list');
const modalCloseBtn = document.getElementById('modal-close-btn');

const navTabs = document.querySelectorAll('.nav-tab');
const tabContents = {
  songs: document.getElementById('tab-songs'),
  gacha: document.getElementById('tab-gacha'),
  characters: document.getElementById('tab-characters'),
  missions: document.getElementById('tab-missions'),
  settings: document.getElementById('tab-settings')
};

function switchView(viewName) {
  menuScreen.style.display = (viewName === 'menu') ? 'flex' : 'none';
  playScreen.style.display = (viewName === 'play') ? 'block' : 'none';
}

navTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    navTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const target = tab.getAttribute('data-tab');
    Object.keys(tabContents).forEach(key => {
      tabContents[key].style.display = (key === target) ? 'flex' : 'none';
    });
  });
});

let stella = 100;
let ownedCharacters = { mashiro: false, huya: false, yuni: false, maro: false, arunyang: false, baku: false };
let equippedUnit = [null, null];
let activeSlotIndex = null;
let missionData = { attendanceClaimed: false };

function loadGameData() {
  const savedStella = localStorage.getItem('rhythm_stella');
  if (savedStella !== null) stella = parseInt(savedStella);
  const savedChars = localStorage.getItem('rhythm_chars');
  if (savedChars !== null) ownedCharacters = JSON.parse(savedChars);
}

function saveGameData() {
  localStorage.setItem('rhythm_stella', stella);
  localStorage.setItem('rhythm_chars', JSON.stringify(ownedCharacters));
}

function resetGameData() {
  if (confirm("정말 모든 데이터를 초기화하시겠습니까?")) {
    localStorage.clear();
    location.reload();
  }
}

loadGameData();

let isPlaying = false;
let startTime = 0;
let score = 0;
let combo = 0;
let maxCombo = 0;
let currentHp = 100;
const maxHp = 100;
let stats = { perfect: 0, great: 0, good: 0, miss: 0 };
let notes = [];
let keyPressed = [false, false, false, false];
let activeTouches = new Map();

let mashiroSkillGauge = 0;
let mashiroSkillActivated = false;
let mashiroSkillTimer = 0;
let feverTimer = 0;
let feverActive = false;
let lastFeverMinute = 0;

const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 570;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

function updateInventoryUI() {
  stellaCountEl.innerText = stella;
  const charMeta = {
    mashiro: { name: '네네코 마시로', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{mashiro_base64}' },
    huya: { name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{huya_base64}' },
    yuni: { name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{yuni_base64}' },
    maro: { name: '마로', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{maro_base64}' },
    arunyang: { name: '아르냥', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{arunyang_base64}' },
    baku: { name: '바쿠', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{baku_base64}' }
  };

  for (let i = 0; i < 2; i++) {
    const slotEl = document.getElementById(`slot-${i+1}`);
    const charId = equippedUnit[i];
    if (charId && charMeta[charId]) {
      const m = charMeta[charId];
      slotEl.className = `unit-slot filled`;
      slotEl.innerHTML = `<img src="data:image/jpeg;base64,{mashiro_base64}" class="slot-img"><div style="font-size:10px; font-weight:bold; color:${m.color};">${m.name}</div>`;
    } else {
      slotEl.className = "unit-slot";
      slotEl.innerHTML = `<div class="plus-icon">+</div><div style="font-size: 10px; color: #8b949e;">슬롯 ${i+1}</div>`;
    }
  }

  const synergyCard = document.getElementById('synergy-card');
  const hasMashiro = equippedUnit.includes('mashiro');
  const hasMaro = equippedUnit.includes('maro');
  if (hasMashiro && hasMaro) {
    synergyCard.style.opacity = "1";
    synergyCard.style.borderColor = "#facc15";
    synergyCard.innerHTML = `<div style="font-weight: bold; color: #facc15;">🐾 [냥냥 집사의 특급 후원] 활성화!</div>`;
  } else {
    synergyCard.style.opacity = "0.5";
    synergyCard.style.borderColor = "#30363d";
    synergyCard.innerHTML = `<div style="font-weight: bold; color: #8b949e;">✨ 시너지 없음 (마시로+마로 조합 필요)</div>`;
  }

  Object.keys(charMeta).forEach(key => {
    if (ownedCharacters[key]) {
      const m = charMeta[key];
      const card = document.getElementById(`char-card-${key}`);
      if (card) {
        card.style.borderColor = m.color;
        document.getElementById(`char-${key}-badge`).innerHTML = `${m.star} (보유)`;
        document.getElementById(`char-${key}-badge`).style.color = m.color;
      }
    }
  });
}

function openCharSelector(slotIndex) {
  activeSlotIndex = slotIndex;
  charSelectList.innerHTML = "";
  const availableChars = [
    { id: 'mashiro', name: '네네코 마시로', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.mashiro, color: '#facc15' },
    { id: 'huya', name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.huya, color: '#facc15' },
    { id: 'yuni', name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.yuni, color: '#facc15' },
    { id: 'maro', name: '마로', star: '⭐⭐⭐⭐', owned: ownedCharacters.maro, color: '#c084fc' },
    { id: 'arunyang', name: '아르냥', star: '⭐⭐⭐⭐', owned: ownedCharacters.arunyang, color: '#c084fc' },
    { id: 'baku', name: '바쿠', star: '⭐⭐⭐⭐', owned: ownedCharacters.baku, color: '#c084fc' }
  ];

  availableChars.forEach(char => {
    const card = document.createElement('div');
    card.className = `char-option-card ${char.owned ? 'owned' : ''}`;
    card.style.opacity = char.owned ? "1" : "0.45";
    card.innerHTML = `
      <div style="font-size:10px; color:${char.color};">${char.star}</div>
      <div style="font-size:11px; font-weight:bold; margin-top:2px;">${char.name}</div>
      <div style="font-size:9px; color:${char.owned ? '#00f2fe' : '#8b949e'}; margin-top:2px;">${char.owned ? '선택 가능' : '미획득'}</div>
    `;
    if (char.owned) {
      card.addEventListener('click', () => {
        equippedUnit[activeSlotIndex] = char.id;
        charSelectModal.style.display = "none";
        updateInventoryUI();
      });
    }
    charSelectList.appendChild(card);
  });
  charSelectModal.style.display = "flex";
}

modalCloseBtn.addEventListener('click', () => { charSelectModal.style.display = "none"; });

function executeGacha(count) {
  const cost = count * 10;
  if (stella < cost) {
    alert("스텔라 재화가 부족합니다!");
    return;
  }
  stella -= cost;
  updateInventoryUI();
  saveGameData();

  let results = [];
  const keys = ['mashiro', 'huya', 'yuni', 'maro', 'arunyang', 'baku'];
  for (let i = 0; i < count; i++) {
    const picked = keys[Math.floor(Math.random() * keys.length)];
    ownedCharacters[picked] = true;
    results.push({ name: picked });
  }
  updateInventoryUI();
  saveGameData();

  gachaResultList.innerHTML = "";
  results.forEach(res => {
    const item = document.createElement('div');
    item.style.cssText = "background:#21262d; border:1px solid #00f2fe; border-radius:10px; padding:8px; text-align:center; width:88px;";
    item.innerHTML = `<div style="font-size:10px; font-weight:bold; margin-top:2px;">${res.name}</div>`;
    gachaResultList.appendChild(item);
  });
  gachaModal.style.display = "flex";
}

gacha1Btn.addEventListener('click', () => executeGacha(1));
gacha10Btn.addEventListener('click', () => executeGacha(10));
gachaCloseBtn.addEventListener('click', () => { gachaModal.style.display = "none"; });

function claimAttendance() {
  if (!missionData.attendanceClaimed) {
    missionData.attendanceClaimed = true;
    stella += 30;
    updateInventoryUI();
    saveGameData();
    alert("출석 보상으로 스텔라 30개를 획득하셨습니다!");
  }
}

function generateBeatmap() {
  notes = [];
  let currentTime = 2.0;
  const totalDuration = {current_song['duration']};
  let seed = 1234;
  
  while (currentTime < totalDuration - 5.0) {
    seed = (seed * 9301 + 49297) % 233280;
    const lane = Math.floor((seed / 233280) * LANES);
    notes.push({ time: currentTime, lane: lane, type: 'normal', hit: false, missed: false });
    currentTime += 1.2;
  }
}

function startGame() {
  score = 0;
  combo = 0;
  maxCombo = 0;
  currentHp = 100;
  stats = { perfect: 0, great: 0, good: 0, miss: 0 };
  
  generateBeatmap();
  gameBgm.pause();
  gameBgm.currentTime = 0;
  gameBgm.play().catch(e => {});

  isPlaying = true;
  startTime = performance.now();
  switchView('play');
  requestAnimationFrame(updateAndDraw);
}

function requestGiveUp() {
  if (!isPlaying) return;
  isPlaying = false;
  gameBgm.pause();
  switchView('menu');
}

function updateHpUI() {
  const percent = (currentHp / maxHp) * 100;
  hpFill.style.width = percent + '%';
  hpText.innerText = Math.round(currentHp) + ' / ' + maxHp;
}

function updateAndDraw() {
  if (!isPlaying) return;
  const currentTime = (performance.now() - startTime) / 1000;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < LANES; i++) {
    const x = i * LANE_WIDTH;
    ctx.fillStyle = keyPressed[i] ? LANE_COLORS[i] : '#1f2630';
    ctx.fillRect(x + 4, HIT_Y + 8, LANE_WIDTH - 8, canvas.height - HIT_Y - 14);
  }

  ctx.strokeStyle = '#00f2fe';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, HIT_Y);
  ctx.lineTo(canvas.width, HIT_Y);
  ctx.stroke();

  let remainingNotes = 0;
  for (let note of notes) {
    if (note.missed || note.hit) continue;
    remainingNotes++;
    const timeDiff = note.time - currentTime;
    const y = HIT_Y - (timeDiff * 450);

    if (timeDiff < -0.35) {
      note.missed = true;
      combo = 0;
      currentHp = Math.max(0, currentHp - 10);
      updateHpUI();
      continue;
    }

    if (y >= -50 && y <= HIT_Y + 20) {
      ctx.fillStyle = LANE_COLORS[note.lane];
      ctx.beginPath();
      ctx.roundRect(note.lane * LANE_WIDTH + 10, y - 12, LANE_WIDTH - 20, 24, 6);
      ctx.fill();
    }
  }

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 22px sans-serif';
  ctx.fillText(`SCORE: ${score}`, 18, 56);

  if (combo > 1) {
    ctx.fillStyle = '#00f2fe';
    ctx.font = 'bold 34px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${combo} COMBO`, canvas.width / 2, 160);
  }

  if (gameBgm.ended || remainingNotes === 0) {
    isPlaying = false;
    gameBgm.pause();
    stella += 25;
    updateInventoryUI();
    saveGameData();
    mainTitle.innerHTML = "🎉 라이브 클리어! (스텔라 +25)";
    statsContainer.innerHTML = `<div>최종 점수: <b>${score.toLocaleString()}</b></div>`;
    statsContainer.style.display = 'block';
    switchView('menu');
    return;
  }

  requestAnimationFrame(updateAndDraw);
}

window.addEventListener('keydown', (e) => {
  if (!isPlaying) return;
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1) {
    keyPressed[idx] = true;
    combo++;
    score += 100;
  }
});

window.addEventListener('keyup', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1) keyPressed[idx] = false;
});

startBtn.addEventListener('click', startGame);
updateInventoryUI();
</script>
</body>
</html>
"""

components.html(rhythm_game_html, height=820)
