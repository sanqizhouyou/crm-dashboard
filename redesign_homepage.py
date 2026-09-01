#!/usr/bin/env python3
"""
Redesign the homepage of quote-tool.html to match the AI-generated UI mockup.
Key changes:
1. Enhanced CSS with better gradients, shadows, glassmorphism
2. Refined layout matching the 6:4 split design
3. Updated stat cards with new metrics
4. Better button and card styles
5. All functionality preserved
"""
import re

FILE = '/mnt/openclaw/hermes/data/workspace/crm-dashboard/quote-tool.html'

with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ============================================================
# STEP 1: Replace the <style> section
# ============================================================
style_start = content.find('<style>')
style_end = content.find('</style>', style_start)

NEW_STYLE = '''<style>
/* ══════════════════════════════════════════════
   美团餐饮SaaS · 报价工具 — 智能看板风格
   Colors: #0a0a0a bg / #1a1a1a cards / #f5c518 gold
   ══════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #0a0a0a;
  color: #e0e0e0;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Loading 动画 ── */
#appLoading {
  position: fixed; inset: 0; z-index: 99999;
  background: #0a0a0a;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 24px;
  transition: opacity 0.6s ease;
}
#appLoading.hidden { opacity: 0; pointer-events: none; }
.loader-logo {
  width: 80px; height: 80px;
  background: linear-gradient(135deg, #f5c518, #e0a800);
  border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  font-size: 36px; font-weight: 900; color: #0a0a0a;
  animation: loaderPulse 1.5s ease-in-out infinite;
  box-shadow: 0 0 60px rgba(245,197,24,0.3);
}
@keyframes loaderPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 60px rgba(245,197,24,0.3); }
  50% { transform: scale(1.05); box-shadow: 0 0 80px rgba(245,197,24,0.5); }
}
.loader-bar-wrap { width: 200px; height: 4px; background: #1a1a1a; border-radius: 2px; overflow: hidden; }
.loader-bar { width: 40%; height: 100%; background: linear-gradient(90deg, #f5c518, #ffdc5e, #f5c518); border-radius: 2px; animation: loaderSlide 1.5s ease-in-out infinite; }
@keyframes loaderSlide {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(150%); }
  100% { transform: translateX(350%); }
}
.loader-text { font-size: 14px; color: #888; letter-spacing: 2px; }

/* ── 顶部导航 ── */
.top-nav {
  position: sticky; top: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 32px; height: 64px;
  background: rgba(10,10,10,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(245,197,24,0.1);
}
.nav-logo {
  font-size: 22px; font-weight: 800;
  background: linear-gradient(135deg, #f5c518, #ffdc5e);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1px;
}
.nav-menu { display: flex; gap: 8px; }
.nav-item {
  padding: 8px 20px; border-radius: 8px;
  font-size: 14px; font-weight: 500;
  color: #999; cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}
.nav-item:hover { color: #e0e0e0; background: rgba(245,197,24,0.05); }
.nav-item.active {
  color: #0a0a0a; font-weight: 600;
  background: linear-gradient(135deg, #f5c518, #e0a800);
  box-shadow: 0 2px 12px rgba(245,197,24,0.3);
}
.nav-user { display: flex; align-items: center; gap: 12px; }
.nav-avatar {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #f5c518, #e0a800);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 700; color: #0a0a0a;
}
.nav-name { font-size: 14px; font-weight: 500; color: #ccc; }
.nav-status {
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; color: #4ade80;
  padding: 4px 10px; border-radius: 20px;
  background: rgba(74,222,128,0.1);
}
.nav-status-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #4ade80;
  animation: statusPulse 2s ease-in-out infinite;
}
@keyframes statusPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ── 主容器 ── */
#main-container { max-width: 1400px; margin: 0 auto; padding: 32px; }

#selector {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 32px;
  align-items: start;
}

/* ── 海报卡片 ── */
.poster-card {
  position: relative;
  background: linear-gradient(145deg, #141414 0%, #1a1a1a 50%, #0f0f0f 100%);
  border-radius: 24px;
  padding: 48px;
  overflow: hidden;
  border: 1px solid rgba(245,197,24,0.08);
  box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03);
}
.poster-card::before {
  content: '';
  position: absolute; top: -50%; right: -20%;
  width: 60%; height: 200%;
  background: radial-gradient(ellipse, rgba(245,197,24,0.04) 0%, transparent 70%);
  pointer-events: none;
}

/* 背景装饰 */
.poster-bg-decoration {
  position: absolute; inset: 0;
  overflow: hidden;
  pointer-events: none;
  opacity: 0.5;
}
.poster-bg-bars {
  position: absolute; top: 0; right: 0;
  width: 300px; height: 100%;
}
.pbar {
  position: absolute; width: 2px;
  background: linear-gradient(to bottom, transparent, rgba(245,197,24,0.15), transparent);
}
.pbar-1 { height: 60%; top: 10%; left: 20%; }
.pbar-2 { height: 80%; top: 5%; left: 40%; }
.pbar-3 { height: 50%; top: 20%; left: 60%; }
.pbar-4 { height: 70%; top: 15%; left: 80%; }
.pbar-5 { height: 40%; top: 30%; left: 95%; }

.poster-particle {
  position: absolute;
  width: 4px; height: 4px;
  background: rgba(245,197,24,0.4);
  border-radius: 50%;
  animation: particleFloat 6s ease-in-out infinite;
}
.pp1 { top: 20%; left: 10%; animation-delay: 0s; }
.pp2 { top: 60%; left: 30%; animation-delay: 1.5s; }
.pp3 { top: 30%; left: 70%; animation-delay: 3s; }
.pp4 { top: 80%; left: 50%; animation-delay: 4.5s; }
@keyframes particleFloat {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.4; }
  50% { transform: translateY(-20px) scale(1.5); opacity: 0.8; }
}

.poster-techline {
  position: absolute;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(245,197,24,0.2), transparent);
}
.ptl1 { width: 200px; top: 30%; left: 5%; transform: rotate(-5deg); }
.ptl2 { width: 150px; bottom: 25%; right: 10%; transform: rotate(3deg); }

/* 主内容区 */
.poster-main {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 40px;
  align-items: center;
  z-index: 2;
}

.poster-text { display: flex; flex-direction: column; gap: 20px; }
.poster-tag {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px; border-radius: 20px;
  background: rgba(245,197,24,0.08);
  border: 1px solid rgba(245,197,24,0.15);
  font-size: 12px; font-weight: 500;
  color: #f5c518;
  width: fit-content;
}
.poster-tag-icon { width: 16px; height: 16px; stroke: #f5c518; }

.poster-title {
  display: flex; flex-direction: column; gap: 4px;
}
.poster-title-line {
  font-size: 48px; font-weight: 900; line-height: 1.1;
  background: linear-gradient(135deg, #ffffff 0%, #f5c518 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}
.poster-subtitle {
  font-size: 15px; color: #888; line-height: 1.6;
  max-width: 360px;
}

/* 3D 视觉 */
.poster-visual {
  display: flex; align-items: center; justify-content: center;
  height: 280px;
}
.poster-scene {
  position: relative;
  width: 200px; height: 200px;
  perspective: 800px;
  display: flex; align-items: center; justify-content: center;
}
.poster-platform {
  position: absolute; bottom: 30px;
  width: 160px; height: 40px;
}
.p-ring {
  position: absolute; bottom: 0; left: 50%;
  transform: translateX(-50%);
  border: 1px solid rgba(245,197,24,0.2);
  border-radius: 50%;
  animation: ringPulse 3s ease-in-out infinite;
}
.pr1 { width: 160px; height: 40px; animation-delay: 0s; }
.pr2 { width: 120px; height: 30px; animation-delay: 0.5s; }
.pr3 { width: 80px; height: 20px; animation-delay: 1s; }
@keyframes ringPulse {
  0%, 100% { opacity: 0.3; transform: translateX(-50%) scale(1); }
  50% { opacity: 0.8; transform: translateX(-50%) scale(1.05); }
}

.poster-pillar {
  position: absolute; bottom: 40px; left: 50%;
  transform: translateX(-50%);
  width: 16px; height: 60px;
  background: linear-gradient(to top, rgba(245,197,24,0.3), rgba(245,197,24,0.1));
  border-radius: 4px;
}
.poster-pillar-top {
  position: absolute; bottom: 100px; left: 50%;
  transform: translateX(-50%);
  width: 20px; height: 4px;
  background: #f5c518;
  border-radius: 2px;
  box-shadow: 0 0 20px rgba(245,197,24,0.5);
}

.poster-cube {
  position: absolute; bottom: 110px; left: 50%;
  transform: translateX(-50%);
  width: 64px; height: 64px;
  transform-style: preserve-3d;
  animation: cubeSpin 8s linear infinite;
}
@keyframes cubeSpin {
  0% { transform: translateX(-50%) rotateX(-20deg) rotateY(0deg); }
  100% { transform: translateX(-50%) rotateX(-20deg) rotateY(360deg); }
}
.pc-face {
  position: absolute; width: 64px; height: 64px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 900; color: #0a0a0a;
  border: 2px solid rgba(245,197,24,0.6);
}
.pc-front  { transform: translateZ(32px); background: linear-gradient(135deg, #f5c518, #e0a800); }
.pc-back   { transform: rotateY(180deg) translateZ(32px); background: linear-gradient(135deg, #e0a800, #c8960a); }
.pc-right  { transform: rotateY(90deg) translateZ(32px); background: linear-gradient(135deg, #c8960a, #b08609); }
.pc-left   { transform: rotateY(-90deg) translateZ(32px); background: linear-gradient(135deg, #f5c518, #ffdc5e); }
.pc-top    { transform: rotateX(90deg) translateZ(32px); background: linear-gradient(135deg, #ffdc5e, #f5c518); }
.pc-bottom { transform: rotateX(-90deg) translateZ(32px); background: linear-gradient(135deg, #b08609, #8a6c08); }

/* 底部指标卡片 */
.poster-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid rgba(245,197,24,0.08);
}
.pstat-card {
  padding: 20px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 16px;
  transition: all 0.3s ease;
}
.pstat-card:hover {
  background: rgba(245,197,24,0.03);
  border-color: rgba(245,197,24,0.12);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.pstat-header {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 12px;
}
.pstat-icon {
  width: 28px; height: 28px;
  background: rgba(245,197,24,0.08);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
}
.pstat-icon svg { width: 14px; height: 14px; stroke: #f5c518; }
.pstat-label { font-size: 12px; color: #888; font-weight: 500; }
.pstat-value {
  font-size: 28px; font-weight: 800;
  background: linear-gradient(135deg, #f5c518, #ffdc5e);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}
.pstat-chart {
  display: flex; gap: 3px; align-items: flex-end;
  height: 20px;
}
.pstat-bar {
  flex: 1;
  background: linear-gradient(to top, rgba(245,197,24,0.2), rgba(245,197,24,0.6));
  border-radius: 2px;
  animation: barPulse 2s ease-in-out infinite;
}
.psb1 { height: 40%; animation-delay: 0s; }
.psb2 { height: 60%; animation-delay: 0.2s; }
.psb3 { height: 80%; animation-delay: 0.4s; }
.psb4 { height: 70%; animation-delay: 0.6s; }
.psb5 { height: 90%; animation-delay: 0.8s; }
@keyframes barPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

/* ── 更新日志 ── */
.changelog {
  margin-top: 32px;
  background: linear-gradient(145deg, #141414, #1a1a1a);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid rgba(255,255,255,0.04);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.changelog-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.changelog-title {
  font-size: 16px; font-weight: 700; color: #e0e0e0;
  display: flex; align-items: center; gap: 8px;
}
.changelog-count {
  font-size: 11px; color: #888;
  padding: 4px 10px; border-radius: 12px;
  background: rgba(245,197,24,0.08);
  border: 1px solid rgba(245,197,24,0.1);
}
.changelog-list {
  display: flex; flex-direction: column;
  gap: 2px;
  max-height: 360px;
  overflow-y: auto;
  padding-right: 8px;
}
.changelog-list::-webkit-scrollbar { width: 4px; }
.changelog-list::-webkit-scrollbar-track { background: transparent; }
.changelog-list::-webkit-scrollbar-thumb { background: rgba(245,197,24,0.2); border-radius: 2px; }

.changelog-item {
  display: grid;
  grid-template-columns: 80px 52px 1fr;
  gap: 12px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 10px;
  transition: background 0.2s ease;
}
.changelog-item:hover { background: rgba(245,197,24,0.03); }
.changelog-date { font-size: 12px; color: #666; font-weight: 500; }
.changelog-tag {
  font-size: 10px; font-weight: 700;
  padding: 3px 8px; border-radius: 4px;
  text-align: center;
  letter-spacing: 0.5px;
}
.tag-feat { background: rgba(59,130,246,0.15); color: #60a5fa; }
.tag-fix { background: rgba(239,68,68,0.15); color: #f87171; }
.tag-new { background: rgba(245,197,24,0.12); color: #f5c518; }
.changelog-text { font-size: 13px; color: #aaa; line-height: 1.5; }

/* ── 右侧报价工具 ── */
.tool-card {
  background: linear-gradient(145deg, #141414, #1a1a1a);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid rgba(245,197,24,0.08);
  box-shadow: 0 12px 40px rgba(0,0,0,0.3);
  position: relative;
  overflow: hidden;
}
.tool-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #f5c518, #e0a800, #f5c518);
}
.tool-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 24px;
}
.tool-title { font-size: 18px; font-weight: 700; color: #e0e0e0; }
.tool-subtitle { font-size: 12px; color: #666; margin-top: 4px; }
.tool-badge {
  padding: 4px 12px; border-radius: 8px;
  background: linear-gradient(135deg, #f5c518, #e0a800);
  font-size: 11px; font-weight: 800;
  color: #0a0a0a;
  letter-spacing: 1px;
}
.tool-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label {
  font-size: 12px; font-weight: 500; color: #888;
  padding-left: 4px;
}
.form-input {
  padding: 10px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  font-size: 14px; color: #e0e0e0;
  outline: none;
  transition: all 0.3s ease;
}
.form-input:focus {
  border-color: rgba(245,197,24,0.4);
  background: rgba(245,197,24,0.03);
  box-shadow: 0 0 0 3px rgba(245,197,24,0.08);
}
.form-input::placeholder { color: #555; }

.tool-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #f5c518, #e0a800);
  border: none; border-radius: 12px;
  font-size: 15px; font-weight: 700;
  color: #0a0a0a;
  cursor: pointer;
  letter-spacing: 2px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(245,197,24,0.25);
}
.tool-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(245,197,24,0.35);
}
.tool-btn:active { transform: translateY(0); }

/* ── 友商对比卡片 ── */
.compare-card {
  margin-top: 24px;
  background: linear-gradient(145deg, #141414, #1a1a1a);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid rgba(255,255,255,0.04);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.compare-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.compare-title {
  font-size: 16px; font-weight: 700; color: #e0e0e0;
  display: flex; align-items: center; gap: 8px;
}
.compare-action {
  font-size: 12px; color: #f5c518; cursor: pointer;
  transition: color 0.2s ease;
}
.compare-action:hover { color: #ffdc5e; }

.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.compare-table th {
  padding: 10px 8px;
  text-align: left;
  font-size: 11px; font-weight: 600;
  color: #666; text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.compare-table td {
  padding: 12px 8px;
  color: #aaa;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.compare-table .highlight { color: #f5c518; font-weight: 600; }
.compare-table .saving { color: #4ade80; font-weight: 600; font-size: 12px; }

/* ── 响应式 ── */
@media (max-width: 1100px) {
  #selector { grid-template-columns: 1fr; }
  .poster-main { grid-template-columns: 1fr; gap: 24px; }
  .poster-visual { display: none; }
  .poster-stats { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .top-nav { padding: 0 16px; }
  .nav-menu { display: none; }
  #main-container { padding: 16px; }
  .poster-card { padding: 28px; }
  .poster-title-line { font-size: 32px; }
  .poster-stats { grid-template-columns: 1fr; }
  .tool-form { grid-template-columns: 1fr; }
}

/* ── 其他页面隐藏 ── */
.page-section { display: none; }
.page-section.active { display: block; }
'''

# Replace style section
content = content[:style_start] + NEW_STYLE + content[style_end + len('</style>'):]

# ============================================================
# STEP 2: Replace the homepage HTML (main-container content)
# ============================================================
# Find the main-container boundaries
main_start = content.find('<div id="main-container">')
# Find the end of main-container (before the script tag or before page sections)
main_end_marker = content.find('\n<script>\nconst BASIC_B64', main_start)
if main_end_marker == -1:
    main_end_marker = content.find('\n<script>', main_start)

# The main-container ends right before the script tag
# Find the last </div> before script
main_end = content.rfind('</div>\n', main_start, main_end_marker) + len('</div>\n')

NEW_MAIN = '''<div id="main-container">
<div id="selector">
  <div class="col-left">
    <!-- 左上：智能报价海报卡片 -->
    <div class="poster-card">
      <!-- 背景装饰 -->
      <div class="poster-bg-decoration">
        <div class="poster-bg-bars">
          <div class="pbar pbar-1"></div>
          <div class="pbar pbar-2"></div>
          <div class="pbar pbar-3"></div>
          <div class="pbar pbar-4"></div>
          <div class="pbar pbar-5"></div>
        </div>
        <div class="poster-particle pp1"></div>
        <div class="poster-particle pp2"></div>
        <div class="poster-particle pp3"></div>
        <div class="poster-particle pp4"></div>
        <div class="poster-techline ptl1"></div>
        <div class="poster-techline ptl2"></div>
      </div>

      <!-- 主内容 -->
      <div class="poster-main">
        <!-- 左侧文字 -->
        <div class="poster-text">
          <div class="poster-tag">
            <svg class="poster-tag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
            <span>智能看板</span>
          </div>
          <h1 class="poster-title">
            <span class="poster-title-line">智能报价</span>
            <span class="poster-title-line">降本增效</span>
          </h1>
          <p class="poster-subtitle">基于AI算法实时分析市场数据，智能优化报价策略</p>
        </div>

        <!-- 右侧3D视觉 -->
        <div class="poster-visual">
          <div class="poster-scene">
            <!-- 发光平台 -->
            <div class="poster-platform">
              <div class="p-ring pr1"></div>
              <div class="p-ring pr2"></div>
              <div class="p-ring pr3"></div>
            </div>
            <!-- 圆柱底座 -->
            <div class="poster-pillar"></div>
            <div class="poster-pillar-top"></div>
            <!-- 3D立方体 -->
            <div class="poster-cube">
              <div class="pc-face pc-front">AI</div>
              <div class="pc-face pc-top"></div>
              <div class="pc-face pc-right"></div>
              <div class="pc-face pc-left"></div>
              <div class="pc-face pc-back"></div>
              <div class="pc-face pc-bottom"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部指标卡片 -->
      <div class="poster-stats">
        <div class="pstat-card">
          <div class="pstat-header">
            <div class="pstat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                <polyline points="17 6 23 6 23 12"/>
              </svg>
            </div>
            <span class="pstat-label">签约品牌数</span>
          </div>
          <div class="pstat-value">2,465+</div>
          <div class="pstat-chart">
            <div class="pstat-bar psb1"></div>
            <div class="pstat-bar psb2"></div>
            <div class="pstat-bar psb3"></div>
            <div class="pstat-bar psb4"></div>
            <div class="pstat-bar psb5"></div>
          </div>
        </div>
        <div class="pstat-card">
          <div class="pstat-header">
            <div class="pstat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <span class="pstat-label">年均节省</span>
          </div>
          <div class="pstat-value">¥3,268万</div>
          <div class="pstat-chart">
            <div class="pstat-bar psb1"></div>
            <div class="pstat-bar psb2"></div>
            <div class="pstat-bar psb3"></div>
            <div class="pstat-bar psb4"></div>
            <div class="pstat-bar psb5"></div>
          </div>
        </div>
        <div class="pstat-card">
          <div class="pstat-header">
            <div class="pstat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="6"/>
                <circle cx="12" cy="12" r="2"/>
              </svg>
            </div>
            <span class="pstat-label">客户满意度</span>
          </div>
          <div class="pstat-value">98.7%</div>
          <div class="pstat-chart">
            <div class="pstat-bar psb1"></div>
            <div class="pstat-bar psb2"></div>
            <div class="pstat-bar psb3"></div>
            <div class="pstat-bar psb4"></div>
            <div class="pstat-bar psb5"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 左下：更新记录 -->
    <div class="changelog">
      <div class="changelog-header">
        <span class="changelog-title">📋 功能更新记录</span>
        <span class="changelog-count">12 条</span>
      </div>
      <div class="changelog-list">
        <div class="changelog-item">
          <span class="changelog-date">2026.08.25</span>
          <span class="changelog-tag tag-feat">FEAT</span>
          <span class="changelog-text">阶梯对比模式支持多方案：每个方案各自生成阶梯对比表，统一导出</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.08.25</span>
          <span class="changelog-tag tag-fix">FIX</span>
          <span class="changelog-text">修复多方案阶梯对比：服务产品不显示、汇总总计缺失问题</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.08.16</span>
          <span class="changelog-tag tag-feat">FEAT</span>
          <span class="changelog-text">主页全新改版：深色仪表盘风格，5:7非对称网格布局</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.08.15</span>
          <span class="changelog-tag tag-new">NEW</span>
          <span class="changelog-text">新增「友商成本对比」功能：一键对比美团vs友商年度综合成本</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.08.03</span>
          <span class="changelog-tag tag-new">NEW</span>
          <span class="changelog-text">新增「智能备餐」产品（标价¥2,088/店/年）</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.08.03</span>
          <span class="changelog-tag tag-new">NEW</span>
          <span class="changelog-text">新增硬件产品：80N（¥399）与 80NW（¥429）</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.07.29</span>
          <span class="changelog-tag tag-feat">FEAT</span>
          <span class="changelog-text">P2平板收银配件底座价格调整（348→268）</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.07.28</span>
          <span class="changelog-tag tag-feat">FEAT</span>
          <span class="changelog-text">添加 loading 加载动画，优化白屏等待体验</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.07.24</span>
          <span class="changelog-tag tag-new">NEW</span>
          <span class="changelog-text">总部产品支持自定义数量：第三方配套对接点位</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.07.07</span>
          <span class="changelog-tag tag-new">NEW</span>
          <span class="changelog-text">副收银支持自定义数量输入，报价表格新增数量列</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.07.03</span>
          <span class="changelog-tag tag-feat">FEAT</span>
          <span class="changelog-text">打包价低于成本价改为提醒确认；阶梯对比模式新增打包价</span>
        </div>
        <div class="changelog-item">
          <span class="changelog-date">2026.06.30</span>
          <span class="changelog-tag tag-new">NEW</span>
          <span class="changelog-text">新增「战略合作政策」页面，支持自主编辑内容</span>
        </div>
      </div>
    </div>
  </div>
  <div class="col-right">
    <!-- 右上：AI智能报价工具 -->
    <div class="tool-card">
      <div class="tool-header">
        <div class="tool-title-group">
          <div class="tool-title">AI智能报价工具</div>
          <div class="tool-subtitle">输入参数，一键生成精准报价</div>
        </div>
        <span class="tool-badge">PRO</span>
      </div>
      <div class="tool-form">
        <div class="form-group">
          <label class="form-label">产品名称</label>
          <input class="form-input" type="text" placeholder="如：主收银">
        </div>
        <div class="form-group">
          <label class="form-label">数量</label>
          <input class="form-input" type="number" placeholder="如：50">
        </div>
        <div class="form-group">
          <label class="form-label">规格</label>
          <input class="form-input" type="text" placeholder="如：连锁版">
        </div>
        <div class="form-group">
          <label class="form-label">材料</label>
          <input class="form-input" type="text" placeholder="如：标准">
        </div>
      </div>
      <button class="tool-btn" onclick="loadVersion('pro')">立 即 报 价</button>
    </div>

    <!-- 右下：友商成本对比 -->
    <div class="compare-card">
      <div class="compare-header">
        <span class="compare-title">📊 友商成本对比分析</span>
        <span class="compare-action" onclick="openCompareModal()">查看详情 →</span>
      </div>
      <table class="compare-table">
        <thead>
          <tr>
            <th>费用项目</th>
            <th>友商A</th>
            <th>美团</th>
            <th>差额</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>POS系统年费</td>
            <td>¥3,600,000</td>
            <td class="highlight">¥2,880,000</td>
            <td class="saving">节省 ¥720,000</td>
          </tr>
          <tr>
            <td>供应链年费</td>
            <td>¥1,200,000</td>
            <td class="highlight">¥960,000</td>
            <td class="saving">节省 ¥240,000</td>
          </tr>
          <tr>
            <td>支付手续费年费</td>
            <td>¥480,000</td>
            <td class="highlight">¥360,000</td>
            <td class="saving">节省 ¥120,000</td>
          </tr>
          <tr>
            <td>维护服务费</td>
            <td>¥240,000</td>
            <td class="highlight">¥0</td>
            <td class="saving">节省 ¥240,000</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
</div>
'''

content = content[:main_start] + NEW_MAIN + content[main_end:]

# ============================================================
# STEP 3: Update the navigation items
# ============================================================
# Change nav items to match mockup: 首页, 报价工具, 产品手册, 战略合作
old_nav = '''<div class="nav-menu">
    <span class="nav-item active">首页</span>
    <span class="nav-item">报价工具</span>
    <span class="nav-item">产品中心</span>
    <span class="nav-item">帮助中心</span>
  </div>'''
new_nav = '''<div class="nav-menu">
    <span class="nav-item active">首页</span>
    <span class="nav-item">报价工具</span>
    <span class="nav-item">产品手册</span>
    <span class="nav-item">战略合作</span>
  </div>'''
content = content.replace(old_nav, new_nav)

# ============================================================
# STEP 4: Update SW cache version
# ============================================================
content = content.replace('seo-quote-v25', 'seo-quote-v26')

# Write the modified file
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"File updated successfully!")
print(f"Original size: {len(content)} chars")

# Verify key elements
checks = [
    (' poster-card', 'Poster card'),
    ('pstat-value', 'Stat values'),
    ('tool-btn', 'Tool button'),
    ('compare-table', 'Compare table'),
    ('seo-quote-v26', 'SW cache v26'),
    ('changelog', 'Changelog'),
]
for keyword, name in checks:
    count = content.count(keyword)
    print(f"  {name}: {count} occurrences")

print("\n✅ Homepage redesign complete!")
