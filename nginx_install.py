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
# Obter a versão do sistema usando lsb_release e salvar em uma variável


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
version: "3"
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '443:443'
      - '81:81'
    environment:
      DB_MYSQL_HOST: "db"
      DB_MYSQL_PORT: 3306
      DB_MYSQL_USER: "nginxproxy"
      DB_MYSQL_PASSWORD: "#Ck8412@"
      DB_MYSQL_NAME: "nginxproxy"
      DISABLE_IPV6: 'true'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
    depends_on:
      - db

  db:
    image: 'jc21/mariadb-aria:latest'
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: '#Ck8412@'
      MYSQL_DATABASE: 'nginxproxy'
      MYSQL_USER: 'nginxproxy'
      MYSQL_PASSWORD: '#Ck8412@'
    volumes:
      - ./data/mysql:/var/lib/mysql
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
print(f"Acesse o host pela URL http://{ip_address}:81")
