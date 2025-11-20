#!/bin/bash

# Generate Gamma presentations for all G1 Robot Tutorial lessons
# This script creates curl commands for each lesson README file

# Base directory for tutorials
BASE_DIR="/Users/wwhs-research/Downloads/humsim/loco-mujoco/examples/g1_tutorials"

# Gamma API configuration
API_URL="https://public-api.gamma.app/v0.2/generations"
API_KEY="sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw"

echo "=== G1 Robot Tutorial Gamma Presentation Generator ==="
echo "Generating curl commands for all lesson README files..."
echo ""

# Array of lesson titles and files
declare -A lessons=(
    ["lesson_1_0_setup_README.md"]="1.0 Setup & Installation Guide"
    ["lesson_1_1_README.md"]="1.1 Quick System Test"
    ["lesson_1_2_README.md"]="1.2 Simple Walk Demo"
    ["lesson_1_3_README.md"]="1.3 Basic Datasets"
    ["lesson_1_4_README.md"]="1.4 LAFAN1 Datasets"
    ["lesson_1_5_README.md"]="1.5 Interactive Control"
    ["lesson_1_6_README.md"]="1.6 Motion Analysis"
    ["lesson_1_7_README.md"]="1.7 Dataset Explorer"
    ["lesson_1_8_README.md"]="1.8 Test Utilities"
    ["lesson_1_9_README.md"]="1.9 Slow Motion Viewer"
    ["lesson_1_10_README.md"]="1.10 Complete Summary"
)

# Function to generate curl command for a lesson
generate_curl_command() {
    local file="$1"
    local title="$2"
    local full_path="$BASE_DIR/$file"
    
    echo "# Generating Gamma presentation for: $title"
    echo "# File: $file"
    echo ""
    
    cat << EOF
curl --request POST \\
  --url $API_URL \\
  --header 'Content-Type: application/json' \\
  --header "X-API-KEY: $API_KEY" \\
  --data '{
    "inputText": "'"$(cat "$full_path" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')"'",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "additionalInstructions": "Create a comprehensive robotics tutorial presentation for \"$title\". Include clear learning objectives, step-by-step instructions, technical diagrams, code examples, and practical exercises. Use a professional technical documentation style suitable for robotics education.",
    "exportAs": "pdf",
    "textOptions": {
      "language": "en"
    },
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: $title"
    }
  }'

EOF
    echo ""
    echo "# -------------------------------------------------------------------"
    echo ""
}

# Generate commands for each lesson
echo "Generating curl commands for all lessons..."
echo ""

for file in "${!lessons[@]}"; do
    if [[ -f "$BASE_DIR/$file" ]]; then
        generate_curl_command "$file" "${lessons[$file]}"
    else
        echo "# WARNING: File not found: $file"
        echo ""
    fi
done

echo "=== All curl commands generated ==="
echo ""
echo "To use these commands:"
echo "1. Copy each curl command block"
echo "2. Run in terminal to generate Gamma presentation"
echo "3. Check response for presentation URL"
echo "4. Download PDF when generation completes"