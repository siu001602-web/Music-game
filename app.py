import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tablet 4-Key Rhythm Game",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Streamlit 기본 여백 최소화 (태블릿 화면 확보)
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

rhythm_game_html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {
    box-sizing: border-box;
    touch-action: manipulation; /* 더블탭 줌 방지 */
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
    max-width: 540px; /* 태블릿에서 넓게 보이도록 확장 */
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
    touch-action: none; /* 캔버스 내부 스크롤/스와이프 완전 차단 */
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
    background: rgba(14, 17, 23, 0.88);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
  }
  button {
    padding: 16px 36px;
    font-size: 20px;
    font-weight: bold;
    color: #0e1117;
    background: #00f2fe;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    transition: transform 0.1s, background 0.2s;
  }
  button:active {
    transform: scale(0.95);
    background: #4facfe;
  }
  .controls-info {
    margin-top: 18px;
    font-size: 15px;
    color: #8b949e;
    line-height: 1.5;
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas" width="480" height="640"></canvas>
  <div id="ui-overlay">
    <h1 id="title-text" style="margin-bottom: 24px; color: #00f2fe; font-size: 32px;">NEON BEAT</h1>
    <button id="start-btn">터치하여 시작 (Start)</button>
    <div class="controls-info">
      📱 태블릿/모바일: 하단 4개 레인 직접 터치 (멀티터치 지원)<br>
      💻 PC: 키보드 [ D ] [ F ] [ J ] [ K ]
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const overlay = document.getElementById('ui-overlay');
const startBtn = document.getElementById('start-btn');
const titleText = document.getElementById('title-text');

// 게임 설정 (태블릿 터치 영역 확보를 위해 판정선 위치 조정)
const LANES = 4;
const LANE_WIDTH = canvas.width / LANES;
const HIT_Y = 510;
const NOTE_SPEED = 420;
const KEYS = ['d', 'f', 'j', 'k'];
const LANE_COLORS = ['#ff4b4b', '#00f2fe', '#00f2fe', '#ff4b4b'];
const FREQS = [261.63, 329.63, 392.00, 523.25];

let audioCtx = null;
let isPlaying = false;
let startTime = 0;
let score = 0;
let combo = 0;
let maxCombo = 0;
let judgementText = "";
let judgementColor = "#fff";
let judgementTimer = 0;

let keyPressed = [false, false, false, false];
let activeTouches = new Map(); // 멀티터치 추적용 (touch.identifier -> lane)
let notes = [];

function playTone(freq, duration = 0.15, type = 'triangle') {
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
  
  gain.gain.setValueAtTime(0.22, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
  
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + duration);
}

function generateBeatmap() {
  notes = [];
  const bpm = 120;
  const beatInterval = 60 / bpm;
  let currentTime = 2.0;

  for (let i = 0; i < 64; i++) {
    const lane = Math.floor(Math.random() * LANES);
    notes.push({ time: currentTime, lane: lane, hit: false, missed: false });

    // 동시타 (멀티터치 테스트용)
    if (i % 4 === 0 && i > 0) {
      let secondLane = (lane + 2) % LANES;
      notes.push({ time: currentTime, lane: secondLane, hit: false, missed: false });
    }
    if (i % 2 === 1 && Math.random() > 0.4) {
      let offBeatLane = (lane + 1) % LANES;
      notes.push({ time: currentTime + beatInterval / 2, lane: offBeatLane, hit: false, missed: false });
    }

    currentTime += beatInterval;
  }
}

function checkHit(lane) {
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

  // 태블릿 터치 오차를 고려해 판정 범위를 약간 여유롭게 설정 (0.20초)
  if (targetNote && minDiff <= 0.20) {
    targetNote.hit = true;
    playTone(FREQS[lane], 0.2, 'sine');
    
    if (minDiff <= 0.07) {
      score += 100 + combo * 2;
      combo++;
      showJudgement("PERFECT!", "#00f2fe");
    } else if (minDiff <= 0.14) {
      score += 70 + combo;
      combo++;
      showJudgement("GREAT!", "#4ade80");
    } else {
      score += 30;
      combo++;
      showJudgement("GOOD", "#facc15");
    }
    if (combo > maxCombo) maxCombo = combo;
  } else {
    playTone(100, 0.05, 'sawtooth');
  }
}

function showJudgement(text, color) {
  judgementText = text;
  judgementColor = color;
  judgementTimer = 30;
}

// 터치 좌표를 캔버스 레인(0~3)으로 변환
function getLaneFromTouch(clientX) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const canvasX = (clientX - rect.left) * scaleX;
  const lane = Math.floor(canvasX / LANE_WIDTH);
  return Math.max(0, Math.min(LANES - 1, lane));
}

// 멀티터치 시작
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  if (!isPlaying) return;

  for (let i = 0; i < e.changedTouches.length; i++) {
    const touch = e.changedTouches[i];
    const lane = getLaneFromTouch(touch.clientX);
    activeTouches.set(touch.identifier, lane);
    
    if (!keyPressed[lane]) {
      keyPressed[lane] = true;
      checkHit(lane);
    }
  }
}, { passive: false });

// 멀티터치 종료 및 취소
function handleTouchEnd(e) {
  e.preventDefault();
  for (let i = 0; i < e.changedTouches.length; i++) {
    const touch = e.changedTouches[i];
    const lane = activeTouches.get(touch.identifier);
    activeTouches.delete(touch.identifier);

    // 같은 레인을 누르고 있는 다른 손가락이 없을 때만 버튼 해제
    if (lane !== undefined) {
      let stillPressed = false;
      for (let activeLane of activeTouches.values()) {
        if (activeLane === lane) stillPressed = true;
      }
      if (!stillPressed) {
        keyPressed[lane] = false;
      }
    }
  }
}

canvas.addEventListener('touchend', handleTouchEnd, { passive: false });
canvas.addEventListener('touchcancel', handleTouchEnd, { passive: false });

// PC 키보드 이벤트 병행 지원
window.addEventListener('keydown', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1 && !keyPressed[idx]) {
    keyPressed[idx] = true;
    if (isPlaying) checkHit(idx);
  }
});

window.addEventListener('keyup', (e) => {
  const idx = KEYS.indexOf(e.key.toLowerCase());
  if (idx !== -1) {
    keyPressed[idx] = false;
  }
});

function updateAndDraw() {
  if (!isPlaying) return;

  const currentTime = (performance.now() - startTime) / 1000;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 1. 레인 및 하단 터치 패드 영역 그리기
  for (let i = 0; i < LANES; i++) {
    const x = i * LANE_WIDTH;
    
    // 상단 레인 이펙트
    if (keyPressed[i]) {
      const grad = ctx.createLinearGradient(0, HIT_Y - 180, 0, HIT_Y);
      grad.addColorStop(0, 'rgba(0, 242, 254, 0)');
      grad.addColorStop(1, 'rgba(0, 242, 254, 0.35)');
      ctx.fillStyle = grad;
      ctx.fillRect(x, HIT_Y - 180, LANE_WIDTH, 180);
    }

    // 하단 대형 터치 패드 UI (판정선 아래 영역)
    ctx.fillStyle = keyPressed[i] ? LANE_COLORS[i] : '#1f2630';
    ctx.fillRect(x + 4, HIT_Y + 8, LANE_WIDTH - 8, canvas.height - HIT_Y - 14);

    // 레인 구분선
    ctx.strokeStyle = '#30363d';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();

    // 터치 패드 안내 텍스트
    ctx.fillStyle = keyPressed[i] ? '#0e1117' : '#8b949e';
    ctx.font = 'bold 20px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('TAP', x + LANE_WIDTH / 2, HIT_Y + 72);
  }

  // 2. 판정선
  ctx.strokeStyle = '#00f2fe';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, HIT_Y);
  ctx.lineTo(canvas.width, HIT_Y);
  ctx.stroke();

  // 3. 노트 렌더링
  let remainingNotes = 0;
  for (let note of notes) {
    if (note.hit || note.missed) continue;
    remainingNotes++;

    const timeDiff = note.time - currentTime;
    const y = HIT_Y - (timeDiff * NOTE_SPEED);

    if (timeDiff < -0.20) {
      note.missed = true;
      combo = 0;
      showJudgement("MISS", "#ff4b4b");
      continue;
    }

    if (y >= -25 && y <= HIT_Y + 20) {
      const x = note.lane * LANE_WIDTH + 10;
      const w = LANE_WIDTH - 20;
      const h = 24; // 태블릿 시인성을 위해 노트 두께 증가

      ctx.fillStyle = LANE_COLORS[note.lane];
      ctx.beginPath();
      ctx.roundRect(x, y - h / 2, w, h, 6);
      ctx.fill();
    }
  }

  // 4. 점수 및 판정 UI
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

  if (remainingNotes === 0) {
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
  activeTouches.clear();
  keyPressed = [false, false, false, false];
  generateBeatmap();
  
  isPlaying = true;
  startTime = performance.now();
  overlay.style.display = 'none';
  requestAnimationFrame(updateAndDraw);
}

function endGame() {
  isPlaying = false;
  titleText.innerHTML = `CLEAR!<br><span style="font-size:20px; color:white;">Score: ${score} | Max Combo: ${maxCombo}</span>`;
  startBtn.innerText = "다시 하기 (Retry)";
  overlay.style.display = 'flex';
}

// 터치 및 클릭 모두 반응하도록 설정
startBtn.addEventListener('click', startGame);
</script>
</body>
</html>
"""

components.html(rhythm_game_html, height=680)
