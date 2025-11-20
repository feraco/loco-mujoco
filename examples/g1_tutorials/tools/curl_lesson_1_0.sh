#!/bin/bash

curl --request POST \
  --url https://public-api.gamma.app/v0.2/generations \
  --header 'Content-Type: application/json' \
  --header "X-API-KEY: sk-gamma-H4jVB1MNCnZsUEqtOkfQEEBvgOIefhv8oTRc61Vw" \
  --data @- << 'EOF'
{
  "inputText": "# Lesson 1.0: Setup and Installation\n\n## Learning Objectives\n\nBy the end of this lesson, you will:\n- Install LocoMuJoCo framework with all dependencies\n- Set up proper Python environment for robotics development\n- Verify installation with system diagnostics\n- Configure dataset caching for optimal performance\n- Prepare development environment for G1 robot tutorials\n\n## What You'll Do\n\n1. **Install LocoMuJoCo and dependencies**\n2. **Set up Python environment (conda/venv/uv)**\n3. **Run installation verification tests**\n4. **Configure dataset caching system**\n5. **Prepare for Unit 1 tutorial series**\n\n## Prerequisites\n\n- macOS, Linux, or Windows system\n- Python 3.8-3.11 installed\n- Git for version control\n- Basic command line familiarity\n\n## Step-by-Step Instructions\n\n### Step 1: Environment Setup\n\n#### Option A: Conda Environment (Recommended)\n```bash\n# Create new conda environment\nconda create -n loco-mujoco python=3.10\nconda activate loco-mujoco\n\n# Verify Python version\npython --version  # Should show Python 3.10.x\n```\n\n#### Option B: Virtual Environment\n```bash\n# Create virtual environment\npython -m venv loco-mujoco-env\n\n# Activate environment\n# On macOS/Linux:\nsource loco-mujoco-env/bin/activate\n# On Windows:\nloco-mujoco-env\\Scripts\\activate\n```\n\n#### Option C: UV Environment (Modern)\n```bash\n# Install uv if not already installed\npip install uv\n\n# Create and activate environment\nuv venv loco-mujoco-env\nsource loco-mujoco-env/bin/activate  # macOS/Linux\n# or: loco-mujoco-env\\Scripts\\activate  # Windows\n```\n\n### Step 2: Install LocoMuJoCo\n\n#### Core Installation\n```bash\n# Install from PyPI\npip install loco-mujoco\n\n# Verify installation\npython -c \"import loco_mujoco; print(f'LocoMuJoCo v{loco_mujoco.__version__} installed successfully')\"\n```\n\n**Expected output:**\n```\nLocoMuJoCo v1.0.1 installed successfully\n```\n\n#### Install Additional Dependencies\n```bash\n# Install visualization and analysis tools\npip install matplotlib seaborn pandas numpy\n\n# Install Jupyter for interactive development (optional)\npip install jupyter notebook ipykernel\n\n# Install development tools (optional)\npip install pytest black isort\n```\n\n### Step 3: Verify Installation\n\n#### Basic Import Test\n```bash\npython -c \"\nimport loco_mujoco\nfrom loco_mujoco import RLFactory, ImitationFactory\nfrom loco_mujoco.datasets import DefaultDatasetConf\nprint('All imports successful!')\n\"\n```\n\n## Key Installation Points\n\n- **Environment Management**: Use conda, venv, or uv for isolation\n- **Version Compatibility**: Python 3.8-3.11 supported\n- **Dependency Resolution**: Install all required packages\n- **System Verification**: Test imports and basic functionality\n- **Performance Setup**: Configure caching for optimal speed\n\n## Troubleshooting\n\n### Common Issues:\n- **Permission Errors**: Use --user flag or fix permissions\n- **Version Conflicts**: Create fresh environment\n- **Graphics Issues**: Install OpenGL dependencies\n- **Cache Problems**: Set up datasets on-demand initially\n\n## What's Next\n\nWith successful installation:\n- **Lesson 1.1**: Quick system verification test\n- **Lesson 1.2**: First robot walking demonstration\n- **Complete Unit 1**: Master fundamental robotics concepts\n\n**A solid foundation enables advanced robotics exploration!**",
  "textMode": "generate",
  "format": "document",
  "themeName": "robostore",
  "cardSplit": "auto", 
  "numCards": 8,
  "additionalInstructions": "Create a comprehensive robotics tutorial presentation for 1.0 Setup and Installation. Include clear learning objectives, step-by-step instructions, and practical setup guidance. Use a professional technical documentation style suitable for robotics education.",
  "exportAs": "pdf",
  "textOptions": {
    "language": "en"
  },
  "sharingOptions": {
    "isPublic": false,
    "title": "G1 Robot Tutorial: 1.0 Setup and Installation"
  }
}
EOF