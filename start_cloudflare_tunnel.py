import subprocess
import time
import sys
import os
import re

app_file = r'02_MaNguon_ChuongTrinh\app.py' if os.path.exists(r'02_MaNguon_ChuongTrinh\app.py') else 'app.py'
print(f"Starting Streamlit app: {app_file} on port 8501...")

# 1. Start Streamlit headless background process
st_cmd = [sys.executable, '-m', 'streamlit', 'run', app_file, '--server.port=8501', '--server.address=0.0.0.0', '--server.headless=true']
st_proc = subprocess.Popen(st_cmd)
time.sleep(3)

# 2. Start Cloudflare Tunnel
cf_cmd = ['./cloudflared.exe', 'tunnel', '--url', 'http://localhost:8501']
print("Establishing Direct Cloudflare HTTPS Tunnel...")
cf_proc = subprocess.Popen(cf_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 3. Read and print Public Direct URL
url = None
for line in cf_proc.stderr:
    print(line.strip(), flush=True)
    m = re.search(r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com', line)
    if m:
        url = m.group(0)
        print(f"\n==========================================", flush=True)
        print(f"DIRECT_CLOUDFLARE_URL: {url}", flush=True)
        print(f"==========================================\n", flush=True)
        break

# Keep running as long-running tunnel daemon
try:
    cf_proc.wait()
except KeyboardInterrupt:
    st_proc.terminate()
    cf_proc.terminate()
