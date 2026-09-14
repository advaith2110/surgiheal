import subprocess
import sys
import time
import webbrowser
import os
import re

def main():
    print("\n" + "=" * 60)
    print("   🩺 SurgiHeal: Launching Live Demo & Public Tunnel...")
    print("=" * 60 + "\n")

    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # 1. Start Streamlit Server
    print("⏳ [1/3] Starting Streamlit Web Engine on http://127.0.0.1:8501...")
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.address", "127.0.0.1",
        "--server.port", "8501",
        "--server.headless", "true"
    ]
    streamlit_proc = subprocess.Popen(
        streamlit_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for Streamlit to initialize
    time.sleep(3)

    # 2. Start SSH Public Tunnel
    print("⏳ [2/3] Establishing secure public HTTPS tunnel for judges...")
    tunnel_cmd = [
        "ssh", "-R", "80:127.0.0.1:8501",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "nokey@localhost.run"
    ]
    tunnel_proc = subprocess.Popen(
        tunnel_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    public_url = None
    start_time = time.time()

    # Read output to capture public URL
    print("⏳ [3/3] Acquiring public link...")
    while time.time() - start_time < 15:
        line = tunnel_proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        # Look for *.lhr.life or https:// in output
        match = re.search(r'(https://[a-zA-Z0-9\.\-]+\.lhr\.life)', line)
        if match:
            public_url = match.group(1)
            break

    # 3. Open Browser to Localhost
    webbrowser.open("http://127.0.0.1:8501")

    # Display Banner
    print("\n" + "=" * 60)
    print("   🎉 SURGIHEAL DEMO IS LIVE & READY FOR JUDGES!")
    print("=" * 60)
    print("   💻 Local Demo URL:   http://127.0.0.1:8501")
    if public_url:
        print(f"   🌐 Public HTTPS URL: {public_url}")
        print("      (Share this link with judges, mentors, or on your phone)")
    else:
        print("   🌐 Public Tunnel: Running in background (connecting...)")
    print("=" * 60)
    print("   👉 Browser opened automatically.")
    print("   🛑 Press Ctrl + C in this window anytime to STOP the demo.")
    print("=" * 60 + "\n")

    try:
        while True:
            time.sleep(1)
            # Check if streamlit is still running
            if streamlit_proc.poll() is not None:
                print("Streamlit process ended.")
                break
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping demo servers...")
    finally:
        streamlit_proc.terminate()
        tunnel_proc.terminate()
        time.sleep(1)
        print("✅ Demo shut down cleanly. System resources freed!\n")

if __name__ == "__main__":
    main()
