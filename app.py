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
        header, footer {visibility: hidden;}
        body { background-color: #0e1117; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# 파일 경로 정의
paths = {
    "s1_m": "music/Screen_Recording_20261117_180140_YouTube_17112026.m4a",
    "s1_i": "Image/SmartSelect_20261117_234657_YouTube.jpg",
    "s2_m": "music/Screen_Recording_20261118_013745_YouTube_18112026.m4a",
    "s2_i": "Image/SmartSelect_20261118_014123_YouTube.jpg",
    "s3_m": "music/Screen_Recording_20261118_180535_YouTube_18112026.m4a",
    "s3_i": "Image/SmartSelect_20261118_180837_YouTube.jpg",
    "yuni_i": "Character/SmartSelect_20261118_003411_NAVER.jpg",
    "yuni_v": "voice/Screen_Recording_20261118_004242_YouTube_18112026.m4a",
    "huya_i": "Character/SmartSelect_20261118_174228_NAVER.jpg",
    "huya_v": "voice/Screen_Recording_20261118_175438_YouTube_18112026.m4a",
    "mashiro_i": "Character/SmartSelect_20261118_202345_NAVER.jpg",
    "mashiro_v": "voice/Screen_Recording_20261118_202921_YouTube_18112026.m4a",
    "arunyang_i": "Character/SmartSelect_20261118_010700_NAVER.jpg",
    "baku_i": "Character/SmartSelect_20261118_174346_NAVER.jpg",
    "maro_i": "Character/SmartSelect_20261118_202541_NAVER.jpg"
}

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

b64 = {k: get_b64(v) for k, v in paths.items()}

rhythm_game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {{ box-sizing: border-box; touch-action: manipulation; -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; }}
  html, body {{ margin: 0; padding: 0; width: 100vw; height: 100vh; background-color: #0e1117; color: white; font-family: 'Segoe UI', sans-serif; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
  #app-wrapper {{ position: relative; width: 100%; max-width: 480px; height: 100vh; max-height: 840px; background-color: #0e1117; border-left: 2px solid #30363d; border-right: 2px solid #30363d; box-shadow: 0 0 25px rgba(0, 255, 255, 0.15); overflow: hidden; }}
  #menu-screen {{ width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; background: linear-gradient(rgba(14, 17, 23, 0.94), rgba(14, 17, 23, 0.94)), url('data:image/jpeg;base64,{b64["s1_i"]}'); background-size: cover; background-position: center; padding: 14px; text-align: center; }}
  #play-screen {{ width: 100%; height: 100%; display: none; position: relative; background-color: #161b22; }}
  canvas {{ width: 100%; height: 100%; display: block; background: linear-gradient(rgba(14, 17, 23, 0.72), rgba(14, 17, 23, 0.72)), url('data:image/jpeg;base64,{b64["s1_i"]}'); background-size: cover; background-position: center; touch-action: none; }}
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
  .new-badge {{ position: absolute; top: 6px; right: 6px; background: #ff4b4b; color: white; font-size: 8px; font-weight: bold; padding: 2px 4px; border-radius: 4px; }}
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
  .unit-slot {{ flex: 1; background: #161b22; border: 2px dashed #30363d; border-radius: 12px; height: 105px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; padding: 6px; text-align: center; }}
  .unit-slot.filled {{ border-style: solid; }}
  .unit-slot.filled.star-5 {{ border-color: #facc15; }}
  .unit-slot.filled.star-4 {{ border-color: #c084fc; }}
  .plus-icon {{ font-size: 26px; color: #8b949e; font-weight: bold; margin-bottom: 2px; }}
  .slot-img {{ width: 42px; height: 42px; border-radius: 50%; object-fit: cover; margin-bottom: 2px; border: 2px solid currentColor; }}
  #char-select-modal, #gacha-result-modal {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(14, 17, 23, 0.96); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 30; padding: 20px; }}
  .char-select-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; margin-bottom: 14px; max-height: 360px; overflow-y: auto; }}
  .char-option-card {{ background: #161b22; border: 2px solid #30363d; border-radius: 12px; padding: 10px; display: flex; flex-direction: column; align-items: center; cursor: pointer; text-align: center; }}
  .prep-skill-card {{ background: rgba(255, 121, 198, 0.1); border: 1px solid #ff79c6; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; font-size: 11px; }}
  .prep-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: auto; }}
  .action-btn {{ padding: 9px 22px; font-size: 14px; font-weight: bold; color: #0e1117; background: #00f2fe; border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4); }}
  .stats-box {{ background: rgba(255, 255, 255, 0.08); border: 1px solid #30363d; border-radius: 10px; padding: 8px 14px; margin: 2px 0 8px 0; width: 100%; text-align: left; font-size: 11px; line-height: 1.4; }}
  .controls-hint {{ margin-top: 6px; font-size: 10px; color: #8b949e; }}
  .gacha-box {{ background: #161b22; border: 2px solid #30363d; border-radius: 14px; padding: 16px; width: 100%; display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  .gacha-btn-group {{ display: flex; gap: 10px; width: 100%; }}
  .gacha-btn {{ flex: 1; padding: 10px; font-size: 13px; font-weight: bold; border: none; border-radius: 20px; cursor: pointer; }}
  .gacha-btn.single {{ background: #21262d; color: #00f2fe; border: 1px solid #00f2fe; }}
  .gacha-btn.multi {{ background: #00f2fe; color: #0e1117; }}
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

<audio id="bgm1" preload="auto"><source src="data:audio/mp4;base64,{b64['s1_m']}" type="audio/mp4"></audio>
<audio id="bgm2" preload="auto"><source src="data:audio/mp4;base64,{b64['s2_m']}" type="audio/mp4"></audio>
<audio id="bgm3" preload="auto"><source src="data:audio/mp4;base64,{b64['s3_m']}" type="audio/mp4"></audio>
<audio id="yuni-voice" preload="auto"><source src="data:audio/mp4;base64,{b64['yuni_v']}" type="audio/mp4"></audio>
<audio id="huya-voice" preload="auto"><source src="data:audio/mp4;base64,{b64['huya_v']}" type="audio/mp4"></audio>
<audio id="mashiro-voice" preload="auto"><source src="data:audio/mp4;base64,{b64['mashiro_v']}" type="audio/mp4"></audio>

<div id="app-wrapper">
  <div id="menu-screen">
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 4px;">
      <h1 id="main-title" style="margin: 0; color: #00f2fe; font-size: 18px;">RHYTHM STAR</h1>
      <div style="background: #161b22; border: 1px solid #facc15; border-radius: 12px; padding: 3px 10px; font-size: 12px; font-weight: bold; color: #facc15;">
        ⭐ 스텔라: <span id="stella-count">100</span>개
      </div>
    </div>
    
    <div class="nav-tabs">
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
      <button id="next-prep-btn" class="action-btn" style="margin-top: 4px;">유니트 편성 및 라이브</button>
      <div class="controls-hint">🎹 노트: <b>[D] [F] [J] [K]</b> | 슬라이드: <b>[←][→]</b> 또는 <b>[A][L]</b></div>
    </div>

    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="gacha-box">
        <div style="font-size: 32px;">🌟</div>
        <div style="font-size: 15px; font-weight: bold; color: #00f2fe;">스타 스카우트 (캐릭터 뽑기)</div>
        <div style="font-size: 11px; color: #8b949e; text-align: center; line-height: 1.4;">
          • ⭐⭐⭐⭐⭐ 5성 픽업 (합산 3%): 유니 / 후야 / 마시로 (각 1%)<br>
          • ⭐⭐⭐⭐ 4성 픽업 (합산 97%): 마로 / 아르냥 / 바쿠 (각 ~32.3%)
        </div>
        <div style="font-size: 12px; color: #facc15; font-weight: bold; margin: 4px 0;">소모 재화: 1회당 스텔라 10개</div>
        <div class="gacha-btn-group">
          <button id="gacha-1-btn" class="gacha-btn single" onclick="executeGacha(1)">1회 스카우트 (10개)</button>
          <button id="gacha-10-btn" class="gacha-btn multi" onclick="executeGacha(10)">10회 스카우트 (100개)</button>
        </div>
      </div>
    </div>

    <div id="tab-characters" class="tab-content" style="display: none;">
      <div class="section-title">보유 캐릭터 도감</div>
      <div id="char-dex-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; width: 100%; margin-top: 4px;"></div>
    </div>

    <div id="tab-missions" class="tab-content" style="display: none; align-items: flex-start; padding: 4px;">
      <div class="section-title">출석 체크 (매일 보상)</div>
      <div class="mission-card">
        <div style="font-size: 11px; text-align: left;"><b>📅 일일 출석 보상</b><br><span style="color: #8b949e; font-size: 10px;">스텔라 30개 수령!</span></div>
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
        <div style="font-size: 11px; color: #8b949e; text-align: center; line-height: 1.4;">데이터를 파일로 백업하고 안전하게 복구하세요!</div>
        <div style="display: flex; gap: 8px; width: 100%; margin-top: 8px;">
          <button onclick="exportSaveData()" class="gacha-btn" style="background: #21262d; color: #4ade80; border: 1px solid #4ade80;">내보내기</button>
          <button onclick="importSaveDataPrompt()" class="gacha-btn" style="background: #00f2fe; color: #0e1117;">불러오기</button>
        </div>
        <button onclick="resetGameData()" style="background: transparent; color: #ff4b4b; border: 1px solid #ff4b4b; border-radius: 10px; padding: 6px; font-size: 11px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 4px;">데이터 초기화</button>
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
      <div style="font-size: 10px; color: #8b949e;">• [유니냥], [조용히, 깨우지 마세요], [미스틱 하모니], [냥냥 집사의 특급 후원] 발동!</div>
    </div>
    <div style="background: rgba(0, 242, 254, 0.08); border: 1px solid #00f2fe; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; font-size: 12px;">
      <div style="font-weight: bold; color: #00f2fe; margin-bottom: 2px;" id="prep-record-title">🏆 [보통] 최고 기록</div>
      <div id="prep-record-content" style="color: #fff;">점수: 0점 (RANK: -)</div>
    </div>
    <div class="prep-footer">
      <button id="prep-back-btn" onclick="switchView('menu')" style="padding: 8px 16px; font-size: 12px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 20px; cursor: pointer;">취소</button>
      <button id="prep-start-btn" class="action-btn" onclick="startGame()">결정 (라이브 시작)</button>
    </div>
  </div>

  <div id="play-screen">
    <canvas id="gameCanvas" width="480" height="720"></canvas>
    <button id="giveup-btn" onclick="requestGiveUp()" title="중도포기">✕</button>
    <div id="hp-bar-container">
      <div style="display: flex; justify-content: space-between; font-size: 9px; font-weight: bold; color: #4ade80;"><span>❤️ HP</span><span id="hp-text">100 / 100</span></div>
      <div class="hp-gauge-bg"><div id="hp-fill" class="hp-gauge-fill"></div></div>
    </div>
    <div id="yuni-popup" class="skill-popup"><img src="data:image/jpeg;base64,{b64['yuni_i']}"><span style="font-size: 11px; font-weight: bold; color: #00f2fe;">[뭘뽀노?] 발동!</span></div>
    <div id="huya-popup" class="skill-popup"><img src="data:image/jpeg;base64,{b64['huya_i']}"><span style="font-size: 11px; font-weight: bold; color: #c084fc;">[에휴에요 에휴] 발동!</span></div>
    <div id="mashiro-popup" class="skill-popup"><img src="data:image/jpeg;base64,{b64['mashiro_i']}"><span style="font-size: 11px; font-weight: bold; color: #facc15;">[반갑쟈나~] 발동!</span></div>
    <div id="fever-popup" class="skill-popup"><span style="font-size: 11px; font-weight: bold; color: #ff79c6;">🐾 [냥냥 피버] 충전 25% UP!</span></div>
    <div id="skill-gauges-wrapper">
      <div id="yuni-skill-bar" class="skill-bar-box"><div style="font-size: 9px; font-weight: bold; color: #00f2fe;">✨ [뭘뽀노?]</div><div class="gauge-bg"><div id="yuni-gauge-fill" class="gauge-fill" style="background: #00f2fe;"></div></div><div id="yuni-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div></div>
      <div id="huya-skill-bar" class="skill-bar-box"><div style="font-size: 9px; font-weight: bold; color: #c084fc;">💤 [에휴에요 에휴]</div><div class="gauge-bg"><div id="huya-gauge-fill" class="gauge-fill" style="background: #c084fc;"></div></div><div id="huya-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div></div>
      <div id="mashiro-skill-bar" class="skill-bar-box"><div style="font-size: 9px; font-weight: bold; color: #facc15;">🐾 [반갑쟈나~]</div><div class="gauge-bg"><div id="mashiro-gauge-fill" class="gauge-fill" style="background: #facc15;"></div></div><div id="mashiro-skill-status" style="font-size: 9px; color: #8b949e; font-weight: bold;">충전 중...</div></div>
    </div>
  </div>

  <div id="char-select-modal">
    <div style="font-size: 15px; font-weight: bold; color: #00f2fe; margin-bottom: 10px;">👤 편성할 캐릭터 선택</div>
    <div class="char-select-grid" id="char-select-list"></div>
    <button onclick="document.getElementById('char-select-modal').style.display='none'" style="padding: 6px 20px; font-size: 12px; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 20px; cursor: pointer;">닫기</button>
  </div>

  <div id="gacha-result-modal">
    <div style="font-size: 16px; font-weight: bold; color: #facc15; margin-bottom: 10px;">🎁 뽑기 결과</div>
    <div id="gacha-result-list" style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-bottom: 15px; max-height: 360px; overflow-y: auto;"></div>
    <button onclick="document.getElementById('gacha-result-modal').style.display='none'" class="action-btn">확인</button>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const songs = [
  {{ id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,{b64["s1_i"]}', audio: document.getElementById('bgm1'), duration: 225, type: 'starter', levels: {{ easy: 'Lv. 5', normal: 'Lv. 11', hard: 'Lv. 18' }} }},
  {{ id: 'bbijilge', title: '삐질게', thumb: 'data:image/jpeg;base64,{b64["s2_i"]}', audio: document.getElementById('bgm2'), duration: 144, type: 'starter', levels: {{ easy: 'Lv. 6', normal: 'Lv. 12', hard: 'Lv. 19' }} }},
  {{ id: 'constellation', title: '별자리가 될 수 있다면', thumb: 'data:image/jpeg;base64,{b64["s3_i"]}', audio: document.getElementById('bgm3'), duration: 255, type: 'advanced', levels: {{ normal: 'Lv. 13', hard: 'Lv. 20', expert: 'Lv. 28' }} }}
];

const charMeta = {{
  yuni: {{ name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{b64["yuni_i"]}' }},
  huya: {{ name: '사키하네 후야', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{b64["huya_i"]}' }},
  mashiro: {{ name: '네네코 마시로', star: '⭐⭐⭐⭐⭐', color: '#facc15', img: '{b64["mashiro_i"]}' }},
  arunyang: {{ name: '아르냥 (팬)', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{b64["arunyang_i"]}' }},
  baku: {{ name: '바쿠 (팬)', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{b64["baku_i"]}' }},
  maro: {{ name: '마로 (팬)', star: '⭐⭐⭐⭐', color: '#c084fc', img: '{b64["maro_i"]}' }}
}};

let currentSongId = 'startrail', currentDifficulty = 'normal', stella = 100;
let ownedCharacters = {{ yuni: false, huya: false, mashiro: false, arunyang: false, baku: false, maro: false }};
let equippedUnit = [null, null], activeSlotIndex = null, isPlaying = false, startTime = 0, score = 0, combo = 0, maxCombo = 0, currentHp = 100, maxHp = 100;
let stats = {{ perfect: 0, great: 0, good: 0, miss: 0 }}, judgementText = "", judgementColor = "#fff", judgementTimer = 0;
let yuniGauge = 0, yuniActive = false, yuniTimer = 0, missShieldCount = 2, hornGlow = 0;
let huyaGauge = 0, huyaActive = false, huyaTimer = 0, doubleTimer = 0;
let mashiroGauge = 0, mashiroActive = false, mashiroTimer = 0, feverActive = false, feverTimer = 0, lastFeverMin = 0, pawTimer = 0;
let keyPressed = [false, false, false, false], activeTouches = new Map(), notes = [];
let bestRecords = {{
  startrail: {{ easy: {{score:0, rank:'-', color:'#94a3b8'}}, normal: {{score:0, rank:'-', color:'#94a3b8'}}, hard: {{score:0, rank:'-', color:'#94a3b8'}} }},
  bbijilge: {{ easy: {{score:0, rank:'-', color:'#94a3b8'}}, normal: {{score:0, rank:'-', color:'#94a3b8'}}, hard: {{score:0, rank:'-', color:'#94a3b8'}} }},
  constellation: {{ normal: {{score:0, rank:'-', color:'#94a3b8'}}, hard: {{score:0, rank:'-', color:'#94a3b8'}}, expert: {{score:0, rank:'-', color:'#94a3b8'}} }}
}};
let missionData = {{ attendanceClaimed: false, playCount: 0, gachaCount: 0, playClaimed: false, gachaClaimed: false, date: new Date().toDateString() }};

function loadData() {
  if (localStorage.getItem('rhythm_stella')) stella = parseInt(localStorage.getItem('rhythm_stella'));
  if (localStorage.getItem('rhythm_chars')) ownedCharacters = JSON.parse(localStorage.getItem('rhythm_chars'));
  if (localStorage.getItem('rhythm_records')) bestRecords = JSON.parse(localStorage.getItem('rhythm_records'));
  if (localStorage.getItem('rhythm_missions')) {
    let p = JSON.parse(localStorage.getItem('rhythm_missions'));
    if (p.date === new Date().toDateString()) missionData = p;
  }
}
function saveData() {
  localStorage.setItem('rhythm_stella', stella);
  localStorage.setItem('rhythm_chars', JSON.stringify(ownedCharacters));
  localStorage.setItem('rhythm_records', JSON.stringify(bestRecords));
  localStorage.setItem('rhythm_missions', JSON.stringify(missionData));
}
loadData();

function switchView(view) {
  document.getElementById('menu-screen').style.display = (view === 'menu') ? 'flex' : 'none';
  document.getElementById('prep-screen').style.display = (view === 'prep') ? 'flex' : 'none';
  document.getElementById('play-screen').style.display = (view === 'play') ? 'block' : 'none';
}

document.querySelectorAll('.nav-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    let target = tab.getAttribute('data-tab');
    ['songs', 'gacha', 'characters', 'missions', 'settings'].forEach(k => {
      document.getElementById('tab-' + k).style.display = (k === target) ? 'flex' : 'none';
    });
  });
});

function updateUI() {
  document.getElementById('stella-count').innerText = stella;
  for (let i = 0; i < 2; i++) {
    let slot = document.getElementById(`slot-${i+1}`);
    let cid = equippedUnit[i];
    if (cid && charMeta[cid]) {
      let m = charMeta[cid];
      slot.className = `unit-slot filled ${cid === 'yuni' || cid === 'huya' || cid === 'mashiro' ? 'star-5' : 'star-4'}`;
      slot.innerHTML = `<img src="data:image/jpeg;base64,${m.img}" class="slot-img" style="color:${m.color};"><div style="font-size:10px; font-weight:bold; color:${m.color};">${m.star}</div><div style="font-size:10px; font-weight:bold;">${m.name}</div>`;
    } else {
      slot.className = "unit-slot";
      slot.innerHTML = `<div class="plus-icon">+</div><div style="font-size: 10px; color: #8b949e;">슬롯 ${i+1}</div>`;
    }
  }

  // 시너지 판별
  let [c1, c2] = equippedUnit;
  let scCard = document.getElementById('synergy-card');
  if ((c1 === 'yuni' && c2 === 'arunyang') || (c1 === 'arunyang' && c2 === 'yuni')) {
    scCard.style.opacity = "1"; scCard.style.borderColor = "#ff79c6";
    scCard.innerHTML = `<div style="font-weight:bold; color:#ff79c6;">🐱 [유니냥] 100콤보 이상 점수 15% 증가!</div>`;
  } else if ((c1 === 'huya' && c2 === 'baku') || (c1 === 'baku' && c2 === 'huya')) {
    scCard.style.opacity = "1"; scCard.style.borderColor = "#f97316";
    scCard.innerHTML = `<div style="font-weight:bold; color:#f97316;">💤 [조용히, 깨우지 마세요] 풀피 시 지속시간 +2초 & 100콤보당 보너스!</div>`;
  } else if ((c1 === 'huya' && c2 === 'yuni') || (c1 === 'yuni' && c2 === 'huya')) {
    scCard.style.opacity = "1"; scCard.style.borderColor = "#c084fc";
    scCard.innerHTML = `<div style="font-weight:bold; color:#c084fc;">🔮 [미스틱 하모니] 더블 스킬 시 기본노트 +25%!</div>`;
  } else if ((c1 === 'mashiro' && c2 === 'maro') || (c1 === 'maro' && c2 === 'mashiro')) {
    scCard.style.opacity = "1"; scCard.style.borderColor = "#facc15";
    scCard.innerHTML = `<div style="font-weight:bold; color:#facc15;">🐾 [냥냥 집사의 특급 후원] 200콤보 & 풀피 시 상시 15% 증가!</div>`;
  } else {
    scCard.style.opacity = "0.5"; scCard.style.borderColor = "#30363d";
    scCard.innerHTML = `<div style="font-weight:bold; color:#8b949e;">✨ 활성화된 시너지 없음</div>`;
  }

  // 도감 렌더링
  let dexHTML = "";
  for (let key in charMeta) {
    let m = charMeta[key];
    let owned = ownedCharacters[key];
    dexHTML += `<div class="unit-slot filled" style="height:auto; padding:10px; border-color:${owned ? m.color : '#30363d'};">
      <div style="font-size:24px; margin-bottom:2px;"><img src="data:image/jpeg;base64,${m.img}" class="slot-img"></div>
      <div style="font-size:9px; font-weight:bold; color:${owned ? m.color : '#8b949e'}">${owned ? m.star + ' (보유)' : '미획득'}</div>
      <div style="font-size:11px; font-weight:bold; margin-top:2px;">${m.name}</div>
    </div>`;
  }
  document.getElementById('char-dex-grid').innerHTML = dexHTML;
  updateMissionUI();
}

function renderSongList() {
  let listEl = document.getElementById('song-list');
  listEl.innerHTML = '';
  songs.forEach(song => {
    let card = document.createElement('div');
    card.className = `song-card ${song.id === currentSongId ? 'selected' : ''}`;
    card.innerHTML = `<div style="position:relative;"><img src="${song.thumb}" class="song-thumb"><span class="new-badge">NEW</span></div><div class="song-name">🎵 ${song.title}</div>`;
    card.onclick = () => {
      currentSongId = song.id;
      document.getElementById('stats-container').style.display = 'none';
      document.getElementById('main-title').innerHTML = 'RHYTHM STAR';
      renderSongList(); renderDiffButtons(); updateRecord();
    };
    listEl.appendChild(card);
  });
}

function renderDiffButtons() {
  let song = songs.find(s => s.id === currentSongId);
  let diffContainer = document.getElementById('difficulty-container');
  diffContainer.innerHTML = '';
  let diffs = song.type === 'starter' ? [
    {key:'easy', label:'쉬움', lv:song.levels.easy}, {key:'normal', label:'보통', lv:song.levels.normal}, {key:'hard', label:'하드', lv:song.levels.hard}
  ] : [
    {key:'normal', label:'보통', lv:song.levels.normal}, {key:'hard', label:'하드', lv:song.levels.hard}, {key:'expert', label:'익스퍼트', lv:song.levels.expert}
  ];
  if (!diffs.some(d => d.key === currentDifficulty)) currentDifficulty = diffs[0].key;

  diffs.forEach(d => {
    let card = document.createElement('div');
    card.className = `diff-card ${d.key === currentDifficulty ? 'selected' : ''}`;
    card.innerHTML = `<div class="diff-lv">${d.lv}</div><div class="diff-name">${d.label}</div>`;
    card.onclick = () => {
      currentDifficulty = d.key;
      renderDiffButtons(); updateRecord();
    };
    diffContainer.appendChild(card);
  });
}

function updateRecord() {
  let rec = bestRecords[currentSongId][currentDifficulty];
  let diffNameMap = {easy:'쉬움', normal:'보통', hard:'하드', expert:'익스퍼트'};
  document.getElementById('menu-diff-label').innerText = `🏆 [${diffNameMap[currentDifficulty]}] 최고 기록`;
  if (rec && rec.score > 0) {
    document.getElementById('menu-diff-record').innerHTML = `<b>${rec.score.toLocaleString()}점</b> (RANK: <span style="color:${rec.color}; font-weight:bold;">${rec.rank}</span>)`;
  } else {
    document.getElementById('menu-diff-record').innerHTML = `기록 없음 (RANK: -)`;
  }
}

function updateMissionUI() {
  let attBtn = document.getElementById('attendance-btn');
  attBtn.innerText = missionData.attendanceClaimed ? "수령 완료" : "수령하기";
  attBtn.disabled = missionData.attendanceClaimed;

  document.getElementById('mission-play-count').innerText = `진행도: ${missionData.playCount} / 3`;
  let playBtn = document.getElementById('mission-play-btn');
  if (missionData.playClaimed) { playBtn.innerText = "완료됨"; playBtn.disabled = true; }
  else if (missionData.playCount >= 3) { playBtn.innerText = "수령 가능 (+30)"; playBtn.disabled = false; }
  else { playBtn.innerText = "진행 중"; playBtn.disabled = true; }

  document.getElementById('mission-gacha-count').innerText = `진행도: ${missionData.gachaCount} / 1`;
  let gachaBtn = document.getElementById('mission-gacha-btn');
  if (missionData.gachaClaimed) { gachaBtn.innerText = "완료됨"; gachaBtn.disabled = true; }
  else if (missionData.gachaCount >= 1) { gachaBtn.innerText = "수령 가능 (+20)"; gachaBtn.disabled = false; }
  else { gachaBtn.innerText = "진행 중"; gachaBtn.disabled = true; }
}

function claimAttendance() {
  if (!missionData.attendanceClaimed) {
    missionData.attendanceClaimed = true; stella += 30;
    updateUI(); saveData(); alert("📅 출석 보상으로 스텔라 30개를 획득하셨습니다!");
  }
}
function claimMission(type) {
  if (type === 'play' && missionData.playCount >= 3 && !missionData.playClaimed) {
    missionData.playClaimed = true; stella += 30;
    updateUI(); saveData(); alert("🎵 라이브 임무 보상으로 스텔라 30개를 획득하셨습니다!");
  } else if (type === 'gacha' && missionData.gachaCount >= 1 && !missionData.gachaClaimed) {
    missionData.gachaClaimed = true; stella += 20;
    updateUI(); saveData(); alert("🎁 스카우트 임무 보상으로 스텔라 20개를 획득하셨습니다!");
  }
}

function openCharSelector(slotIndex) {
  activeSlotIndex = slotIndex;
  let list = document.getElementById('char-select-list');
  list.innerHTML = "";
  let chars = [
    {id: 'yuni', name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐'},
    {id: 'huya', name: '사키하네 후야', star: '⭐⭐⭐⭐⭐'},
    {id: 'mashiro', name: '네네코 마시로', star: '⭐⭐⭐⭐⭐'},
    {id: 'arunyang', name: '아르냥', star: '⭐⭐⭐⭐'},
    {id: 'baku', name: '바쿠', star: '⭐⭐⭐⭐'},
    {id: 'maro', name: '마로', star: '⭐⭐⭐⭐'}
  ];
  chars.forEach(c => {
    let owned = ownedCharacters[c.id];
    let otherSlot = slotIndex === 0 ? 1 : 0;
    let equipped = equippedUnit[otherSlot] === c.id;
    let card = document.createElement('div');
    card.className = `char-option-card`;
    card.style.opacity = (owned && !equipped) ? "1" : "0.45";
    card.innerHTML = `<img src="data:image/jpeg;base64,${charMeta[c.id].img}" style="width:38px;height:38px;border-radius:50%;object-fit:cover;margin-bottom:4px;border:2px solid ${charMeta[c.id].color};"><div style="font-size:9px;color:${charMeta[c.id].color};">${c.star}</div><div style="font-size:11px;font-weight:bold;margin-top:2px;">${c.name}</div>`;
    if (owned && !equipped) {
      card.onclick = () => { equippedUnit[activeSlotIndex] = c.id; document.getElementById('char-select-modal').style.display = "none"; updateUI(); };
    }
    list.appendChild(card);
  });
  document.getElementById('char-select-modal').style.display = "flex";
}

function executeGacha(count) {
  let cost = count * 10;
  if (stella < cost) { alert("스텔라 재화가 부족합니다!"); return; }
  stella -= cost; missionData.gachaCount += 1;
  let results = [];
  for (let i = 0; i < count; i++) {
    let r = Math.random() * 100;
    let cid = "";
    // 5성 합산 3% (각 1%: 유니, 후야, 마시로) / 4성 합산 97% (각 ~32.3%: 아르냥, 바쿠, 마로)
    if (r < 1.0) { cid = 'yuni'; ownedCharacters.yuni = true; }
    else if (r < 2.0) { cid = 'huya'; ownedCharacters.huya = true; }
    else if (r < 3.0) { cid = 'mashiro'; ownedCharacters.mashiro = true; }
    else if (r < 35.3) { cid = 'arunyang'; ownedCharacters.arunyang = true; }
    else if (r < 67.6) { cid = 'baku'; ownedCharacters.baku = true; }
    else { cid = 'maro'; ownedCharacters.maro = true; }
    results.push(charMeta[cid]);
  }
  updateUI(); saveData();
  let resList = document.getElementById('gacha-result-list');
  resList.innerHTML = "";
  results.forEach(res => {
    let item = document.createElement('div');
    item.style.cssText = "background:#21262d;border:1px solid " + res.color + ";border-radius:10px;padding:8px;display:flex;flex-direction:column;align-items:center;width:88px;";
    item.innerHTML = `<img src="data:image/jpeg;base64,${res.img}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;margin-bottom:2px;"><div style="font-size:9px;color:${res.color};">${res.star}</div><div style="font-size:10px;font-weight:bold;margin-top:2px;">${res.name}</div>`;
    resList.appendChild(item);
  });
  document.getElementById('gacha-result-modal').style.display = "flex";
}

function generateBeatmap(songId, difficulty) {
  notes = [];
  let seed = songId === 'bbijilge' ? 2000 : (songId === 'constellation' ? 3000 : 1000);
  seed += difficulty === 'easy' ? 50 : (difficulty === 'normal' ? 100 : (difficulty === 'hard' ? 200 : 300));
  let rnd = () => { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
  let songObj = songs.find(s => s.id === songId);
  let beatInterval = 60 / 125, currentTime = 2.0;
  window.NOTE_SPEED = difficulty === 'expert' ? 520 : (difficulty === 'hard' ? 490 : 450);

  let idx = 0;
  while (currentTime < songObj.duration - 5.0) {
    let lane = Math.floor(rnd() * 4), r = rnd();
    if (idx % 4 === 0 && r < 0.45) {
      notes.push({ time: currentTime, lane: lane, type: 'swipe', swipeDir: lane === 0 ? 'right' : 'left', hit: false, missed: false });
    } else {
      notes.push({ time: currentTime, lane: lane, type: 'normal', hit: false, missed: false });
    }
    currentTime += difficulty === 'easy' ? beatInterval * 1.8 : (difficulty === 'normal' ? beatInterval * 1.2 : beatInterval * 0.75);
    idx++;
  }
}

function startGame() {
  score = 0; combo = 0; maxCombo = 0; currentHp = 100; judgementTimer = 0;
  yuniGauge = 0; yuniActive = false; huyaGauge = 0; huyaActive = false; mashiroGauge = 0; mashiroActive = false; feverActive = false;
  document.getElementById('yuni-skill-bar').style.display = equippedUnit.includes('yuni') ? 'flex' : 'none';
  document.getElementById('huya-skill-bar').style.display = equippedUnit.includes('huya') ? 'flex' : 'none';
  document.getElementById('mashiro-skill-bar').style.display = equippedUnit.includes('mashiro') ? 'flex' : 'none';
  stats = { perfect: 0, great: 0, good: 0, miss: 0 };
  generateBeatmap(currentSongId, currentDifficulty);
  let bgm = songs.find(s => s.id === currentSongId).audio;
  bgm.pause(); bgm.currentTime = 0; bgm.play().catch(e=>{});
  isPlaying = true; startTime = performance.now();
  switchView('play');
  requestAnimationFrame(updateAndDraw);
}

function requestGiveUp() {
  if (!isPlaying) return;
  isPlaying = false;
  songs.forEach(s => s.audio.pause());
  if (confirm("정말 나가겠습니까? (진행 중인 게임은 저장되지 않습니다)")) {
    switchView('menu');
  } else {
    isPlaying = true; requestAnimationFrame(updateAndDraw);
  }
}

function updateAndDraw() {
  if (!isPlaying) return;
  let currentTime = (performance.now() - startTime) / 1000;
  let bgm = songs.find(s => s.id === currentSongId).audio;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < 4; i++) {
    let x = i * LANE_WIDTH;
    ctx.fillStyle = keyPressed[i] ? LANE_COLORS[i] : '#1f2630';
    ctx.fillRect(x + 4, HIT_Y + 8, LANE_WIDTH - 8, canvas.height - HIT_Y - 14);
    ctx.strokeStyle = '#30363d'; ctx.lineWidth = 2; ctx.strokeRect(x, 0, LANE_WIDTH, canvas.height);
  }
  ctx.strokeStyle = '#00f2fe'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, HIT_Y); ctx.lineTo(canvas.width, HIT_Y); ctx.stroke();

  let rem = 0;
  notes.forEach(n => {
    if (n.missed || n.hit) return;
    rem++;
    let tDiff = n.time - currentTime, y = HIT_Y - (tDiff * window.NOTE_SPEED);
    if (!n.hit && tDiff < -0.35) { n.missed = true; combo = 0; currentHp = Math.max(0, currentHp - 10); }
    if (y >= -50 && y <= HIT_Y + 20) {
      ctx.fillStyle = LANE_COLORS[n.lane];
      ctx.beginPath(); ctx.roundRect(n.lane * LANE_WIDTH + 10, y - 12, LANE_WIDTH - 20, 24, 6); ctx.fill();
    }
  });

  ctx.fillStyle = '#ffffff'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'left'; ctx.fillText(`SCORE: ${score}`, 18, 56);
  if (combo > 1) { ctx.fillStyle = '#00f2fe'; ctx.font = 'bold 34px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(`${combo} COMBO`, canvas.width / 2, 160); }

  if (bgm.ended || (rem === 0 && currentTime > 5.0)) { endGame(); return; }
  requestAnimationFrame(updateAndDraw);
}

function endGame() {
  isPlaying = false;
  songs.forEach(s => s.audio.pause());
  let rec = bestRecords[currentSongId][currentDifficulty];
  if (!rec || score > rec.score) {
    bestRecords[currentSongId][currentDifficulty] = { score: score, rank: 'S', color: '#facc15' };
  }
  stella += 25; missionData.playCount += 1;
  saveData(); updateUI(); updateRecord();
  document.getElementById('stats-container').style.display = 'block';
  document.getElementById('stats-container').innerHTML = `🏆 최종 점수: <b>${score.toLocaleString()}점</b> | <span style="color:#facc15;">🌟 스텔라 +25!</span>`;
  switchView('menu');
}

renderSongList(); renderDiffButtons(); updateUI(); updateRecord();
</script>
</body>
</html>
"""

rhythm_game_html = rhythm_game_html.replace("{b64['s1_m']}", b64['s1_m'])
rhythm_game_html = rhythm_game_html.replace("{b64['s1_i']}", b64['s1_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['s2_m']}", b64['s2_m'])
rhythm_game_html = rhythm_game_html.replace("{b64['s2_i']}", b64['s2_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['s3_m']}", b64['s3_m'])
rhythm_game_html = rhythm_game_html.replace("{b64['s3_i']}", b64['s3_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['yuni_i']}", b64['yuni_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['huya_i']}", b64['huya_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['mashiro_i']}", b64['mashiro_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['arunyang_i']}", b64['arunyang_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['baku_i']}", b64['baku_i'])
rhythm_game_html = rhythm_game_html.replace("{b64['maro_i']}", b64['maro_i'])

components.html(rhythm_game_html, height=820)
