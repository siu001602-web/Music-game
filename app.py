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

song4_music = "music/Screen_Recording_20261118_210521_YouTube_18112026.m4a"
song4_img = "Image/SmartSelect_20261118_211358_YouTube.jpg"

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
    padding: 16px;
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
  .song-grid::-webkit-scrollbar { height: 5px; }
  .song-grid::-webkit-scrollbar-thumb { background: #00f2fe; border-radius: 4px; }

  .song-card {
    flex: 0 0 102px;
    background: transparent;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: transform 0.2s ease;
    position: relative;
  }
  .song-card:hover { transform: translateY(-2px); }
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
  .song-thumb { width: 100%; height: 100%; object-fit: cover; display: block; }
  .new-badge {
    position: absolute; top: 4px; right: 4px;
    background: rgba(255, 255, 255, 0.85); color: #ff4b82;
    font-size: 9px; font-weight: 900; padding: 1px 5px; border-radius: 6px;
  }
  .song-name {
    margin-top: 6px; font-size: 11px; font-weight: 700; color: #e6edf3;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 2px;
  }
  .song-card.selected .song-name { color: #00f2fe; }

  .difficulty-select-container { display: flex; gap: 8px; width: 100%; justify-content: center; margin-bottom: 10px; }
  .diff-card {
    flex: 1; background: #161b22; border: 2px solid #30363d; border-radius: 10px;
    padding: 8px 4px; cursor: pointer; text-align: center; transition: all 0.2s;
  }
  .diff-card.selected { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); background: #1f2630; }
  .diff-card[data-diff="hard"].selected { border-color: #ff4b4b; box-shadow: 0 0 10px rgba(255, 75, 75, 0.4); }
  .diff-card[data-diff="extreme"].selected { border-color: #c084fc; box-shadow: 0 0 10px rgba(192, 132, 252, 0.4); }

  .diff-lv { font-size: 10px; font-weight: bold; color: #8b949e; margin-bottom: 2px; }
  .diff-name { font-size: 12px; font-weight: 900; }
  .diff-card[data-diff="normal"] .diff-name { color: #00f2fe; }
  .diff-card[data-diff="hard"] .diff-name { color: #ff4b4b; }
  .diff-card[data-diff="extreme"] .diff-name { color: #c084fc; }

  .selected-diff-record-box {
    width: 100%; background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d;
    border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; font-size: 12px;
    display: flex; justify-content: space-between; align-items: center;
  }

  .action-btn {
    width: 100%; padding: 12px; font-size: 15px; font-weight: bold; color: #0e1117; background: #00f2fe;
    border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    margin-top: 10px;
  }

  .stats-box {
    background: rgba(255, 255, 255, 0.08); border: 1px solid #30363d; border-radius: 10px;
    padding: 10px 14px; margin: 6px 0 12px 0; width: 100%; text-align: left; font-size: 12px; line-height: 1.4;
  }
  .controls-hint { margin-top: 12px; font-size: 11px; color: #8b949e; }

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
  .hp-gauge-fill { width: 100%; height: 100%; background: #4ade80; transition: width 0.1s linear; }
</style>
</head>
<body>

<audio id="bgm1" preload="auto"><source src="data:audio/mp4;base64,AUDIO1_BASE64_PLACEHOLDER" type="audio/mp4"></audio>
<audio id="bgm2" preload="auto"><source src="data:audio/mp4;base64,AUDIO2_BASE64_PLACEHOLDER" type="audio/mp4"></audio>
<audio id="bgm3" preload="auto"><source src="data:audio/mp4;base64,AUDIO3_BASE64_PLACEHOLDER" type="audio/mp4"></audio>
<audio id="bgm4" preload="auto"><source src="data:audio/mp4;base64,AUDIO4_BASE64_PLACEHOLDER" type="audio/mp4"></audio>

<div id="app-wrapper">
  <div id="menu-screen">
    <h1 id="main-title" style="margin: 0 0 12px 0; color: #00f2fe; font-size: 20px;">RHYTHM STAR</h1>

    <div id="stats-container" class="stats-box" style="display: none;"></div>

    <div class="section-title">Select Song (좌우로 밀어 악보 선택)</div>
    <div id="song-list" class="song-grid"></div>

    <div class="section-title">Difficulty (난이도 선택)</div>
    <div id="difficulty-container" class="difficulty-select-container"></div>

    <div class="selected-diff-record-box">
      <span id="menu-diff-label" style="font-weight: bold; color: #00f2fe;">🏆 [보통] 최고 기록</span>
      <span id="menu-diff-record" style="color: #fff;">기록 없음 (RANK: -)</span>
    </div>

    <button id="start-btn" class="action-btn">라이브 시작</button>

    <div id="controls-hint" class="controls-hint">
      🎹 노트 키: <b>[D] [F] [J] [K]</b> | 터치: <b>화면 각 레인 탭</b>
    </div>
  </div>

  <div id="play-screen">
    <canvas id="gameCanvas" width="480" height="720"></canvas>
    <button id="giveup-btn" onclick="requestGiveUp()" title="포기하기">✕</button>

    <div id="hp-bar-container">
      <div style="display: flex; justify-content: space-between; font-size: 9px; font-weight: bold; color: #4ade80;">
        <span>❤️ HP</span>
        <span id="hp-text">100 / 100</span>
      </div>
      <div class="hp-gauge-bg"><div id="hp-fill" class="hp-gauge-fill"></div></div>
    </div>
  </div>
</div>

<script>
const menuScreen = document.getElementById('menu-screen');
const playScreen = document.getElementById('play-screen');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');

const menuDiffLabel = document.getElementById('menu-diff-label');
const menuDiffRecord = document.getElementById('menu-diff-record');
const difficultyContainer = document.getElementById('difficulty-container');
const mainTitle = document.getElementById('main-title');
const statsContainer = document.getElementById('stats-container');
const songListContainer = document.getElementById('song-list');

const hpFill = document.getElementById('hp-fill');
const hpText = document.getElementById('hp-text');

const bgm1 = document.getElementById('bgm1');
const bgm2 = document.getElementById('bgm2');
const bgm3 = document.getElementById('bgm3');
const bgm4 = document.getElementById('bgm4');

const songs = [
  { id: 'springdream', title: '봄꿈', thumb: 'data:image/jpeg;base64,IMAGE4_BASE64_PLACEHOLDER', audio: bgm4, duration: 185, levels: { normal: 'Lv. 8', hard: 'Lv. 15', extreme: 'Lv. 25' } },
  { id: 'startrail', title: 'Star Trail', thumb: 'data:image/jpeg;base64,IMAGE1_BASE64_PLACEHOLDER', audio: bgm1, duration: 225, levels: { normal: 'Lv. 11', hard: 'Lv. 18', extreme: 'Lv. 26' } },
  { id: 'bbijilge', title: '삐질게', thumb: 'data:image/jpeg;base64,IMAGE2_BASE64_PLACEHOLDER', audio: bgm2, duration: 144, levels: { normal: 'Lv. 12', hard: 'Lv. 19', extreme: 'Lv. 27' } },
  { id: 'constellation', title: '별자리가 될 수 있다면', thumb: 'data:image/jpeg;base64,IMAGE3_BASE64_PLACEHOLDER', audio: bgm3, duration: 255, levels: { normal: 'Lv. 13', hard: 'Lv. 20', extreme: 'Lv. 29' } }
];

const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 570;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

let currentSongId = 'springdream';
let currentDifficulty = 'normal';
let bestRecords = {
  springdream: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } },
  startrail: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } },
  bbijilge: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } },
  constellation: { normal: { score: 0, rank: '-', color: '#94a3b8' }, hard: { score: 0, rank: '-', color: '#94a3b8' }, extreme: { score: 0, rank: '-', color: '#94a3b8' } }
};

function switchView(viewName) {
  menuScreen.style.display = (viewName === 'menu') ? 'flex' : 'none';
  playScreen.style.display = (viewName === 'play') ? 'block' : 'none';
}

function updateSelectedRecordDisplay() {
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

renderSongList();
renderDifficultyButtons();
updateSelectedRecordDisplay();

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
let notes = [];

function getActiveBgm() {
  const s = songs.find(item => item.id === currentSongId);
  return s ? s.audio : bgm4;
}

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
  if (minDiff <= 0.12) {
    score += (100 + (combo * 2));
    incrementCombo();
    stats.perfect++;
    healHp(1.2);
    showJudgement("PERFECT!", "#00f2fe");
  } else if (minDiff <= 0.22) {
    score += (70 + combo);
    incrementCombo();
    stats.great++;
    healHp(0.6);
    showJudgement("GREAT!", "#4ade80");
  } else {
    score += 30;
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

canvas.addEventListener('touchend', (e) => {
  e.preventDefault();
  keyPressed = [false, false, false, false];
}, { passive: false });

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

  updateSelectedRecordDisplay();

  mainTitle.innerHTML = `CLEAR! RANK ${rankInfo.rank}`;
  mainTitle.style.color = rankInfo.color;

  statsContainer.innerHTML = `
    <div>최종 점수: <b>${score.toLocaleString()}</b></div>
    <div>최대 콤보: ${maxCombo} | 완곡 성공!</div>
  `;
  statsContainer.style.display = 'block';
  switchView('menu');
}

startBtn.addEventListener('click', startGame);
</script>
</body>
</html>
"""

# Base64 변환 데이터 치환
rhythm_game_html = rhythm_game_html.replace("AUDIO1_BASE64_PLACEHOLDER", audio1_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE1_BASE64_PLACEHOLDER", image1_base64)
rhythm_game_html = rhythm_game_html.replace("AUDIO2_BASE64_PLACEHOLDER", audio2_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE2_BASE64_PLACEHOLDER", image2_base64)
rhythm_game_html = rhythm_game_html.replace("AUDIO3_BASE64_PLACEHOLDER", audio3_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE3_BASE64_PLACEHOLDER", image3_base64)
rhythm_game_html = rhythm_game_html.replace("AUDIO4_BASE64_PLACEHOLDER", audio4_base64)
rhythm_game_html = rhythm_game_html.replace("IMAGE4_BASE64_PLACEHOLDER", image4_base64)

components.html(rhythm_game_html, height=820)
