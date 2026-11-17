import base64
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rhythm Game with Long Notes",
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

# 1. 음원 파일 읽기 및 Base64 변환
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
    background: rgba(14, 17, 23, 0.92);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
  }
  .difficulty-container {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  .diff-btn {
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    color: #8b949e;
    background: #21262d;
    border: 2px solid #30363d;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .diff-btn.selected {
    color: #0e1117;
    background: #00f2fe;
    border-color: #00f2fe;
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
  }
  #start-btn {
    padding: 14px 36px;
    font-size: 18px;
    font-weight: bold;
    color: #0e1117;
    background: #00f2fe;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    transition: transform 0.1s, background 0.2s;
  }
  #start-btn:active {
    transform: scale(0.95);
    background: #4facfe;
  }
  .controls-info {
    margin-top: 15px;
    font-size: 14px;
    color: #8b949e;
    line-height: 1.4;
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
    <h1 style="margin-bottom: 10px; color: #00f2fe; font-size: 28px;">STAR TRAIL</h1>
    <p style="margin-bottom: 15px; color: #8b949e; font-size: 14px;">난이도를 선택하세요 (롱 노트 포함)</p>
    
    <div class="difficulty-container">
      <button class="diff-btn" data-diff="easy">하 (Easy)</button>
      <button class="diff-btn selected" data-diff="normal">중 (Normal)</button>
      <button class="diff-btn" data-diff="hard">상 (Hard)</button>
    </div>

    <button id="start-btn">게임 시작 (Start)</button>
    <div class="controls-info">
      📱 태블릿/모바일: 하단 레인 터치 (롱 노트는 누르고 있기)<br>
      💻 PC: 키보드 [ D ] [ F ] [ J ] [ K ]
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const overlay = document.getElementById('ui-overlay');
const startBtn = document.getElementById('start-btn');
const bgm = document.getElementById('bgm');
const diffBtns = document.querySelectorAll('.diff-btn');

const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 510;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];

let currentDifficulty = 'normal';
let isPlaying = false;
let startTime = 0;
let score = 0;
let combo = 0;
let maxCombo = 0;
let judgementText = "";
let judgementColor = "#fff";
let judgementTimer = 0;

let keyPressed = [false, false, false, false];
let activeTouches = new Map();
let notes = [];

diffBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    diffBtns.forEach(b => b.classList.remove('selected'));
    e.target.classList.add('selected');
    currentDifficulty = e.target.getAttribute('data-diff');
  });
});

// 3분 45초(225초) 채보 생성 (롱 노트 포함, 상 난이도 완화)
function generateBeatmap(difficulty) {
  notes = [];
  const bpm = 125;
  const beatInterval = 60 / bpm; 
  let currentTime = 2.0;
  const totalDuration = 225.0;

  let speed = 400;
  if (difficulty === 'normal') speed = 420;
  if (difficulty === 'hard') speed = 450; // 기존보다 속도 낮춤

  window.NOTE_SPEED = speed;

  let index = 0;
  while (currentTime < totalDuration - 5.0) {
    const lane = Math.floor(Math.random() * LANES);
    
    // 난이도별 롱 노트 확률 설정 (Hard도 과하지 않게 25% 확률)
    let isLong = false;
    let duration = 0;
    if (difficulty !== 'easy' && index % 3 === 0 && Math.random() < (difficulty === 'hard' ? 0.35 : 0.2)) {
      isLong = true;
      duration = beatInterval * (Math.random() * 1.5 + 1.0); // 1~2.5박자 길이
    }

    notes.push({
      time: currentTime,
      lane: lane,
      isLong: isLong,
      duration: duration,
      tailHit: false,
      hit: false,
      missed: false,
      holding: false
    });

    // Normal / Hard 동시타 추가 (확률 조정)
    if (difficulty !== 'easy' && index % 4 === 0 && Math.random() < 0.3) {
      let secondLane = (lane + 2) % LANES;
      notes.push({
        time: currentTime,
        lane: secondLane,
        isLong: false,
        duration: 0,
        tailHit: false,
        hit: false,
        missed: false,
        holding: false
      });
    }

    if (difficulty === 'easy') {
      currentTime += beatInterval * 1.8;
    } else if (difficulty === 'normal') {
      currentTime += beatInterval * 1.2;
    } else {
      currentTime += beatInterval * 0.8; // 상 난이도 간격을 넓혀서 피로도 줄임
    }
    index++;
  }
}

function handleKeyDown(lane) {
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

  if (targetNote && minDiff <= 0.22) {
    targetNote.hit = true;
    if (targetNote.isLong) {
      targetNote.holding = true;
    }
    
    if (minDiff <= 0.07) {
      score += 100 + combo * 2;
      combo++;
      showJudgement("PERFECT!", "#00f2fe");
    } else if (minDiff <= 0.15) {
      score += 70 + combo;
      combo++;
      showJudgement("GREAT!", "#4ade80");
    } else {
      score += 30;
      combo++;
      showJudgement("GOOD", "#facc15");
    }
    if (combo > maxCombo) maxCombo = combo;
  }
}

function handleKeyUp(lane) {
  const currentTime = (performance.now() - startTime) / 1000;
  for (let note of notes) {
    if (note.isLong && note.holding && !note.tailHit && note.lane === lane) {
      const endTime = note.time + note.duration;
      const diff = Math.abs(endTime - currentTime);
      note.holding = false;
      note.tailHit = true;

      if (diff <= 0.25) {
        score += 50;
        combo++;
        showJudgement("HOLD END", "#00f2fe");
      } else {
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
    activeTouches.set(touch.identifier, lane);
    
    if (!keyPressed[lane]) {
      keyPressed[lane] = true;
      handleKeyDown(lane);
    }
  }
}, { passive: false });

function handleTouchEnd(e) {
  e.preventDefault();
  for (let i = 0; i < e.changedTouches.length; i++) {
    const touch = e.changedTouches[i];
    const lane = activeTouches.get(touch.identifier);
    activeTouches.delete(touch.identifier);

    if (lane !== undefined) {
      let stillPressed = false;
      for (let activeLane of activeTouches.values()) {
        if (activeLane === lane) stillPressed = true;
      }
      if (!stillPressed) {
        keyPressed[lane] = false;
        handleKeyUp(lane);
      }
    }
  }
}

canvas.addEventListener('touchend', handleTouchEnd, { passive: false });
canvas.addEventListener('touchcancel', handleTouchEnd, { passive: false });

window.addEventListener('keydown', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1 && !keyPressed[idx]) {
    keyPressed[idx] = true;
    handleKeyDown(idx);
  }
});

window.addEventListener('keyup', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1) {
    keyPressed[idx] = false;
    handleKeyUp(idx);
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

  let remainingNotes = 0;
  for (let note of notes) {
    if (note.missed || (note.hit && (!note.isLong || note.tailHit))) continue;
    remainingNotes++;

    const timeDiff = note.time - currentTime;
    const y = HIT_Y - (timeDiff * window.NOTE_SPEED);

    // 롱 노트 처리 중인 경우
    if (note.isLong && note.holding) {
      const endY = HIT_Y - ((note.time + note.duration - currentTime) * window.NOTE_SPEED);
      const x = note.lane * LANE_WIDTH + 14;
      const w = LANE_WIDTH - 28;
      
      ctx.fillStyle = 'rgba(0, 242, 254, 0.4)';
      ctx.fillRect(x, Math.max(0, endY), w, HIT_Y - Math.max(0, endY));

      if (currentTime >= note.time + note.duration) {
        note.holding = false;
        note.tailHit = true;
        score += 50;
        combo++;
        showJudgement("PERFECT!", "#00f2fe");
      }
      continue;
    }

    if (!note.hit && timeDiff < -0.22) {
      note.missed = true;
      combo = 0;
      showJudgement("MISS", "#ff4b4b");
      continue;
    }

    if (y >= -50 && y <= HIT_Y + 20) {
      const x = note.lane * LANE_WIDTH + 10;
      const w = LANE_WIDTH - 20;

      if (note.isLong) {
        const tailY = y - (note.duration * window.NOTE_SPEED);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.fillRect(x + 4, tailY, w - 8, y - tailY);

        ctx.fillStyle = '#facc15'; // 롱 노트 머리는 노란색 계열
        ctx.beginPath();
        ctx.roundRect(x, y - 12, w, 24, 6);
        ctx.fill();
      } else {
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
  score = 0;
  combo = 0;
  maxCombo = 0;
  judgementTimer = 0;
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
  document.querySelector('h1').innerHTML = "CLEAR!";
  document.querySelector('p').innerHTML = `Score: ${score} | Max Combo: ${maxCombo}`;
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
