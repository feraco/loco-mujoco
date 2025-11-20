# Gamma Presentation Generation Commands

This document contains simplified curl commands to generate Gamma presentations for all G1 Robot Tutorial lessons.

## Setup

Make sure you have the Gamma API key available. Each command creates a professional presentation from the lesson README content.

## Commands

### Lesson 1.0: Setup and Installation

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Setup and Installation\n\nLearn to install LocoMuJoCo framework, set up Python environments, and configure your system for robotics development. Includes troubleshooting guides and performance optimization.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore", 
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.0 Setup and Installation"
    }
  }'
```

### Lesson 1.1: Quick Test

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Quick System Test\n\nVerify your LocoMuJoCo installation with comprehensive system diagnostics. Test robot models, performance benchmarks, and graphics capabilities to ensure everything is working correctly.",
    "textMode": "generate",
    "format": "document", 
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.1 Quick Test"
    }
  }'
```

### Lesson 1.2: Simple Walk Test

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Simple Walk Test\n\nExperience your first robot walking simulation. Learn about trajectory playback, physics simulation, and basic robot control while watching the G1 robot perform natural walking motions.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto", 
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.2 Simple Walk Test"
    }
  }'
```

### Lesson 1.3: Basic Datasets

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Basic Datasets\n\nExplore built-in motion datasets including walking, running, sitting, and squatting. Learn dataset structure, trajectory sampling, and how to work with different motion types for robotics research.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8, 
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.3 Basic Datasets"
    }
  }'
```

### Lesson 1.4: LAFAN1 Datasets

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: LAFAN1 Datasets\n\nWork with professional motion capture data from the LAFAN1 dataset. Learn advanced motion analysis techniques, dataset comparison, and how to use high-quality human motion data for robotics.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf", 
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.4 LAFAN1 Datasets"
    }
  }'
```

### Lesson 1.5: Interactive Control

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Interactive Control\n\nTake direct control of the G1 robot with real-time keyboard input. Learn joint-level control, safety mechanisms, and human-robot interaction while controlling the robot in real-time.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.5 Interactive Control"
    }
  }'
```

### Lesson 1.6: Motion Analysis

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Motion Analysis\n\nAnalyze robot motion with live data visualization. Learn scientific motion analysis, biomechanical metrics, and real-time data collection while observing joint positions, velocities, and energy dynamics.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.6 Motion Analysis"
    }
  }'
```

### Lesson 1.7: Dataset Explorer

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Dataset Explorer\n\nNavigate large motion dataset collections systematically. Learn to filter, search, and compare motion data while exploring advanced dataset organization and metadata systems.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore", 
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.7 Dataset Explorer"
    }
  }'
```

### Lesson 1.8: Test Utilities

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Test Utilities\n\nRun comprehensive automated testing suites for robot systems. Learn professional validation methods, debugging techniques, and systematic testing approaches for robotics research projects.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false, 
      "title": "G1 Robot Tutorial: 1.8 Test Utilities"
    }
  }'
```

### Lesson 1.9: Slow Motion Viewer

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Slow Motion Viewer\n\nAnalyze robot motion frame-by-frame in slow motion. Learn precision motion analysis techniques, biomechanical movement patterns, and detailed motion debugging methods.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.9 Slow Motion Viewer"
    }
  }'
```

### Lesson 1.10: Complete Summary

```bash
curl -X POST "https://public-api.gamma.app/v0.2/generations" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  -d '{
    "inputText": "G1 Robot Tutorial: Complete Summary\n\nReview and consolidate all Unit 1 tutorial concepts. Complete comprehensive skills assessment, demonstrate mastery of fundamental robotics skills, and graduate to advanced topics.",
    "textMode": "generate",
    "format": "document",
    "themeName": "robostore",
    "cardSplit": "auto",
    "numCards": 8,
    "exportAs": "pdf",
    "sharingOptions": {
      "isPublic": false,
      "title": "G1 Robot Tutorial: 1.10 Complete Summary"
    }
  }'
```

## Usage Instructions

1. **Copy any command** from above
2. **Paste into terminal** and press Enter
3. **Check the response** for:
   - Success message with generation ID
   - Presentation URL for viewing
   - Any error messages
4. **Visit the URL** to view/download the presentation
5. **Export as PDF** once generation completes

## Expected Response Format

```json
{
  "id": "generation_id_here",
  "status": "generating",
  "url": "https://gamma.app/docs/presentation_url_here"
}
```

## Notes

- Each command creates a professional 8-slide presentation
- Uses "robostore" theme optimized for technical content
- Presentations are private by default
- PDF export is automatically configured
- Generation typically takes 30-60 seconds per presentation

## Troubleshooting

If a command fails:
1. Check internet connection
2. Verify API key is correct
3. Ensure proper JSON formatting
4. Try running individual commands
5. Check Gamma API status if multiple failures occur