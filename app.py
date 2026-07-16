#!/usr/bin/env python3
import os
import requests
import urllib3
from flask import Flask, render_template_string, request, jsonify

urllib3.disable_warnings()

app = Flask(__name__)

VISIT_FILE = "visits_like_booster.txt"

def get_and_increment_visits():
    count = 1042  
    try:
        if os.path.exists(VISIT_FILE):
            with open(VISIT_FILE, "r") as f:
                count = int(f.read().strip())
        count += 1
        with open(VISIT_FILE, "w") as f:
            f.write(str(count))
    except Exception:
        pass
    return count


# PREMIUM DYNAMIC COMMON HEADERS (No stylized decorative fonts, clean sans-serif only)
UI_COMMON_HEADER = r"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --p:#00ffe7; /* Neon Teal */
  --p2:#00c9b1;
  --p3:#7fffd4;
  --g1:#ff007f; /* Neon Magenta */
  --acc:#ffd700;
  --dark:#040212;
  --card:rgba(12, 6, 32, 0.75);
  --brd:rgba(0, 255, 231, 0.18);
  --glow: rgba(0, 255, 231, 0.4);
}
body {
    /* Using standard system sans-serif font for maximum clean readability */
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: var(--dark);
    color: #f0ebfa;
    overflow-x: hidden;
    width: 100%;
    margin: 0; padding: 0;
}
#vanta-bg { position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: -1; pointer-events: none; }
body::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.07)2px,rgba(0,0,0,.07)4px);}

.shell{position:relative;z-index:2;max-width:440px;margin:0 auto;padding:1.2rem 1rem 3rem}

/* Top Header Bar */
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card);
    backdrop-filter: blur(25px);
    border: 1px solid var(--brd);
    padding: 0.8rem 1.2rem;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.gradient-text {
    background: linear-gradient(90deg, #00ffe7, #ff007f, #00ffe7);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
    letter-spacing: 1px;
}

/* Compact CD Player in header */
.compact-player {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  background: rgba(12, 6, 36, 0.65);
  padding: 0.35rem 0.7rem;
  border-radius: 20px;
  border: 1px solid var(--brd);
  box-shadow: 0 0 15px var(--glow);
  transition: all 0.3s;
}
.compact-player:hover {
  border-color: var(--p);
}
.disc-wrapper {
  position: relative;
  width: 24px; height: 28px;
}
.mdisc{
  font-size:1.6rem;
  color: var(--p);
  animation:discSpin 4s linear infinite;
}
.mdisc.paused{animation-play-state:paused}
@keyframes discSpin{to{transform:rotate(360deg)}}
.disc-center {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 8px; height: 8px;
  background: var(--dark);
  border-radius: 50%;
  border: 1px solid #fff;
}
.compact-lbl {
  font-size: 0.6rem;
  letter-spacing: 1px;
  color: var(--p);
  text-transform: uppercase;
  font-weight: bold;
}

/* Glowing organic curves - No hard rectangular enclosing lines allowed */
@keyframes pulseGlow {
    0% { border-color: rgba(0, 255, 231, 0.15); box-shadow: 0 0 15px rgba(0, 255, 231, 0.1); }
    50% { border-color: rgba(0, 255, 231, 0.45); box-shadow: 0 0 25px rgba(0, 255, 231, 0.25); }
    100% { border-color: rgba(0, 255, 231, 0.15); box-shadow: 0 0 15px rgba(0, 255, 231, 0.1); }
}

.organic-card {
    background: var(--card);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1.5px solid var(--brd);
    
    /* Dynamic organic rounded curves */
    border-radius: 35px 12px;
    padding: 1.8rem 1.4rem;
    position: relative;
    box-shadow: 0 10px 40px rgba(0,0,0,0.7);
    margin-bottom: 15px;
    animation: pulseGlow 6s infinite ease-in-out;
}

.card-head{display:flex;align-items:center;gap:0.6rem;margin-bottom:1.2rem}
.card-ico{font-size:1.2rem;color:var(--p)}
.card-ttl{font-size:0.85rem;font-weight:900;color:#fff;letter-spacing:1px;text-transform:uppercase}

/* Form inputs with smooth curves */
.inp-wrap {
    position: relative;
    margin-bottom: 0.8rem;
}
.inp-lbl {
    font-size: .65rem;
    color: var(--dim);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: .35rem;
    display: block;
    font-weight: bold;
}
.inp {
    width:100%;
    background:rgba(0, 0, 0, 0.5);
    border:1.5px solid var(--brd);
    border-radius: 12px;
    padding:.8rem 2.5rem .8rem 1rem;
    font-size:.85rem;
    color:#fff;
    outline:none;
    transition:all .25s;
}
.inp:focus {
    border-color:var(--p);
    box-shadow:0 0 15px var(--glow);
}
.iico{position:absolute;right:1rem;top:50%;color:var(--p);font-size:.85rem;pointer-events:none}

.auth-select {
    width: 100%;
    background: rgba(0, 0, 0, 0.5);
    border: 1.5px solid var(--brd);
    border-radius: 12px;
    color: #fff;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    outline: none;
    cursor: pointer;
    margin-bottom: 0.8rem;
}
.auth-select option {
    background: #020108;
    color: #fff;
}

/* Linear Glowing Button */
.btn-glow {
    background: linear-gradient(135deg, #00ffd7, #00c9b1);
    color: #03020e; border: none; cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 255, 231, 0.35);
    padding: 0.95rem 2rem; 
    border-radius: 12px; 
    font-weight: 800;
    letter-spacing: 1px;
    display: inline-flex; align-items: center; justify-content: center; gap: 0.6rem;
    width: 100%; text-transform: uppercase;
    font-size: 0.85rem;
}
.btn-glow:hover { box-shadow: 0 0 25px var(--glow); transform: translateY(-2px); }

/* Holographic Security Profile badge of Owner */
.vip-card {
  background: var(--card);
  border: 1.5px solid var(--brd);
  border-radius: 35px 12px;
  padding: 1.2rem;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.85);
  position: relative;
  overflow: hidden;
  max-width: 580px;
  margin: 0 auto 1.5rem;
  animation: pulseGlow 5s infinite ease-in-out;
}
.profile-wrap{width:140px;height:120px;position:relative;display:flex;align-items:center;justify-content:center;margin: 0 auto 0.5rem}
.profile-inner{width:85px;height:85px;border-radius:50%;overflow:hidden;position:relative;z-index:5;background:rgba(0, 255, 231, 0.1);display:flex;align-items:center;justify-content:center;box-shadow:0 0 25px var(--glow)}
.profile-inner img{width:100%;height:100%;object-fit:cover;border-radius:50%;}
.pico-owner { font-size: 2.2rem; background: linear-gradient(135deg, var(--p), var(--g1)); -webkit-background-clip: text;-webkit-text-fill-color: transparent; }

.orbit-ring { position: absolute; border-radius: 50%; pointer-events: none; transition: border-color 0.5s; }
.ring-1 {
    width: 105px; height: 110px; z-index: 2;
    border: 1.5px solid var(--p);
    animation: rotateClockwise 8s linear infinite;
}
.ring-1::before {
    content: ""; position: absolute; width: 6px; height: 6px; background: var(--p);
    border-radius: 50%; top: -3px; left: 50%; transform: translateX(-50%);
}
.ring-2 {
    width: 120px; height: 120px; z-index: 1;
    border: 2px dashed rgba(0, 255, 231, 0.3);
    animation: rotateCounterClockwise 12s linear infinite;
}

@keyframes rotateClockwise { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes rotateCounterClockwise { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }

.vip-title {
  font-size: 1.4rem; font-weight: 900; letter-spacing: 2px; text-align:center;
  background: linear-gradient(90deg, #fff, var(--p), #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 0.2rem;
}
.vip-sub {
  font-size: 0.6rem; color: var(--dim); letter-spacing: 1px; text-align:center; text-transform: uppercase; margin-bottom: 1rem; font-weight: bold;
}
.vip-details-box {
  width: 100%; border-top: 1px solid rgba(0, 255, 231, 0.2); padding-top: 1rem; display: flex; flex-direction: column; gap: 0.6rem;
}
.vip-row {
  display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;
}
.vip-lbl {
  color: var(--dim); font-size: 0.65rem; letter-spacing: 1px; display: flex; align-items: center; gap: 0.4rem; font-weight: bold;
}
.vip-row:nth-child(1) .vip-lbl i { color: var(--acc); }
.vip-row:nth-child(2) .vip-lbl i { color: var(--p); }
.vip-row:nth-child(3) .vip-lbl i { color: #ff3366; }
.vip-val {
  font-weight: 700; color: #fff;
}

/* Glass loading transition overlay */
.overlay{position:fixed;inset:0;background:rgba(0, 0, 0, 0.85);backdrop-filter:blur(10px);z-index:9000;display:none;flex-direction:column;align-items:center;justify-content:center;gap:1.2rem}
.overlay.show { display: flex; }
.ov-ring{width:64px;height:64px;border-radius:50%;border:3px solid rgba(0, 255, 231, 0.2);border-top-color:#00ffe7;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.ov-txt{font-size:.78rem;letter-spacing:1px;color:#00ffe7;font-weight: bold;}
.ov-sub{font-size:.65rem;color:var(--dim);letter-spacing:1px}

/* Interactive Success Modal Overlay */
.modal-overlay {
    position: fixed; inset: 0;
    background: rgba(2, 1, 8, 0.85);
    backdrop-filter: blur(12px);
    z-index: 99990; display: none;
    align-items: center; justify-content: center;
}
.modal-overlay.show { display: flex; }

/* TALL LUXURIOUS SOCIAL PROFILE SUCCESS CARD */
.success-social-card {
    background: linear-gradient(135deg, rgba(14, 8, 32, 0.95), rgba(4, 2, 14, 0.98));
    border: 2px solid var(--p);
    border-radius: 40px 12px;
    padding: 2.2rem 1.6rem; /* Increased padding vertically to make the box taller (lamba kora) */
    max-width: 380px;
    width: 95%;
    box-shadow: 0 0 35px var(--p);
    text-align: center;
}

/* Banner Frame */
.banner-frame {
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    border: 1.5px solid var(--brd);
    box-shadow: 0 0 15px var(--glow);
    margin-bottom: 1.2rem;
}
.banner-img {
    width: 100%;
    height: auto;
    display: block;
}

/* Response Grid design */
.response-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 1rem 0;
    text-align: left;
}
.response-item {
    border: 1.5px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 10px 12px; /* Taller inner metric boxes */
    background: rgba(0, 0, 0, 0.4);
}
.response-lbl {
    font-size: 0.65rem; /* Clean normal typography - No Orbitron */
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.response-val {
    font-size: 0.82rem;
    font-weight: 700;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Multi-color glows for Metatags */
.res-before {
    border-color: rgba(255, 110, 199, 0.4);
    box-shadow: 0 0 10px rgba(255, 110, 199, 0.15);
}
.res-before .response-lbl { color: #ff6ec7; text-shadow: 0 0 8px rgba(255, 110, 199, 0.4); }

.res-given {
    border-color: rgba(0, 255, 231, 0.4);
    box-shadow: 0 0 10px rgba(0, 255, 231, 0.15);
}
.res-given .response-lbl { color: #00ffe7; text-shadow: 0 0 8px rgba(0, 255, 231, 0.4); }

.res-after {
    border-color: rgba(0, 255, 136, 0.4);
    box-shadow: 0 0 10px rgba(0, 255, 136, 0.15);
}
.res-after .response-lbl { color: #00ff88; text-shadow: 0 0 8px rgba(0, 255, 136, 0.4); }

.res-remains {
    border-color: rgba(255, 215, 0, 0.4);
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.15);
}
.res-remains .response-lbl { color: #ffd700; text-shadow: 0 0 8px rgba(255, 215, 0, 0.4); }

/* Toast Messages notifications */
.toast{position:fixed;bottom:1.5rem;right:1.5rem;z-index:99999;background:rgba(18, 20, 38, 0.95);border-radius:.8rem;padding:.85rem 1.2rem;font-size:.7rem;letter-spacing:1px;display:flex;align-items:center;gap:.7rem;max-width:320px;box-shadow:0 8px 30px rgba(0,0,0,.6);animation:toastIn .3s ease;border:1px solid rgba(0, 255, 231, 0.4);border-left:3px solid #00ffe7;color:#00ffe7}
@keyframes toastIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}
</style>
"""

# MASTER MAIN GENERATOR INTERFACE (JINJA FREE RAW CODE)
MAIN_INTERFACE_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    __COMMON_HEADER__
</head>
<body>
<div id="vanta-bg"></div>
<audio id="bgAudio" loop><source src="/static/music.mp3" type="audio/mpeg"></audio>
<div class="overlay" id="loadOverlay"><div class="ov-ring"></div><div class="ov-txt">PROCESSING</div><div class="ov-sub">Injecting Like Payload...</div></div>

<!-- Decrypted Response Verification Frame -->
<div class="modal-overlay" id="success-popup">
    <div class="success-crooked-frame success-social-card" id="success-content-box">
        <div style="font-size:3rem; color:var(--p); margin-bottom:0.8rem;">
            <i class="fas fa-heartbeat animate-pulse"></i>
        </div>
        <h3 style="font-size:1.1rem; color:var(--p); margin-bottom:0.2rem; letter-spacing:1px; font-weight:900;">TRANSMISSION COMPLETE</h3>
        <p style="font-size:0.6rem; color:var(--dim); text-transform:uppercase; margin-bottom:1rem; font-weight:bold;">Likes Dispatched • Garena Status 200</p>
        
        <!-- Live Garena Banner Image Profile display (Referrer-bypassed with loading protection) -->
        <div class="banner-frame" style="min-height: 80px; background: rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; position: relative;">
            <div id="banner-loader" style="position: absolute; color: var(--p); font-size: 0.8rem; font-weight: bold;"><i class="fas fa-spinner fa-spin"></i> Syncing Banner...</div>
            <img class="banner-img" id="success-banner" src="" referrerpolicy="no-referrer" alt="Player Banner" style="width: 100%; height: auto; display: none;" onload="document.getElementById('banner-loader').style.display='none'; this.style.display='block';">
        </div>

        <div class="response-grid">
            <div class="response-item res-before">
                <div class="response-lbl">Likes Before</div>
                <div class="response-val" id="success-before">--</div>
            </div>
            <div class="response-item res-given">
                <div class="response-lbl">Likes Dispatched</div>
                <div class="response-val" id="success-given">--</div>
            </div>
            <div class="response-item res-after">
                <div class="response-lbl">Likes After</div>
                <div class="response-val" id="success-after" style="color:var(--success);">--</div>
            </div>
            <div class="response-item res-remains">
                <div class="response-lbl">API Remains</div>
                <div class="response-val" id="success-remains">--</div>
            </div>
        </div>
        
        <div style="font-size:0.55rem; color:var(--p); margin-top:1rem; opacity:0.8; letter-spacing:1px; font-weight:bold;">
            <i class="fas fa-shield-alt"></i> AYAN NETWORK MAIN-FRAME
        </div>
        
        <button onclick="closeSuccessPopup()" class="btn-glow" style="margin-top:1.2rem; margin-bottom:0; font-size:0.75rem; padding:0.5rem 1rem;">Confirm Node</button>
    </div>
</div>

<div class="shell">

  <div class="header-bar">
    <span class="gradient-text text-glow">
        <i class="fa-solid fa-heart mr-2"></i>
        Aʏᴀɴ Lɪᴋᴇ Bᴏᴏsᴛᴇʀ
    </span>

    <!-- Small Golden Disc Player -->
    <div class="compact-player" id="mBtn">
      <div class="disc-wrapper">
        <i class="fas fa-compact-disc mdisc paused" id="mDisc"></i>
        <div class="disc-center"></div>
      </div>
      <span class="compact-lbl" id="mLbl">PLAY BGM</span>
    </div>
  </div>

  <!-- Unique Crooked VIP Owner Card -->
  <div class="vip-card">
    <div class="vip-head">
      <div class="profile-wrap">
        <div class="orbit-ring ring-1"></div>
        <div class="orbit-ring ring-2"></div>
        <div class="profile-inner">
          <img id="owner_avatar" src="/static/pic.jpg" alt="Ayan Bro" onerror="this.style.display='none'; document.getElementById('fallback_pico').style.display='inline-block'">
          <i class="fas fa-fire pico-owner" id="fallback_pico" style="display:none;"></i>
        </div>
      </div>
      <h2 class="vip-title">Aʏᴀɴ Wᴇʙsɪᴛᴇ</h2>
      <p class="vip-sub">Owner Portal Directory</p>
      
      <div class="vip-details-box">
        <div class="vip-row">
          <span class="vip-lbl"><i class="fas fa-crown"></i> Founder Role</span>
          <span class="vip-val" style="color:var(--acc);">Owner &amp; Lead</span>
        </div>
        <div class="vip-row">
          <span class="vip-lbl"><i class="fas fa-fingerprint"></i> System UID</span>
          <span class="vip-val" style="color:var(--p);">2279016714</span>
        </div>
        <div class="vip-row">
          <span class="vip-lbl"><i class="fas fa-phone-alt"></i> Phone Number</span>
          <span class="vip-val">018447826820</span>
        </div>
      </div>
    </div>
  </div>

  <!-- MAIN LIKE DISPATCH STATION CARD -->
  <div class="organic-card">
    <div class="card-head">
      <div class="card-ico"><i class="fas fa-heartbeat"></i></div>
      <div>
        <div class="card-ttl">Likes Dispatch Terminal</div>
      </div>
    </div>

    <!-- Inputs -->
    <div class="inp-wrap">
      <div class="inp-lbl">Target Account UID</div>
      <input class="inp" type="text" id="target-uid" placeholder="Enter Garena Account UID ">
      <i class="fas fa-id-card iico"></i>
    </div>
    
    <div class="inp-wrap" style="margin-top:0.8rem">
      <div class="inp-lbl">Target Server</div>
      <select class="auth-select" id="target-server">
        <option value="bd" selected>BD - Bangladesh</option>
        <option value="ind">IND - India</option>
        <option value="sg">SG - Singapore</option>
        <option value="pk">PK - Pakistan</option>
        <option value="br">BR - Brazil</option>
        <option value="us">US - United States</option>
      </select>
    </div>
    
    <button onclick="dispatchLikes()" class="btn-glow" style="margin-top:1rem;">
      <i class="fas fa-heart"></i> Dispatch Likes
    </button>
  </div>

</div>

<hr class="divider">
<div class="foot">Crafted With <span>♥</span> By <span>AYAN</span> &nbsp;•&nbsp; VIP Extractor Suite</div>

<div class="toast" id="toast"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js"></script>
<script>
async function dispatchLikes() {
    const loader = document.getElementById('loadOverlay');
    const uid = document.getElementById('target-uid').value.trim();
    const server = document.getElementById('target-server').value;
    
    if(!uid) {
        toast('Please enter a target account UID!', false);
        return;
    }

    loader.style.display = 'flex';
    document.getElementById('success-banner').style.display = 'none';
    document.getElementById('banner-loader').style.display = 'block';

    try {
        const queryUrl = '/api/like?uid=' + encodeURIComponent(uid) + '&server_name=' + encodeURIComponent(server);
        const r = await fetch(queryUrl);
        const data = await r.json();
        loader.style.display = 'none';

        if (data.success && data.api_response) {
            const apiRes = data.api_response;
            
            // Populating dynamic elements on the premium Social card
            document.getElementById('success-before').innerText = apiRes.LikesbeforeCommand || '0';
            document.getElementById('success-given').innerText = '+' + (apiRes.LikesGivenByAPI || '0');
            document.getElementById('success-after').innerText = apiRes.LikesafterCommand || '0';
            document.getElementById('success-remains').innerText = apiRes.remains || 'N/A';
            
            // Injecting the live Banner API Image inside success card dynamically with cache bypass
            const bannerUrl = 'https://nirob-free-fire-baner.vercel.app/profile?uid=' + uid + '&t=' + new Date().getTime();
            document.getElementById('success-banner').src = bannerUrl;
            
            // Pop success modal smoothly via GSAP
            document.getElementById('success-popup').classList.add('show');
            gsap.fromTo('#success-content-box', {scale: 0.85, opacity: 0}, {scale: 1, opacity: 1, duration: 0.35, ease: 'back.out(1.5)'});
        } else {
            toast(data.error || 'Decryption failed. Garena refused authorization.', false);
        }
    } catch(e) {
        loader.style.display = 'none';
        toast('Connection timed out.', false);
    }
}

function closeSuccessPopup() {
    gsap.to('#success-content-box', {scale: 0.85, opacity: 0, duration: 0.25, onComplete: () => {
        document.getElementById('success-popup').classList.remove('show');
    }});
}

// BGM Music Player with full auto play mapping inside document click
const audio=document.getElementById('bgAudio');let playing=false;const mDisc=document.getElementById('mDisc');
function setMusic(on){playing=on;mDisc.classList.toggle('paused',!on);}
document.getElementById('mBtn').onclick=()=>{if(playing){audio.pause();setMusic(false);}else{audio.play().then(()=>setMusic(true)).catch(()=>{});}};

// Auto play algorithm bypassing chrome sandbox on touch/interaction automatically!
let interactTriggered = false;
function autoPlayHandler() {
    if (interactTriggered) return;
    interactTriggered = true;
    audio.play().then(() => {
        setMusic(true);
    }).catch(e => {
        console.log("Autoplay blocked by sandbox. Interactive listener initialized.");
    });
}
['click', 'touchstart', 'scroll'].forEach(evt => {
    document.addEventListener(evt, autoPlayHandler, {once: true});
});

function toast(msg, success=true){
    const t=document.getElementById('toast');
    t.innerHTML = (success ? '<i class="fas fa-check-circle"></i> ' : '<i class="fas fa-exclamation-triangle"></i> ') + msg;
    t.className = 'toast';
    setTimeout(()=>t.classList.add('show'), 10);
    setTimeout(()=>t.classList.remove('show'), 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    VANTA.WAVES({
        el: "#vanta-bg",
        mouseControls: true, touchControls: true, gyroControls: false,
        minHeight: 200.00, minWidth: 200.00, scale: 1.00, scaleMobile: 1.00,
        color: 0x05041a, shininess: 45.00, waveHeight: 12.00, waveSpeed: 0.7, zoom: 0.90
    });
});
</script>
</body>
</html>
"""

# Replace Common Headers gracefully without Python f-string conflicts
MAIN_INTERFACE_HTML_FINAL = MAIN_INTERFACE_HTML.replace('__COMMON_HEADER__', UI_COMMON_HEADER)


# ----------------- FLASK ENDPOINTS / ROUTES -----------------

@app.route('/', methods=['GET'])
def index():
    visit_count = get_and_increment_visits()
    # Simple static replace bypasses Flask Jinja parser to 100% prevent 500 error!
    return MAIN_INTERFACE_HTML_FINAL.replace('{{ visit_count }}', str(visit_count))

# API GATEWAY PROXIER (Avoid CORS/browser blocks completely)
@app.route('/api/like', methods=['GET'])
def api_like():
    uid = request.args.get('uid', '').strip()
    server_name = request.args.get('server_name', 'bd').strip()
    if not uid:
        return jsonify({"success": False, "error": "Missing uid parameters"}), 400
        
    try:
        # Standard Garena proxy targeting like API ob54 key structure
        target_url = f"https://ayan-like-ob54.vercel.app/like?uid={uid}&server_name={server_name}&key=JMLB"
        resp = requests.get(target_url, timeout=20)
        
        try:
            data = resp.json()
        except:
            data = {"raw_text": resp.text}
            
        if resp.status_code == 200 and data.get("status") == 1:
            return jsonify({
                "success": True, 
                "api_response": data
            })
        else:
            err_msg = data.get("error") or "Garena server limit reached."
            return jsonify({"success": False, "error": err_msg})
    except Exception as e:
        return jsonify({"success": False, "error": f"API Connection timed out: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)