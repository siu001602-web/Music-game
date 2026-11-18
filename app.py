import base64
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Star Trail - Rhythm Game",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# 곡 경로 설정
song1_music = "music/Screen_Recording_20261117_180140_YouTube_17112026.m4a"
song1_img = "Image/SmartSelect_20261117_234657_YouTube.jpg"

song2_music = "music/Screen_Recording_20261118_013745_YouTube_18112026.m4a"
song2_img = "Image/SmartSelect_20261118_014123_YouTube.jpg"

song3_music = "music/Screen_Recording_20261118_180535_YouTube_18112026.m4a"
song3_img = "Image/SmartSelect_20261118_180837_YouTube.jpg"

# '봄꿈' 곡 및 새로운 표지 이미지 경로 설정
song4_music = "music/Screen_Recording_20261118_210521_YouTube_18112026.m4a"
song4_img = "Image/SmartSelect_20261118_211358_YouTube.jpg"

# 캐릭터 및 보이스 경로 설정
mashiro_img_path = "Character/SmartSelect_20261118_202345_NAVER.jpg"     # 시로 (네네코 마시로)
maro_img_path = "Character/SmartSelect_20261118_202541_NAVER.jpg"       # 마로
huya_img_path = "Character/SmartSelect_20261118_174228_NAVER.jpg"       # 후야
yuni_img_path = "Character/SmartSelect_20261118_003411_NAVER.jpg"       # 유니
arunyang_img_path = "Character/SmartSelect_20261118_010700_NAVER.jpg"   # 아르냥
baku_img_path = "Character/SmartSelect_20261118_174346_NAVER.jpg"       # 바쿠

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

audio4_base64 = get_base64(song4_music)
image4_base64 = get_base64(song4_img)

mashiro_base64 = get_base64(mashiro_img_path)
maro_base64 = get_base64(maro_img_path)
huya_base64 = get_base64(huya_img_path)
yuni_base64 = get_base64(yuni_img_path)
arunyang_base64 = get_base64(arunyang_img_path)
baku_base64 = get_base64(baku_img_path)

mashiro_voice_base64 = get_base64(mashiro_voice_path)
yuni_voice_base64 = get_base64(yuni_voice_path)
huya_voice_base64 = get_base64(huya_voice_path)

rhythm_game_html = """
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
    background: linear-gradient(rgba(14, 17, 23, 0.90), rgba(14, 17, 23, 0.94)), url('data:image/jpeg;base64,IMAGE4_BASE64_PLACEHOLDER');
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
    background: linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('data:image/jpeg;base64,IMAGE4_BASE64_PLACEHOLDER');
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

  .section-title { font-size: 11px; color: #8b949e; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }

  .song-grid {
    display: flex;
    flex-direction: row;
    gap: 10px;
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 6px 4px 10px 4px;
    margin-bottom: 10px;
    scrollbar-width: thin;
    scrollbar-color: #00f2fe #161b22;
  }
  .song-grid::-webkit-scrollbar {
    height: 5px;
  }
  .song-grid::-webkit-scrollbar-thumb {
    background: #00f2fe;
    border-radius: 4px;
  }

  .song-card {
    flex: 0 0 102px;
    background: transparent;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: transform 0.2s ease;
    position: relative;
  }
  .song-card:hover {
    transform: translateY(-2px);
  }
  .song-thumb-wrapper {
    position: relative;
    width: 102px;
    height: 102px;
    border-radius: 14px;
    overflow: hidden;
    border: 2.5px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    transition: all 0.2s ease;
  }
  .song-card.selected .song-thumb-wrapper {
    border-color: #00f2fe;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.65);
    transform: scale(1.03);
  }
  .song-thumb {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  .new-badge {
    position: absolute;
    top: 4px;
    right: 4px;
    background: rgba(255, 255, 255, 0.85);
    color: #ff4b82;
    font-size: 9px;
    font-weight: 900;
    padding: 1px 5px;
    border-radius: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
  }
  .song-name {
    margin-top: 6px;
    font-size: 11px;
    font-weight: 700;
    color: #e6edf3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0 2px;
  }
  .song-card.selected .song-name {
    color: #00f2fe;
  }

  .difficulty-select-container { display: flex; gap: 8px; width: 100%; justify-content: center; margin-bottom: 8px; }
  .diff-card {
    flex: 1; background: #161b22; border: 2px solid #30363d; border-radius: 10px;
    padding: 6px 4px; cursor: pointer; text-align: center; transition: all 0.2s;
  }
  .diff-card.selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); background: #1f2630; }
  .diff-card[data-diff="normal"].selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); }
  .diff-card[data-diff="hard"].selected { border-color: #ff4b4b; box-shadow: 0 0 10px rgba(255, 75, 75, 0.4); }
  .diff-card[data-diff="extreme"].selected { border-color: #c084fc; box-shadow: 0 0 10px rgba(192, 132, 252, 0.4); }

  .diff-lv { font-size: 10px; font-weight: bold; color: #8b949e; margin-bottom: 2px; }
  .diff-name { font-size: 11px; font-weight: 900; }
  .diff-card[data-diff="normal"] .diff-name { color: #00f2fe; }
  .diff-card[data-diff="hard"] .diff-name { color: #ff4b4b; }
  .diff-card[data-diff="extreme"] .diff-name { color: #c084fc; }

  .selected-diff-record-box {
    width: 100%;
    background: rgba(22, 27, 34, 0.85);
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 7px 12px;
    margin-bottom: 8px;
    font-size: 11px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  #prep-screen {
    width: 100%; height: 100%;
    background: rgba(14, 17, 23, 0.98); padding: 16px; display: none; flex-direction: column; text-align: left;
  }
  .prep-header { font-size: 14px; font-weight: bold; color: #00f2fe; margin-bottom: 2px; }
  .prep-sub { font-size: 11px; color: #8b949e; margin-bottom: 8px; }
  
  .unit-slots { display: flex; gap: 8px; margin-bottom: 8px; }
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
    padding: 8px 10px; margin-bottom: 8px; font-size: 11px;
  }
  .prep-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }

  .action-btn {
    padding: 9px 22px; font-size: 14px; font-weight: bold; color: #0e1117; background: #00f2fe;
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
  #yuni-popup { top: 56px; border-color: #c084fc; background: rgba(192, 132, 252, 0.25); }
  #huya-popup { top: 100px; border-color: #ff79c6; background: rgba(255, 121, 198, 0.25); }
  #fever-popup { top: 144px; border-color: #4ade80; background: rgba(74, 222, 128, 0.25); }

  #giveup-btn {
    position: absolute; top: 12px; right: 12px; width: 36px; height: 36px;
    background: rgba(255, 75, 75, 0.2); border: 2px solid #ff4b4b; border-radius: 50%;
    color: #ff4b4b; font-size: 16px; font-weight: bold; display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 25; transition: all 0.2s;
  }
  #giveup-btn:hover { background: rgba(255, 75, 75, 0.4); transform: scale(1.05); }

  #hp-bar-container {
    position: absolute; top: 12px; left: 18px; width: 140px;
    background: rgba(14, 17, 23, 0.85); border: 2px solid #30363d; border-radius: 10px;
    padding: 4px 8px; display: flex; flex-direction: column; gap: 2px; z-index: 20;
  }
  .hp-gauge-bg { width: 100%; height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; }
  .hp-gauge-fill { width: 100%; height: 100%; background: #4ade80; transition: width 0.1s linear, background-color 0.2s; }

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

<audio id="bgm1" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO1_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="bgm2" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO2_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="bgm3" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO3_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="bgm4" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO4_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="mashiro-voice" preload="auto">
  <source src="data:audio/mp4;base64,MASHIRO_VOICE_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="yuni-voice" preload="auto">
  <source src="data:audio/mp4;base64,YUNI_VOICE_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="huya-voice" preload="auto">
  <source src="data:audio/mp4;base64,HUYA_VOICE_PLACEHOLDER" type="audio/mp4">
</audio>

<div id="app-wrapper">

  <div id="menu-screen">
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 4px;">
      <h1 id="main-title" style="margin: 0; color: #00f2fe; font-size: 18px;">RHYTHM STAR</h1>
      <div style="background: #161b22; border: 1px solid #facc15; border-radius: 12px; padding: 3px 10px; font-size: 12px; font-weight: bold; color: #facc15;">
        ⭐ 스텔라: <span id="stella-count">100</span>개
      </div>
    </div>
    
    <div id="nav-tabs" class="nav-tabs">
      <button class="nav-tab active" data-tab="songs">🎵 악보</button>
      <button class="nav-tab" data-tab="gacha">🎁 뽑기</button>
      <button class="nav-tab" data-tab="characters">👤 도감</button>
      <button class="nav-tab" data-tab="missions">📋 임무</button>
      <button class="nav-tab" data-tab="settings">💾 데이터</button>
    </div>

    <div id="tab-songs" class="tab-content">
      <div id="stats-container" class="stats-box" style="display: none;"></div>

      <div id="menu-group" style="width: 100%; display: flex; flex-direction: column; align-items: center;">
        <div class="section-title">Select Song (좌우로 밀어 악보 선택)</div>
        <div id="song-list" class="song-grid"></div>

        <div class="section-title">Difficulty (난이도 선택)</div>
        <div id="difficulty-container" class="difficulty-select-container"></div>

        <div class="selected-diff-record-box">
          <span id="menu-diff-label" style="font-weight: bold; color: #00f2fe;">🏆 [보통] 최고 기록</span>
          <span id="menu-diff-record" style="color: #fff;">기록 없음 (RANK: -)</span>
        </div>
      </div>

      <button id="next-prep-btn" class="action-btn" style="margin-top: 4px; padding: 9px 22px; font-size: 14px;">유니트 편성 및 라이브</button>

      <div id="controls-hint" class="controls-hint">
        🎹 노트: <b>[D] [F] [J] [K]</b> | 터치: <b>화면 각 레인 탭</b>
      </div>
    </div>

    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="gacha-box">
        <div style="font-size: 32px;">🌟</div>
        <div style="font-size: 15px; font-weight: bold; color: #00f2fe;">스타 스카우트 (캐릭터 뽑기)</div>
        <div style="font-size: 11px; color: #8b949e; text-align: center; line-height: 1.4;">
          • ⭐⭐⭐⭐⭐ 5성 픽업 (합산 3%): 시로, 후야, 유니<br>
          • ⭐⭐⭐⭐ 4성 픽업 (합산 97%): 마로, 아르냥, 바쿠
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
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">네네코 마시로 (시로)</div>
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
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">마로 (팬)</div>
        </div>
        <div id="char-card-arunyang" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-arunyang-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-arunyang-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">아르냥 (팬)</div>
        </div>
        <div id="char-card-baku" class="unit-slot filled" style="height: auto; padding: 10px; border-color: #30363d;">
          <div id="char-baku-img-box" style="font-size: 24px; margin-bottom: 2px;">👤</div>
          <div id="char-baku-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">바쿠 (팬)</div>
        </div>
      </div>
    </div>

    <div id="tab-missions" class="tab-content" style="display: none; align-items: flex-start; padding: 4px;">
      <div class="section-title">출석 체크 (매일 보상)</div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;">
          <b>📅 일일 출석 보상</b><br>
          <span style="color: #8b949e; font-size: 10px;">매일 접속하고 스텔라 30개를 받으세요!</span>
        </div>
        <button id="attendance-btn" onclick="claimAttendance()" style="padding: 6px 12px; font-size: 11px; font-weight: bold; background: #00f2fe; color: #0e1117; border: none; border-radius: 12px; cursor: pointer;">수령하기</button>
      </div>
    </div>

    <div id="tab-settings" class="tab-content" style="display: none; align-items: center; justify-content: center; padding: 10px;">
      <div class="gacha-box">
        <div style="font-size: 24px;">💾</div>
        <div style="font-size: 14px; font-weight: bold; color: #00f2fe;">게임 데이터 백업 및 복원</div>
        <div style="display: flex; gap: 8px; width: 100%; margin-top: 8px;">
          <button onclick="exportSaveData()" class="gacha-btn" style="background: #21262d; color: #4ade80; border: 1px solid #4ade80;">데이터 내보내기</button>
          <button onclick="importSaveDataPrompt()" class="gacha-btn" style="background: #00f2fe; color: #0e1117;">데이터 불러오기</button>
        </div>
        <button onclick="resetGameData()" style="background: transparent; color: #ff4b4b; border: 1px solid #ff4b4b; border-radius: 10px; padding: 6px; font-size: 11px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 4px;">데이터 초기화</button>
      </div>
    </div>
  </div>

  <div id="prep-screen">
    <div class="prep-header" id="prep-song-title">🎵 봄꿈</div>
    <div class="prep-sub">+ 버튼을 눌러 출전할 캐릭터 2명을 편성하세요.</div>

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
    </div>

    <div style="background: rgba(0, 242, 254, 0.08); border: 1px solid #00f2fe; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; font-size: 12px;">
      <div style="font-weight: bold; color: #00f2fe; margin-bottom: 2px;" id="prep-record-title">🏆 [보통] 최고 기록</div>
      <div id="prep-record-content" style="color: #fff;">점수: 0점 (RANK: -)</div>
    </div>

    <div class="prep-footer">
      <button id="prep-back-btn" style="padding: 8px 16px; font-size: 12px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 20px; cursor: pointer;">취소</button>
      <button id="prep-start-btn" class="action-btn" style="padding: 8px 22px; font-size: 14px;">결정 (라이브 시작)</button>
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
      <img src="data:image/jpeg;base64,MASHIRO_IMG_PLACEHOLDER">
      <span style="font-size: 11px; font-weight: bold; color: #facc15;">[반갑쟈나~] 발동!</span>
    </div>

    <div id="yuni-popup" class="skill-popup">
      <img src="data:image/jpeg;base64,YUNI_IMG_PLACEHOLDER">
      <span style="font-size: 11px; font-weight: bold; color: #c084fc;">[뭘뽀노?] 발동!</span>
    </div>

    <div id="huya-popup" class="skill-popup">
      <img src="data:image/jpeg;base64,HUYA_IMG_PLACEHOLDER">
      <span style="font-size: 11px; font-weight: bold; color: #ff79c6;">[포근한 꿈결 속으로] 발동!</span>
    </div>

    <div id="fever-popup" class="skill-popup">
      <span style="font-size: 11px; font-weight: bold; color: #4ade80;">✨ [더블 스킬] 점수 +25% 폭발!</span>
    </div>

    <div id="skill-gauges-wrapper">
      <div id="mashiro-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #facc15;">🐾 [반갑쟈나~]</div>
        <div class="gauge-bg"><div id="mashiro-gauge-fill" class="gauge-fill" style="background: #facc15;"></div></div>
        <div id="mashiro-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div>
      </div>
      <div id="yuni-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #c084fc;">✨ [뭘뽀노?]</div>
        <div class="gauge-bg"><div id="yuni-gauge-fill" class="gauge-fill" style="background: #c084fc;"></div></div>
        <div id="yuni-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div>
      </div>
      <div id="huya-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #ff79c6;">💤 [포근한 꿈결]</div>
        <div class="gauge-bg"><div id="huya-gauge-fill" class="gauge-fill" style="background: #ff79c6;"></div></div>
        <div id="huya-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div>
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
    <div id="gacha-result-list" style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-bottom: 15px; max-height: 360px; overflow-y: auto;"></div>
    <button id="gacha-close-btn" class="action-btn">확인</button>
  </div>

</div>

<script>
const menuScreen = document.getElementById('menu-screen');
const prepScreen = document.getElementById('prep-screen');
const playScreen = document.getElementById('play-screen');

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('prep-start-btn');
const nextPrepBtn = document.getElementById('next-prep-btn');
const prepBackBtn = document.getElementById('prep-back-btn');
const prepSongTitle = document.getElementById('prep-song-title');
const prepRecordTitle = document.getElementById('prep-record-title');
const prepRecordContent = document.getElementById('prep-record-content');

const menuDiffLabel = document.getElementById('menu-diff-label');
const menuDiffRecord = document.getElementById('menu-diff-record');
const difficultyContainer = document.getElementById('difficulty-container');

const hpFill = document.getElementById('hp-fill');
const hpText = document.getElementById('hp-text');

const bgm1 = document.getElementById('bgm1');
const bgm2 = document.getElementById('bgm2');
const bgm3 = document.getElementById('bgm3');
const bgm4 = document.getElementById('bgm4');

const mashiroVoice = document.getElementById('mashiro-voice');
const yuniVoice = document.getElementById('yuni-voice');
const huyaVoice = document.getElementById('huya-voice');

const mashiroPopup = document.getElementById('mashiro-popup');
const yuniPopup = document.getElementById('yuni-popup');
const huyaPopup = document.getElementById('huya-popup');
const feverPopup = document.getElementById('fever-popup');

const mashiroSkillBar = document.getElementById('mashiro-skill-bar');
const mashiroGaugeFill = document.getElementById('mashiro-gauge-fill');
const mashiroSkillStatus = document.getElementById('mashiro-skill-status');

const yuniSkillBar = document.getElementById('yuni-skill-bar');
const yuniGaugeFill = document.getElementById('yuni-gauge-fill');
const yuniSkillStatus = document.getElementById('yuni-skill-status');

const huyaSkillBar = document.getElementById('huya-skill-bar');
const huyaGaugeFill = document.getElementById('huya-gauge-fill');
const huyaSkillStatus = document.getElementById('huya-skill-status');

const stellaCountEl = document.getElementById('stella-count');

const gacha1Btn = document.getElementById('gacha-1-btn');
const gacha10Btn = document.getElementById('gacha-10-btn');
const gachaModal = document.getElementById('gacha-result-modal');
const gachaResultList = document.getElementById('gacha-result-list');
const gachaCloseBtn = document.getElementById('gacha-close-btn');

const charSelectModal = document.getElementById('char-select-modal');
const charSelectList = document.getElementById('char-select-list');
const modalCloseBtn = document.getElementById('modal-close-btn');

const mainTitle = document.getElementById('main-title');
const statsContainer = document.getElementById('stats-container');
const songListContainer = document.getElementById('song-list');

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
  prepScreen.style.display = (viewName === 'prep') ? 'flex' : 'none';
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

const songs = [
  { 
    id: 'springdream', title: '봄꿈', thumb: 'data:image/jpeg;base64,IMAGE4_BASE64_PLACEHOLDER', audio: bgm4, duration: 185,
    levels: { normal: 'Lv. 8', hard: 'Lv. 15', extreme: 'Lv. 25' } 
  },
  { 
    id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER', audio: bgm1, duration: 225,
    levels: { normal: 'Lv. 11', hard: 'Lv. 18', extreme: 'Lv. 26' } 
  },
  { 
    id: 'bbijilge', title: '삐질게', thumb: 'data:image/jpeg;base64,IMAGE2_BASE64_PLACEHOLDER', audio: bgm2, duration: 144,
    levels: { normal: 'Lv. 12', hard: 'Lv. 19', extreme: 'Lv. 27' } 
  },
  { 
    id: 'constellation', title: '별자리가 될 수 있다면', thumb: 'data:image/jpeg;base64,IMAGE3_BASE64_PLACEHOLDER', audio: bgm3, duration: 255,
    levels: { normal: 'Lv. 13', hard: 'Lv. 20', extreme: 'Lv. 29' } 
  }
];

const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 570;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

let currentSongId = 'springdream';
let currentDifficulty = 'normal';

let stella = 100;
let ownedCharacters = { mashiro: false, huya: false, yuni: false, maro: false, arunyang: false, baku: false };
let equippedUnit = [null, null];
let activeSlotIndex = null;

let bestRecords = {
  springdream: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } },
  startrail: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } },
  bbijilge: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } },
  constellation: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } }
};

let missionData = {
  attendanceClaimed: false,
  playCount: 0,
  gachaCount: 0,
  playClaimed: false,
  gachaClaimed: false
};

function loadGameData() {
  const savedStella = localStorage.getItem('rhythm_stella');
  if (savedStella !== null) stella = parseInt(savedStella);

  const savedChars = localStorage.getItem('rhythm_chars');
  if (savedChars !== null) ownedCharacters = JSON.parse(savedChars);

  const savedRecords = localStorage.getItem('rhythm_records');
  if (savedRecords !== null) {
    const parsed = JSON.parse(savedRecords);
    bestRecords = { ...bestRecords, ...parsed };
  }
}

function saveGameData() {
  localStorage.setItem('rhythm_stella', stella);
  localStorage.setItem('rhythm_chars', JSON.stringify(ownedCharacters));
  localStorage.setItem('rhythm_records', JSON.stringify(bestRecords));
}

function resetGameData() {
  if (confirm("⚠️ 모든 게임 데이터가 초기화됩니다.")) {
    localStorage.clear();
    location.reload();
  }
}

function exportSaveData() {
  const saveData = { stella, ownedCharacters, bestRecords };
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(saveData));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", "rhythm_star_save.json");
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
}

function importSaveDataPrompt() {
  const inputString = prompt("세이브 파일의 JSON 텍스트를 붙여넣어 주세요:");
  if (!inputString) return;
  try {
    const parsed = JSON.parse(inputString.trim());
    if (parsed.stella !== undefined) stella = parsed.stella;
    if (parsed.ownedCharacters) ownedCharacters = parsed.ownedCharacters;
    if (parsed.bestRecords) bestRecords = parsed.bestRecords;
    saveGameData();
    alert("데이터가 복원되었습니다!");
  } catch (err) {
    alert("잘못된 형식입니다.");
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
let judgementText = "";
let judgementColor = "#fff";
let judgementTimer = 0;

let keyPressed = [false, false, false, false];
let activeTouches = new Map();
let notes = [];

function getActiveBgm() {
  const s = songs.find(item => item.id === currentSongId);
  return s ? s.audio : bgm4;
}

function updateSelectedRecordDisplay() {
  if (!bestRecords[currentSongId]) {
    bestRecords[currentSongId] = { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } };
  }
  if (!bestRecords[currentSongId][currentDifficulty]) {
    currentDifficulty = 'normal';
  }
  const rec = bestRecords[currentSongId][currentDifficulty];
  const diffColorMap = { normal: '#00f2fe', hard: '#ff4b4b', extreme: '#c084fc' };
  const diffNameMap = { normal: '보통', hard: '하드', extreme: '익스트림' };
  
  menuDiffLabel.innerText = `🏆 [${diffNameMap[currentDifficulty]}] 최고 기록`;
  menuDiffLabel.style.color = diffColorMap[currentDifficulty];
  
  if (rec && rec.score > 0) {
    menuDiffRecord.innerHTML = `<b>${rec.score.toLocaleString()}점</b> (RANK: <span style="color:${rec.color}; font-weight:bold;">${rec.rank}</span>)`;
  } else {
    menuDiffRecord.innerHTML = `기록 없음 (RANK: -)`;
  }
}

function renderDifficultyButtons() {
  const song = songs.find(s => s.id === currentSongId);
  difficultyContainer.innerHTML = '';
  
  const diffs = [
    { key: 'normal', label: '보통', lv: song.levels.normal },
    { key: 'hard', label: '하드', lv: song.levels.hard },
    { key: 'extreme', label: '익스트림', lv: song.levels.extreme }
  ];

  diffs.forEach(d => {
    const card = document.createElement('div');
    card.className = `diff-card ${d.key === currentDifficulty ? 'selected' : ''}`;
    card.setAttribute('data-diff', d.key);
    card.innerHTML = `<div class="diff-lv">${d.lv}</div><div class="diff-name">${d.label}</div>`;
    
    card.addEventListener('click', () => {
      document.querySelectorAll('.diff-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      currentDifficulty = d.key;
      statsContainer.style.display = 'none';
      mainTitle.innerHTML = 'RHYTHM STAR';
      mainTitle.style.color = '#00f2fe';
      updateSelectedRecordDisplay();
    });
    difficultyContainer.appendChild(card);
  });
}

function renderSongList() {
  songListContainer.innerHTML = '';
  songs.forEach(song => {
    const card = document.createElement('div');
    card.className = `song-card ${song.id === currentSongId ? 'selected' : ''}`;
    card.innerHTML = `
      <div class="song-thumb-wrapper">
        <img src="${song.thumb}" class="song-thumb">
        <span class="new-badge">NEW!</span>
      </div>
      <div class="song-name">♬ ${song.title}</div>
    `;
    card.addEventListener('click', () => {
      currentSongId = song.id;
      statsContainer.style.display = 'none';
      mainTitle.innerHTML = 'RHYTHM STAR';
      mainTitle.style.color = '#00f2fe';
      
      canvas.style.backgroundImage = `linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('${song.thumb}')`;
      menuScreen.style.backgroundImage = `linear-gradient(rgba(14, 17, 23, 0.90), rgba(14, 17, 23, 0.94)), url('${song.thumb}')`;
      
      renderSongList();
      renderDifficultyButtons();
      updateSelectedRecordDisplay();
    });
    songListContainer.appendChild(card);
  });
}

function updateMissionUI() {
  const attBtn = document.getElementById('attendance-btn');
  if (missionData.attendanceClaimed) {
    attBtn.innerText = "수령 완료";
    attBtn.style.background = "#21262d";
    attBtn.style.color = "#8b949e";
    attBtn.disabled = true;
  }
}

function claimAttendance() {
  if (!missionData.attendanceClaimed) {
    missionData.attendanceClaimed = true;
    stella += 30;
    updateInventoryUI();
    updateMissionUI();
    saveGameData();
    alert("출석 보상으로 스텔라 30개를 획득하셨습니다!");
  }
}

renderSongList();
renderDifficultyButtons();
updateSelectedRecordDisplay();
updateMissionUI();

nextPrepBtn.addEventListener('click', () => {
  const song = songs.find(s => s.id === currentSongId);
  const diffNameMap = { normal: '보통', hard: '하드', extreme: '익스트림' };
  prepSongTitle.innerHTML = `🎵 ${song.title} [${diffNameMap[currentDifficulty]}]`;
  
  const rec = bestRecords[currentSongId][currentDifficulty];
  prepRecordTitle.innerHTML = `🏆 [${diffNameMap[currentDifficulty]}] 최고 기록`;
  if (rec && rec.score > 0) {
    prepRecordContent.innerHTML = `최고 점수: <b>${rec.score.toLocaleString()}점</b> | RANK: <span style="color:${rec.color}; font-weight:bold;">${rec.rank}</span>`;
  } else {
    prepRecordContent.innerHTML = `기록 없음`;
  }
  switchView('prep');
});

prepBackBtn.addEventListener('click', () => { switchView('menu'); });

function updateInventoryUI() {
  stellaCountEl.innerText = stella;
  const charMeta = {
    mashiro: { name: '네네코 마시로', star: '⭐⭐⭐⭐⭐', cls: 'star-5', color: '#facc15', img: 'MASHIRO_IMG_PLACEHOLDER' },
    huya: { name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', cls: 'star-5', color: '#facc15', img: 'HUYA_IMG_PLACEHOLDER' },
    yuni: { name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', cls: 'star-5', color: '#facc15', img: 'YUNI_IMG_PLACEHOLDER' },
    maro: { name: '마로', star: '⭐⭐⭐⭐', cls: 'star-4', color: '#c084fc', img: 'MARO_IMG_PLACEHOLDER' },
    arunyang: { name: '아르냥', star: '⭐⭐⭐⭐', cls: 'star-4', color: '#c084fc', img: 'ARUNYANG_IMG_PLACEHOLDER' },
    baku: { name: '바쿠', star: '⭐⭐⭐⭐', cls: 'star-4', color: '#c084fc', img: 'BAKU_IMG_PLACEHOLDER' }
  };

  for (let i = 0; i < 2; i++) {
    const slotEl = document.getElementById(`slot-${i+1}`);
    const charId = equippedUnit[i];
    if (charId && charMeta[charId]) {
      const m = charMeta[charId];
      slotEl.className = `unit-slot filled ${m.cls}`;
      slotEl.innerHTML = `<img src="data:image/jpeg;base64,${m.img}" class="slot-img"><div style="font-size:10px; font-weight:bold;">${m.name}</div>`;
    } else {
      slotEl.className = "unit-slot";
      slotEl.innerHTML = `<div class="plus-icon">+</div><div style="font-size: 10px; color: #8b949e;">슬롯 ${i+1}</div>`;
    }
  }

  Object.keys(charMeta).forEach(key => {
    if (ownedCharacters[key]) {
      const m = charMeta[key];
      const card = document.getElementById(`char-card-${key}`);
      if (card) {
        card.style.borderColor = m.color;
        document.getElementById(`char-${key}-img-box`).innerHTML = `<img src="data:image/jpeg;base64,${m.img}" class="slot-img">`;
        document.getElementById(`char-${key}-badge`).innerHTML = `${m.star} (보유)`;
      }
    }
  });
}

function openCharSelector(slotIndex) {
  activeSlotIndex = slotIndex;
  charSelectList.innerHTML = "";
  const availableChars = [
    { id: 'mashiro', name: '네네코 마시로', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.mashiro, img: 'MASHIRO_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'huya', name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.huya, img: 'HUYA_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'yuni', name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.yuni, img: 'YUNI_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'maro', name: '마로', star: '⭐⭐⭐⭐', owned: ownedCharacters.maro, img: 'MARO_IMG_PLACEHOLDER', color: '#c084fc' },
    { id: 'arunyang', name: '아르냥', star: '⭐⭐⭐⭐', owned: ownedCharacters.arunyang, img: 'ARUNYANG_IMG_PLACEHOLDER', color: '#c084fc' },
    { id: 'baku', name: '바쿠', star: '⭐⭐⭐⭐', owned: ownedCharacters.baku, img: 'BAKU_IMG_PLACEHOLDER', color: '#c084fc' }
  ];

  availableChars.forEach(char => {
    const card = document.createElement('div');
    card.className = `char-option-card ${char.owned ? 'owned' : ''}`;
    card.style.opacity = char.owned ? "1" : "0.45";
    card.innerHTML = `<img src="data:image/jpeg;base64,${char.img}" style="width:38px; height:38px; border-radius:50%; object-fit:cover;"><div style="font-size:11px; font-weight:bold; margin-top:2px;">${char.name}</div>`;
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
  if (stella < cost) { alert("스텔라가 부족합니다!"); return; }
  stella -= cost;
  updateInventoryUI();
  saveGameData();

  let results = [];
  for (let i = 0; i < count; i++) {
    const rand = Math.random();
    if (rand < 0.33) {
      ownedCharacters.mashiro = true;
      results.push({ name: "네네코 마시로", color: "#facc15", img: "MASHIRO_IMG_PLACEHOLDER" });
    } else if (rand < 0.66) {
      ownedCharacters.yuni = true;
      results.push({ name: "아야츠노 유니", color: "#facc15", img: "YUNI_IMG_PLACEHOLDER" });
    } else {
      ownedCharacters.huya = true;
      results.push({ name: "사키하네 후야", color: "#facc15", img: "HUYA_IMG_PLACEHOLDER" });
    }
  }
  updateInventoryUI();
  saveGameData();
  gachaResultList.innerHTML = "";
  results.forEach(res => {
    const item = document.createElement('div');
    item.style.cssText = "background:#21262d; border:1px solid " + res.color + "; border-radius:10px; padding:8px; display:flex; flex-direction:column; align-items:center; width:88px;";
    item.innerHTML = `<img src="data:image/jpeg;base64,${res.img}" style="width:36px; height:36px; border-radius:50%;"><div style="font-size:10px; font-weight:bold; margin-top:3px;">${res.name}</div>`;
    gachaResultList.appendChild(item);
  });
  gachaModal.style.display = "flex";
}

gacha1Btn.addEventListener('click', () => executeGacha(1));
gacha10Btn.addEventListener('click', () => executeGacha(10));
gachaCloseBtn.addEventListener('click', () => { gachaModal.style.display = "none"; });

function generateBeatmap(songId, difficulty) {
  notes = [];
  let seed = songId === 'springdream' ? 4000 : (songId === 'startrail' ? 1000 : (songId === 'bbijilge' ? 2000 : 3000));
  function seededRandom() {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  }

  const songObj = songs.find(s => s.id === songId);
  const beatInterval = 0.55; 
  let currentTime = 2.0;
  const totalDuration = songObj ? songObj.duration : 185.0;

  window.NOTE_SPEED = difficulty === 'normal' ? 420 : (difficulty === 'hard' ? 480 : 540);

  let index = 0;
  while (currentTime < totalDuration - 3.0) {
    const lane = Math.floor(seededRandom() * LANES);
    const isLong = difficulty !== 'normal' && index % 4 === 0 && seededRandom() < 0.35;

    if (isLong) {
      const longDuration = beatInterval * 1.5;
      notes.push({ time: currentTime, lane: lane, type: 'long', duration: longDuration, tailHit: false, holding: false, hit: false, missed: false });
    } else {
      notes.push({ time: currentTime, lane: lane, type: 'normal', hit: false, missed: false });
    }

    currentTime += difficulty === 'normal' ? 1.2 : (difficulty === 'hard' ? 0.85 : 0.55);
    index++;
  }
}

function incrementCombo() {
  combo++;
  if (combo > maxCombo) maxCombo = combo;
}

function applyHitScore(note, minDiff) {
  let mult = 1;
  if (minDiff <= 0.12) {
    score += Math.round((100 + (combo * 2)) * mult);
    incrementCombo();
    stats.perfect++;
    healHp(1.2);
    showJudgement("PERFECT!", "#00f2fe");
  } else if (minDiff <= 0.22) {
    score += Math.round((70 + combo) * mult);
    incrementCombo();
    stats.great++;
    healHp(0.6);
    showJudgement("GREAT!", "#4ade80");
  } else {
    score += Math.round(30 * mult);
    incrementCombo();
    stats.good++;
    showJudgement("GOOD", "#facc15");
  }
}

function healHp(amount) {
  currentHp = Math.min(maxHp, currentHp + amount);
  updateHpUI();
}

function damageHp(amount) {
  currentHp = Math.max(0, currentHp - amount);
  updateHpUI();
  if (currentHp <= 0) triggerGameOver();
}

function updateHpUI() {
  const percent = (currentHp / maxHp) * 100;
  hpFill.style.width = percent + '%';
  hpText.innerText = Math.round(currentHp) + ' / ' + maxHp;
}

function showJudgement(text, color) {
  judgementText = text;
  judgementColor = color;
  judgementTimer = 30;
}

function requestGiveUp() {
  if (!isPlaying) return;
  isPlaying = false;
  getActiveBgm().pause();
  if (confirm("정말 포기하시겠습니까?")) {
    switchView('menu');
  } else {
    isPlaying = true;
    requestAnimationFrame(updateAndDraw);
  }
}

function handleTapDown(lane) {
  if (!isPlaying) return;
  const currentTime = (performance.now() - startTime) / 1000;
  let targetNote = null;
  let minDiff = Infinity;

  for (let note of notes) {
    if (!note.hit && !note.missed && note.lane === lane) {
      const diff = Math.abs(note.time - currentTime);
      if (diff < minDiff) {
        minDiff = diff;
        targetNote = note;
      }
    }
  }

  if (targetNote && minDiff <= 0.35) {
    targetNote.hit = true;
    if (targetNote.type === 'long') targetNote.holding = true;
    applyHitScore(targetNote, minDiff);
  }
}

function handleMiss() {
  stats.miss++;
  combo = 0;
  damageHp(12);
  showJudgement("MISS", "#ff4b4b");
}

function getLaneFromTouch(clientX) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  return Math.max(0, Math.min(LANES - 1, Math.floor(((clientX - rect.left) * scaleX) / LANE_WIDTH)));
}

canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  if (!isPlaying) return;
  for (let i = 0; i < e.changedTouches.length; i++) {
    const lane = getLaneFromTouch(e.changedTouches[i].clientX);
    keyPressed[lane] = true;
    handleTapDown(lane);
  }
}, { passive: false });

const handleTouchEnd = (e) => {
  e.preventDefault();
  keyPressed = [false, false, false, false];
};
canvas.addEventListener('touchend', handleTouchEnd, { passive: false });

window.addEventListener('keydown', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1 && !keyPressed[idx]) {
    keyPressed[idx] = true;
    handleTapDown(idx);
  }
});
window.addEventListener('keyup', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1) keyPressed[idx] = false;
});

function calculateRank(finalScore, difficulty) {
  let threshold = difficulty === 'normal' ? 150000 : (difficulty === 'hard' ? 240000 : 350000);
  if (finalScore >= threshold * 0.95) return { rank: 'SS', color: '#ff79c6' };
  if (finalScore >= threshold * 0.80) return { rank: 'S', color: '#facc15' };
  if (finalScore >= threshold * 0.65) return { rank: 'A', color: '#00f2fe' };
  if (finalScore >= threshold * 0.50) return { rank: 'B', color: '#4ade80' };
  if (finalScore >= threshold * 0.30) return { rank: 'C', color: '#fb923c' };
  return { rank: 'D', color: '#94a3b8' };
}

function updateAndDraw() {
  if (!isPlaying) return;
  const currentBgm = getActiveBgm();
  const currentTime = (performance.now() - startTime) / 1000;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < LANES; i++) {
    const x = i * LANE_WIDTH;
    ctx.fillStyle = keyPressed[i] ? LANE_COLORS[i] : '#1f2630';
    ctx.fillRect(x + 4, HIT_Y + 8, LANE_WIDTH - 8, canvas.height - HIT_Y - 14);
    ctx.strokeStyle = '#30363d';
    ctx.lineWidth = 2;
    ctx.strokeRect(x, 0, LANE_WIDTH, canvas.height);
  }

  ctx.strokeStyle = '#00f2fe';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, HIT_Y);
  ctx.lineTo(canvas.width, HIT_Y);
  ctx.stroke();

  let remainingNotes = 0;
  for (let note of notes) {
    if (note.missed || (note.hit && (note.type !== 'long' || note.tailHit))) continue;
    remainingNotes++;

    const timeDiff = note.time - currentTime;
    const y = HIT_Y - (timeDiff * window.NOTE_SPEED);

    if (note.type === 'long' && note.holding) {
      if (currentTime >= note.time + note.duration) {
        note.holding = false;
        note.tailHit = true;
        score += 50;
        incrementCombo();
        stats.perfect++;
        healHp(1.0);
      }
      continue;
    }

    if (!note.hit && timeDiff < -0.35) {
      note.missed = true;
      handleMiss();
      continue;
    }

    if (y >= -50 && y <= HIT_Y + 20) {
      const x = note.lane * LANE_WIDTH + 10;
      const w = LANE_WIDTH - 20;
      ctx.fillStyle = LANE_COLORS[note.lane];
      ctx.beginPath();
      ctx.roundRect(x, y - 12, w, 24, 6);
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

  if (judgementTimer > 0) {
    ctx.fillStyle = judgementColor;
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(judgementText, canvas.width / 2, 205);
    judgementTimer--;
  }

  const songObj = songs.find(s => s.id === currentSongId);
  const durationLimit = songObj ? songObj.duration : 185.0;

  if (currentBgm.ended || (remainingNotes === 0 && currentTime > durationLimit - 2.0)) {
    endGame();
    return;
  }

  requestAnimationFrame(updateAndDraw);
}

function startGame() {
  score = 0; combo = 0; maxCombo = 0; judgementTimer = 0;
  currentHp = 100;
  updateHpUI();
  stats = { perfect: 0, great: 0, good: 0, miss: 0 };
  activeTouches.clear();
  keyPressed = [false, false, false, false];
  
  generateBeatmap(currentSongId, currentDifficulty);
  
  const currentBgm = getActiveBgm();
  currentBgm.pause();
  currentBgm.currentTime = 0;
  currentBgm.play().catch(e => {});

  isPlaying = true;
  startTime = performance.now();
  switchView('play');
  requestAnimationFrame(updateAndDraw);
}

function triggerGameOver() {
  isPlaying = false;
  getActiveBgm().pause();
  mainTitle.innerHTML = "💔 GAME OVER";
  mainTitle.style.color = "#ff4b4b";
  statsContainer.innerHTML = `체력이 소진되었습니다. 최종 점수: ${score.toLocaleString()}`;
  statsContainer.style.display = 'block';
  switchView('menu');
}

function endGame() {
  isPlaying = false;
  getActiveBgm().pause();

  const rankInfo = calculateRank(score, currentDifficulty);
  if (!bestRecords[currentSongId][currentDifficulty] || score > bestRecords[currentSongId][currentDifficulty].score) {
    bestRecords[currentSongId][currentDifficulty] = { score: score, rank: rankInfo.rank, color: rankInfo.color };
  }

  stella += 25;
  saveGameData();
  updateSelectedRecordDisplay();

  mainTitle.innerHTML = `CLEAR! RANK ${rankInfo.rank}`;
  mainTitle.style.color = rankInfo.color;

  statsContainer.innerHTML = `
    <div>최종 점수: <b>${score.toLocaleString()}</b></div>
    <div>최대 콤보: ${maxCombo} | 스텔라 +25 획득!</div>
  `;
  statsContainer.style.display = 'block';
  switchView('menu');
}

startBtn.addEventListener('click', startGame);
updateInventoryUI();
</script>
</body>
</html>
"""

# 치환 처리
rhythm_game_html = rhythm_game_html.replace("AUDIO1_BASE64_PLACEHOLDER", audio1_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE1_BASE64_PLACEHOLDER", image1_base64)
rhythm_game_html = rhythm_game_html.replace("AUDIO2_BASE64_PLACEHOLDER", audio2_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE2_BASE64_PLACEHOLDER", image2_base64)
rhythm_game_html = rhythm_game_html.replace("AUDIO3_BASE64_PLACEHOLDER", audio3_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE3_BASE64_PLACEHOLDER", image3_base64)
rhythm_game_html = rhythm_game_html.replace("AUDIO4_BASE64_PLACEHOLDER", audio4_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE4_BASE64_PLACEHOLDER", image4_base64)

rhythm_game_html = rhythm_game_html.replace("MASHIRO_IMG_PLACEHOLDER", mashiro_base64)
rhythm_game_html = rhythm_game_html.replace("MARO_IMG_PLACEHOLDER", maro_base64)
rhythm_game_html = rhythm_game_html.replace("HUYA_IMG_PLACEHOLDER", huya_base64)
rhythm_game_html = rhythm_game_html.replace("YUNI_IMG_PLACEHOLDER", yuni_base64)
rhythm_game_html = rhythm_game_html.replace("ARUNYANG_IMG_PLACEHOLDER", arunyang_base64)
rhythm_game_html = rhythm_game_html.replace("BAKU_IMG_PLACEHOLDER", baku_base64)

rhythm_game_html = rhythm_game_html.replace("MASHIRO_VOICE_PLACEHOLDER", mashiro_voice_base64)
rhythm_game_html = rhythm_game_html.replace("YUNI_VOICE_PLACEHOLDER", yuni_voice_base64)
rhythm_game_html = rhythm_game_html.replace("HUYA_VOICE_PLACEHOLDER", huya_voice_base64)

components.html(rhythm_game_html, height=820)
