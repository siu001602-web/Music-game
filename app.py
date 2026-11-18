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

song1_music = "music/Screen_Recording_20261117_180140_YouTube_17112026.m4a"
song1_img = "Image/SmartSelect_20261117_234657_YouTube.jpg"

song2_music = "music/Screen_Recording_20261118_013745_YouTube_18112026.m4a"
song2_img = "Image/SmartSelect_20261118_014123_YouTube.jpg"

song3_music = "music/Screen_Recording_20261118_180535_YouTube_18112026.m4a"
song3_img = "Image/SmartSelect_20261118_180837_YouTube.jpg"

# 신곡: 봄꿈
song4_music = "music/Screen_Recording_20261118_210521_YouTube_18112026.m4a"
song4_img = "Image/SmartSelect_20261117_234657_YouTube.jpg"

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
    background: linear-gradient(rgba(14, 17, 23, 0.94), rgba(14, 17, 23, 0.94)), url('data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER');
    background-size: cover;
    background-position: center;
    padding: 12px;
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
    background: linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER');
    background-size: cover;
    background-position: center;
    touch-action: none;
  }

  .nav-tabs {
    display: flex; gap: 3px; width: 100%;
    background: rgba(22, 27, 34, 0.9); padding: 4px;
    border-radius: 12px; border: 1px solid #30363d; margin-bottom: 6px;
  }
  .nav-tab {
    flex: 1; padding: 5px 0; font-size: 10px; font-weight: bold;
    color: #8b949e; background: transparent; border: none; border-radius: 8px; cursor: pointer;
  }
  .nav-tab.active { color: #0e1117; background: #00f2fe; box-shadow: 0 2px 10px rgba(0, 242, 254, 0.3); }

  .tab-content { width: 100%; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; overflow-y: auto; }

  .section-title { font-size: 11px; color: #8b949e; margin-bottom: 3px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }

  .song-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
    width: 100%; max-height: 135px; overflow-y: auto; margin-bottom: 6px; padding: 2px;
  }
  .song-card {
    background: #161b22; border: 2px solid #30363d; border-radius: 10px;
    padding: 5px; cursor: pointer; text-align: left; transition: all 0.2s; position: relative;
  }
  .song-card.selected { border-color: #00f2fe; box-shadow: 0 0 12px rgba(0, 242, 254, 0.4); background: #1f2630; }
  .song-thumb { width: 100%; height: 42px; border-radius: 6px; object-fit: cover; margin-bottom: 3px; }
  .song-name { font-size: 10px; font-weight: bold; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .new-badge { position: absolute; top: 5px; right: 5px; background: #ff4b4b; color: white; font-size: 7px; font-weight: bold; padding: 2px 3px; border-radius: 3px; }

  .difficulty-select-container { display: flex; gap: 6px; width: 100%; justify-content: center; margin-bottom: 6px; }
  .diff-card {
    flex: 1; background: #161b22; border: 2px solid #30363d; border-radius: 10px;
    padding: 5px 3px; cursor: pointer; text-align: center; transition: all 0.2s;
  }
  .diff-card.selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); background: #1f2630; }
  .diff-card[data-diff="easy"].selected { border-color: #4ade80; box-shadow: 0 0 10px rgba(74, 222, 128, 0.4); }
  .diff-card[data-diff="normal"].selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); }
  .diff-card[data-diff="hard"].selected { border-color: #ff4b4b; box-shadow: 0 0 10px rgba(255, 75, 75, 0.4); }
  .diff-card[data-diff="expert"].selected { border-color: #c084fc; box-shadow: 0 0 10px rgba(192, 132, 252, 0.4); }
  .diff-card[data-diff="extreme"].selected { border-color: #ff007f; box-shadow: 0 0 10px rgba(255, 0, 127, 0.4); }

  .diff-lv { font-size: 9px; font-weight: bold; color: #8b949e; margin-bottom: 1px; }
  .diff-name { font-size: 10px; font-weight: 900; }
  .diff-card[data-diff="easy"] .diff-name { color: #4ade80; }
  .diff-card[data-diff="normal"] .diff-name { color: #00f2fe; }
  .diff-card[data-diff="hard"] .diff-name { color: #ff4b4b; }
  .diff-card[data-diff="expert"] .diff-name { color: #c084fc; }
  .diff-card[data-diff="extreme"] .diff-name { color: #ff007f; }

  .selected-diff-record-box {
    width: 100%;
    background: rgba(22, 27, 34, 0.85);
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 6px 10px;
    margin-bottom: 6px;
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
    padding: 8px 20px; font-size: 13px; font-weight: bold; color: #0e1117; background: #00f2fe;
    border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
  }

  .stats-box {
    background: rgba(255, 255, 255, 0.08); border: 1px solid #30363d; border-radius: 10px;
    padding: 6px 10px; margin: 2px 0 6px 0; width: 100%; text-align: left; font-size: 11px; line-height: 1.4;
  }
  .controls-hint { margin-top: 4px; font-size: 10px; color: #8b949e; }

  .gacha-box {
    background: #161b22; border: 2px solid #30363d; border-radius: 14px; padding: 14px;
    width: 100%; display: flex; flex-direction: column; align-items: center; gap: 8px;
  }
  .gacha-btn-group { display: flex; gap: 10px; width: 100%; }
  .gacha-btn { flex: 1; padding: 9px; font-size: 12px; font-weight: bold; border: none; border-radius: 20px; cursor: pointer; }
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
  #yuni-popup { top: 56px; border-color: #00f2fe; background: rgba(0, 242, 254, 0.25); }
  #huya-popup { top: 100px; border-color: #ff79c6; background: rgba(255, 121, 198, 0.25); }
  #fever-popup { top: 144px; border-color: #ff007f; background: rgba(255, 0, 127, 0.25); }

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
    background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 8px 10px;
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
      <h1 id="main-title" style="margin: 0; color: #00f2fe; font-size: 16px;">RHYTHM STAR</h1>
      <div style="background: #161b22; border: 1px solid #facc15; border-radius: 12px; padding: 2px 8px; font-size: 11px; font-weight: bold; color: #facc15;">
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
        <div class="section-title">Select Song (악보 선택)</div>
        <div id="song-list" class="song-grid"></div>

        <div class="section-title">Difficulty (난이도 선택)</div>
        <div id="difficulty-container" class="difficulty-select-container"></div>

        <div class="selected-diff-record-box">
          <span id="menu-diff-label" style="font-weight: bold; color: #00f2fe;">🏆 [보통] 최고 기록</span>
          <span id="menu-diff-record" style="color: #fff;">기록 없음 (RANK: -)</span>
        </div>
      </div>

      <button id="next-prep-btn" class="action-btn" style="margin-top: 2px;">유니트 편성 및 라이브</button>

      <div id="controls-hint" class="controls-hint">
        🎹 노트: <b>[D] [F] [J] [K]</b> | 슬라이드: <b>[←][→]</b> 또는 <b>[A][L]</b>
      </div>
    </div>

    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="gacha-box">
        <div style="font-size: 28px;">🌟</div>
        <div style="font-size: 14px; font-weight: bold; color: #00f2fe;">스타 스카우트 (캐릭터 뽑기)</div>
        <div style="font-size: 10px; color: #8b949e; text-align: center; line-height: 1.4;">
          • ⭐⭐⭐⭐⭐ 5성 픽업 (합산 3%): 시로(마시로), 후야, 유니<br>
          • ⭐⭐⭐⭐ 4성 픽업 (합산 97%): 마로, 아르냥, 바쿠
        </div>
        <div style="font-size: 11px; color: #facc15; font-weight: bold; margin: 2px 0;">소모 재화: 1회당 스텔라 10개</div>
        <div class="gacha-btn-group">
          <button id="gacha-1-btn" class="gacha-btn single">1회 스카우트 (10개)</button>
          <button id="gacha-10-btn" class="gacha-btn multi">10회 스카우트 (100개)</button>
        </div>
      </div>
    </div>

    <div id="tab-characters" class="tab-content" style="display: none;">
      <div class="section-title">보유 캐릭터 도감</div>
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; width: 100%; margin-top: 2px;">
        <div id="char-card-mashiro" class="unit-slot filled" style="height: auto; padding: 8px; border-color: #30363d;">
          <div id="char-mashiro-img-box" style="font-size: 22px; margin-bottom: 2px;">👤</div>
          <div id="char-mashiro-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">네네코 마시로 (시로)</div>
        </div>
        <div id="char-card-huya" class="unit-slot filled" style="height: auto; padding: 8px; border-color: #30363d;">
          <div id="char-huya-img-box" style="font-size: 22px; margin-bottom: 2px;">👤</div>
          <div id="char-huya-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">사키하네 후야</div>
        </div>
        <div id="char-card-yuni" class="unit-slot filled" style="height: auto; padding: 8px; border-color: #30363d;">
          <div id="char-yuni-img-box" style="font-size: 22px; margin-bottom: 2px;">👤</div>
          <div id="char-yuni-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">아야츠노 유니</div>
        </div>
        <div id="char-card-maro" class="unit-slot filled" style="height: auto; padding: 8px; border-color: #30363d;">
          <div id="char-maro-img-box" style="font-size: 22px; margin-bottom: 2px;">👤</div>
          <div id="char-maro-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">마로 (팬)</div>
        </div>
        <div id="char-card-arunyang" class="unit-slot filled" style="height: auto; padding: 8px; border-color: #30363d;">
          <div id="char-arunyang-img-box" style="font-size: 22px; margin-bottom: 2px;">👤</div>
          <div id="char-arunyang-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">아르냥 (팬)</div>
        </div>
        <div id="char-card-baku" class="unit-slot filled" style="height: auto; padding: 8px; border-color: #30363d;">
          <div id="char-baku-img-box" style="font-size: 22px; margin-bottom: 2px;">👤</div>
          <div id="char-baku-badge" style="font-size: 9px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 10px; font-weight: bold; margin-top: 2px;">바쿠 (팬)</div>
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
        <button id="attendance-btn" onclick="claimAttendance()" style="padding: 5px 10px; font-size: 11px; font-weight: bold; background: #00f2fe; color: #0e1117; border: none; border-radius: 12px; cursor: pointer;">수령하기</button>
      </div>

      <div class="section-title" style="margin-top: 6px;">일일 임무</div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;">
          <b>🎵 라이브 3회 플레이</b><br>
          <span id="mission-play-count" style="color: #8b949e; font-size: 10px;">진행도: 0 / 3</span>
        </div>
        <button id="mission-play-btn" onclick="claimMission('play')" disabled style="padding: 5px 10px; font-size: 11px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 12px; cursor: pointer;">완료 (+30)</button>
      </div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;">
          <b>🎁 스카우트 1회 진행</b><br>
          <span id="mission-gacha-count" style="color: #8b949e; font-size: 10px;">진행도: 0 / 1</span>
        </div>
        <button id="mission-gacha-btn" onclick="claimMission('gacha')" disabled style="padding: 5px 10px; font-size: 11px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 12px; cursor: pointer;">완료 (+20)</button>
      </div>
    </div>

    <div id="tab-settings" class="tab-content" style="display: none; align-items: center; justify-content: center; padding: 10px;">
      <div class="gacha-box">
        <div style="font-size: 22px;">💾</div>
        <div style="font-size: 13px; font-weight: bold; color: #00f2fe;">게임 데이터 백업 및 복원</div>
        <div style="font-size: 10px; color: #8b949e; text-align: center; line-height: 1.4;">
          코드가 바뀌거나 브라우저 캐시가 초기화되어도<br>데이터를 파일로 백업해 두면 안전하게 복구할 수 있습니다!
        </div>
        <div style="display: flex; gap: 8px; width: 100%; margin-top: 6px;">
          <button onclick="exportSaveData()" class="gacha-btn" style="background: #21262d; color: #4ade80; border: 1px solid #4ade80;">데이터 내보내기</button>
          <button onclick="importSaveDataPrompt()" class="gacha-btn" style="background: #00f2fe; color: #0e1117;">데이터 불러오기</button>
        </div>
        <button onclick="resetGameData()" style="background: transparent; color: #ff4b4b; border: 1px solid #ff4b4b; border-radius: 10px; padding: 5px; font-size: 11px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 4px;">데이터 초기화 (문제 해결용)</button>
      </div>
    </div>
  </div>

  <div id="prep-screen">
    <div class="prep-header" id="prep-song-title">🎵 Star Trail</div>
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
      <div style="font-size: 10px; color: #8b949e;">• [시로+마로] / [유니+아르냥] / [후야+바쿠] / [유니+후야(애버리스!)] 시너지 발동 가능!</div>
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
      <span style="font-size: 11px; font-weight: bold; color: #00f2fe;">[뭘뽀노?] 은하수 폭발!</span>
    </div>

    <div id="huya-popup" class="skill-popup">
      <img src="data:image/jpeg;base64,HUYA_IMG_PLACEHOLDER">
      <span style="font-size: 11px; font-weight: bold; color: #ff79c6;">[포근한 꿈결 속으로]</span>
    </div>

    <div id="fever-popup" class="skill-popup">
      <span style="font-size: 11px; font-weight: bold; color: #ff007f;">✨ [애버리스!] 더블 스킬 버프!</span>
    </div>

    <div id="skill-gauges-wrapper">
      <div id="mashiro-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #facc15;">🐾 [시로 액티브]</div>
        <div class="gauge-bg"><div id="mashiro-gauge-fill" class="gauge-fill" style="background: #facc15;"></div></div>
        <div id="mashiro-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div>
      </div>
      <div id="yuni-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #00f2fe;">🎤 [유니: 뭘뽀노?]</div>
        <div class="gauge-bg"><div id="yuni-gauge-fill" class="gauge-fill" style="background: #00f2fe;"></div></div>
        <div id="yuni-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div>
      </div>
      <div id="huya-skill-bar" class="skill-bar-box">
        <div style="font-size: 9px; font-weight: bold; color: #ff79c6;">💤 [후야: 꿈결 속으로]</div>
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
    id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER', audio: bgm1, duration: 225,
    type: 'starter',
    levels: { easy: 'Lv. 5', normal: 'Lv. 11', hard: 'Lv. 18' } 
  },
  { 
    id: 'bbijilge', title: '삐질게', thumb: 'data:image/jpeg;base64,IMAGE2_BASE64_PLACEHOLDER', audio: bgm2, duration: 144,
    type: 'starter',
    levels: { easy: 'Lv. 6', normal: 'Lv. 12', hard: 'Lv. 19' } 
  },
  { 
    id: 'constellation', title: '별자리가 될 수 있다면', thumb: 'data:image/jpeg;base64,IMAGE3_BASE64_PLACEHOLDER', audio: bgm3, duration: 255,
    type: 'advanced',
    levels: { normal: 'Lv. 13', hard: 'Lv. 20', expert: 'Lv. 28' } 
  },
  { 
    id: 'springdream', title: '봄꿈', thumb: 'data:image/jpeg;base64,IMAGE4_BASE64_PLACEHOLDER', audio: bgm4, duration: 185,
    type: 'extreme_song',
    levels: { normal: 'Lv. 14', hard: 'Lv. 22', expert: 'Lv. 30', extreme: 'Lv. 35' } 
  }
];

const LANES = 4;
let LANE_WIDTH = 120;
const HIT_Y = 570;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

let currentSongId = 'startrail';
let currentDifficulty = 'normal';

let stella = 100;
let ownedCharacters = { mashiro: false, huya: false, yuni: false, maro: false, arunyang: false, baku: false };
let equippedUnit = [null, null];
let activeSlotIndex = null;

let bestRecords = {
  startrail: { easy: { score: 0, rank: '-', color: '#94a3b8' }, normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' } },
  bbijilge: { easy: { score: 0, rank: '-', color: '#94a3b8' }, normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' } },
  constellation: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, expert: { score: 0, rank: '-', color: '#94a3b8' } },
  springdream: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, expert: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } }
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
  if (savedRecords !== null) bestRecords = JSON.parse(savedRecords);

  const savedMissions = localStorage.getItem('rhythm_missions');
  if (savedMissions !== null) {
    const parsed = JSON.parse(savedMissions);
    const today = new Date().toDateString();
    if (parsed.date === today) {
      missionData = parsed;
    } else {
      missionData = { attendanceClaimed: false, playCount: 0, gachaCount: 0, playClaimed: false, gachaClaimed: false, date: today };
    }
  } else {
    missionData.date = new Date().toDateString();
  }
}

function saveGameData() {
  localStorage.setItem('rhythm_stella', stella);
  localStorage.setItem('rhythm_chars', JSON.stringify(ownedCharacters));
  localStorage.setItem('rhythm_records', JSON.stringify(bestRecords));
  localStorage.setItem('rhythm_missions', JSON.stringify(missionData));
}

function resetGameData() {
  if (confirm("⚠️ 모든 게임 데이터가 초기화됩니다. 정말 진행하시겠습니까?")) {
    localStorage.clear();
    location.reload();
  }
}

function exportSaveData() {
  const saveData = {
    stella: stella,
    ownedCharacters: ownedCharacters,
    bestRecords: bestRecords,
    missionData: missionData
  };
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(saveData));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", "rhythm_star_save.json");
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
}

function importSaveDataPrompt() {
  const inputString = prompt("백업했던 세이브 파일의 JSON 텍스트를 여기에 붙여넣어 주세요:");
  if (!inputString) return;

  try {
    let fileContent = inputString.trim();
    if (fileContent.includes('%7B') || fileContent.includes('%22') || fileContent.startsWith('%')) {
      fileContent = decodeURIComponent(fileContent);
    }

    const parsed = JSON.parse(fileContent);
    if (parsed.stella !== undefined) stella = parsed.stella;
    if (parsed.ownedCharacters) ownedCharacters = parsed.ownedCharacters;
    if (parsed.bestRecords) bestRecords = parsed.bestRecords;
    if (parsed.missionData) missionData = parsed.missionData;
    
    saveGameData();
    updateInventoryUI();
    updateMissionUI();
    updateSelectedRecordDisplay();
    
    alert("💾 데이터가 성공적으로 복원되었습니다!");
  } catch (err) {
    console.error(err);
    alert("❌ 잘못된 형식의 세이브 데이터입니다.");
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

// 캐릭터별 액티브 스킬 상태 관리
let mashiroSkillGauge = 0;
let mashiroSkillActivated = false;
let mashiroSkillTimer = 0;

let yuniSkillGauge = 0;
let yuniSkillActivated = false;
let yuniSkillTimer = 0;
let yuniMissShieldCount = 2; // 유니 패시브: 곡당 최대 2회 미스 콤보 보호

let huyaSkillGauge = 0;
let huyaSkillActivated = false;
let huyaSkillTimer = 0;

let doubleSkillActive = false; // 유니&후야 더블 스킬 버프
let doubleSkillTimer = 0;

let iberisComboTracker = 0; // 후야&바쿠 시너지 콤보 트래커
let feverTimer = 0;
let feverActive = false;
let pawPrintAnimTimer = 0;
let galaxyAnimTimer = 0;

let keyPressed = [false, false, false, false];
let activeTouches = new Map();
let notes = [];

function getActiveBgm() {
  const s = songs.find(item => item.id === currentSongId);
  return s ? s.audio : bgm1;
}

function updateSelectedRecordDisplay() {
  if (!bestRecords[currentSongId][currentDifficulty]) {
    currentDifficulty = 'normal';
  }
  const rec = bestRecords[currentSongId][currentDifficulty];
  const diffColorMap = { easy: '#4ade80', normal: '#00f2fe', hard: '#ff4b4b', expert: '#c084fc', extreme: '#ff007f' };
  const diffNameMap = { easy: '쉬움', normal: '보통', hard: '하드', expert: '익스퍼트', extreme: '익스트림' };
  
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
  
  let diffs = [];
  if (song.type === 'starter') {
    diffs = [
      { key: 'easy', label: '쉬움', lv: song.levels.easy },
      { key: 'normal', label: '보통', lv: song.levels.normal },
      { key: 'hard', label: '하드', lv: song.levels.hard }
    ];
  } else if (song.type === 'advanced') {
    diffs = [
      { key: 'normal', label: '보통', lv: song.levels.normal },
      { key: 'hard', label: '하드', lv: song.levels.hard },
      { key: 'expert', label: '익스퍼트', lv: song.levels.expert }
    ];
  } else {
    diffs = [
      { key: 'normal', label: '보통', lv: song.levels.normal },
      { key: 'hard', label: '하드', lv: song.levels.hard },
      { key: 'expert', label: '익스퍼트', lv: song.levels.expert },
      { key: 'extreme', label: '익스트림', lv: song.levels.extreme }
    ];
  }

  if (!diffs.some(d => d.key === currentDifficulty)) {
    currentDifficulty = diffs[0].key;
  }

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
      <div style="position:relative;">
        <img src="${song.thumb}" class="song-thumb">
        <span class="new-badge">NEW</span>
      </div>
      <div class="song-name">🎵 ${song.title}</div>
    `;
    card.addEventListener('click', () => {
      currentSongId = song.id;
      statsContainer.style.display = 'none';
      mainTitle.innerHTML = 'RHYTHM STAR';
      mainTitle.style.color = '#00f2fe';
      
      canvas.style.backgroundImage = `linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('${song.thumb}')`;
      menuScreen.style.backgroundImage = `linear-gradient(rgba(14, 17, 23, 0.94), rgba(14, 17, 23, 0.94)), url('${song.thumb}')`;
      
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
  } else {
    attBtn.innerText = "수령하기";
    attBtn.style.background = "#00f2fe";
    attBtn.style.color = "#0e1117";
    attBtn.disabled = false;
  }

  const playCountSpan = document.getElementById('mission-play-count');
  const playBtn = document.getElementById('mission-play-btn');
  playCountSpan.innerText = `진행도: ${missionData.playCount} / 3`;
  if (missionData.playClaimed) {
    playBtn.innerText = "완료됨";
    playBtn.style.background = "#21262d";
    playBtn.style.color = "#8b949e";
    playBtn.disabled = true;
  } else if (missionData.playCount >= 3) {
    playBtn.innerText = "수령 가능 (+30)";
    playBtn.style.background = "#4ade80";
    playBtn.style.color = "#0e1117";
    playBtn.disabled = false;
  } else {
    playBtn.innerText = "진행 중";
    playBtn.style.background = "#21262d";
    playBtn.style.color = "#8b949e";
    playBtn.disabled = true;
  }

  const gachaCountSpan = document.getElementById('mission-gacha-count');
  const gachaBtn = document.getElementById('mission-gacha-btn');
  gachaCountSpan.innerText = `진행도: ${missionData.gachaCount} / 1`;
  if (missionData.gachaClaimed) {
    gachaBtn.innerText = "완료됨";
    gachaBtn.style.background = "#21262d";
    gachaBtn.style.color = "#8b949e";
    gachaBtn.disabled = true;
  } else if (missionData.gachaCount >= 1) {
    gachaBtn.innerText = "수령 가능 (+20)";
    gachaBtn.style.background = "#4ade80";
    gachaBtn.style.color = "#0e1117";
    gachaBtn.disabled = false;
  } else {
    gachaBtn.innerText = "진행 중";
    gachaBtn.style.background = "#21262d";
    gachaBtn.style.color = "#8b949e";
    gachaBtn.disabled = true;
  }
}

function claimAttendance() {
  if (!missionData.attendanceClaimed) {
    missionData.attendanceClaimed = true;
    stella += 30;
    updateInventoryUI();
    updateMissionUI();
    saveGameData();
    alert("📅 일일 출석 보상으로 스텔라 30개를 획득하셨습니다!");
  }
}

function claimMission(type) {
  if (type === 'play' && missionData.playCount >= 3 && !missionData.playClaimed) {
    missionData.playClaimed = true;
    stella += 30;
    updateInventoryUI();
    updateMissionUI();
    saveGameData();
    alert("🎵 라이브 플레이 임무 보상으로 스텔라 30개를 획득하셨습니다!");
  } else if (type === 'gacha' && missionData.gachaCount >= 1 && !missionData.gachaClaimed) {
    missionData.gachaClaimed = true;
    stella += 20;
    updateInventoryUI();
    updateMissionUI();
    saveGameData();
    alert("🎁 뽑기 임무 보상으로 스텔라 20개를 획득하셨습니다!");
  }
}

renderSongList();
renderDifficultyButtons();
updateSelectedRecordDisplay();
updateMissionUI();

nextPrepBtn.addEventListener('click', () => {
  const song = songs.find(s => s.id === currentSongId);
  const diffNameMap = { 
    easy: `쉬움 (${song.levels.easy})`, 
    normal: `보통 (${song.levels.normal})`, 
    hard: `하드 (${song.levels.hard})`, 
    expert: `익스퍼트 (${song.levels.expert})`,
    extreme: `익스트림 (${song.levels.extreme})`
  };
  prepSongTitle.innerHTML = `🎵 ${song.title} [${diffNameMap[currentDifficulty]}]`;
  
  const rec = bestRecords[currentSongId][currentDifficulty];
  const diffNameUI = { easy: '쉬움', normal: '보통', hard: '하드', expert: '익스퍼트', extreme: '익스트림' };
  prepRecordTitle.innerHTML = `🏆 [${diffNameUI[currentDifficulty]}] 최고 기록`;
  if (rec && rec.score > 0) {
    prepRecordContent.innerHTML = `최고 점수: <b>${rec.score.toLocaleString()}점</b> | RANK: <span style="color:${rec.color}; font-weight:bold;">${rec.rank}</span>`;
  } else {
    prepRecordContent.innerHTML = `기록 없음 (첫 클리어에 도전하세요!)`;
  }

  switchView('prep');
});

prepBackBtn.addEventListener('click', () => {
  switchView('menu');
});

function updateInventoryUI() {
  stellaCountEl.innerText = stella;

  const charMeta = {
    mashiro: { name: '네네코 마시로 (시로)', star: '⭐⭐⭐⭐⭐', cls: 'star-5', color: '#facc15', img: 'MASHIRO_IMG_PLACEHOLDER' },
    huya: { name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', cls: 'star-5', color: '#facc15', img: 'HUYA_IMG_PLACEHOLDER' },
    yuni: { name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', cls: 'star-5', color: '#facc15', img: 'YUNI_IMG_PLACEHOLDER' },
    maro: { name: '마로 (팬)', star: '⭐⭐⭐⭐', cls: 'star-4', color: '#c084fc', img: 'MARO_IMG_PLACEHOLDER' },
    arunyang: { name: '아르냥 (팬)', star: '⭐⭐⭐⭐', cls: 'star-4', color: '#c084fc', img: 'ARUNYANG_IMG_PLACEHOLDER' },
    baku: { name: '바쿠 (팬)', star: '⭐⭐⭐⭐', cls: 'star-4', color: '#c084fc', img: 'BAKU_IMG_PLACEHOLDER' }
  };

  for (let i = 0; i < 2; i++) {
    const slotEl = document.getElementById(`slot-${i+1}`);
    const charId = equippedUnit[i];
    if (charId && charMeta[charId]) {
      const m = charMeta[charId];
      slotEl.className = `unit-slot filled ${m.cls}`;
      slotEl.innerHTML = `
        <img src="data:image/jpeg;base64,${m.img}" class="slot-img" style="color:${m.color};">
        <div style="font-size:10px; font-weight:bold; color:${m.color};">${m.star}</div>
        <div style="font-size:10px; font-weight:bold;">${m.name}</div>
      `;
    } else {
      slotEl.className = "unit-slot";
      slotEl.innerHTML = `
        <div class="plus-icon">+</div>
        <div style="font-size: 10px; color: #8b949e;">슬롯 ${i+1}</div>
      `;
    }
  }

  const synergyCard = document.getElementById('synergy-card');
  const hasMashiro = equippedUnit.includes('mashiro');
  const hasMaro = equippedUnit.includes('maro');
  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');
  const hasHuya = equippedUnit.includes('huya');
  const hasBaku = equippedUnit.includes('baku');

  let synergyTexts = [];
  if (hasMashiro && hasMaro) synergyTexts.push("[냥냥 집사의 특급 후원]");
  if (hasYuni && hasArunyang) synergyTexts.push("[유니&아르냥: 파스텔 방패 & 체력 회복]");
  if (hasHuya && hasBaku) synergyTexts.push("[후야&바쿠: 조용히, 깨우지 마세요]");
  if (hasYuni && hasHuya) synergyTexts.push("[유니&후야: 애버리스! (더블 스킬 버프)]");

  if (synergyTexts.length > 0) {
    synergyCard.style.opacity = "1";
    synergyCard.style.borderColor = "#00f2fe";
    synergyCard.innerHTML = `
      <div style="font-weight: bold; color: #00f2fe; margin-bottom: 2px;">✨ 활성화된 시너지 (${synergyTexts.length}개)</div>
      <div style="font-size: 10px; color: #fff;">• ${synergyTexts.join("<br>• ")}</div>
    `;
  } else {
    synergyCard.style.opacity = "0.5";
    synergyCard.style.borderColor = "#30363d";
    synergyCard.innerHTML = `
      <div style="font-weight: bold; color: #8b949e; margin-bottom: 2px;">✨ 활성화된 시너지 없음</div>
      <div style="font-size: 10px; color: #8b949e;">• [시로+마로] / [유니+아르냥] / [후야+바쿠] / [유니+후야] 조합 시 특수 시너지 발동!</div>
    `;
  }

  Object.keys(charMeta).forEach(key => {
    if (ownedCharacters[key]) {
      const m = charMeta[key];
      const card = document.getElementById(`char-card-${key}`);
      card.style.borderColor = m.color;
      document.getElementById(`char-${key}-img-box`).innerHTML = `<img src="data:image/jpeg;base64,${m.img}" class="slot-img" style="color:${m.color};">`;
      document.getElementById(`char-${key}-badge`).innerHTML = `${m.star} (보유)`;
      document.getElementById(`char-${key}-badge`).style.color = m.color;
    }
  });
}

function openCharSelector(slotIndex) {
  activeSlotIndex = slotIndex;
  charSelectList.innerHTML = "";

  const availableChars = [
    { id: 'mashiro', name: '네네코 마시로 (시로)', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.mashiro, img: 'MASHIRO_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'huya', name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.huya, img: 'HUYA_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'yuni', name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.yuni, img: 'YUNI_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'maro', name: '마로 (팬)', star: '⭐⭐⭐⭐', owned: ownedCharacters.maro, img: 'MARO_IMG_PLACEHOLDER', color: '#c084fc' },
    { id: 'arunyang', name: '아르냥 (팬)', star: '⭐⭐⭐⭐', owned: ownedCharacters.arunyang, img: 'ARUNYANG_IMG_PLACEHOLDER', color: '#c084fc' },
    { id: 'baku', name: '바쿠 (팬)', star: '⭐⭐⭐⭐', owned: ownedCharacters.baku, img: 'BAKU_IMG_PLACEHOLDER', color: '#c084fc' }
  ];

  availableChars.forEach(char => {
    const otherSlot = slotIndex === 0 ? 1 : 0;
    const alreadyEquipped = equippedUnit[otherSlot] === char.id;

    const card = document.createElement('div');
    card.className = `char-option-card ${char.owned && !alreadyEquipped ? 'owned' : ''}`;
    card.style.opacity = (char.owned && !alreadyEquipped) ? "1" : "0.45";
    card.innerHTML = `
      <img src="data:image/jpeg;base64,${char.img}" style="width:38px; height:38px; border-radius:50%; object-fit:cover; margin-bottom:4px; border:2px solid ${char.color};">
      <div style="font-size:9px; color:${char.color};">${char.star}</div>
      <div style="font-size:11px; font-weight:bold; margin-top:2px;">${char.name}</div>
      <div style="font-size:9px; color:${char.owned ? (alreadyEquipped ? '#facc15' : '#00f2fe') : '#8b949e'}; margin-top:2px;">
        ${!char.owned ? '미획득' : (alreadyEquipped ? '편성 중' : '선택 가능')}
      </div>
    `;

    if (char.owned && !alreadyEquipped) {
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
    alert("스텔라 재화가 부족합니다! 곡을 클리어하여 모아보세요.");
    return;
  }
  stella -= cost;
  
  missionData.gachaCount += 1;
  updateMissionUI();
  updateInventoryUI();
  saveGameData();

  let results = [];
  for (let i = 0; i < count; i++) {
    const rand = Math.random() * 100;
    if (rand < 3.0) {
      const r5 = Math.random();
      if (r5 < 0.33) {
        ownedCharacters.mashiro = true;
        results.push({ name: "네네코 마시로 (5성)", star: "⭐⭐⭐⭐⭐", color: "#facc15", img: "MASHIRO_IMG_PLACEHOLDER" });
      } else if (r5 < 0.66) {
        ownedCharacters.huya = true;
        results.push({ name: "사키하네 후야 (5성)", star: "⭐⭐⭐⭐⭐", color: "#facc15", img: "HUYA_IMG_PLACEHOLDER" });
      } else {
        ownedCharacters.yuni = true;
        results.push({ name: "아야츠노 유니 (5성)", star: "⭐⭐⭐⭐⭐", color: "#facc15", img: "YUNI_IMG_PLACEHOLDER" });
      }
    } else {
      const r4 = Math.random();
      if (r4 < 0.33) {
        ownedCharacters.maro = true;
        results.push({ name: "마로 (4성)", star: "⭐⭐⭐⭐", color: "#c084fc", img: "MARO_IMG_PLACEHOLDER" });
      } else if (r4 < 0.66) {
        ownedCharacters.arunyang = true;
        results.push({ name: "아르냥 (4성)", star: "⭐⭐⭐⭐", color: "#c084fc", img: "ARUNYANG_IMG_PLACEHOLDER" });
      } else {
        ownedCharacters.baku = true;
        results.push({ name: "바쿠 (4성)", star: "⭐⭐⭐⭐", color: "#c084fc", img: "BAKU_IMG_PLACEHOLDER" });
      }
    }
  }

  updateInventoryUI();
  saveGameData();

  gachaResultList.innerHTML = "";
  results.forEach(res => {
    const item = document.createElement('div');
    item.style.cssText = "background:#21262d; border:1px solid " + res.color + "; border-radius:10px; padding:8px; display:flex; flex-direction:column; align-items:center; width:88px;";
    item.innerHTML = `
      <img src="data:image/jpeg;base64,${res.img}" style="width:36px; height:36px; border-radius:50%; object-fit:cover; margin-bottom:2px;">
      <div style="font-size:9px; color:${res.color};">${res.star}</div>
      <div style="font-size:10px; font-weight:bold; margin-top:2px;">${res.name.split(' ')[0]}</div>
    `;
    gachaResultList.appendChild(item);
  });
  gachaModal.style.display = "flex";
}

gacha1Btn.addEventListener('click', () => executeGacha(1));
gacha10Btn.addEventListener('click', () => executeGacha(10));
gachaCloseBtn.addEventListener('click', () => { gachaModal.style.display = "none"; });

function generateBeatmap(songId, difficulty) {
  notes = [];
  
  let seed = 1000;
  if (songId === 'bbijilge') seed = 2000;
  else if (songId === 'constellation') seed = 3000;
  else if (songId === 'springdream') seed = 4000;

  if (difficulty === 'easy') seed += 50;
  else if (difficulty === 'normal') seed += 100;
  else if (difficulty === 'hard') seed += 200;
  else if (difficulty === 'expert') seed += 300;
  else if (difficulty === 'extreme') seed += 400;

  function seededRandom() {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  }

  const songObj = songs.find(s => s.id === songId);
  const bpm = 130;
  const beatInterval = 60 / bpm; 
  let currentTime = 2.0;
  const totalDuration = songObj ? songObj.duration : 185.0;

  let speed = 440;
  if (difficulty === 'normal') speed = 470;
  if (difficulty === 'hard') speed = 510;
  if (difficulty === 'expert') speed = 550;
  if (difficulty === 'extreme') speed = 600;
  window.NOTE_SPEED = speed;

  let activeLongEndTimes = [0, 0, 0, 0];

  let index = 0;
  while (currentTime < totalDuration - 5.0) {
    const lane = Math.floor(seededRandom() * LANES);
    const rand = seededRandom();

    if (currentTime < activeLongEndTimes[lane]) {
      if (difficulty === 'easy') currentTime += beatInterval * 1.6;
      else if (difficulty === 'normal') currentTime += beatInterval * 1.0;
      else if (difficulty === 'hard') currentTime += beatInterval * 0.75;
      else if (difficulty === 'expert') currentTime += beatInterval * 0.5;
      else currentTime += beatInterval * 0.35;
      index++;
      continue;
    }

    if (index % 5 === 0 && rand < (difficulty === 'extreme' ? 0.6 : 0.35)) {
      const pairLane = (lane + 2) % LANES;
      if (currentTime >= activeLongEndTimes[lane] && currentTime >= activeLongEndTimes[pairLane]) {
        const bridgeId = `bridge_${index}`;
        notes.push({ time: currentTime, lane: lane, type: 'bridge', pairLane: pairLane, bridgeId: bridgeId, hit: false, missed: false });
        notes.push({ time: currentTime, lane: pairLane, pairLane: lane, bridgeId: bridgeId, hit: false, missed: false });
      }
    }
    else if (index % 4 === 0 && (rand < (difficulty === 'extreme' ? 0.7 : 0.45))) {
      notes.push({ time: currentTime, lane: lane, type: 'swipe', swipeDir: lane === 0 ? 'right' : 'left', hit: false, missed: false });
    }
    else if (difficulty !== 'easy' && index % 6 === 0 && rand < 0.45) {
      notes.push({ time: currentTime, lane: lane, type: 'bonus', hit: false, missed: false });
    }
    else if (difficulty !== 'easy' && index % 7 === 0 && rand < (difficulty === 'extreme' ? 0.65 : 0.45)) {
      const zigzagDur = beatInterval * 1.2;
      const targetLane = (lane + (seededRandom() < 0.5 ? 1 : -1) + LANES) % LANES;
      if (currentTime >= activeLongEndTimes[targetLane]) {
        notes.push({ 
          time: currentTime, lane: lane, type: 'zigzag', duration: zigzagDur, 
          targetLane: targetLane, tailHit: false, holding: false, hit: false, missed: false 
        });
        activeLongEndTimes[lane] = currentTime + zigzagDur + 0.2;
        activeLongEndTimes[targetLane] = currentTime + zigzagDur + 0.2;
      }
    }
    else if (difficulty !== 'easy' && index % 3 === 0 && rand < 0.4) {
      const releaseDur = beatInterval * (seededRandom() * 0.8 + 0.8);
      notes.push({ time: currentTime, lane: lane, type: 'release', duration: releaseDur, tailHit: false, holding: false, hit: false, missed: false });
      activeLongEndTimes[lane] = currentTime + releaseDur + 0.2;
    }
    else if (difficulty !== 'easy' && index % 3 === 1 && rand < 0.45) {
      const longDuration = beatInterval * (seededRandom() * 1.0 + 0.8);
      notes.push({ time: currentTime, lane: lane, type: 'long', duration: longDuration, tailHit: false, holding: false, hit: false, missed: false });
      activeLongEndTimes[lane] = currentTime + longDuration + 0.2;
    }
    else {
      notes.push({ time: currentTime, lane: lane, type: 'normal', hit: false, missed: false });
    }

    if (difficulty === 'easy') {
      currentTime += beatInterval * 1.6;
    } else if (difficulty === 'normal') {
      currentTime += beatInterval * 1.0;
    } else if (difficulty === 'hard') {
      currentTime += beatInterval * 0.75;
    } else if (difficulty === 'expert') {
      currentTime += beatInterval * 0.5;
    } else {
      currentTime += beatInterval * 0.35;
    }
    index++;
  }
}

function incrementComboAndCheckMilestone() {
  combo++;
  if (combo > maxCombo) maxCombo = combo;

  const hasHuya = equippedUnit.includes('huya');
  const hasBaku = equippedUnit.includes('baku');
  if (hasHuya && hasBaku && currentHp >= maxHp) {
    iberisComboTracker++;
    if (iberisComboTracker >= 100) {
      iberisComboTracker = 0;
      score += 2500;
      showJudgement("🌟 100 COMBO BONUS!", "#ff79c6");
    }
  }
}

function applyHitScore(note, minDiff) {
  let mult = note.type === 'bonus' ? 3 : 1;
  const hasMashiro = equippedUnit.includes('mashiro');
  const hasMaro = equippedUnit.includes('maro');
  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');

  if (hasMashiro && mashiroSkillActivated && (note.type === 'swipe' || note.type === 'zigzag' || note.type === 'bridge')) {
    mult *= 1.40;
  }

  if (hasYuni && yuniSkillActivated) {
    mult *= 2.2;
    if (note.type === 'long' || note.type === 'release') {
      mult *= 1.5;
    }
  }

  if (doubleSkillActive) {
    mult *= 1.25;
  }

  if (hasMashiro && hasMaro && combo >= 200 && currentHp >= maxHp) {
    mult *= 1.15;
  }

  let effectiveCombo = combo;
  if (hasMashiro && mashiroSkillActivated) effectiveCombo += 50;

  // 패시브: 후야의 나른한 낮잠 시간 (곡 시작 시 10초 동안 스킬 게이지 쿨타임 15% 빠르게)
  let timeElapsed = (performance.now() - startTime) / 1000;
  let huyaPassiveBoost = (equippedUnit.includes('huya') && timeElapsed <= 10.0) ? 1.15 : 1.0;

  let chargeRate = 2.5 * huyaPassiveBoost;

  if (hasMashiro && !mashiroSkillActivated) {
    mashiroSkillGauge = Math.min(100, mashiroSkillGauge + chargeRate);
  }
  if (hasYuni && !yuniSkillActivated) {
    yuniSkillGauge = Math.min(100, yuniSkillGauge + chargeRate * 0.9);
  }
  if (hasHuya && !huyaSkillActivated) {
    huyaSkillGauge = Math.min(100, huyaSkillGauge + chargeRate * 0.9);
  }
  updateSkillUI();

  if (minDiff <= 0.15) {
    score += Math.round((100 + (effectiveCombo * 2)) * mult);
    incrementComboAndCheckMilestone();
    stats.perfect++;
    healHp(1.5);
    showJudgement(note.type === 'bonus' ? "BONUS PERFECT!" : "PERFECT!", note.type === 'bonus' ? "#c084fc" : "#00f2fe");
  } else if (minDiff <= 0.28) {
    let greatMult = (hasYuni && hasArunyang) ? 1.1 : 1.0;
    score += Math.round((70 + effectiveCombo) * mult * greatMult);
    incrementComboAndCheckMilestone();
    stats.great++;
    healHp(0.8);
    showJudgement(note.type === 'bonus' ? "BONUS GREAT!" : "GREAT!", "#4ade80");
  } else {
    score += Math.round(30 * mult);
    incrementComboAndCheckMilestone();
    stats.good++;
    showJudgement("GOOD", "#facc15");
  }
}

function healHp(amount) {
  const hasHuya = equippedUnit.includes('huya');
  const hasBaku = equippedUnit.includes('baku');
  let healMultiplier = (hasHuya && hasBaku) ? 1.2 : 1.0;
  currentHp = Math.min(maxHp, currentHp + (amount * healMultiplier));
  updateHpUI();
}

function damageHp(amount) {
  const hasHuya = equippedUnit.includes('huya');
  const hasBaku = equippedUnit.includes('baku');
  let dmgMultiplier = (hasHuya && hasBaku) ? 0.8 : 1.0;

  currentHp = Math.max(0, currentHp - (amount * dmgMultiplier));
  updateHpUI();
  if (currentHp <= 0) {
    triggerGameOver();
  }
}

function updateHpUI() {
  const percent = (currentHp / maxHp) * 100;
  hpFill.style.width = percent + '%';
  hpText.innerText = Math.round(currentHp) + ' / ' + maxHp;
  
  if (percent > 50) {
    hpFill.style.backgroundColor = '#4ade80';
  } else if (percent > 25) {
    hpFill.style.backgroundColor = '#facc15';
  } else {
    hpFill.style.backgroundColor = '#ff4b4b';
  }
}

function updateSkillUI() {
  mashiroGaugeFill.style.width = mashiroSkillGauge + '%';
  if (mashiroSkillGauge >= 100 && !mashiroSkillActivated && equippedUnit.includes('mashiro')) {
    triggerMashiroSkill();
  }

  yuniGaugeFill.style.width = yuniSkillGauge + '%';
  if (yuniSkillGauge >= 100 && !yuniSkillActivated && equippedUnit.includes('yuni')) {
    triggerYuniSkill();
  }

  huyaGaugeFill.style.width = huyaSkillGauge + '%';
  if (huyaSkillGauge >= 100 && !huyaSkillActivated && equippedUnit.includes('huya')) {
    triggerHuyaSkill();
  }
}

function triggerMashiroSkill() {
  mashiroSkillGauge = 0;
  mashiroGaugeFill.style.width = '0%';
  mashiroSkillActivated = true;
  mashiroSkillTimer = 12 * 60;
  
  mashiroSkillStatus.innerText = "🐾 발동 중!";
  mashiroSkillStatus.style.color = "#facc15";

  mashiroVoice.currentTime = 0;
  mashiroVoice.play().catch(e => {});
  mashiroPopup.classList.add('show');
  pawPrintAnimTimer = 40;
}

function triggerYuniSkill() {
  yuniSkillGauge = 0;
  yuniGaugeFill.style.width = '0%';
  yuniSkillActivated = true;
  
  let duration = equippedUnit.includes('huya') ? 12 * 60 : 10 * 60;
  yuniSkillTimer = duration;

  yuniSkillStatus.innerText = "🎤 [뭘뽀노?] ON";
  yuniSkillStatus.style.color = "#00f2fe";

  yuniVoice.currentTime = 0;
  yuniVoice.play().catch(e => {});
  yuniPopup.classList.add('show');
  galaxyAnimTimer = 50;

  if (huyaSkillActivated) {
    triggerDoubleSkill();
  }
}

function triggerHuyaSkill() {
  huyaSkillGauge = 0;
  huyaGaugeFill.style.width = '0%';
  huyaSkillActivated = true;

  const hasBaku = equippedUnit.includes('baku');
  let baseDuration = equippedUnit.includes('yuni') ? 17 * 60 : 15 * 60;
  if (hasBaku && currentHp >= maxHp) {
    baseDuration += 2 * 60;
  }
  huyaSkillTimer = baseDuration;

  huyaSkillStatus.innerText = "💤 [꿈결 속으로] ON";
  huyaSkillStatus.style.color = "#ff79c6";

  huyaVoice.currentTime = 0;
  huyaVoice.play().catch(e => {});
  huyaPopup.classList.add('show');

  if (yuniSkillActivated) {
    triggerDoubleSkill();
  }
}

function triggerDoubleSkill() {
  doubleSkillActive = true;
  doubleSkillTimer = 10 * 60;
  feverPopup.classList.add('show');
  setTimeout(() => { feverPopup.classList.remove('show'); }, 3000);
}

function requestGiveUp() {
  if (!isPlaying) return;
  isPlaying = false;
  const currentBgm = getActiveBgm();
  currentBgm.pause();

  if (confirm("정말 나가겠습니까? (진행 중인 게임은 저장되지 않습니다)")) {
    mashiroPopup.classList.remove('show');
    yuniPopup.classList.remove('show');
    huyaPopup.classList.remove('show');
    feverPopup.classList.remove('show');
    mashiroSkillBar.style.display = 'none';
    yuniSkillBar.style.display = 'none';
    huyaSkillBar.style.display = 'none';

    mainTitle.innerHTML = "RHYTHM STAR";
    mainTitle.style.color = "#00f2fe";
    statsContainer.style.display = 'none';
    nextPrepBtn.innerText = "유니트 편성 및 라이브";
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
    if (!note.hit && !note.missed && note.lane === lane && note.type !== 'swipe') {
      const diff = Math.abs(note.time - currentTime);
      if (diff < minDiff) {
        minDiff = diff;
        targetNote = note;
      }
    }
  }

  if (targetNote && minDiff <= 0.35) {
    targetNote.hit = true;
    if (targetNote.type === 'long' || targetNote.type === 'release' || targetNote.type === 'zigzag') {
      targetNote.holding = true;
    }
    applyHitScore(targetNote, minDiff);
  }
}

function handleSwipe(lane, dir) {
  if (!isPlaying) return;
  const currentTime = (performance.now() - startTime) / 1000;
  let targetNote = null;
  let minDiff = Infinity;

  for (let note of notes) {
    if (!note.hit && !note.missed && note.type === 'swipe' && Math.abs(note.lane - lane) <= 1) {
      const diff = Math.abs(note.time - currentTime);
      if (diff < minDiff) {
        minDiff = diff;
        targetNote = note;
      }
    }
  }

  if (targetNote && minDiff <= 0.35 && targetNote.swipeDir === dir) {
    targetNote.hit = true;
    const hasMashiro = equippedUnit.includes('mashiro');
    const hasMaro = equippedUnit.includes('maro');

    let mult = 1.0;
    if (hasMashiro && mashiroSkillActivated) mult *= 1.40;
    if (doubleSkillActive) mult *= 1.25;
    if (hasMashiro && hasMaro && combo >= 200 && currentHp >= maxHp) mult *= 1.15;

    let effectiveCombo = combo;
    if (hasMashiro && mashiroSkillActivated) effectiveCombo += 50;

    score += Math.round((120 + (effectiveCombo * 2)) * mult);
    incrementComboAndCheckMilestone();
    stats.perfect++;
    healHp(1.5);

    if (hasMashiro && !mashiroSkillActivated) {
      mashiroSkillGauge = Math.min(100, mashiroSkillGauge + 3.0);
    }
    showJudgement("SLIDE!", "#4ade80");
  }
}

function handleTapUp(lane) {
  const currentTime = (performance.now() - startTime) / 1000;
  for (let note of notes) {
    if ((note.type === 'long' || note.type === 'release' || note.type === 'zigzag') && note.holding && !note.tailHit && (note.lane === lane || (note.type === 'zigzag' && note.targetLane === lane))) {
      const endTime = note.time + note.duration;
      const diff = Math.abs(endTime - currentTime);
      note.holding = false;
      note.tailHit = true;

      let releaseWindow = (note.type === 'release') ? 0.3 : 0.4;

      if (diff <= releaseWindow || currentTime >= endTime - 0.25) {
        let addScore = (note.type === 'release') ? 100 : 50;
        const hasMashiro = equippedUnit.includes('mashiro');
        const hasMaro = equippedUnit.includes('maro');

        let mult = 1.0;
        if (hasMashiro && mashiroSkillActivated) mult *= 1.40;
        if (doubleSkillActive) mult *= 1.25;
        if (hasMashiro && hasMaro && combo >= 200 && currentHp >= maxHp) mult *= 1.15;

        score += Math.round(addScore * mult);
        incrementComboAndCheckMilestone();
        stats.perfect++;
        healHp(1.2);

        if (hasMashiro && !mashiroSkillActivated) {
          mashiroSkillGauge = Math.min(100, mashiroSkillGauge + 2.5);
        }
        showJudgement(note.type === 'release' ? "RELEASE PERFECT!" : "HOLD CLEAR", note.type === 'release' ? "#ff79c6" : "#00f2fe");
      } else {
        handleMiss();
      }
    }
  }
}

function handleMiss() {
  stats.miss++;
  iberisComboTracker = 0;

  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');

  if (hasYuni && yuniMissShieldCount > 0) {
    yuniMissShieldCount--;
    showJudgement(`🛡️ 유니 방패 발동! (잔여 ${yuniMissShieldCount}회)`, "#00f2fe");
    damageHp(5);
    return;
  }

  if (hasYuni && hasArunyang && yuniMissShieldCount <= 0 && yuniMissShieldCount > -2) {
    yuniMissShieldCount = -5;
    showJudgement(`🐾 아르냥 연계 방패 발동!`, "#c084fc");
    damageHp(5);
    return;
  }

  combo = 0;
  damageHp(10);
  showJudgement("MISS", "#ff4b4b");
}

function showJudgement(text, color) {
  judgementText = text;
  judgementColor = color;
  judgementTimer = 30;
}

function getLaneFromTouch(clientX) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const canvasX = (clientX - rect.left) * scaleX;
  const lane = Math.floor(canvasX / LANE_WIDTH);
  return Math.max(0, Math.min(LANES - 1, lane));
}

canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  if (!isPlaying) return;
  for (let i = 0; i < e.changedTouches.length; i++) {
    const touch = e.changedTouches[i];
    const lane = getLaneFromTouch(touch.clientX);
    activeTouches.set(touch.identifier, { lane: lane, startX: touch.clientX, swiped: false });
    keyPressed[lane] = true;
    handleTapDown(lane);
  }
}, { passive: false });

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  if (!isPlaying) return;
  for (let i = 0; i < e.changedTouches.length; i++) {
    const touch = e.changedTouches[i];
    const data = activeTouches.get(touch.identifier);
    if (data && !data.swiped) {
      const deltaX = touch.clientX - data.startX;
      if (Math.abs(deltaX) > 25) {
        data.swiped = true;
        handleSwipe(data.lane, deltaX > 0 ? 'right' : 'left');
      }
    }
  }
}, { passive: false });

function handleTouchEnd(e) {
  e.preventDefault();
  for (let i = 0; i < e.changedTouches.length; i++) {
    const touch = e.changedTouches[i];
    const data = activeTouches.get(touch.identifier);
    activeTouches.delete(touch.identifier);
    if (data !== undefined) {
      let stillPressed = false;
      for (let activeData of activeTouches.values()) {
        if (activeData.lane === data.lane) stillPressed = true;
      }
      if (!stillPressed) {
        keyPressed[data.lane] = false;
        handleTapUp(data.lane);
      }
    }
  }
}

canvas.addEventListener('touchend', handleTouchEnd, { passive: false });
canvas.addEventListener('touchcancel', handleTouchEnd, { passive: false });

window.addEventListener('keydown', (e) => {
  const key = e.key.toLowerCase();
  if (e.key === 'ArrowLeft' || key === 'a') {
    handleSwipe(1, 'left');
    handleSwipe(2, 'left');
    return;
  }
  if (e.key === 'ArrowRight' || key === 'l') {
    handleSwipe(1, 'right');
    handleSwipe(2, 'right');
    return;
  }
  const idx = KEYS.indexOf(key);
  if (idx !== -1 && !keyPressed[idx]) {
    keyPressed[idx] = true;
    handleTapDown(idx);
  }
});

window.addEventListener('keyup', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1) {
    keyPressed[idx] = false;
    handleTapUp(idx);
  }
});

function calculateRank(songId, difficulty, finalScore) {
  let multiplier = 1.0;
  if (songId === 'constellation') multiplier = 1.35;
  else if (songId === 'bbijilge') multiplier = 0.85;
  else if (songId === 'springdream') multiplier = 1.5;

  if (difficulty === 'easy') {
    if (finalScore >= 90000 * multiplier) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 75000 * multiplier) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 60000 * multiplier) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 45000 * multiplier) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 30000 * multiplier) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else if (difficulty === 'normal') {
    if (finalScore >= 180000 * multiplier) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 145000 * multiplier) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 115000 * multiplier) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 90000 * multiplier) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 65000 * multiplier) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else if (difficulty === 'hard') {
    if (finalScore >= 260000 * multiplier) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 210000 * multiplier) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 170000 * multiplier) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 135000 * multiplier) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 95000 * multiplier) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else if (difficulty === 'expert') {
    if (finalScore >= 350000 * multiplier) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 290000 * multiplier) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 230000 * multiplier) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 180000 * multiplier) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 120000 * multiplier) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else {
    if (finalScore >= 450000 * multiplier) return { rank: 'SS+', color: '#ff007f' };
    if (finalScore >= 380000 * multiplier) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 310000 * multiplier) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 250000 * multiplier) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 180000 * multiplier) return { rank: 'B', color: '#4ade80' };
    return { rank: 'C', color: '#fb923c' };
  }
}

function updateAndDraw() {
  if (!isPlaying) return;

  const currentBgm = getActiveBgm();
  const currentTime = (performance.now() - startTime) / 1000;

  // 1. 유니&아르냥 시너지: 체력 50% 미만 시 초당 체력 0.5% 자동 회복
  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');
  if (hasYuni && hasArunyang && currentHp < 50 && currentHp > 0) {
    currentHp = Math.min(maxHp, currentHp + 0.035);
    updateHpUI();
  }

  // 2. 기본 자연 회복 (체력이 100 미만일 때 서서히 회복)
  if (currentHp < maxHp && currentHp > 0) {
    currentHp = Math.min(maxHp, currentHp + 0.015);
    updateHpUI();
  }

  // 액티브 스킬 타이머 처리
  if (mashiroSkillActivated) {
    mashiroSkillTimer--;
    if (mashiroSkillTimer <= 0) {
      mashiroSkillActivated = false;
      mashiroPopup.classList.remove('show');
      mashiroSkillStatus.innerText = "충전 중...";
      mashiroSkillStatus.style.color = "#8b949e";
    }
  }

  if (yuniSkillActivated) {
    yuniSkillTimer--;
    if (yuniSkillTimer <= 0) {
      yuniSkillActivated = false;
      yuniPopup.classList.remove('show');
      yuniSkillStatus.innerText = "충전 중...";
      yuniSkillStatus.style.color = "#8b949e";
    }
  }

  if (huyaSkillActivated) {
    huyaSkillTimer--;
    currentHp = Math.min(maxHp, currentHp + 0.12); // 후야 액티브: 지속 체력 회복
    updateHpUI();

    if (huyaSkillTimer <= 0) {
      huyaSkillActivated = false;
      huyaPopup.classList.remove('show');
      huyaSkillStatus.innerText = "충전 중...";
      huyaSkillStatus.style.color = "#8b949e";
    }
  }

  if (doubleSkillActive) {
    doubleSkillTimer--;
    if (doubleSkillTimer <= 0) {
      doubleSkillActive = false;
    }
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (pawPrintAnimTimer > 0) {
    ctx.fillStyle = 'rgba(250, 204, 21, 0.35)';
    ctx.font = '24px sans-serif';
    ctx.fillText('🐾', 20, 250);
    ctx.fillText('🐾', 430, 250);
    pawPrintAnimTimer--;
  }

  if (galaxyAnimTimer > 0) {
    ctx.fillStyle = 'rgba(0, 242, 254, 0.35)';
    ctx.font = '24px sans-serif';
    ctx.fillText('✨🌌', 40, 220);
    ctx.fillText('🌌✨', 410, 220);
    galaxyAnimTimer--;
  }

  for (let i = 0; i < LANES; i++) {
    const x = i * LANE_WIDTH;
    
    if (keyPressed[i]) {
      const grad = ctx.createLinearGradient(0, HIT_Y - 200, 0, HIT_Y);
      grad.addColorStop(0, 'rgba(0, 242, 254, 0)');
      grad.addColorStop(1, 'rgba(0, 242, 254, 0.35)');
      ctx.fillStyle = grad;
      ctx.fillRect(x, HIT_Y - 200, LANE_WIDTH, 200);
    }

    ctx.fillStyle = keyPressed[i] ? LANE_COLORS[i] : '#1f2630';
    ctx.fillRect(x + 4, HIT_Y + 8, LANE_WIDTH - 8, canvas.height - HIT_Y - 14);

    ctx.strokeStyle = '#30363d';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();

    ctx.fillStyle = keyPressed[i] ? '#0e1117' : '#8b949e';
    ctx.font = 'bold 20px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('TAP', x + LANE_WIDTH / 2, HIT_Y + 72);
  }

  ctx.strokeStyle = '#00f2fe';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, HIT_Y);
  ctx.lineTo(canvas.width, HIT_Y);
  ctx.stroke();

  for (let note of notes) {
    if (note.type === 'bridge' && !note.missed && !note.hit && note.lane < note.pairLane) {
      const timeDiff = note.time - currentTime;
      const y = HIT_Y - (timeDiff * window.NOTE_SPEED);
      if (y >= -30 && y <= HIT_Y + 20) {
        const x1 = note.lane * LANE_WIDTH + LANE_WIDTH / 2;
        const x2 = note.pairLane * LANE_WIDTH + LANE_WIDTH / 2;
        ctx.strokeStyle = 'rgba(244, 114, 182, 0.75)';
        ctx.lineWidth = 8;
        ctx.beginPath();
        ctx.moveTo(x1, y);
        ctx.lineTo(x2, y);
        ctx.stroke();
      }
    }
  }

  let remainingNotes = 0;
  for (let note of notes) {
    if (note.missed || (note.hit && (note.type !== 'long' && note.type !== 'release' && note.type !== 'zigzag' || note.tailHit))) continue;
    remainingNotes++;

    const timeDiff = note.time - currentTime;
    const y = HIT_Y - (timeDiff * window.NOTE_SPEED);

    if ((note.type === 'long' || note.type === 'release' || note.type === 'zigzag') && note.holding) {
      const endY = HIT_Y - ((note.time + note.duration - currentTime) * window.NOTE_SPEED);

      if (note.type === 'zigzag') {
        const x1 = note.lane * LANE_WIDTH + LANE_WIDTH / 2;
        const x2 = note.targetLane * LANE_WIDTH + LANE_WIDTH / 2;
        ctx.strokeStyle = 'rgba(192, 132, 252, 0.85)';
        ctx.lineWidth = 12;
        ctx.beginPath();
        ctx.moveTo(x1, HIT_Y);
        ctx.lineTo(x2, Math.max(0, endY));
        ctx.stroke();
      } else {
        const x = note.lane * LANE_WIDTH + 14;
        const w = LANE_WIDTH - 28;
        ctx.fillStyle = note.type === 'release' ? 'rgba(255, 121, 198, 0.45)' : 'rgba(250, 204, 21, 0.45)';
        ctx.fillRect(x, Math.max(0, endY), w, HIT_Y - Math.max(0, endY));
      }

      if (currentTime >= note.time + note.duration) {
        note.holding = false;
        note.tailHit = true;
        let addScore = (note.type === 'release') ? 100 : 50;
        const hasMashiro = equippedUnit.includes('mashiro');
        const hasMaro = equippedUnit.includes('maro');

        let mult = 1.0;
        if (hasMashiro && mashiroSkillActivated) mult *= 1.40;
        if (yuniSkillActivated) mult *= 2.2;
        if (doubleSkillActive) mult *= 1.25;
        if (hasMashiro && hasMaro && combo >= 200 && currentHp >= maxHp) mult *= 1.15;

        score += Math.round(addScore * mult);
        incrementComboAndCheckMilestone();
        stats.perfect++;
        healHp(1.2);

        if (hasMashiro && !mashiroSkillActivated) {
          mashiroSkillGauge = Math.min(100, mashiroSkillGauge + 2.5);
        }
        showJudgement(note.type === 'release' ? "RELEASE PERFECT!" : "HOLD CLEAR", note.type === 'release' ? "#ff79c6" : "#00f2fe");
      }
      continue;
    }

    if (!note.hit && timeDiff < -0.40) {
      note.missed = true;
      handleMiss();
      continue;
    }

    if (y >= -50 && y <= HIT_Y + 20) {
      const x = note.lane * LANE_WIDTH + 10;
      const w = LANE_WIDTH - 20;

      if (note.type === 'long') {
        const tailY = y - (note.duration * window.NOTE_SPEED);
        ctx.fillStyle = 'rgba(250, 204, 21, 0.3)';
        ctx.fillRect(x + 4, tailY, w - 8, y - tailY);
        ctx.fillStyle = '#facc15';
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
      } 
      else if (note.type === 'release') {
        const tailY = y - (note.duration * window.NOTE_SPEED);
        ctx.fillStyle = 'rgba(255, 121, 198, 0.3)';
        ctx.fillRect(x + 4, tailY, w - 8, y - tailY);
        ctx.fillStyle = '#ff79c6';
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('▲UP', x + w / 2, y + 4);
      }
      else if (note.type === 'zigzag') {
        ctx.fillStyle = '#c084fc';
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('ZIG', x + w / 2, y + 4);
      }
      else if (note.type === 'swipe') {
        ctx.fillStyle = '#4ade80';
        ctx.beginPath();
        ctx.roundRect(x, y - 14, w, 28, 8);
        ctx.fill();
        ctx.fillStyle = '#0e1117';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(note.swipeDir === 'left' ? '◀ SLIDE' : 'SLIDE ▶', x + w / 2, y + 7);
      }
      else if (note.type === 'bridge') {
        ctx.fillStyle = '#f472b6';
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
      }
      else if (note.type === 'bonus') {
        ctx.fillStyle = '#c084fc';
        ctx.shadowColor = '#c084fc';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.roundRect(x, y - 14, w, 28, 8);
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('★3X★', x + w / 2, y + 5);
      }
      else {
        ctx.fillStyle = (yuniSkillActivated && (note.lane === 1 || note.lane === 2)) ? '#00f2fe' : LANE_COLORS[note.lane];
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
      }
    }
  }

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 22px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(`SCORE: ${score}`, 18, 56);

  let statusY = 76;
  const hasMashiro = equippedUnit.includes('mashiro');
  const hasMaro = equippedUnit.includes('maro');

  if (hasMashiro && mashiroSkillActivated) {
    ctx.fillStyle = '#facc15';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText('🐾 [시로] 플릭/연타 +40%', 18, statusY);
    statusY += 18;
  }

  if (yuniSkillActivated) {
    ctx.fillStyle = '#00f2fe';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText('🎤 [유니] 뭘뽀노? (점수 120% UP)', 18, statusY);
    statusY += 18;
  }

  if (huyaSkillActivated) {
    ctx.fillStyle = '#ff79c6';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText('💤 [후야] 포근한 꿈결 속으로 (체력 지속 회복)', 18, statusY);
    statusY += 18;
  }

  if (doubleSkillActive) {
    ctx.fillStyle = '#ff007f';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText('✨ [애버리스!] 더블 스킬 버프 발동중!', 18, statusY);
    statusY += 18;
  }

  if (hasMashiro && hasMaro && combo >= 200 && currentHp >= maxHp) {
    ctx.fillStyle = '#facc15';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText('✨ [냥냥 집사의 특급 후원] 상시 점수 +15%', 18, statusY);
  }

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
  score = 0;
  combo = 0;
  maxCombo = 0;
  judgementTimer = 0;
  
  mashiroSkillGauge = 0;
  mashiroSkillActivated = false;
  mashiroSkillTimer = 0;

  yuniSkillGauge = 0;
  yuniSkillActivated = false;
  yuniSkillTimer = 0;
  yuniMissShieldCount = 2;

  huyaSkillGauge = 0;
  huyaSkillActivated = false;
  huyaSkillTimer = 0;

  doubleSkillActive = false;
  doubleSkillTimer = 0;
  iberisComboTracker = 0;

  feverActive = false;
  
  currentHp = 100;
  updateHpUI();
  
  const hasMashiro = equippedUnit.includes('mashiro');
  if (hasMashiro) {
    mashiroSkillBar.style.display = 'flex';
    mashiroSkillStatus.innerText = "충전 중...";
    mashiroSkillStatus.style.color = "#8b949e";
    mashiroGaugeFill.style.width = '0%';
  } else {
    mashiroSkillBar.style.display = 'none';
  }

  const hasYuni = equippedUnit.includes('yuni');
  if (hasYuni) {
    yuniSkillBar.style.display = 'flex';
    yuniSkillStatus.innerText = "충전 중...";
    yuniSkillStatus.style.color = "#8b949e";
    yuniGaugeFill.style.width = '0%';
  } else {
    yuniSkillBar.style.display = 'none';
  }

  const hasHuya = equippedUnit.includes('huya');
  if (hasHuya) {
    huyaSkillBar.style.display = 'flex';
    huyaSkillStatus.innerText = "충전 중...";
    huyaSkillStatus.style.color = "#8b949e";
    huyaGaugeFill.style.width = '0%';
  } else {
    huyaSkillBar.style.display = 'none';
  }

  stats = { perfect: 0, great: 0, good: 0, miss: 0 };
  activeTouches.clear();
  keyPressed = [false, false, false, false];
  
  generateBeatmap(currentSongId, currentDifficulty);
  
  const currentBgm = getActiveBgm();
  currentBgm.pause();
  currentBgm.currentTime = 0;
  currentBgm.play().catch(error => {});

  isPlaying = true;
  startTime = performance.now();
  
  switchView('play');
  requestAnimationFrame(updateAndDraw);
}

function triggerGameOver() {
  isPlaying = false;
  const currentBgm = getActiveBgm();
  currentBgm.pause();
  mashiroPopup.classList.remove('show');
  yuniPopup.classList.remove('show');
  huyaPopup.classList.remove('show');
  feverPopup.classList.remove('show');
  mashiroSkillBar.style.display = 'none';
  yuniSkillBar.style.display = 'none';
  huyaSkillBar.style.display = 'none';

  mainTitle.innerHTML = "💔 GAME OVER (체력 소진)";
  mainTitle.style.color = "#ff4b4b";
  mainTitle.style.fontSize = "16px";

  statsContainer.innerHTML = `
    <div style="text-align: center; margin-bottom: 2px;">
      <div style="font-size: 10px; color: #ff4b4b; font-weight: bold;">FAILED</div>
      <div style="color: #ff4b4b; font-size: 16px; font-weight: bold;">체력이 모두 소진되었습니다.</div>
    </div>
    <div>🏆 중단 당시 점수: <b>${score.toLocaleString()}</b></div>
    <div>💎 최대 콤보: ${maxCombo} | 미스 횟수: ${stats.miss}회</div>
  `;
  
  navTabs.forEach(t => t.classList.remove('active'));
  navTabs[0].classList.add('active');
  tabContents.songs.style.display = 'flex';
  tabContents.gacha.style.display = 'none';
  tabContents.characters.style.display = 'none';
  tabContents.missions.style.display = 'none';
  tabContents.settings.style.display = 'none';

  statsContainer.style.display = 'block';
  nextPrepBtn.innerText = "유니트 편성 및 라이브 (Retry)";
  switchView('menu');
}

function endGame() {
  isPlaying = false;
  const currentBgm = getActiveBgm();
  currentBgm.pause();
  mashiroPopup.classList.remove('show');
  yuniPopup.classList.remove('show');
  huyaPopup.classList.remove('show');
  feverPopup.classList.remove('show');
  mashiroSkillBar.style.display = 'none';
  yuniSkillBar.style.display = 'none';
  huyaSkillBar.style.display = 'none';

  let clearTitle = "CLEAR!";
  let titleColor = "#ffffff";

  if (stats.miss === 0) {
    if (stats.great === 0 && stats.good === 0) {
      clearTitle = "퍼펙트 풀콤보! (ALL PERFECTION)";
      titleColor = '#c084fc';
    } else {
      clearTitle = "풀콤보! (FULL COMBO)";
      titleColor = '#00f2fe';
    }
  }

  const rankInfo = calculateRank(currentSongId, currentDifficulty, score);

  if (!bestRecords[currentSongId][currentDifficulty] || score > bestRecords[currentSongId][currentDifficulty].score) {
    bestRecords[currentSongId][currentDifficulty] = { score: score, rank: rankInfo.rank, color: rankInfo.color };
    clearTitle = "🎉 NEW RECORD! " + clearTitle;
  }

  stella += 25;
  missionData.playCount += 1;
  updateInventoryUI();
  updateMissionUI();
  updateSelectedRecordDisplay();
  saveGameData();

  const diffNameUI = { easy: '쉬움', normal: '보통', hard: '하드', expert: '익스퍼트', extreme: '익스트림' };
  mainTitle.innerHTML = `[${diffNameUI[currentDifficulty]}] ${clearTitle}`;
  mainTitle.style.color = titleColor;
  mainTitle.style.fontSize = "16px";

  statsContainer.innerHTML = `
    <div style="text-align: center; margin-bottom: 2px;">
      <div style="font-size: 10px; color: #8b949e;">[${diffNameUI[currentDifficulty]}] PLAY RESULT</div>
      <div class="rank-badge" style="color: ${rankInfo.color}; font-size: 18px; font-weight: bold;">RANK ${rankInfo.rank}</div>
    </div>
    <div>🏆 최종 점수: <b>${score.toLocaleString()}</b> (최고: ${bestRecords[currentSongId][currentDifficulty].score.toLocaleString()})</div>
    <div>💎 최대 콤보: ${maxCombo} | <span style="color: #facc15;">🌟 스텔라 +25 획득!</span></div>
    <div style="margin-top: 4px; border-top: 1px solid #30363d; padding-top: 4px;">
      ✨ PERFECT: <span style="color: #00f2fe;">${stats.perfect}</span> | 🌟 GREAT: <span style="color: #4ade80;">${stats.great}</span><br>
      ⚡ GOOD: <span style="color: #facc15;">${stats.good}</span> | ❌ MISS: <span style="color: #ff4b4b;">${stats.miss}</span>
    </div>
  `;
  
  navTabs.forEach(t => t.classList.remove('active'));
  navTabs[0].classList.add('active');
  tabContents.songs.style.display = 'flex';
  tabContents.gacha.style.display = 'none';
  tabContents.characters.style.display = 'none';
  tabContents.missions.style.display = 'none';
  tabContents.settings.style.display = 'none';

  statsContainer.style.display = 'block';
  nextPrepBtn.innerText = "유니트 편성 및 라이브 (Retry)";
  switchView('menu');
}

startBtn.addEventListener('click', startGame);
updateInventoryUI();
updateMissionUI();
</script>
</body>
</html>
"""

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
rhythm_game_html = rhythm_game_html.notes_match = True if False else rhythm_game_html.replace("YUNI_VOICE_PLACEHOLDER", yuni_voice_base64)
rhythm_game_html = rhythm_game_html.replace("HUYA_VOICE_PLACEHOLDER", huya_voice_base64)

components.html(rhythm_game_html, height=820)
