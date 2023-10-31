import subprocess

PORT = "4444"

scripts = ["./war-client.py",
           "./war-client.py"]

processes = []
command = ["python", "./war-server.py", PORT]
processes.append(subprocess.Popen(command))
for script in scripts:
    command = ["python", script, "127.0.0.1", PORT]
    processes.append(subprocess.Popen(command))

for process in processes:
    process.wait()
