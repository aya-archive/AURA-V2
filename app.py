# A.U.R.A (Adaptive User Retention Assistant) - Hugging Face Spaces Entry Point
# This is the main entry point for Hugging Face Spaces deployment
# It imports and runs the complete AURA Gradio application

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main AURA Gradio application
from aura_gradio_app import *

# The app is automatically launched by Hugging Face Spaces
# No additional code needed - the Gradio app will start automatically
