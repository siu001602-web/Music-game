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
            padding: 0rem !important;
            max-width: 100% !important;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        body { background-color: #0e1117; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

SONG_FILES = [
    ("music/Screen_Recording_20261117_180140_YouTube_17112026.m4a", "Image/SmartSelect_20261117_234657_YouTube.jpg"),
    ("music/Screen_Recording_20261118_013745_YouTube_18112026.m4a", "Image/SmartSelect_20261118_014123_YouTube.jpg"),
    ("music/Screen_Recording_20261118_180535_YouTube_18112026.m4a", "Image/SmartSelect_20261118_180837_YouTube.jpg")
]

CHAR_FILES = {
    "mashiro": "Character/SmartSelect_20261118_202345_NAVER.jpg",
    "huya": "Character/SmartSelect_20261118_174228_NAVER.jpg",
    "yuni": "Character/SmartSelect_20261118_003411_NAVER.jpg",
    "maro": "Character/SmartSelect_20261118_202541_NAVER.jpg",
    "arunyang": "Character/SmartSelect_20261118_010700_NAVER.jpg",
    "baku": "Character/SmartSelect_20261118_174346_NAVER.jpg"
}

VOICE_FILES = {
    "mashiro": "voice/Screen_Recording_20261118_202921_YouTube_18112026.m4a",
    "huya": "voice/Screen_Recording_20261118_175438_YouTube_18112026.m4a",
    "yuni": "voice/Screen_Recording_20261118_004242_YouTube_18112026.m4a"
}

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

audio_b64s = [get_b64(m) for m, i in SONG_FILES]
image_b64s = [get_b64(i) for m, i in SONG_FILES]
char_b64s = {k: get_b64(v) for k, v in CHAR_FILES.items()}
voice_b64s = {k: get_b64(v) for k, v in VOICE_FILES.items()}

rhythm_game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {{ box-sizing: border-box; touch-action: manipulation; -webkit-touch-callout: none; user-select: none; }}
  html, body {{ margin: 0; padding: 0; width: 100vw; height: 100vh; background-color: #0e1117; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
  #app-wrapper {{ position: relative; width: 100%; max-width: 480px; height: 100vh; max-height: 840px; background-color: #0e1117; border-left: 2px solid #30363d; border-right: 2px solid #30363d; overflow: hidden; }}
  #menu-screen {{ width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; background: linear-gradient(rgba(14, 17, 23, 0.94), rgba(14, 17, 23, 0.94)), url('data:image/jpeg;base64,{image_b64s[0]}'); background-size: cover; background-position: center; padding: 14px; text-align: center; }}
  #play-screen {{ width: 100%; height: 100%; display: none; position: relative; background-color: #161b22; }}
  canvas {{ width: 100%; height: 100%; display: block; background: linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('data:image/jpeg;base64,{image_b64s[0]}'); background-size: cover; background-position: center; touch-action: none; }}
  .nav-tabs {{ display: flex; gap: 3px; width: 100%; background: rgba(22, 27, 34, 0.9); padding: 5px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 8px; }}
  .nav-tab {{ flex: 1; padding: 6px 0; font-size: 10px; font-weight: bold; color: #8b949e; background: transparent; border: none; border-radius: 8px; cursor: pointer; }}
  .nav-tab.active {{ color: #0e1117; background: #00f2fe; box-shadow: 0 2px 10px rgba(0, 242, 254, 0.3); }}
  .tab-content {{ width: 100%; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow-y: auto; }}
  .section-title {{ font-size: 11px; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }}
  .song-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; width: 100%; max-height: 130px; overflow-y: auto; margin-bottom: 8px; padding: 4px; }}
  .song-card {{ background: #161b22; border: 2px solid #30363d; border-radius: 10px; padding: 6px; cursor: pointer; text-align: left; position: relative; }}
  .song-card.selected {{ border-color: #00f2fe; background: #1f2630; }}
  .song-thumb {{ width: 100%; height: 48px; border-radius: 6px; object-fit: cover; margin-bottom: 4px; }}
  .song-name {{ font-size: 10px; font-weight: bold; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .difficulty-select-container {{ display: flex; gap: 8px; width: 100%; justify-content: center; margin-bottom: 8px; }}
  .diff-card {{ flex: 1; background: #161b22; border: 2px solid #30363d; border-radius: 10px; padding: 6px 4px; cursor: pointer; text-align: center; }}
  .diff-card.selected {{ border-color: #00f2fe; background: #1f2630; }}
  .diff-lv {{ font-size: 10px; font-weight: bold; color: #8b949e; margin-bottom: 2px; }}
  .diff-name {{ font-size: 11px; font-weight: 900; }}
  .selected-diff-record-box {{ width: 100%; background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d; border-radius: 10px; padding: 7px 12px; margin-bottom: 8px; font-size: 11px; display: flex; justify-content: space-between; align-items: center; }}
  #prep-screen {{ width: 100%; height: 100%; background: rgba(14, 17, 23, 0.98); padding: 16px; display: none; flex-direction: column; text-align: left; }}
  .prep-header {{ font-size: 14px; font-weight: bold; color: #00f2fe; margin-bottom: 2px; }}
  .prep-sub {{ font-size: 11px; color: #8b949e; margin-bottom: 8px; }}
  .unit-slots {{ display: flex; gap: 8px; margin-bottom: 8px; }}
  .unit-slot {{ flex: 1; background: #161b22; border: 2px dashed #30363d; border-radius: 12px; height: 105px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; position: relative; padding: 6px; text-align: center; }}
  .unit-slot.filled {{ border-style: solid; }}
  .unit-slot.filled.star-5 {{ border-color: #facc15; }}
  .unit-slot.filled.star-4 {{ border-color: #c084fc; }}
  .slot-img {{ width: 42px; height: 42px; border-radius: 50%; object-fit: cover; margin-bottom: 2px; border: 2px solid currentColor; }}
  #char-select-modal {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(14, 17, 23, 0.96); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 30; padding: 20px; }}
  .char-select-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; margin-bottom: 14px; max-height: 360px; overflow-y: auto; }}
  .char-option-card {{ background: #161b22; border: 2px solid #30363d; border-radius: 12px; padding: 10px; display: flex; flex-direction: column; align-items: center; cursor: pointer; text-align: center; }}
  .prep-skill-card {{ background: rgba(255, 121, 198, 0.1); border: 1px solid #ff79c6; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; font-size: 11px; }}
  .prep-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: auto; }}
  .action-btn {{ padding: 9px 22px; font-size: 14px; font-weight: bold; color: #0e1117; background: #00f2fe; border: none; border-radius: 30px; cursor: pointer; }}
  .stats-box {{ background: rgba(255, 255, 255, 0.08); border: 1px solid #30363d; border-radius: 10px; padding: 8px 14px; margin: 2px 0 8px 0; width: 100%; text-align: left; font-size: 11px; line-height: 1.4; }}
  .controls-hint {{ margin-top: 6px; font-size: 10px; color: #8b949e; }}
  .gacha-box {{ background: #161b22; border: 2px solid #30363d; border-radius: 14px; padding: 16px; width: 100%; display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  .gacha-btn-group {{ display: flex; gap: 10px; width: 100%; }}
  .gacha-btn {{ flex: 1; padding: 10px; font-size: 13px; font-weight: bold; border: none; border-radius: 20px; cursor: pointer; }}
  .gacha-btn.single {{ background: #21262d; color: #00f2fe; border: 1px solid #00f2fe; }}
  .gacha-btn.multi {{ background: #00f2fe; color: #0e1117; }}
  #gacha-result-modal {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(14, 17, 23, 0.95); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 25; padding: 20px; }}
  .skill-popup {{ position: absolute; right: 55px; display: flex; align-items: center; gap: 8px; background: rgba(0, 242, 254, 0.25); border: 2px solid #00f2fe; border-radius: 30px; padding: 4px 12px 4px 4px; z-index: 20; opacity: 0; transform: translateY(-10px); transition: all 0.3s ease; pointer-events: none; }}
  .skill-popup.show {{ opacity: 1; transform: translateY(0); }}
  .skill-popup img {{ width: 30px; height: 30px; border-radius: 50%; object-fit: cover; }}
  #giveup-btn {{ position: absolute; top: 12px; right: 12px; width: 36px; height: 36px; background: rgba(255, 75, 75, 0.2); border: 2px solid #ff4b4b; border-radius: 50%; color: #ff4b4b; font-size: 16px; font-weight: bold; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 25; }}
  #hp-bar-container {{ position: absolute; top: 12px; left: 18px; width: 140px; background: rgba(14, 17, 23, 0.85); border: 2px solid #30363d; border-radius: 10px; padding: 4px 8px; display: flex; flex-direction: column; gap: 2px; z-index: 20; }}
  .hp-gauge-bg {{ width: 100%; height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; }}
  .hp-gauge-fill {{ width: 100%; height: 100%; background: #4ade80; transition: width 0.1s linear; }}
  #skill-gauges-wrapper {{ position: absolute; bottom: 12px; right: 12px; display: flex; flex-direction: column; gap: 6px; z-index: 20; }}
  .skill-bar-box {{ background: rgba(14, 17, 23, 0.85); border: 2px solid #30363d; border-radius: 12px; padding: 5px 10px; display: none; flex-direction: column; align-items: center; gap: 2px; }}
  .gauge-bg {{ width: 95px; height: 6px; background: #21262d; border-radius: 4px; overflow: hidden; }}
  .gauge-fill {{ width: 0%; height: 100%; transition: width 0.1s linear; }}
  .mission-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 10px; width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
</style>
</head>
<body>

<audio id="bgm1" preload="auto"><source src="data:audio/mp4;base64,{audio_b64s[0]}" type="audio/mp4"></audio>
<audio id="bgm2" preload="auto"><source src="data:audio/mp4;base64,{audio_b64s[1]}" type="audio/mp4"></audio>
<audio id="bgm3" preload="auto"><source src="data:audio/mp4;base64,{audio_b64s[2]}" type="audio/mp4"></audio>
<audio id="mashiro-voice" preload="auto"><source src="data:audio/mp4;base64,{voice_b64s['mashiro']}" type="audio/mp4"></audio>
<audio id="huya-voice" preload="auto"><source src="data:audio/mp4;base64,{voice_b64s['huya']}" type="audio/mp4"></audio>
<audio id="yuni-voice" preload="auto"><source src="data:audio/mp4;base64,{voice_b64s['yuni']}" type="audio/mp4"></audio>

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
        <div class="section-title">Select Song (악보 선택)</div>
        <div id="song-list" class="song-grid"></div>
        <div class="section-title">Difficulty (난이도 선택)</div>
        <div id="difficulty-container" class="difficulty-select-container"></div>
        <div class="selected-diff-record-box">
          <span id="menu-diff-label" style="font-weight: bold; color: #00f2fe;">🏆 [보통] 최고 기록</span>
          <span id="menu-diff-record" style="color: #fff;">기록 없음 (RANK: -)</span>
        </div>
      </div>
      <button id="next-prep-btn" class="action-btn" style="margin-top: 4px; padding: 9px 22px; font-size: 14px;">유니트 편성 및 라이브</button>
      <div id="controls-hint" class="controls-hint">🎹 노트: <b>[D] [F] [J] [K]</b> | 슬라이드: <b>[←][→]</b> 또는 <b>[A][L]</b></div>
    </div>

    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="gacha-box">
        <div style="font-size: 32px;">🌟</div>
        <div style="font-size: 15px; font-weight: bold; color: #00f2fe;">스타 스카우트 (캐릭터 뽑기)</div>
        <div style="font-size: 11px; color: #8b949e; text-align: center; line-height: 1.4;">
          • ⭐⭐⭐⭐⭐ 5성 픽업 (총 3%): 마시로(1%) / 후야(1%) / 유니(1%)<br>
          • ⭐⭐⭐⭐ 4성 픽업 (총 97%): 마로(33%) / 아르냥(32%) / 바쿠(32%)
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
      <div id="char-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; width: 100%; margin-top: 4px;"></div>
    </div>

    <div id="tab-missions" class="tab-content" style="display: none; align-items: flex-start; padding: 4px;">
      <div class="section-title">출석 체크 (매일 보상)</div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;"><b>📅 일일 출석 보상</b><br><span style="color: #8b949e; font-size: 10px;">스텔라 30개 받기</span></div>
        <button id="attendance-btn" onclick="claimAttendance()" style="padding: 6px 12px; font-size: 11px; font-weight: bold; background: #00f2fe; color: #0e1117; border: none; border-radius: 12px; cursor: pointer;">수령하기</button>
      </div>
      <div class="section-title" style="margin-top: 8px;">일일 임무</div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;"><b>🎵 라이브 3회 플레이</b><br><span id="mission-play-count" style="color: #8b949e; font-size: 10px;">진행도: 0 / 3</span></div>
        <button id="mission-play-btn" onclick="claimMission('play')" disabled style="padding: 6px 12px; font-size: 11px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 12px; cursor: pointer;">완료 (+30)</button>
      </div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;"><b>🎁 스카우트 1회 진행</b><br><span id="mission-gacha-count" style="color: #8b949e; font-size: 10px;">진행도: 0 / 1</span></div>
        <button id="mission-gacha-btn" onclick="claimMission('gacha')" disabled style="padding: 6px 12px; font-size: 11px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 12px; cursor: pointer;">완료 (+20)</button>
      </div>
    </div>

    <div id="tab-settings" class="tab-content" style="display: none; align-items: center; justify-content: center; padding: 10px;">
      <div class="gacha-box">
        <div style="font-size: 24px;">💾</div>
        <div style="font-size: 14px; font-weight: bold; color: #00f2fe;">게임 데이터 백업 및 복원</div>
        <div style="display: flex; gap: 8px; width: 100%; margin-top: 8px;">
          <button onclick="exportSaveData()" class="gacha-btn" style="background: #21262d; color: #4ade80; border: 1px solid #4ade80;">내보내기</button>
          <button onclick="importSaveDataPrompt()" class="gacha-btn" style="background: #00f2fe; color: #0e1117;">불러오기</button>
        </div>
        <button onclick="resetGameData()" style="background: transparent; color: #ff4b4b; border: 1px solid #ff4b4b; border-radius: 10px; padding: 6px; font-size: 11px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 4px;">초기화</button>
      </div>
    </div>
  </div>

  <div id="prep-screen">
    <div class="prep-header" id="prep-song-title">🎵 Star Trail</div>
    <div class="prep-sub">출전할 캐릭터 2명을 편성하세요.</div>
    <div class="unit-slots">
      <div id="slot-1" class="unit-slot" onclick="openCharSelector(0)"><div class="plus-icon">+</div><div style="font-size: 10px; color: #8b949e;">슬롯 1</div></div>
      <div id="slot-2" class="unit-slot" onclick="openCharSelector(1)"><div class="plus-icon">+</div><div style="font-size: 10px; color: #8b949e;">슬롯 2</div></div>
    </div>
    <div id="synergy-card" class="prep-skill-card" style="opacity: 0.5;">
      <div style="font-weight: bold; color: #8b949e; margin-bottom: 2px;">✨ 활성화된 시너지 없음</div>
      <div style="font-size: 10px; color: #8b949e;">• 조합에 따라 특수 시너지 발동!</div>
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
      <div style="display: flex; justify-content: space-between; font-size: 9px; font-weight: bold; color: #4ade80;"><span>❤️ HP</span><span id="hp-text">100 / 100</span></div>
      <div class="hp-gauge-bg"><div id="hp-fill" class="hp-gauge-fill"></div></div>
    </div>
    <div id="mashiro-popup" class="skill-popup"><img src="data:image/jpeg;base64,{char_b64s['mashiro']}"><span style="font-size: 11px; font-weight: bold; color: #facc15;">[반갑쟈나~] 발동!</span></div>
    <div id="fever-popup" class="skill-popup"><span style="font-size: 11px; font-weight: bold; color: #ff79c6;">🐾 [냥냥 피버] 충전 25% UP!</span></div>
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
    <div id="gacha-result-list" style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-bottom: 15px; max-height: 360px; overflow-y: auto;"></div>
    <button id="gacha-close-btn" class="action-btn">확인</button>
  </div>
</div>

<script>
const CHAR_DATA = {{
  mashiro: {{ name: '네네코 마시로', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{char_b64s["mashiro"]}' }},
  huya: {{ name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{char_b64s["huya"]}' }},
  yuni: {{ name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{char_b64s["yuni"]}' }},
  maro: {{ name: '마로 (팬)', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{char_b64s["maro"]}' }},
  arunyang: {{ name: '아르냥 (팬)', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{char_b64s["arunyang"]}' }},
  baku: {{ name: '바쿠 (팬)', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{char_b64s["baku"]}' }}
}};

const songs = [
  {{ id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,{image_b64s[0]}', audio: document.getElementById('bgm1'), duration: 225, type: 'starter', levels: {{ easy: 'Lv. 5', normal: 'Lv. 11', hard: 'Lv. 18' }} }},
  {{ id: 'bbijilge', title: '삐질게', thumb: 'data:image/jpeg;base64,{image_b64s[1]}', audio: document.getElementById('bgm2'), duration: 144, type: 'starter', levels: {{ easy: 'Lv. 6', normal: 'Lv. 12', hard: 'Lv. 19' }} }},
  {{ id: 'constellation', title: '별자리가 될 수 있다면', thumb: 'data:image/jpeg;base64,{image_b64s[2]}', audio: document.getElementById('bgm3'), duration: 255, type: 'advanced', levels: {{ normal: 'Lv. 13', hard: 'Lv. 20', expert: 'Lv. 28' }} }}
];

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let currentSongId = 'startrail', currentDifficulty = 'normal';
let stella = 100, ownedCharacters = {{ mashiro: false, huya: false, yuni: false, maro: false, arunyang: false, baku: false }}, equippedUnit = [null, null], activeSlotIndex = null;
let bestRecords = {{ startrail: {{}}, bbijilge: {{}}, constellation: {{}} }};
let missionData = {{ attendanceClaimed: false, playCount: 0, gachaCount: 0, playClaimed: false, gachaClaimed: false, date: new Date().toDateString() }};

function loadGameData() {{
  if (localStorage.getItem('rhythm_stella')) stella = parseInt(localStorage.getItem('rhythm_stella'));
  if (localStorage.getItem('rhythm_chars')) ownedCharacters = JSON.parse(localStorage.getItem('rhythm_chars'));
  if (localStorage.getItem('rhythm_records')) bestRecords = JSON.parse(localStorage.getItem('rhythm_records'));
  const m = localStorage.getItem('rhythm_missions');
  if (m) {{
    let parsed = JSON.parse(m);
    if (parsed.date === new Date().toDateString()) missionData = parsed;
  }}
}}
function saveGameData() {{
  localStorage.setItem('rhythm_stella', stella);
  localStorage.setItem('rhythm_chars', JSON.stringify(ownedCharacters));
  localStorage.setItem('rhythm_records', JSON.stringify(bestRecords));
  localStorage.setItem('rhythm_missions', JSON.stringify(missionData));
}}
loadGameData();

let isPlaying = false, startTime = 0, score = 0, combo = 0, maxCombo = 0, currentHp = 100, maxHp = 100;
let stats = {{ perfect: 0, great: 0, good: 0, miss: 0 }}, judgementText = "", judgementColor = "#fff", judgementTimer = 0;
let mashiroSkillGauge = 0, mashiroSkillActivated = false, mashiroSkillTimer = 0, feverActive = false, feverTimer = 0, lastFeverMinute = 0, pawPrintAnimTimer = 0;
let keyPressed = [false, false, false, false], activeTouches = new Map(), notes = [];

function getActiveBgm() {{ return songs.find(s => s.id === currentSongId).audio; }}

document.querySelectorAll('.nav-tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const target = tab.getAttribute('data-tab');
    Object.entries({{ songs: 'flex', gacha: 'flex', characters: 'flex', missions: 'flex', settings: 'flex' }}).forEach(([k, disp]) => {{
      document.getElementById('tab-' + k).style.display = (k === target) ? disp : 'none';
    }});
  }});
}});

function updateInventoryUI() {{
  document.getElementById('stella-count').innerText = stella;
  for (let i = 0; i < 2; i++) {{
    const slot = document.getElementById(`slot-${{i+1}}`), cid = equippedUnit[i];
    if (cid && CHAR_DATA[cid]) {{
      let c = CHAR_DATA[cid];
      slot.className = `unit-slot filled ${{c.star.length === 5 ? 'star-5' : 'star-4'}}`;
      slot.innerHTML = `<img src="data:image/jpeg;base64,${{c.img}}" class="slot-img" style="color:${{c.color}};"><div style="font-size:10px; font-weight:bold; color:${{c.color}};">${{c.star}}</div><div style="font-size:10px; font-weight:bold;">${{c.name}}</div>`;
    }} else {{
      slot.className = "unit-slot";
      slot.innerHTML = `<div class="plus-icon">+</div><div style="font-size: 10px; color: #8b949e;">슬롯 ${{i+1}}</div>`;
    }}
  }}

  let grid = document.getElementById('char-grid');
  grid.innerHTML = '';
  Object.entries(CHAR_DATA).forEach(([id, c]) => {{
    let owned = ownedCharacters[id];
    grid.innerHTML += `<div id="char-card-${{id}}" class="unit-slot filled" style="height: auto; padding: 10px; border-color: ${{owned ? c.color : '#30363d'}}; opacity: ${{owned ? 1 : 0.5}};">
      <div style="font-size: 24px; margin-bottom: 2px;"><img src="data:image/jpeg;base64,${{c.img}}" class="slot-img" style="color:${{c.color}};"></div>
      <div style="font-size: 9px; font-weight: bold; color: ${{c.color}};">${{c.star}} (${{owned ? '보유' : '미획득'}})</div>
      <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">${{c.name}}</div>
    </div>`;
  }});

  const synergy = document.getElementById('synergy-card');
  if (equippedUnit.includes('mashiro') && equippedUnit.includes('maro')) {{
    synergy.style.opacity = "1"; synergy.style.borderColor = "#facc15";
    synergy.innerHTML = `<div style="font-weight: bold; color: #facc15; margin-bottom: 2px;">🐾 활성화된 시너지: [냥냥 집사의 특급 후원]</div><div style="font-size: 10px; color: #fff;">• 200콤보 & HP 100% 시 노트 점수 상시 15% 증가!</div>`;
  }} else {{
    synergy.style.opacity = "0.5"; synergy.style.borderColor = "#30363d";
    synergy.innerHTML = `<div style="font-weight: bold; color: #8b949e; margin-bottom: 2px;">✨ 활성화된 시너지 없음</div><div style="font-size: 10px; color: #8b949e;">• 마시로 + 마로 편성 시 시너지 발동!</div>`;
  }}
}}

function openCharSelector(idx) {{
  activeSlotIndex = idx;
  let list = document.getElementById('char-select-list');
  list.innerHTML = '';
  Object.entries(CHAR_DATA).forEach(([id, c]) => {{
    let owned = ownedCharacters[id], equipped = equippedUnit.includes(id);
    list.innerHTML += `<div class="char-option-card" style="opacity: ${{owned && !equipped ? 1 : 0.45}}; border-color: ${{c.color}};" ${{owned && !equipped ? `onclick="selectChar('${{id}}')"` : ''}}>
      <img src="data:image/jpeg;base64,${{c.img}}" style="width:38px; height:38px; border-radius:50%; object-fit:cover; margin-bottom:4px; border:2px solid ${{c.color}};">
      <div style="font-size:9px; color:${{c.color}};">${{c.star}}</div>
      <div style="font-size:11px; font-weight:bold; margin-top:2px;">${{c.name}}</div>
      <div style="font-size:9px; color:${{owned ? (equipped ? '#facc15' : '#00f2fe') : '#8b949e'}}; margin-top:2px;">${{!owned ? '미획득' : (equipped ? '편성 중' : '선택 가능')}}</div>
    </div>`;
  }});
  document.getElementById('char-select-modal').style.display = 'flex';
}}
function selectChar(id) {{
  equippedUnit[activeSlotIndex] = id;
  document.getElementById('char-select-modal').style.display = 'none';
  updateInventoryUI();
}}
document.getElementById('modal-close-btn').addEventListener('click', () => {{ document.getElementById('char-select-modal').style.display = 'none'; }});

function executeGacha(count) {{
  let cost = count * 10;
  if (stella < cost) {{ alert("스텔라 재화가 부족합니다!"); return; }}
  stella -= cost;
  missionData.gachaCount += 1;
  updateMissionUI(); saveGameData();

  let results = [];
  for (let i = 0; i < count; i++) {{
    let r = Math.random() * 100, cid;
    if (r < 1.0) {{ cid = 'mashiro'; ownedCharacters.mashiro = true; }}
    else if (r < 2.0) {{ cid = 'huya'; ownedCharacters.huya = true; }}
    else if (r < 3.0) {{ cid = 'yuni'; ownedCharacters.yuni = true; }}
    else if (r < 35.33) {{ cid = 'maro'; ownedCharacters.maro = true; }}
    else if (r < 67.66) {{ cid = 'arunyang'; ownedCharacters.arunyang = true; }}
    else {{ cid = 'baku'; ownedCharacters.baku = true; }}
    results.push(CHAR_DATA[cid]);
  }}
  updateInventoryUI(); saveGameData();

  let rList = document.getElementById('gacha-result-list');
  rList.innerHTML = '';
  results.forEach(res => {{
    rList.innerHTML += `<div style="background:#21262d; border:1px solid ${{res.color}}; border-radius:10px; padding:8px; display:flex; flex-direction:column; align-items:center; width:88px;">
      <img src="data:image/jpeg;base64,${{res.img}}" style="width:36px; height:36px; border-radius:50%; object-fit:cover; margin-bottom:2px;">
      <div style="font-size:9px; color:${{res.color}};">${{res.star}}</div>
      <div style="font-size:10px; font-weight:bold; margin-top:2px;">${{res.name.split(' ')[0]}}</div>
    </div>`;
  }});
  document.getElementById('gacha-result-modal').style.display = 'flex';
}}
document.getElementById('gacha-1-btn').addEventListener('click', () => executeGacha(1));
document.getElementById('gacha-10-btn').addEventListener('click', () => executeGacha(10));
document.getElementById('gacha-close-btn').addEventListener('click', () => {{ document.getElementById('gacha-result-modal').style.display = 'none'; }});

function renderSongList() {{
  let sl = document.getElementById('song-list');
  sl.innerHTML = '';
  songs.forEach(s => {{
    sl.innerHTML += `<div class="song-card ${{s.id === currentSongId ? 'selected' : ''}}" onclick="selectSong('${{s.id}}')">
      <img src="${{s.thumb}}" class="song-thumb"><div class="song-name">🎵 ${{s.title}}</div>
    </div>`;
  }});
}}
function selectSong(id) {{
  currentSongId = id;
  renderSongList(); renderDifficultyButtons(); updateSelectedRecordDisplay();
}}
function renderDifficultyButtons() {{
  let s = songs.find(x => x.id === currentSongId), dc = document.getElementById('difficulty-container');
  dc.innerHTML = '';
  let diffs = s.type === 'starter' ? ['easy','normal','hard'] : ['normal','hard','expert'];
  if (!diffs.includes(currentDifficulty)) currentDifficulty = diffs[0];
  diffs.forEach(d => {{
    let nameMap = {{ easy: '쉬움', normal: '보통', hard: '하드', expert: '익스퍼트' }};
    dc.innerHTML += `<div class="diff-card ${{d === currentDifficulty ? 'selected' : ''}}" onclick="selectDiff('${{d}}')">
      <div class="diff-lv">${{s.levels[d]}}</div><div class="diff-name" style="color: ${{d==='easy'?'#4ade80':d==='normal'?'#00f2fe':d==='hard'?'#ff4b4b':'#c084fc'}}">${{nameMap[d]}}</div>
    </div>`;
  }});
}}
function selectDiff(d) {{ currentDifficulty = d; renderDifficultyButtons(); updateSelectedRecordDisplay(); }}
function updateSelectedRecordDisplay() {{
  let rec = bestRecords[currentSongId][currentDifficulty];
  let nameMap = {{ easy: '쉬움', normal: '보통', hard: '하드', expert: '익스퍼트' }};
  document.getElementById('menu-diff-label').innerText = `🏆 [${{nameMap[currentDifficulty]}}] 최고 기록`;
  document.getElementById('menu-diff-record').innerHTML = rec && rec.score > 0 ? `<b>${{rec.score.toLocaleString()}}점</b> (RANK: <span style="color:${{rec.color}}; font-weight:bold;">${{rec.rank}}</span>)` : `기록 없음 (RANK: -)`;
}}
renderSongList(); renderDifficultyButtons(); updateSelectedRecordDisplay();

document.getElementById('next-prep-btn').addEventListener('click', () => {{
  let s = songs.find(x => x.id === currentSongId);
  document.getElementById('prep-song-title').innerHTML = `🎵 ${{s.title}} [${{currentDifficulty}}]`;
  let rec = bestRecords[currentSongId][currentDifficulty];
  document.getElementById('prep-record-content').innerHTML = rec && rec.score > 0 ? `최고 점수: <b>${{rec.score.toLocaleString()}}점</b>` : `기록 없음`;
  document.getElementById('prep-screen').style.display = 'flex';
}});
document.getElementById('prep-back-btn').addEventListener('click', () => {{ document.getElementById('prep-screen').style.display = 'none'; }});
document.getElementById('prep-start-btn').addEventListener('click', startGame);

function generateBeatmap(songId, diff) {{
  notes = [];
  let seed = songId === 'bbijilge' ? 2000 : songId === 'constellation' ? 3000 : 1000;
  seed += diff === 'easy' ? 50 : diff === 'normal' ? 100 : diff === 'hard' ? 200 : 300;
  function rnd() {{ seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }}
  let t = 2.0, dur = songs.find(s => s.id === songId).duration, interval = 60 / 125;
  window.NOTE_SPEED = diff === 'expert' ? 520 : diff === 'hard' ? 490 : diff === 'normal' ? 450 : 420;
  
  let i = 0;
  while (t < dur - 5.0) {{
    let lane = Math.floor(rnd() * 4), r = rnd();
    if (i % 4 === 0 && r < 0.45) notes.push({{ time: t, lane: lane, type: 'swipe', swipeDir: lane === 0 ? 'right' : 'left', hit: false, missed: false }});
    else notes.push({{ time: t, lane: lane, type: 'normal', hit: false, missed: false }});
    t += interval * (diff === 'easy' ? 1.8 : diff === 'normal' ? 1.2 : diff === 'hard' ? 0.85 : 0.52);
    i++;
  }}
}}

function startGame() {{
  score = 0; combo = 0; maxCombo = 0; currentHp = 100; mashiroSkillGauge = 0; mashiroSkillActivated = false; feverActive = false;
  document.getElementById('prep-screen').style.display = 'none';
  document.getElementById('play-screen').style.display = 'block';
  document.getElementById('mashiro-skill-bar').style.display = equippedUnit.includes('mashiro') ? 'flex' : 'none';
  generateBeatmap(currentSongId, currentDifficulty);
  let bgm = getActiveBgm(); bgm.pause(); bgm.currentTime = 0; bgm.play().catch(e => {{}});
  isPlaying = true; startTime = performance.now();
  requestAnimationFrame(updateAndDraw);
}}

function requestGiveUp() {{
  if (!isPlaying) return;
  isPlaying = false; getActiveBgm().pause();
  if (confirm("정말 나가겠습니까?")) {{
    document.getElementById('play-screen').style.display = 'none';
    document.getElementById('mashiro-popup').classList.remove('show');
  }} else {{ isPlaying = true; requestAnimationFrame(updateAndDraw); }}
}}

function updateAndDraw() {{
  if (!isPlaying) return;
  let t = (performance.now() - startTime) / 1000, bgm = getActiveBgm();
  
  let curMin = Math.floor(t / 60);
  if (curMin > lastFeverMinute) {{ lastFeverMinute = curMin; feverActive = true; feverTimer = 3 * 60; document.getElementById('fever-popup').classList.add('show'); setTimeout(() => document.getElementById('fever-popup').classList.remove('show'), 3000); }}
  if (feverActive && --feverTimer <= 0) feverActive = false;
  if (mashiroSkillActivated && --mashiroSkillTimer <= 0) {{ mashiroSkillActivated = false; document.getElementById('mashiro-popup').classList.remove('show'); }}

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (pawPrintAnimTimer > 0) {{ ctx.fillStyle = 'rgba(250, 204, 21, 0.35)'; ctx.font = '24px sans-serif'; ctx.fillText('🐾', 20, 250); ctx.fillText('🐾', 430, 250); pawPrintAnimTimer--; }}

  for (let i = 0; i < 4; i++) {{
    ctx.fillStyle = keyPressed[i] ? ['#ff4b4b','#00f2fe','#00f2fe','#ff4b4b'][i] : '#1f2630';
    ctx.fillRect(i * 120 + 4, 578, 112, 134);
  }}
  ctx.strokeStyle = '#00f2fe'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, 570); ctx.lineTo(480, 570); ctx.stroke();

  let rem = 0;
  notes.forEach(n => {{
    if (n.missed || n.hit) return;
    rem++;
    let diff = n.time - t, y = 570 - (diff * window.NOTE_SPEED);
    if (diff < -0.35) {{ n.missed = true; combo = 0; currentHp = Math.max(0, currentHp - 10); document.getElementById('hp-fill').style.width = currentHp + '%'; return; }}
    if (y >= -50 && y <= 590) {{
      ctx.fillStyle = n.type === 'swipe' ? '#4ade80' : ['#ff4b4b','#00f2fe','#00f2fe','#ff4b4b'][n.lane];
      ctx.beginPath(); ctx.roundRect(n.lane * 120 + 10, y - 12, 100, 24, 6); ctx.fill();
    }}
  }});

  ctx.fillStyle = '#ffffff'; ctx.font = 'bold 22px sans-serif'; ctx.fillText(`SCORE: ${{score}}`, 18, 56);
  if (combo > 1) {{ ctx.fillStyle = '#00f2fe'; ctx.font = 'bold 34px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(`${{combo}} COMBO`, 240, 160); }}

  if (bgm.ended || (rem === 0 && t > songs.find(s=>s.id===currentSongId).duration - 2.0)) {{ endGame(); return; }}
  requestAnimationFrame(updateAndDraw);
}}

function endGame() {{
  isPlaying = false; getActiveBgm().pause();
  document.getElementById('play-screen').style.display = 'none';
  stella += 25; missionData.playCount++; saveGameData(); updateInventoryUI(); updateMissionUI();
  alert(`클리어! 점수: ${{score.toLocaleString()}}점 (스텔라 +25 획득)`);
}}

window.addEventListener('keydown', e => {{
  let k = e.key.toLowerCase(), idx = ['d','f','j','k'].indexOf(k);
  if (idx !== -1) {{
    keyPressed[idx] = true;
    let t = (performance.now() - startTime) / 1000;
    notes.forEach(n => {{
      if (!n.hit && !n.missed && n.lane === idx && Math.abs(n.time - t) <= 0.32) {{
        n.hit = true; combo++; score += 100 + combo * 2;
        if (equippedUnit.includes('mashiro') && !mashiroSkillActivated) {{
          mashiroSkillGauge = Math.min(100, mashiroSkillGauge + (feverActive ? 1.0 : 0.8));
          document.getElementById('mashiro-gauge-fill').style.width = mashiroSkillGauge + '%';
          if (mashiroSkillGauge >= 100) {{
            mashiroSkillActivated = true; mashiroSkillGauge = 0; mashiroSkillTimer = 12 * 60; pawPrintAnimTimer = 40;
            document.getElementById('mashiro-voice').play().catch(e=>{{}});
            document.getElementById('mashiro-popup').classList.add('show');
          }}
        }}
      }}
    });
  }}
}});
window.addEventListener('keyup', e => {{
  let idx = ['d','f','j','k'].indexOf(e.key.toLowerCase());
  if (idx !== -1) keyPressed[idx] = false;
}});

function updateMissionUI() {{
  document.getElementById('mission-play-count').innerText = `진행도: ${{missionData.playCount}} / 3`;
}}
updateInventoryUI();
</script>
</body>
</html>
"""

rhythm_game_html = rhythm_game_html.replace("{audio_b64s[0]}", audio_b64s[0])
rhythm_game_html = rhythm_game_html.replace("{audio_b64s[1]}", audio_b64s[1])
rhythm_game_html = rhythm_game_html.replace("{audio_b64s[2]}", audio_b64s[2])

components.html(rhythm_game_html, height=820)
