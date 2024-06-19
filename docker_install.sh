#!/bin/bash

# Log file
LOGFILE="install_docker_compose.log"

# Function to log messages
log() {
  echo "[*] $1" | tee -a $LOGFILE
}

# Function to check the operating system
check_os() {
  log "Checking operating system version..."
  
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [[ -f /etc/os-release ]]; then
      . /etc/os-release
      OS=$ID
      log "Detected Linux distribution: $NAME"
      
      case "$OS" in
        debian|ubuntu|kali)
          log "The operating system is Debian-based."
          ;;
        arch)
          log "The operating system is Arch-based."
          ;;
        *)
          log "The operating system is Linux-based but not specifically detected."
          ;;
      esac
    else
      log "The operating system is Linux-based but /etc/os-release is not found."
    fi
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    log "The operating system is macOS."
    OS="macos"
  elif [[ "$OSTYPE" == "cygwin" ]]; then
    log "The operating system is Windows (Cygwin)."
    OS="windows"
  elif [[ "$OSTYPE" == "msys" ]]; then
    log "The operating system is Windows (MSYS)."
    OS="windows"
  elif [[ "$OSTYPE" == "win32" ]]; then
    log "The operating system is Windows."
    OS="windows"
  else
    log "The operating system could not be detected."
    OS="unknown"
  fi
}

# Function to check and install Docker on Debian-based systems
install_docker_debian() {
  log "Checking Docker installation on Debian-based system..."
  if ! command -v docker &> /dev/null; then
    log "Docker is not installed. Installing Docker..."
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    log "Docker installed successfully."
  else
    log "Docker is already installed."
  fi
}

# Function to check and install Docker Compose on Debian-based systems
install_docker_compose_debian() {
  log "Checking Docker Compose installation on Debian-based system..."
  if ! command -v docker-compose &> /dev/null; then
    log "Docker Compose is not installed. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    log "Docker Compose installed successfully."
  else
    log "Docker Compose is already installed."
  fi
}

# Main function to check OS and install Docker and Docker Compose
main() {
  log "=============================================================================================="
  log "Starting Docker and Docker Compose installation"
  log "=============================================================================================="
  
  OS=$(check_os)
  log "Detected OS: $OS"
  
  if [[ "$OS" == "debian" || "$OS" == "ubuntu" || "$OS" == "kali" ]]; then
    install_docker_debian
    install_docker_compose_debian
  else
    log "Docker installation script is only configured for Debian-based systems."
  fi
  
  log "=============================================================================================="
  log "Installation process completed successfully"
  log "=============================================================================================="
}

# Run the main function
main