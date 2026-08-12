import subprocess
import time
import sys
import os

app_file = r'02_MaNguon_ChuongTrinh\app.py' if os.path.exists(r'02_MaNguon_ChuongTrinh\app.py') else 'app.py'
print(f"Starting Streamlit app: {app_file} on port 8501...")

# 1. Start Streamlit headless background process
st_cmd = [sys.executable, '-m', 'streamlit', 'run', app_file, '--server.port=8501', '--server.address=0.0.0.0', '--server.headless=true']
st_proc = subprocess.Popen(st_cmd)
time.sleep(3)

# 2. Start Localtunnel background process
lt_cmd = 'npx --yes localtunnel --port 8501'
print("Establishing Public HTTPS Tunnel...")
lt_proc = subprocess.Popen(lt_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 3. Read and print Public URL
for line in lt_proc.stdout:
    print(line.strip(), flush=True)
    if 'your url is:' in line:
        url = line.strip().split('your url is: ')[-1]
        print(f"\n==========================================", flush=True)
        print(f"PUBLIC_URL: {url}", flush=True)
        print(f"==========================================\n", flush=True)
        break

# Keep running as long-running tunnel daemon
try:
    lt_proc.wait()
except KeyboardInterrupt:
    st_proc.terminate()
    lt_proc.terminate()
