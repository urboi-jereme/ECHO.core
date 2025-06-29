#!/bin/bash

echo -e "\n🔧 \033[1;34mSetting up ECHO.Core environment...\033[0m"

# Ensure we're in the project root
cd "$(dirname "$0")"

# Install system packages
echo -e "\n📦 \033[1;33mInstalling system dependencies...\033[0m"
sudo apt update && sudo apt install -y \
  python3 python3-venv python3-pip git \
  build-essential libffi-dev libssl-dev

# Create Python virtual environment
if [ ! -d ".venv" ]; then
  echo -e "\n🐍 \033[1;32mCreating virtual environment...\033[0m"
  python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Ensure pip is up to date
echo -e "\n📦 \033[1;33mUpgrading pip...\033[0m"
pip install --upgrade pip

# Create requirements.txt if missing
if [ ! -f requirements.txt ]; then
  echo -e "\n⚠️ \033[1;31mrequirements.txt not found. Creating a default one...\033[0m"
  cat <<EOF > requirements.txt
pyyaml
rich
jupyter
pandas
matplotlib
ipykernel
EOF
fi

# Install Python dependencies
echo -e "\n📚 \033[1;34mInstalling Python dependencies...\033[0m"
pip install -r requirements.txt

# Summary
echo -e "\n✅ \033[1;32mECHO.Core environment setup complete.\033[0m"
echo -e "🔁 Run \033[1;36msource .venv/bin/activate\033[0m to activate the environment."
echo -e "🚀 To launch, try \033[1;36mpython3 echo_main.py\033[0m or \033[1;36mjupyter notebook\033[0m."
