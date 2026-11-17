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

music_file_path = "Screen_Recording_20261117_180140_YouTube_17112026.m4a"
audio_base64 = ""

if os.path.exists(music_file_path):
    with open(music_file_path, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
else:
    st.warning(f"⚠️ '{music_file_path}' 파일을 찾을 수 없습니다. 깃허브 메인 화면에 음원 파일을 추가해 주세요!")

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
    justify-content: center;
    align-items: center;
    background: rgba(14, 17, 23, 0.95);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    z-index: 10;
  }
  .section-title {
    font-size: 13px;
    color: #8b949e;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .song-selector {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
  }
  .song-btn {
    padding: 8px 20px;
    font-size: 14px;
    font-weight: bold;
    color: #8b949e;
    background: #21262d;
    border: 2px solid #30363d;
    border-radius: 20px;
    cursor: pointer;
  }
  .song-btn.selected {
    color: #0e1117;
    background: #4facfe;
    border-color: #4facfe;
  }
  .difficulty-container {
    display: flex;
    gap: 10px;
    margin-bottom: 18px;
  }
  .diff-btn {
    padding: 8px 18px;
    font-size: 14px;
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
    padding: 12px 34px;
    font-size: 17px;
    font-weight: bold;
    color: #0e1117;
    background: #00f2fe;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
  }
  .stats-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px 20px;
    margin: 12px 0;
    width: 80%;
    text-align: left;
    font-size: 14px;
    line-height: 1.6;
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
    <h1 id="main-title" style="margin-bottom: 4px; color: #00f2fe; font-size: 26px;">RHYTHM STAR</h1>
    
    <div id="menu-group">
      <div class="section-title">Select Song</div>
      <div class="song-selector">
        <button class="song-btn selected" data-song="startrail">Star Trail</button>
      </div>

      <div class="section-title">Difficulty</div>
      <div class="difficulty-container">
        <button class="diff-btn" data-diff="easy">하 (Easy)</button>
        <button class="diff-btn selected" data-diff="normal">중 (Normal)</button>
        <button class="diff-btn" data-diff="hard">상 (Hard)</button>
      </div>
    </div>

    <div id="stats-container" style="display: none;"></div>

    <button id="start-btn">게임 시작 (Start)</button>
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
const diffBtns = document.querySelectorAll('.diff-btn');
const songBtns = document.querySelectorAll('.song-btn');

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

songBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    songBtns.forEach(b => b.classList.remove('selected'));
    e.target.classList.add('selected');
    currentSong = e.target.getAttribute('data-song');
  });
});

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
  if (e.key === 'ArrowLeft') { handleSwipe(1, 'left'); handleSwipe(2, 'left'); return; }
  if (e.key === 'ArrowRight') { handleSwipe(1, 'right'); handleSwipe(2, 'right'); return; }
  const idx = KEYS.indexOf(e.key.toLowerCase());
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
  // 오디오 재생 실패 여부와 상관없이 화면 전환이 확실히 되도록 처리
  bgm.play().catch(error => {
    console.log("Audio play failed:", error);
  });

  isPlaying = true;
  startTime = performance.now();
  
  // UI 확실히 숨기기
  overlay.style.display = 'none';
  menuGroup.style.display = 'none';
  statsContainer.style.display = 'none';

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

  mainTitle.innerHTML = clearTitle;
  mainTitle.style.color = titleColor;
  mainTitle.style.fontSize = "22px";

  statsContainer.innerHTML = `
    <div>🏆 최종 점수: <b>${score}</b></div>
    <div>💎 최대 콤보: ${maxCombo}</div>
    <div style="margin-top: 6px; border-top: 1px solid #30363d; padding-top: 6px;">
      ✨ PERFECT: <span style="color: #00f2fe;">${stats.perfect}</span><br>
      🌟 GREAT: <span style="color: #4ade80;">${stats.great}</span><br>
      ⚡ GOOD: <span style="color: #facc15;">${stats.good}</span><br>
      ❌ MISS: <span style="color: #ff4b4b;">${stats.miss}</span>
    </div>
  `;
  statsContainer.style.display = 'block';
  menuGroup.style.display = 'none';

  startBtn.innerText = "다시 하기 (Retry)";
  overlay.style.display = 'flex';
}

startBtn.addEventListener('click', startGame);
</script>
</body>
</html>
"""

rhythm_game_html = rhythm_game_html.replace("AUDIO_BASE64_PLACEHOLDER", audio_base64)

components.html(rhythm_game_html, height=680)
