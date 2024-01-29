import platform

print(platform.system())  # Sistema operacional
print(platform.release())  # Versão do sistema operacional
print(platform.machine())  # Arquitetura da máquina
print(platform.processor())  # Processador
print(platform.architecture())  # Arquitetura do processador


import wmi

# Conectando ao serviço Windows Management Instrumentation (WMI)
c = wmi.WMI()

# Obtendo o número de série do sistema
for system in c.Win32_ComputerSystem():
    print("Número de Série do Computador (Windows):", system)



