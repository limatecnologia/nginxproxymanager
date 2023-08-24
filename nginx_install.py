import os
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print("Instalação do nginxproxymanager")
print("")
print("Primeiro vamos dar um update nessa merda né?!")
print("")
os.system("apt update")
print("")
print("Agora vamos atualizar essa bosta...")
print("")
os.system("apt upgrade -y")
print("")
print("E bora lá")
print("")
print("Instalação do Docker")
os.system("apt install ca-certificates curl gnupg2 apt-transport-https lsb-release -y")
os.system("curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -")
release_codename = os.popen("cat /etc/os-release | grep VERSION= | cut -d'(' -f2 | cut -d')' -f1").read().strip()
os.system(f"echo 'deb https://download.docker.com/linux/debian {release_codename} stable' > /etc/apt/sources.list.d/docker.list")
os.system("apt update")
os.system("apt install docker-ce docker-ce-cli containerd.io -y")
print("Instalação do Docker Compose")
os.system("curl -L https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose")
os.system("chmod +x /usr/local/bin/docker-compose")
os.system("ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose")
print("Criando as pastas...")
os.system("mkdir /etc/nginx-proxy")
os.system("mkdir /etc/nginx-proxy/{data,letsencrypt}")
print("")
print("Criando arquivo docker-compose.yml")
print("")
# Criar ou atualizar arquivo docker-compose.yml
compose_content = """
version: '3.8'
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      # These ports are in format <host-port>:<container-port>
      - '80:80' # Public HTTP Port
      - '443:443' # Public HTTPS Port
      - '81:81' # Admin Web Port
      # Add any other Stream port you want to expose
      # - '21:21' # FTP

    # Uncomment the next line if you uncomment anything in the section
    # environment:
      # Uncomment this if you want to change the location of
      # the SQLite DB file within the container
      # DB_SQLITE_FILE: "/data/database.sqlite"

      # Uncomment this if IPv6 is not enabled on your host
      DISABLE_IPV6: 'true'

    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
"""
compose_file_path = "/etc/nginx-proxy/docker-compose.yml"
with open(compose_file_path, "w") as compose_file:
    compose_file.write(compose_content)
# Executar o docker-compose
print("Executando o docker-compose")
os.chdir("/etc/nginx-proxy")
os.system("docker-compose up -d")
print("")
print("Instalação finalizada!")
sleep 5
print("")
print("Aguenta aí que vou reiniciar a parada hehehehe!")
os.system("reboot now")
#print(f"Acesse o host pela URL http://{ip_address}:81")
