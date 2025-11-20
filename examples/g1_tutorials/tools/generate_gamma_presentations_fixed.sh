#!/bin/bash

# Generate Gamma presentations for all G1 Robot Tutorial lessons
echo "=== G1 Robot Tutorial Gamma Presentation Generator ==="
echo "Generating curl commands for all lesson README files..."
echo ""

# Base directory for tutorials
BASE_DIR="/Users/wwhs-research/Downloads/humsim/loco-mujoco/examples/g1_tutorials"

# Gamma API configuration
API_URL="https://public-api.gamma.app/v0.2/generations"
API_KEY="sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw"

# Function to generate curl command for a lesson
generate_curl() {
    local file="$1"
    local title="$2"
    local full_path="$BASE_DIR/$file"
    
    if [[ -f "$full_path" ]]; then
        echo "# =================================================================="
        echo "# Lesson: $title"
        echo "# File: $file"
        echo "# =================================================================="
        echo ""
        
        # Read file content and escape for JSON
        content=$(cat "$full_path" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | awk '{printf "%s\\n", $0}')
        
        echo "curl --request POST \\"
        echo "  --url $API_URL \\"
        echo "  --header 'Content-Type: application/json' \\"
        echo "  --header \"X-API-KEY: $API_KEY\" \\"
        echo "  --data '{"
        echo "    \"inputText\": \"$content\","
        echo "    \"textMode\": \"generate\","
        echo "    \"format\": \"document\","
        echo "    \"themeName\": \"robostore\","
        echo "    \"cardSplit\": \"auto\","
        echo "    \"numCards\": 8,"
        echo "    \"additionalInstructions\": \"Create a comprehensive robotics tutorial presentation for $title. Include clear learning objectives, step-by-step instructions, technical diagrams, code examples, and practical exercises. Use a professional technical documentation style suitable for robotics education.\","
        echo "    \"exportAs\": \"pdf\","
        echo "    \"textOptions\": {"
        echo "      \"language\": \"en\""
        echo "    },"
        echo "    \"sharingOptions\": {"
        echo "      \"isPublic\": false,"
        echo "      \"title\": \"G1 Robot Tutorial: $title\""
        echo "    }"
        echo "  }'"
        echo ""
        echo ""
    else
        echo "# WARNING: File not found: $file"
        echo ""
    fi
}

# Generate commands for each lesson
echo "Generating individual curl commands..."
echo ""

generate_curl "lesson_1_0_setup_README.md" "1.0 Setup & Installation Guide"
generate_curl "lesson_1_1_README.md" "1.1 Quick System Test"
generate_curl "lesson_1_2_README.md" "1.2 Simple Walk Demo"
generate_curl "lesson_1_3_README.md" "1.3 Basic Datasets"
generate_curl "lesson_1_4_README.md" "1.4 LAFAN1 Datasets"
generate_curl "lesson_1_5_README.md" "1.5 Interactive Control"
generate_curl "lesson_1_6_README.md" "1.6 Motion Analysis"
generate_curl "lesson_1_7_README.md" "1.7 Dataset Explorer"
generate_curl "lesson_1_8_README.md" "1.8 Test Utilities"
generate_curl "lesson_1_9_README.md" "1.9 Slow Motion Viewer"
generate_curl "lesson_1_10_README.md" "1.10 Complete Summary"

echo "=== All curl commands generated ==="
echo ""
echo "To use these commands:"
echo "1. Copy each curl command block"
echo "2. Run in terminal to generate Gamma presentation"
echo "3. Check response for presentation URL"
echo "4. Download PDF when generation completes"