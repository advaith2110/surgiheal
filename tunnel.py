import subprocess
import re
import time
import sys

def run_tunnel():
    print("Starting secure public HTTPS tunnel...", flush=True)
    cmd = [
        "ssh", "-R", "80:localhost:8501",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "nokey@localhost.run"
    ]
    while True:
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in iter(proc.stdout.readline, ''):
                print(line, end="", flush=True)
                match = re.search(r'(https://[a-zA-Z0-9\.\-]+\.lhr\.life)', line)
                if match:
                    url = match.group(1)
                    print(f"\n>>> PUBLIC_URL_READY: {url} <<<\n", flush=True)
            proc.wait()
        except Exception as e:
            print(f"Tunnel error: {e}", flush=True)
        print("Reconnecting tunnel in 3 seconds...", flush=True)
        time.sleep(3)

if __name__ == "__main__":
    run_tunnel()
