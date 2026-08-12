import subprocess
import time
import sys
import os
import re
import urllib.request

ws_dir = r"C:\Users\Admin\.gemini\antigravity-ide\scratch\quan_ly_thu_chi"
app_file = os.path.join(ws_dir, "02_MaNguon_ChuongTrinh", "app.py")
if not os.path.exists(app_file):
    app_file = os.path.join(ws_dir, "app.py")

print(f"Target Streamlit app file: {app_file}")

# 1. Start Streamlit process on port 8501
st_cmd = [sys.executable, "-m", "streamlit", "run", app_file, "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
print("Launching Streamlit Server on Port 8501...")
st_proc = subprocess.Popen(st_cmd, cwd=ws_dir)

# 2. Wait until localhost:8501 responds
started = False
for i in range(15):
    time.sleep(1)
    try:
        req = urllib.request.urlopen("http://localhost:8501", timeout=2)
        if req.status == 200:
            print(f"✅ Streamlit Server is LIVE on http://localhost:8501 after {i+1}s!")
            started = True
            break
    except Exception:
        pass

if not started:
    print("Warning: Streamlit server check timed out, attempting tunnel anyway...")

# 3. Launch Cloudflare Tunnel
cf_exe = os.path.join(ws_dir, "cloudflared.exe")
cf_cmd = [cf_exe, "tunnel", "--url", "http://localhost:8501"]
print("Establishing Fast Cloudflare HTTPS Tunnel...")
cf_proc = subprocess.Popen(cf_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=ws_dir)

url = None
for line in cf_proc.stderr:
    print(line.strip(), flush=True)
    m = re.search(r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com', line)
    if m:
        url = m.group(0)
        print(f"\n==========================================", flush=True)
        print(f"LIVE_FAST_URL: {url}", flush=True)
        print(f"==========================================\n", flush=True)
        break

try:
    cf_proc.wait()
except KeyboardInterrupt:
    st_proc.terminate()
    cf_proc.terminate()
