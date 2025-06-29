#!/bin/bash

echo "🔧 Setting up ECHO.Core environment..."

# Ensure we're in the project root
cd "$(dirname "$0")"

# Install required system packages
echo "📦 Updating and installing system packages..."
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git

# Create Python virtual environment if not already present
if [ ! -d ".venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
if [ ! -f requirements.txt ]; then
  echo "⚠️ requirements.txt not found. Creating one with basics..."
  echo -e "pyyaml\nrich\npandas" > requirements.txt
fi
pip install -r requirements.txt

echo "🔍 Validating and scaffolding required YAML files..."

# List of required YAML files and optional headers
declare -A yaml_templates=(
  ["memory/ECHO_MEMORY.yaml"]="# echo_memory: []"
  ["memory/MOTIF_PRESSURE.yaml"]="# motif_pressure: {}"
  ["memory/AGENT_STATE.yaml"]="# agent_state: {}"
  ["memory/GOALS.yaml"]="# goals: []"
  ["memory/META_PREFERENCES.yaml"]="# meta_preferences: {}"
  ["memory/RECURSIVE_ALIGNMENTS.yaml"]="# recursive_alignments: []"
)

missing_any=false

# Check each file, report status, and optionally create it
for file in "${!yaml_templates[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing: $file"
    echo "📄 Creating placeholder..."
    mkdir -p "$(dirname "$file")"
    echo -e "${yaml_templates[$file]}" > "$file"
    missing_any=true
  else
    echo "✅ Found: $file"
  fi
done

if [ "$missing_any" = true ]; then
  echo "⚠️  Some YAML files were missing and have been created as placeholders."
else
  echo "🎉 All required YAML files are present."
fi

# Optional: Basic YAML syntax validation using Python
echo "🧪 Validating YAML syntax..."
for file in "${!yaml_templates[@]}"; do
  python3 -c "import yaml, sys; yaml.safe_load(open('$file'))" 2>/dev/null
  if [ $? -eq 0 ]; then
    echo "✅ YAML OK: $file"
  else
    echo "❌ YAML SYNTAX ERROR in $file"
  fi
done

# Git status summary (optional)
if git rev-parse --git-dir > /dev/null 2>&1; then
  echo "📍 Git status:"
  git status -s
fi

echo "✅ ECHO.Core environment setup complete."
echo "👉 To activate the environment in the future, run: source .venv/bin/activate"
