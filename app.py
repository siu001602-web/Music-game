import base64
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Star Trail - Rhythm Game",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 0rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

music_file_path = "music/Screen_Recording_20261117_180140_YouTube_17112026.m4a"
image_file_path = "Image/SmartSelect_20261117_234657_YouTube.jpg"

audio_base64 = ""
if os.path.exists(music_file_path):
    with open(music_file_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
else:
    st.warning(f"⚠️ '{music_file_path}' 음원 파일을 찾을 수 없습니다.")

image_base64 = ""
if os.path.exists(image_file_path):
    with open(image_file_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
else:
    st.warning(f"⚠️ '{image_file_path}' 이미지 파일을 찾을 수 없습니다.")

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
  body {
    margin: 0;
    background-color: #0e1117;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  #game-container {
    position: relative;
    width: 100%;
    max-width: 540px;
    display: flex;
    justify-content: center;
  }
  canvas {
    width: 100%;
    height: auto;
    background: linear-gradient(rgba(14, 17, 23, 0.7), rgba(14, 17, 23, 0.7)), url('data:image/jpeg;base64,IMAGE_BASE64_PLACEHOLDER');
    background-size: cover;
    background-position: center;
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.15);
    touch-action: none;
  }
  #ui-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    background: linear-gradient(rgba(14, 17, 23, 0.9), rgba(14, 17, 23, 0.9)), url('data:image/jpeg;base64,IMAGE_BASE64_PLACEHOLDER');
    background-size: cover;
    background-position: center;
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    z-index: 10;
  }

  /* 상단 메인 카테고리 탭 바 */
  .nav-tabs {
    display: flex;
    gap: 8px;
    width: 100%;
    background: rgba(22, 27, 34, 0.9);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid #30363d;
    margin-bottom: 14px;
  }
  .nav-tab {
    flex: 1;
    padding: 8px 0;
    font-size: 13px;
    font-weight: bold;
    color: #8b949e;
    background: transparent;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .nav-tab.active {
    color: #0e1117;
    background: #00f2fe;
    box-shadow: 0 2px 10px rgba(0, 242, 254, 0.3);
  }

  .tab-content {
    width: 100%;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .section-title {
    font-size: 12px;
    color: #8b949e;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
  }

  /* 곡 선택 그리드 카드 스타일 */
  .song-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    width: 100%;
    max-height: 175px;
    overflow-y: auto;
    margin-bottom: 12px;
    padding: 4px;
  }
  .song-card {
    background: #161b22;
    border: 2px solid #30363d;
    border-radius: 10px;
    padding: 6px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
    position: relative;
  }
  .song-card.selected {
    border-color: #00f2fe;
    box-shadow: 0 0 12px rgba(0, 242, 254, 0.4);
    background: #1f2630;
  }
  .song-thumb {
    width: 100%;
    height: 70px;
    border-radius: 6px;
    object-fit: cover;
    margin-bottom: 4px;
  }
  .song-name {
    font-size: 13px;
    font-weight: bold;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .new-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    background: #ff4b4b;
    color: white;
    font-size: 9px;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 4px;
  }

  /* 뽑기 & 캐릭터 임시 플레이스홀더 박스 */
  .placeholder-box {
    width: 92%;
    background: rgba(22, 27, 34, 0.85);
    border: 1px dashed #30363d;
    border-radius: 14px;
    padding: 32px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }
  .placeholder-icon {
    font-size: 42px;
  }
  .placeholder-title {
    font-size: 18px;
    font-weight: bold;
    color: #00f2fe;
  }
  .placeholder-desc {
    font-size: 13px;
    color: #8b949e;
    line-height: 1.5;
  }

  /* 캐릭터 미리보기 슬롯 */
  .char-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    width: 100%;
    margin-top: 8px;
  }
  .char-slot {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .char-slot.locked {
    opacity: 0.45;
  }

  .difficulty-container {
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
  }
  .diff-btn {
    padding: 6px 16px;
    font-size: 13px;
    font-weight: bold;
    color: #8b949e;
    background: #21262d;
    border: 2px solid #30363d;
    border-radius: 20px;
    cursor: pointer;
  }
  .diff-btn.selected {
    color: #0e1117;
    background: #00f2fe;
    border-color: #00f2fe;
  }
  #start-btn {
    padding: 10px 30px;
    font-size: 16px;
    font-weight: bold;
    color: #0e1117;
    background: #00f2fe;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
  }
  .rank-badge {
    font-size: 45px;
    font-weight: 900;
    margin: 2px 0;
    line-height: 1;
    text-shadow: 0 0 15px currentColor;
  }
  .stats-box {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 8px 16px;
    margin: 4px 0 10px 0;
    width: 85%;
    text-align: left;
    font-size: 12px;
    line-height: 1.4;
  }
  .controls-hint {
    margin-top: 8px;
    font-size: 11px;
    color: #8b949e;
  }
</style>
</head>
<body>

<audio id="bgm" preload="auto">
  <source src="data:audio/mp4;base64,AUDIO_BASE64_PLACEHOLDER" type="audio/mp4">
</audio>

<div id="game-container">
  <canvas id="gameCanvas" width="480" height="640"></canvas>
  <div id="ui-overlay">
    <h1 id="main-title" style="margin: 0 0 8px 0; color: #00f2fe; font-size: 21px;">RHYTHM STAR</h1>
    
    <!-- 상단 카테고리 전환 탭 -->
    <div id="nav-tabs" class="nav-tabs">
      <button class="nav-tab active" data-tab="songs">🎵 악보</button>
      <button class="nav-tab" data-tab="gacha">✨ 뽑기</button>
      <button class="nav-tab" data-tab="characters">👤 캐릭터</button>
    </div>

    <!-- 1. 악보(곡 선택) 탭 화면 -->
    <div id="tab-songs" class="tab-content">
      <div id="stats-container" class="stats-box" style="display: none;"></div>

      <div id="menu-group" style="width: 100%; display: flex; flex-direction: column; align-items: center;">
        <div class="section-title">Select Song (악보 목록)</div>
        <div id="song-list" class="song-grid"></div>

        <div class="section-title">Difficulty (난이도)</div>
        <div class="difficulty-container">
          <button class="diff-btn" data-diff="easy">하 (Easy)</button>
          <button class="diff-btn selected" data-diff="normal">중 (Normal)</button>
          <button class="diff-btn" data-diff="hard">상 (Hard)</button>
        </div>
      </div>

      <button id="start-btn">게임 시작 (Start)</button>

      <div id="controls-hint" class="controls-hint">
        🎹 노트: <b>[D] [F] [J] [K]</b> | 슬라이드: <b>[←][→]</b> 또는 <b>[A][L]</b>
      </div>
    </div>

    <!-- 2. 뽑기(Gacha) 탭 화면 (준비 틀) -->
    <div id="tab-gacha" class="tab-content" style="display: none;">
      <div class="placeholder-box">
        <div class="placeholder-icon">🎁</div>
        <div class="placeholder-title">스타 스카우트 (뽑기)</div>
        <div class="placeholder-desc">
          새로운 캐릭터와 특별 스킨을 획득할 수 있는<br>
          뽑기 시스템이 곧 오픈됩니다!
        </div>
        <button disabled style="margin-top:8px; padding:8px 20px; border-radius:20px; border:1px solid #30363d; background:#21262d; color:#8b949e; font-weight:bold;">
          준비 중 (Coming Soon)
        </button>
      </div>
    </div>

    <!-- 3. 캐릭터(Characters) 탭 화면 (준비 틀) -->
    <div id="tab-characters" class="tab-content" style="display: none;">
      <div class="section-title">보유 캐릭터 목록</div>
      <div class="char-grid">
        <div class="char-slot" style="border-color: #00f2fe;">
          <div style="font-size: 28px;">🌟</div>
          <div style="font-size: 12px; font-weight: bold; color: #fff;">기본 스타</div>
          <div style="font-size: 10px; color: #00f2fe;">장착 중</div>
        </div>
        <div class="char-slot locked">
          <div style="font-size: 28px;">🔒</div>
          <div style="font-size: 12px; font-weight: bold;">미획득</div>
          <div style="font-size: 10px;">뽑기 해금</div>
        </div>
        <div class="char-slot locked">
          <div style="font-size: 28px;">🔒</div>
          <div style="font-size: 12px; font-weight: bold;">미획득</div>
          <div style="font-size: 10px;">뽑기 해금</div>
        </div>
      </div>
      <div class="placeholder-box" style="margin-top: 14px; padding: 16px;">
        <div class="placeholder-desc">
          캐릭터별 고유 스킬(점수 보너스, 판정 완화 등) 기능이<br>추후 업데이트될 예정입니다.
        </div>
      </div>
    </div>

  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const overlay = document.getElementById('ui-overlay');
const startBtn = document.getElementById('start-btn');
const bgm = document.getElementById('bgm');
const mainTitle = document.getElementById('main-title');
const menuGroup = document.getElementById('menu-group');
const statsContainer = document.getElementById('stats-container');
const controlsHint = document.getElementById('controls-hint');
const diffBtns = document.querySelectorAll('.diff-btn');
const songListContainer = document.getElementById('song-list');

// 탭 전환 로직
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

// 등록된 곡 리스트
const songs = [
  { id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,IMAGE_BASE64_PLACEHOLDER' }
];

const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 510;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

let audioCtx = null;
let currentSong = 'startrail';
let currentDifficulty = 'normal';
let isPlaying = false;
let startTime = 0;
let score = 0;
let combo = 0;
let maxCombo = 0;

let stats = { perfect: 0, great: 0, good: 0, miss: 0 };
let judgementText = "";
let judgementColor = "#fff";
let judgementTimer = 0;

let keyPressed = [false, false, false, false];
let activeTouches = new Map();
let notes = [];

function renderSongList() {
  songListContainer.innerHTML = '';
  songs.forEach(song => {
    const card = document.createElement('div');
    card.className = `song-card ${song.id === currentSong ? 'selected' : ''}`;
    card.innerHTML = `
      <div style="position:relative;">
        <img src="${song.thumb}" class="song-thumb">
        <span class="new-badge">NEW</span>
      </div>
      <div class="song-name">🎵 ${song.title}</div>
    `;
    card.addEventListener('click', () => {
      currentSong = song.id;
      renderSongList();
    });
    songListContainer.appendChild(card);
  });
}
renderSongList();

diffBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    diffBtns.forEach(b => b.classList.remove('selected'));
    e.target.classList.add('selected');
    currentDifficulty = e.target.getAttribute('data-diff');
  });
});

function playBonusSound() {
  try {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(1320, audioCtx.currentTime + 0.12);
    gain.gain.setValueAtTime(0.18, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.15);
  } catch(e) {}
}

function generateBeatmap(difficulty) {
  notes = [];
  const bpm = 125;
  const beatInterval = 60 / bpm; 
  let currentTime = 2.0;
  const totalDuration = 225.0;

  let speed = 400;
  if (difficulty === 'normal') speed = 420;
  if (difficulty === 'hard') speed = 450;
  window.NOTE_SPEED = speed;

  let index = 0;
  while (currentTime < totalDuration - 5.0) {
    const lane = Math.floor(Math.random() * LANES);
    const rand = Math.random();

    if (index % 5 === 0 && rand < 0.35) {
      const pairLane = (lane + 2) % LANES;
      const bridgeId = `bridge_${index}`;
      notes.push({ time: currentTime, lane: lane, type: 'bridge', pairLane: pairLane, bridgeId: bridgeId, hit: false, missed: false });
      notes.push({ time: currentTime, lane: pairLane, type: 'bridge', pairLane: lane, bridgeId: bridgeId, hit: false, missed: false });
    }
    else if (index % 4 === 0 && rand < 0.45) {
      const dir = lane === 0 ? 'right' : (lane === 3 ? 'left' : (Math.random() < 0.5 ? 'left' : 'right'));
      notes.push({ time: currentTime, lane: lane, type: 'swipe', swipeDir: dir, hit: false, missed: false });
    }
    else if (difficulty !== 'easy' && index % 6 === 0 && rand < 0.5) {
      notes.push({ time: currentTime, lane: lane, type: 'bonus', hit: false, missed: false });
    }
    else if (difficulty !== 'easy' && index % 3 === 0 && rand < 0.45) {
      notes.push({ time: currentTime, lane: lane, type: 'long', duration: beatInterval * (Math.random() * 1.2 + 1.0), tailHit: false, holding: false, hit: false, missed: false });
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
  if (note.type === 'bonus') playBonusSound();

  if (minDiff <= 0.08) {
    score += (100 + combo * 2) * mult;
    combo++;
    stats.perfect++;
    showJudgement(note.type === 'bonus' ? "BONUS PERFECT!" : "PERFECT!", note.type === 'bonus' ? "#c084fc" : "#00f2fe");
  } else if (minDiff <= 0.16) {
    score += (70 + combo) * mult;
    combo++;
    stats.great++;
    showJudgement(note.type === 'bonus' ? "BONUS GREAT!" : "GREAT!", "#4ade80");
  } else {
    score += 30 * mult;
    combo++;
    stats.good++;
    showJudgement("GOOD", "#facc15");
  }
  if (combo > maxCombo) maxCombo = combo;
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

  if (targetNote && minDiff <= 0.23) {
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

  if (targetNote && minDiff <= 0.26 && targetNote.swipeDir === dir) {
    targetNote.hit = true;
    score += 120 + combo * 2;
    combo++;
    stats.perfect++;
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

      if (diff <= 0.26) {
        score += 50;
        combo++;
        stats.perfect++;
        showJudgement("HOLD CLEAR", "#00f2fe");
      } else {
        stats.miss++;
        showJudgement("MISS", "#ff4b4b");
        combo = 0;
      }
    }
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
      if (Math.abs(deltaX) > 28) {
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
    if (finalScore >= 80000) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 70000) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 60000) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 50000) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else if (difficulty === 'normal') {
    if (finalScore >= 130000) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 100000) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 80000) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 60000) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  } else {
    if (finalScore >= 250000) return { rank: 'S', color: '#facc15' };
    if (finalScore >= 200000) return { rank: 'A', color: '#00f2fe' };
    if (finalScore >= 150000) return { rank: 'B', color: '#4ade80' };
    if (finalScore >= 100000) return { rank: 'C', color: '#fb923c' };
    return { rank: 'D', color: '#94a3b8' };
  }
}

function updateAndDraw() {
  if (!isPlaying) return;

  const currentTime = (performance.now() - startTime) / 1000;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < LANES; i++) {
    const x = i * LANE_WIDTH;
    
    if (keyPressed[i]) {
      const grad = ctx.createLinearGradient(0, HIT_Y - 180, 0, HIT_Y);
      grad.addColorStop(0, 'rgba(0, 242, 254, 0)');
      grad.addColorStop(1, 'rgba(0, 242, 254, 0.35)');
      ctx.fillStyle = grad;
      ctx.fillRect(x, HIT_Y - 180, LANE_WIDTH, 180);
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
        score += 50;
        combo++;
        stats.perfect++;
        showJudgement("HOLD CLEAR", "#00f2fe");
      }
      continue;
    }

    if (!note.hit && timeDiff < -0.24) {
      note.missed = true;
      stats.miss++;
      combo = 0;
      showJudgement("MISS", "#ff4b4b");
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

  if (bgm.ended || (remainingNotes === 0 && currentTime > notes[notes.length - 1].time + 1.0)) {
    endGame();
    return;
  }

  requestAnimationFrame(updateAndDraw);
}

function startGame() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }

  score = 0;
  combo = 0;
  maxCombo = 0;
  judgementTimer = 0;
  stats = { perfect: 0, great: 0, good: 0, miss: 0 };
  activeTouches.clear();
  keyPressed = [false, false, false, false];
  
  generateBeatmap(currentDifficulty);
  
  bgm.currentTime = 0;
  bgm.play().catch(error => {
    console.log("Audio play failed:", error);
  });

  isPlaying = true;
  startTime = performance.now();
  
  overlay.style.display = 'none';
  requestAnimationFrame(updateAndDraw);
}

function endGame() {
  isPlaying = false;
  bgm.pause();

  let clearTitle = "CLEAR!";
  let titleColor = "#ffffff";

  if (stats.miss === 0) {
    if (stats.great === 0 && stats.good === 0) {
      clearTitle = "퍼펙트 풀콤보! (ALL PERFECTION)";
      titleColor = "#c084fc";
    } else {
      clearTitle = "풀콤보! (FULL COMBO)";
      titleColor = "#00f2fe";
    }
  }

  const rankInfo = calculateRank(currentDifficulty, score);

  mainTitle.innerHTML = clearTitle;
  mainTitle.style.color = titleColor;
  mainTitle.style.fontSize = "18px";

  statsContainer.innerHTML = `
    <div style="text-align: center; margin-bottom: 2px;">
      <div style="font-size: 10px; color: #8b949e;">RANK</div>
      <div class="rank-badge" style="color: ${rankInfo.color};">${rankInfo.rank}</div>
    </div>
    <div>🏆 최종 점수: <b>${score.toLocaleString()}</b></div>
    <div>💎 최대 콤보: ${maxCombo}</div>
    <div style="margin-top: 4px; border-top: 1px solid #30363d; padding-top: 4px;">
      ✨ PERFECT: <span style="color: #00f2fe;">${stats.perfect}</span> | 🌟 GREAT: <span style="color: #4ade80;">${stats.great}</span><br>
      ⚡ GOOD: <span style="color: #facc15;">${stats.good}</span> | ❌ MISS: <span style="color: #ff4b4b;">${stats.miss}</span>
    </div>
  `;
  
  // 게임 종료 후 악보 탭으로 돌아가며 결과 표시
  navTabs.forEach(t => t.classList.remove('active'));
  navTabs[0].classList.add('active');
  tabContents.songs.style.display = 'flex';
  tabContents.gacha.style.display = 'none';
  tabContents.characters.style.display = 'none';

  statsContainer.style.display = 'block';
  startBtn.innerText = "다시 하기 (Retry)";
  overlay.style.display = 'flex';
}

startBtn.addEventListener('click', startGame);
</script>
</body>
</html>
"""

rhythm_game_html = rhythm_game_html.replace("AUDIO_BASE64_PLACEHOLDER", audio_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE_BASE64_PLACEHOLDER", image_base64)

components.html(rhythm_game_html, height=680)
