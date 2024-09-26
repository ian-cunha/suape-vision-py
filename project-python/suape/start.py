import subprocess

# Rodar o primeiro script
process1 = subprocess.Popen(['python3', 'images/images.py'])

# Rodar o segundo script
process2 = subprocess.Popen(['python3', 'getContainers/video.py'])

# Espera ambos os processos terminarem
process1.wait()
process2.wait()

print("Ambos os scripts foram executados.")