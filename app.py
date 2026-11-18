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

yuni_img_path = "Character/SmartSelect_20261118_003411_NAVER.jpg"
arunyang_img_path = "Character/SmartSelect_20261118_010700_NAVER.jpg"
yuni_voice_path = "voice/Screen_Recording_20261118_004242_YouTube_18112026.m4a"

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

audio1_base64 = get_base64(song1_music)
image1_base64 = get_base64(song1_img)

audio2_base64 = get_base64(song2_music)
image2_base64 = get_base64(song2_img)

yuni_img_base64 = get_base64(yuni_img_path)
arunyang_img_base64 = get_base64(arunyang_img_path)
yuni_voice_base64 = get_base64(yuni_voice_path)

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
  #game-container {
    position: relative;
    width: 100%;
    max-width: 480px;
    height: 100vh;
    max-height: 840px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #0e1117;
  }
  canvas {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: linear-gradient(rgba(14, 17, 23, 0.7), rgba(14, 17, 23, 0.7)), url('data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER');
    background-size: cover;
    background-position: center;
    background-color: #161b22;
    border-left: 2px solid #30363d;
    border-right: 2px solid #30363d;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.15);
    touch-action: none;
  }
  #ui-overlay {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex; flex-direction: column; justify-content: flex-start; align-items: center;
    background: linear-gradient(rgba(14, 17, 23, 0.94), rgba(14, 17, 23, 0.94)), url('data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER');
    background-size: cover; background-position: center;
    padding: 14px; text-align: center; z-index: 10;
  }

  .nav-tabs {
    display: flex; gap: 8px; width: 100%;
    background: rgba(22, 27, 34, 0.9); padding: 6px;
    border-radius: 12px; border: 1px solid #30363d; margin-bottom: 8px;
  }
  .nav-tab {
    flex: 1; padding: 6px 0; font-size: 12px; font-weight: bold;
    color: #8b949e; background: transparent; border: none; border-radius: 8px; cursor: pointer;
  }
  .nav-tab.active { color: #0e1117; background: #00f2fe; box-shadow: 0 2px 10px rgba(0, 242, 254, 0.3); }

  .tab-content { width: 100%; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }

  .section-title { font-size: 11px; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }

  .song-grid {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;
    width: 100%; max-height: 140px; overflow-y: auto; margin-bottom: 8px; padding: 4px;
  }
  .song-card {
    background: #161b22; border: 2px solid #30363d; border-radius: 10px;
    padding: 6px; cursor: pointer; text-align: left; transition: all 0.2s; position: relative;
  }
  .song-card.selected { border-color: #00f2fe; box-shadow: 0 0 12px rgba(0, 242, 254, 0.4); background: #1f2630; }
  .song-thumb { width: 100%; height: 55px; border-radius: 6px; object-fit: cover; margin-bottom: 4px; }
  .song-name { font-size: 12px; font-weight: bold; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .new-badge { position: absolute; top: 6px; right: 6px; background: #ff4b4b; color: white; font-size: 8px; font-weight: bold; padding: 2px 4px; border-radius: 4px; }

  .difficulty-select-container { display: flex; gap: 8px; width: 100%; justify-content: center; margin-bottom: 8px; }
  .diff-card {
    flex: 1; background: #161b22; border: 2px solid #30363d; border-radius: 10px;
    padding: 6px 4px; cursor: pointer; text-align: center; transition: all 0.2s;
  }
  .diff-card.selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); background: #1f2630; }
  .diff-card[data-diff="easy"].selected { border-color: #4ade80; box-shadow: 0 0 10px rgba(74, 222, 128, 0.4); }
  .diff-card[data-diff="normal"].selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); }
  .diff-card[data-diff="hard"].selected { border-color: #ff4b4b; box-shadow: 0 0 10px rgba(255, 75, 75, 0.4); }

  .diff-lv { font-size: 10px; font-weight: bold; color: #8b949e; margin-bottom: 2px; }
  .diff-name { font-size: 12px; font-weight: 900; }
  .diff-card[data-diff="easy"] .diff-name { color: #4ade80; }
  .diff-card[data-diff="normal"] .diff-name { color: #00f2fe; }
  .diff-card[data-diff="hard"] .diff-name { color: #ff4b4b; }

  #prep-screen {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(14, 17, 23, 0.97); padding: 16px; display: none; flex-direction: column; z-index: 15; text-align: left;
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
  .char-select-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; margin-bottom: 14px; }
  .char-option-card {
    background: #161b22; border: 2px solid #30363d; border-radius: 12px; padding: 12px;
    display: flex; flex-direction: column; align-items: center; cursor: pointer; text-align: center;
  }
  .char-option-card.owned { border-color: #00f2fe; }

  .prep-skill-card {
    background: rgba(255, 121, 198, 0.1); border: 1px solid #ff79c6; border-radius: 8px;
    padding: 6px 10px; margin-bottom: 8px; font-size: 11px;
  }
  .prep-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }

  .action-btn {
    padding: 9px 22px; font-size: 14px; font-weight: bold; color: #0e1117; background: #00f2fe;
    border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
  }

  .stats-box {
    background: rgba(255, 255, 255, 0.08); border: 1px solid #30363d; border-radius: 10px;
    padding: 8px 14px; margin: 2px 0 6px 0; width: 85%; text-align: left; font-size: 11px; line-height: 1.4;
  }
  .controls-hint { margin-top: 4px; font-size: 10px; color: #8b949e; }

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

  #yuni-popup {
    position: absolute; top: 15px; right: 15px;
    display: flex; align-items: center; gap: 8px; background: rgba(0, 242, 254, 0.25);
    border: 2px solid #00f2fe; border-radius: 30px; padding: 4px 12px 4px 4px; z-index: 20;
    opacity: 0; transform: translateY(-10px); transition: all 0.3s ease; pointer-events: none;
  }
  #yuni-popup.show { opacity: 1; transform: translateY(0); }
  #yuni-popup img { width: 30px; height: 30px; border-radius: 50%; object-fit: cover; }

  #skill-bar-container {
    position: absolute; bottom: 12px; right: 12px;
    background: rgba(14, 17, 23, 0.85); border: 2px solid #30363d; border-radius: 12px;
    padding: 6px 10px; display: none; flex-direction: column; align-items: center; gap: 3px; z-index: 20;
  }
  .gauge-bg { width: 90px; height: 7px; background: #21262d; border-radius: 4px; overflow: hidden; }
  .gauge-fill { width: 0%; height: 100%; background: #ff79c6; transition: width 0.1s linear; }
</style>
</head>
<body>

<audio id="bgm1" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO1_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="bgm2" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO2_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>
<audio id="yuni-voice" preload="auto">
  <source src="data:audio/mp4;base64,YUNI_VOICE_PLACEHOLDER" type="audio/mp4">
</audio>

<div id="game-container">
  <canvas id="gameCanvas" width="480" height="720"></canvas>
  
  <div id="yuni-popup">
    <img src="data:image/jpeg;base64,YUNI_IMG_PLACEHOLDER">
    <span style="font-size: 11px; font-weight: bold; color: #00f2fe;">[뭘뽀노?] 발동!</span>
  </div>

  <div id="skill-bar-container">
    <div style="font-size: 9px; font-weight: bold; color: #ff79c6;">✨ [뭘뽀노?] 게이지</div>
    <div class="gauge-bg"><div id="gauge-fill" class="gauge-fill"></div></div>
    <div id="skill-status" style="font-size: 10px; color: #8b949e; font-weight: bold;">자동 충전 중...</div>
  </div>

  <div id="char-select-modal">
    <div style="font-size: 15px; font-weight: bold; color: #00f2fe; margin-bottom: 10px;">👤 편성할 캐릭터 선택</div>
    <div class="char-select-grid" id="char-select-list"></div>
    <button id="modal-close-btn" style="padding: 6px 20px; font-size: 12px; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 20px; cursor: pointer;">닫기</button>
  </div>

  <div id="gacha-result-modal">
    <div style="font-size: 16px; font-weight: bold; color: #facc15; margin-bottom: 10px;">🎁 뽑기 결과</div>
    <div id="gacha-result-list" style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin-bottom: 15px;"></div>
    <button id="gacha-close-btn" class="action-btn">확인</button>
  </div>

  <div id="prep-screen">
    <div class="prep-header" id="prep-song-title">🎵 Star Trail</div>
    <div class="prep-sub">+ 버튼을 눌러 출전할 캐릭터를 편성하세요.</div>

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

    <div id="synergy-card" class="prep-skill-card" style="opacity: 0.4;">
      <div style="font-weight: bold; color: #ff79c6; margin-bottom: 2px;">🐱 시너지: [유니냥] (비활성)</div>
      <div style="font-size: 10px; color: #8b949e;" id="synergy-desc">• 유니와 아르냥을 모두 편성 시 100콤보 이상 점수 +15%</div>
    </div>

    <div style="background: rgba(0, 242, 254, 0.08); border: 1px solid #00f2fe; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; font-size: 12px;">
      <div style="font-weight: bold; color: #00f2fe; margin-bottom: 2px;" id="prep-record-title">🏆 [Normal] 최고 기록</div>
      <div id="prep-record-content" style="color: #fff;">점수: 0점 (RANK: -)</div>
    </div>

    <div class="prep-footer">
      <button id="prep-back-btn" style="padding: 8px 16px; font-size: 12px; font-weight: bold; background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius: 20px; cursor: pointer;">취소</button>
      <button id="prep-start-btn" class="action-btn" style="padding: 8px 22px; font-size: 14px;">결정 (라이브 시작)</button>
    </div>
  </div>

  <div id="ui-overlay">
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 4px;">
      <h1 id="main-title" style="margin: 0; color: #00f2fe; font-size: 18px;">RHYTHM STAR</h1>
      <div style="background: #161b22; border: 1px solid #facc15; border-radius: 12px; padding: 3px 10px; font-size: 12px; font-weight: bold; color: #facc15;">
        ⭐ 스텔라: <span id="stella-count">100</span>개
      </div>
    </div>
    
    <div id="nav-tabs" class="nav-tabs">
      <button class="nav-tab active" data-tab="songs">🎵 악보</button>
      <button class="nav-tab" data-tab="gacha">🎁 스카우트</button>
      <button class="nav-tab" data-tab="characters">👤 캐릭터</button>
    </div>

    <div id="tab-songs" class="tab-content">
      <div id="stats-container" class="stats-box" style="display: none;"></div>

      <div id="menu-group" style="width: 100%; display: flex; flex-direction: column; align-items: center;">
        <div class="section-title">Select Song (악보 선택)</div>
        <div id="song-list" class="song-grid"></div>

        <div class="section-title">Difficulty (난이도 선택)</div>
        <div class="difficulty-select-container">
          <div class="diff-card" data-diff="easy"><div class="diff-lv" id="lv-easy">Lv. 5</div><div class="diff-name">EASY</div></div>
          <div class="diff-card selected" data-diff="normal"><div class="diff-lv" id="lv-normal">Lv. 11</div><div class="diff-name">NORMAL</div></div>
          <div class="diff-card" data-diff="hard"><div class="diff-lv" id="lv-hard">Lv. 18</div><div class="diff-name">HARD</div></div>
        </div>
      </div>

      <button id="next-prep-btn" class="action-btn" style="margin-top: 6px; padding: 9px 22px; font-size: 14px;">유니트 편성 및 라이브</button>

      <div id="controls-hint" class="controls-hint">
        🎹 노트: <b>[D] [F] [J] [K]</b> | 슬라이드: <b>[←][→]</b> 또는 <b>[A][L]</b>
      </div>
    </div>

    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="gacha-box">
        <div style="font-size: 32px;">🌟</div>
        <div style="font-size: 15px; font-weight: bold; color: #00f2fe;">스타 스카우트 (캐릭터 뽑기)</div>
        <div style="font-size: 11px; color: #8b949e; text-align: center; line-height: 1.3;">
          • 5성 아야츠노 유니 (확률 5%)<br>• 4성 아르냥 팬 캐릭터 (확률 95%)
        </div>
        <div style="font-size: 12px; color: #facc15; font-weight: bold; margin: 4px 0;">소모 재화: 1회당 스텔라 10개</div>
        <div class="gacha-btn-group">
          <button id="gacha-1-btn" class="gacha-btn single">1회 스카우트 (10개)</button>
          <button id="gacha-10-btn" class="gacha-btn multi">10회 스카우트 (100개)</button>
        </div>
      </div>
    </div>

    <div id="tab-characters" class="tab-content" style="display: none;">
      <div class="section-title">보유 캐릭터 상태</div>
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; margin-top: 8px;">
        <div id="char-card-yuni" class="unit-slot filled" style="height: auto; padding: 12px; border-color: #30363d;">
          <div id="char-yuni-img-box" style="font-size: 26px; margin-bottom: 2px;">👤</div>
          <div id="char-yuni-badge" style="font-size: 10px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">아야츠노 유니</div>
        </div>
        <div id="char-card-arunyang" class="unit-slot filled" style="height: auto; padding: 12px; border-color: #30363d;">
          <div id="char-arunyang-img-box" style="font-size: 26px; margin-bottom: 2px;">👤</div>
          <div id="char-arunyang-badge" style="font-size: 10px; font-weight: bold; color: #8b949e;">미획득</div>
          <div style="font-size: 11px; font-weight: bold; margin-top: 2px;">아르냥 (팬)</div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const overlay = document.getElementById('ui-overlay');
const startBtn = document.getElementById('prep-start-btn');
const prepScreen = document.getElementById('prep-screen');
const nextPrepBtn = document.getElementById('next-prep-btn');
const prepBackBtn = document.getElementById('prep-back-btn');
const prepSongTitle = document.getElementById('prep-song-title');
const prepRecordTitle = document.getElementById('prep-record-title');
const prepRecordContent = document.getElementById('prep-record-content');

const bgm1 = document.getElementById('bgm1');
const bgm2 = document.getElementById('bgm2');
const yuniVoice = document.getElementById('yuni-voice');
const yuniPopup = document.getElementById('yuni-popup');
const skillBarContainer = document.getElementById('skill-bar-container');
const gaugeFill = document.getElementById('gauge-fill');
const skillStatus = document.getElementById('skill-status');
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
const diffCards = document.querySelectorAll('.diff-card');
const songListContainer = document.getElementById('song-list');

const lvEasy = document.getElementById('lv-easy');
const lvNormal = document.getElementById('lv-normal');
const lvHard = document.getElementById('lv-hard');

const navTabs = document.querySelectorAll('.nav-tab');
const tabContents = {
  songs: document.getElementById('tab-songs'),
  gacha: document.getElementById('tab-gacha'),
  characters: document.getElementById('tab-characters')
};

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
  { id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER', audio: bgm1, levels: { easy: 'Lv. 5', normal: 'Lv. 11', hard: 'Lv. 18' } },
  { id: 'bbijilge', title: '삐질게', thumb: 'data:image/jpeg;base64,IMAGE2_BASE64_PLACEHOLDER', audio: bgm2, levels: { easy: 'Lv. 6', normal: 'Lv. 12', hard: 'Lv. 19' } }
];

const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 570;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

let currentSongId = 'startrail';
let currentDifficulty = 'normal';

let stella = 100;
let ownedCharacters = { yuni: false, arunyang: false };
let equippedUnit = [null, null];
let activeSlotIndex = null;

let bestRecords = {
  startrail: {
    easy: { score: 0, rank: '-', color: '#94a3b8' },
    normal: { score: 0, rank: '-', color: '#94a3b8' },
    hard: { score: 0, rank: '-', color: '#94a3b8' }
  },
  bbijilge: {
    easy: { score: 0, rank: '-', color: '#94a3b8' },
    normal: { score: 0, rank: '-', color: '#94a3b8' },
    hard: { score: 0, rank: '-', color: '#94a3b8' }
  }
};

let isPlaying = false;
let startTime = 0;
let score = 0;
let combo = 0;
let maxCombo = 0;

let stats = { perfect: 0, great: 0, good: 0, miss: 0 };
let judgementText = "";
let judgementColor = "#fff";
let judgementTimer = 0;

let skillGauge = 0;
let yuniSkillActivated = false;
let yuniSkillTimer = 0;
let missShieldCount = 2;
let hornGlowTimer = 0;

let keyPressed = [false, false, false, false];
let activeTouches = new Map();
let notes = [];

function getActiveBgm() {
  const s = songs.find(item => item.id === currentSongId);
  return s ? s.audio : bgm1;
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
      renderSongList();
      updateDifficultyLevels();
    });
    songListContainer.appendChild(card);
  });
}

function updateDifficultyLevels() {
  const song = songs.find(s => s.id === currentSongId);
  if (song) {
    lvEasy.innerText = song.levels.easy;
    lvNormal.innerText = song.levels.normal;
    lvHard.innerText = song.levels.hard;
  }
}

renderSongList();
updateDifficultyLevels();

diffCards.forEach(card => {
  card.addEventListener('click', () => {
    diffCards.forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    currentDifficulty = card.getAttribute('data-diff');
  });
});

nextPrepBtn.addEventListener('click', () => {
  const song = songs.find(s => s.id === currentSongId);
  const diffNameMap = { easy: `EASY (${song.levels.easy})`, normal: `NORMAL (${song.levels.normal})`, hard: `HARD (${song.levels.hard})` };
  prepSongTitle.innerHTML = `🎵 ${song.title} [${diffNameMap[currentDifficulty]}]`;
  
  const rec = bestRecords[currentSongId][currentDifficulty];
  prepRecordTitle.innerHTML = `🏆 [${currentDifficulty.toUpperCase()}] 최고 기록`;
  if (rec.score > 0) {
    prepRecordContent.innerHTML = `최고 점수: <b>${rec.score.toLocaleString()}점</b> | RANK: <span style="color:${rec.color}; font-weight:bold;">${rec.rank}</span>`;
  } else {
    prepRecordContent.innerHTML = `기록 없음 (첫 클라이언트에 도전하세요!)`;
  }

  prepScreen.style.display = 'flex';
});

prepBackBtn.addEventListener('click', () => {
  prepScreen.style.display = 'none';
});

function updateInventoryUI() {
  stellaCountEl.innerText = stella;

  for (let i = 0; i < 2; i++) {
    const slotEl = document.getElementById(`slot-${i+1}`);
    const charId = equippedUnit[i];
    if (charId === 'yuni') {
      slotEl.className = "unit-slot filled star-5";
      slotEl.innerHTML = `
        <img src="data:image/jpeg;base64,YUNI_IMG_PLACEHOLDER" class="slot-img" style="color:#facc15;">
        <div style="font-size:10px; font-weight:bold; color:#facc15;">⭐⭐⭐⭐⭐</div>
        <div style="font-size:10px; font-weight:bold;">아야츠노 유니</div>
      `;
    } else if (charId === 'arunyang') {
      slotEl.className = "unit-slot filled star-4";
      slotEl.innerHTML = `
        <img src="data:image/jpeg;base64,USER_IMG_PLACEHOLDER" class="slot-img" style="color:#c084fc;">
        <div style="font-size:10px; font-weight:bold; color:#c084fc;">⭐⭐⭐⭐</div>
        <div style="font-size:10px; font-weight:bold;">아르냥 (팬)</div>
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
  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');

  if (hasYuni && hasArunyang) {
    synergyCard.style.opacity = "1";
    synergyCard.style.borderColor = "#ff79c6";
    synergyCard.innerHTML = `
      <div style="font-weight: bold; color: #ff79c6; margin-bottom: 2px;">🐱 활성화된 시너지: [유니냥]</div>
      <div style="font-size: 10px; color: #fff;">• <b>100콤보 이상 유지 시</b>, 기본/롱노트 점수 <b>15% 추가 증가!</b></div>
    `;
  } else {
    synergyCard.style.opacity = "0.4";
    synergyCard.style.borderColor = "#ff79c6";
    synergyCard.innerHTML = `
      <div style="font-weight: bold; color: #ff79c6; margin-bottom: 2px;">🐱 시너지: [유니냥] (비활성)</div>
      <div style="font-size: 10px; color: #8b949e;" id="synergy-desc">• 유니와 아르냥을 모두 편성 시 100콤보 이상 점수 +15%</div>
    `;
  }

  const charYuniCard = document.getElementById('char-card-yuni');
  const charArunyangCard = document.getElementById('char-card-arunyang');

  if (ownedCharacters.yuni) {
    charYuniCard.style.borderColor = "#facc15";
    document.getElementById('char-yuni-img-box').innerHTML = `<img src="data:image/jpeg;base64,YUNI_IMG_PLACEHOLDER" class="slot-img" style="color:#facc15;">`;
    document.getElementById('char-yuni-badge').innerHTML = "⭐⭐⭐⭐⭐ (보유)";
    document.getElementById('char-yuni-badge').style.color = "#facc15";
  }
  if (ownedCharacters.arunyang) {
    charArunyangCard.style.borderColor = "#c084fc";
    document.getElementById('char-arunyang-img-box').innerHTML = `<img src="data:image/jpeg;base64,USER_IMG_PLACEHOLDER" class="slot-img" style="color:#c084fc;">`;
    document.getElementById('char-arunyang-badge').innerHTML = "⭐⭐⭐⭐ (보유)";
    document.getElementById('char-arunyang-badge').style.color = "#c084fc";
  }
}

function openCharSelector(slotIndex) {
  activeSlotIndex = slotIndex;
  charSelectList.innerHTML = "";

  const availableChars = [
    { id: 'yuni', name: '아야츠노 유니', star: '⭐⭐⭐⭐⭐', owned: ownedCharacters.yuni, img: 'YUNI_IMG_PLACEHOLDER', color: '#facc15' },
    { id: 'arunyang', name: '아르냥 (팬)', star: '⭐⭐⭐⭐', owned: ownedCharacters.arunyang, img: 'USER_IMG_PLACEHOLDER', color: '#c084fc' }
  ];

  availableChars.forEach(char => {
    const card = document.createElement('div');
    card.className = `char-option-card ${char.owned ? 'owned' : ''}`;
    card.style.opacity = char.owned ? "1" : "0.5";
    card.innerHTML = `
      <img src="data:image/jpeg;base64,${char.img}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; margin-bottom:4px; border:2px solid ${char.color};">
      <div style="font-size:10px; color:${char.color};">${char.star}</div>
      <div style="font-size:11px; font-weight:bold; margin-top:2px;">${char.name}</div>
      <div style="font-size:9px; color:${char.owned ? '#00f2fe' : '#8b949e'}; margin-top:2px;">${char.owned ? '선택 가능' : '미획득 (스카우트 필요)'}</div>
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
    alert("스텔라 재화가 부족합니다! 곡을 클리어하여 모아보세요.");
    return;
  }
  stella -= cost;
  updateInventoryUI();

  let results = [];
  for (let i = 0; i < count; i++) {
    const rand = Math.random() * 100;
    if (rand < 5.0) {
      ownedCharacters.yuni = true;
      results.push({ name: "아야츠노 유니 (5성)", star: "⭐⭐⭐⭐⭐", color: "#facc15", img: "YUNI_IMG_PLACEHOLDER" });
    } else {
      ownedCharacters.arunyang = true;
      results.push({ name: "아르냥 (4성)", star: "⭐⭐⭐⭐", color: "#c084fc", img: "USER_IMG_PLACEHOLDER" });
    }
  }

  updateInventoryUI();

  gachaResultList.innerHTML = "";
  results.forEach(res => {
    const item = document.createElement('div');
    item.style.cssText = "background:#21262d; border:1px solid " + res.color + "; border-radius:10px; padding:8px; display:flex; flex-direction:column; align-items:center; width:90px;";
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
  
  let seed = songId === 'startrail' ? 1000 : 2000;
  if (difficulty === 'easy') seed += 100;
  else if (difficulty === 'normal') seed += 200;
  else if (difficulty === 'hard') seed += 300;

  function seededRandom() {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  }

  const bpm = 125;
  const beatInterval = 60 / bpm; 
  let currentTime = 2.0;
  
  // 🌟 삐질게는 2분 20초(~140초) 길이에 맞춰 채보 생성, 스타트레일은 기존 유지
  const totalDuration = (songId === 'bbijilge') ? 140.0 : 225.0;

  let speed = 420;
  if (difficulty === 'normal') speed = 450;
  if (difficulty === 'hard') speed = 490;
  window.NOTE_SPEED = speed;

  let index = 0;
  while (currentTime < totalDuration - 5.0) {
    const lane = Math.floor(seededRandom() * LANES);
    const rand = seededRandom();

    if (index % 5 === 0 && rand < 0.35) {
      const pairLane = (lane + 2) % LANES;
      const bridgeId = `bridge_${index}`;
      notes.push({ time: currentTime, lane: lane, type: 'bridge', pairLane: pairLane, bridgeId: bridgeId, hit: false, missed: false });
      notes.push({ time: currentTime, lane: pairLane, pairLane: lane, bridgeId: bridgeId, hit: false, missed: false });
    }
    else if (index % 4 === 0 && rand < 0.45) {
      const dir = lane === 0 ? 'right' : (lane === 3 ? 'left' : (seededRandom() < 0.5 ? 'left' : 'right'));
      notes.push({ time: currentTime, lane: lane, type: 'swipe', swipeDir: dir, hit: false, missed: false });
    }
    else if (difficulty !== 'easy' && index % 6 === 0 && rand < 0.5) {
      notes.push({ time: currentTime, lane: lane, type: 'bonus', hit: false, missed: false });
    }
    else if (difficulty !== 'easy' && index % 3 === 0 && rand < 0.45) {
      notes.push({ time: currentTime, lane: lane, type: 'long', duration: beatInterval * (seededRandom() * 1.2 + 1.0), tailHit: false, holding: false, hit: false, missed: false });
    }
    else {
      notes.push({ time: currentTime, lane: lane, type: 'normal', hit: false, missed: false });
    }

    if (difficulty === 'easy') {
      currentTime += beatInterval * 1.8;
    } else if (difficulty === 'normal') {
      currentTime += beatInterval * 1.2;
    } else {
      currentTime += beatInterval * 0.85;
    }
    index++;
  }
}

function applyHitScore(note, minDiff) {
  let mult = note.type === 'bonus' ? 3 : 1;
  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');

  if (hasYuni && yuniSkillActivated) {
    mult *= 1.05;
  }

  if (hasYuni && hasArunyang && combo >= 100 && (note.type === 'normal' || note.type === 'long')) {
    mult *= 1.15;
  }

  if (hasYuni && !yuniSkillActivated) {
    skillGauge = Math.min(100, skillGauge + 0.8);
    updateSkillUI();
  }

  if (minDiff <= 0.12) {
    score += Math.round((100 + combo * 2) * mult);
    combo++;
    stats.perfect++;
    showJudgement(note.type === 'bonus' ? "BONUS PERFECT!" : "PERFECT!", note.type === 'bonus' ? "#c084fc" : "#00f2fe");
  } else if (minDiff <= 0.22) {
    score += Math.round((70 + combo) * mult);
    combo++;
    stats.great++;
    showJudgement(note.type === 'bonus' ? "BONUS GREAT!" : "GREAT!", "#4ade80");
  } else {
    score += Math.round(30 * mult);
    combo++;
    stats.good++;
    showJudgement("GOOD", "#facc15");
  }
  if (combo > maxCombo) maxCombo = combo;
}

function updateSkillUI() {
  gaugeFill.style.width = skillGauge + '%';
  if (skillGauge >= 100 && !yuniSkillActivated && equippedUnit.includes('yuni')) {
    triggerYuniSkill();
  }
}

function triggerYuniSkill() {
  skillGauge = 0;
  gaugeFill.style.width = '0%';
  yuniSkillActivated = true;
  yuniSkillTimer = 600;
  
  skillStatus.innerText = "✨ [뭘뽀노?] 발동 중!";
  skillStatus.style.color = "#ff79c6";

  yuniVoice.currentTime = 0;
  yuniVoice.play().catch(e => {});
  yuniPopup.classList.add('show');
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

  if (targetNote && minDiff <= 0.32) {
    targetNote.hit = true;
    if (targetNote.type === 'long') targetNote.holding = true;
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

  if (targetNote && minDiff <= 0.32 && targetNote.swipeDir === dir) {
    targetNote.hit = true;
    let addScore = 120 + combo * 2;
    const hasYuni = equippedUnit.includes('yuni');
    if (hasYuni && yuniSkillActivated) addScore *= 1.05;
    score += Math.round(addScore);
    combo++;
    stats.perfect++;
    if (hasYuni && !yuniSkillActivated) {
      skillGauge = Math.min(100, skillGauge + 0.8);
      updateSkillUI();
    }
    if (combo > maxCombo) maxCombo = combo;
    showJudgement("SLIDE!", "#4ade80");
  }
}

function handleTapUp(lane) {
  const currentTime = (performance.now() - startTime) / 1000;
  for (let note of notes) {
    if (note.type === 'long' && note.holding && !note.tailHit && note.lane === lane) {
      const endTime = note.time + note.duration;
      const diff = Math.abs(endTime - currentTime);
      note.holding = false;
      note.tailHit = true;

      if (diff <= 0.35 || currentTime >= endTime - 0.2) {
        let addScore = 50;
        const hasYuni = equippedUnit.includes('yuni');
        const hasArunyang = equippedUnit.includes('arunyang');
        if (hasYuni && yuniSkillActivated) addScore *= 1.05;
        if (hasYuni && hasArunyang && combo >= 100) addScore *= 1.15;
        score += Math.round(addScore);
        combo++;
        stats.perfect++;
        if (hasYuni && !yuniSkillActivated) {
          skillGauge = Math.min(100, skillGauge + 0.8);
          updateSkillUI();
        }
        showJudgement("HOLD CLEAR", "#00f2fe");
      } else {
        handleMiss();
      }
    }
  }
}

function handleMiss() {
  stats.miss++;
  const hasYuni = equippedUnit.includes('yuni');
  if (hasYuni && missShieldCount > 0) {
    missShieldCount--;
    hornGlowTimer = 40;
    showJudgement("UNI SHIELD! (콤보 유지)", "#ff79c6");
  } else {
    combo = 0;
    showJudgement("MISS", "#ff4b4b");
  }
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
    if (!keyPressed[lane]) {
      keyPressed[lane] = true;
      handleTapDown(lane);
    }
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

function calculateRank(difficulty, finalScore) {
  if (difficulty === 'easy') {
    if (finalScore >= 90000) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 80000) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 70000) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 60000) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 50000) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else if (difficulty === 'normal') {
    if (finalScore >= 195000) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 150000) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 120000) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 95000) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 70000) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else {
    if (finalScore >= 280000) return { rank: 'SS', color: '#ff79c6' };
    if (finalScore >= 250000) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 200000) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 150000) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 100000) return { rank: 'C', color: '#00f2fe' };
    return { rank: 'D', color: '#94a3b8' };
  }
}

function updateAndDraw() {
  if (!isPlaying) return;

  const currentBgm = getActiveBgm();
  const currentTime = (performance.now() - startTime) / 1000;

  if (yuniSkillActivated) {
    yuniSkillTimer--;
    if (yuniSkillTimer <= 0) {
      yuniSkillActivated = false;
      yuniPopup.classList.remove('show');
      skillStatus.innerText = "자동 충전 중...";
      skillStatus.style.color = "#8b949e";
    }
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);

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

  ctx.strokeStyle = hornGlowTimer > 0 ? '#ff79c6' : '#00f2fe';
  ctx.lineWidth = hornGlowTimer > 0 ? 8 : 4;
  ctx.beginPath();
  ctx.moveTo(0, HIT_Y);
  ctx.lineTo(canvas.width, HIT_Y);
  ctx.stroke();
  if (hornGlowTimer > 0) hornGlowTimer--;

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
    if (note.missed || (note.hit && (note.type !== 'long' || note.tailHit))) continue;
    remainingNotes++;

    const timeDiff = note.time - currentTime;
    const y = HIT_Y - (timeDiff * window.NOTE_SPEED);

    if (note.type === 'long' && note.holding) {
      const endY = HIT_Y - ((note.time + note.duration - currentTime) * window.NOTE_SPEED);
      const x = note.lane * LANE_WIDTH + 14;
      const w = LANE_WIDTH - 28;
      
      ctx.fillStyle = 'rgba(250, 204, 21, 0.45)';
      ctx.fillRect(x, Math.max(0, endY), w, HIT_Y - Math.max(0, endY));

      if (currentTime >= note.time + note.duration) {
        note.holding = false;
        note.tailHit = true;
        let addScore = 50;
        const hasYuni = equippedUnit.includes('yuni');
        const hasArunyang = equippedUnit.includes('arunyang');
        if (hasYuni && yuniSkillActivated) addScore *= 1.05;
        if (hasYuni && hasArunyang && combo >= 100) addScore *= 1.15;
        score += Math.round(addScore);
        combo++;
        stats.perfect++;
        if (hasYuni && !yuniSkillActivated) {
          skillGauge = Math.min(100, skillGauge + 0.8);
          updateSkillUI();
        }
        showJudgement("HOLD CLEAR", "#00f2fe");
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

      if (note.type === 'long') {
        const tailY = y - (note.duration * window.NOTE_SPEED);
        ctx.fillStyle = 'rgba(250, 204, 21, 0.3)';
        ctx.fillRect(x + 4, tailY, w - 8, y - tailY);
        ctx.fillStyle = '#facc15';
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
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
        ctx.fillStyle = LANE_COLORS[note.lane];
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
      }
    }
  }

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 22px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(`SCORE: ${score}`, 18, 36);

  const hasYuni = equippedUnit.includes('yuni');
  const hasArunyang = equippedUnit.includes('arunyang');

  if (hasYuni && yuniSkillActivated) {
    ctx.fillStyle = '#ff79c6';
    ctx.font = 'bold 13px sans-serif';
    ctx.fillText('✨ [뭘뽀노?] 보너스 점수 +5%', 18, 56);
  }

  if (hasYuni && hasArunyang && combo >= 100) {
    ctx.fillStyle = '#c084fc';
    ctx.font = 'bold 13px sans-serif';
    ctx.fillText('🐱 [유니냥] 시너지 상시 점수 +15%', 18, 76);
  }

  if (combo > 1) {
    ctx.fillStyle = '#00f2fe';
    ctx.font = 'bold 34px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${combo} COMBO`, canvas.width / 2, 140);
  }

  if (judgementTimer > 0) {
    ctx.fillStyle = judgementColor;
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(judgementText, canvas.width / 2, 185);
    judgementTimer--;
  }

  if (currentBgm.ended || (remainingNotes === 0 && currentTime > notes[notes.length - 1].time + 2.0)) {
    endGame();
    return;
  }

  requestAnimationFrame(updateAndDraw);
}

function startGame() {
  prepScreen.style.display = 'none';

  score = 0;
  combo = 0;
  maxCombo = 0;
  judgementTimer = 0;
  skillGauge = 0;
  yuniSkillActivated = false;
  missShieldCount = 2;
  
  const hasYuni = equippedUnit.includes('yuni');
  if (hasYuni) {
    skillBarContainer.style.display = 'flex';
    skillStatus.innerText = "자동 충전 중...";
    skillStatus.style.color = "#8b949e";
    gaugeFill.style.width = '0%';
  } else {
    skillBarContainer.style.display = 'none';
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
  
  overlay.style.display = 'none';
  requestAnimationFrame(updateAndDraw);
}

function endGame() {
  isPlaying = false;
  const currentBgm = getActiveBgm();
  currentBgm.pause();
  yuniPopup.classList.remove('show');
  skillBarContainer.style.display = 'none';

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

  const rankInfo = calculateRank(currentDifficulty, score);

  if (score > bestRecords[currentSongId][currentDifficulty].score) {
    bestRecords[currentSongId][currentDifficulty] = { score: score, rank: rankInfo.rank, color: rankInfo.color };
    clearTitle = "🎉 NEW RECORD! " + clearTitle;
  }

  stella += 25;
  updateInventoryUI();

  mainTitle.innerHTML = clearTitle;
  mainTitle.style.color = titleColor;
  mainTitle.style.fontSize = "17px";

  statsContainer.innerHTML = `
    <div style="text-align: center; margin-bottom: 2px;">
      <div style="font-size: 10px; color: #8b949e;">RANK</div>
      <div class="rank-badge" style="color: ${rankInfo.color};">${rankInfo.rank}</div>
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

  statsContainer.style.display = 'block';
  nextPrepBtn.innerText = "유니트 편성 및 라이브 (Retry)";
  overlay.style.display = 'flex';
}

startBtn.addEventListener('click', startGame);
updateInventoryUI();
</script>
</body>
</html>
"""

rhythm_game_html = rhythm_game_html.replace("AUDIO1_BASE64_PLACEHOLDER", audio1_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE1_BASE64_PLACEHOLDER", image1_base64)

rhythm_game_html = rhythm_game_html.replace("AUDIO2_BASE64_PLACEHOLDER", audio2_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE2_BASE64_PLACEHOLDER", image2_base64)

rhythm_game_html = rhythm_game_html.replace("YUNI_IMG_PLACEHOLDER", yuni_img_base64)
rhythm_game_html = rhythm_game_html.replace("USER_IMG_PLACEHOLDER", arunyang_img_base64)
rhythm_game_html = rhythm_game_html.replace("YUNI_VOICE_PLACEHOLDER", yuni_voice_base64)

components.html(rhythm_game_html, height=820)
