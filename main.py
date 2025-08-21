# ==============================================================================
# 🎯 Placement Cell - Company Information & Video Generator
#
# Description:
# This Streamlit application automates the process of extracting placement
# information from company emails, researching the company using the Gemini AI,
# and generating a professional, short-form video for student preparation.
#
# Setup:
# 1. Install required packages:
#    pip install streamlit google-generativeai pywhatkit moviepy==1.0.3 pillow gtts matplotlib requests python-dotenv pydub
#
# 2. Create a `.env` file in the same directory with your credentials:
#    GEMINI_API_KEY="your_google_gemini_api_key"
#    WHATSAPP_PHONE="+91xxxxxxxxxx"
# ==============================================================================

import base64
import os
import re
import tempfile
import logging
from datetime import datetime, timedelta
from io import BytesIO

import google.generativeai as genai
import pywhatkit as kit
import requests
import streamlit as st
from dotenv import load_dotenv

# Enhanced imports for professional video production
try:
    from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips, 
    CompositeVideoClip, VideoFileClip, TextClip, ColorClip
)
# Replace these imports
    from moviepy.video.fx.fadein import fadein
    from moviepy.video.fx.fadeout import fadeout
    from moviepy.audio.fx.volumex import volumex
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import matplotlib.pyplot as plt
    from gtts import gTTS
    from pydub import AudioSegment
    import threading
    from pathlib import Path
    from typing import List, Dict, Optional, Tuple, Any
    from dataclasses import dataclass
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    import json
    VIDEO_LIBS_AVAILABLE = True
except ImportError:
    VIDEO_LIBS_AVAILABLE = False
    st.error("⚠️ Required libraries not installed. Run: pip install moviepy pillow gtts matplotlib pydub")

# Load environment variables from .env file
load_dotenv()

print(f"GEMINI_API_KEY from .env: {os.getenv('GEMINI_API_KEY')}")
print(f"WHATSAPP_PHONE from .env: {os.getenv('WHATSAPP_PHONE')}")

@dataclass
class VideoConfig:
    """Professional video configuration"""
    resolution: Tuple[int, int] = (1920, 1080)  # Full HD
    fps: int = 30
    video_codec: str = 'libx264'
    audio_codec: str = 'aac'
    preset: str = 'medium'
    crf: int = 23  # Constant Rate Factor for quality
    max_slide_duration: float = 20.0
    min_slide_duration: float = 3.0
    fade_duration: float = 0.5
    background_music: bool = False
    watermark: bool = True
    subtitle_support: bool = True

@dataclass 
class SlideMetrics:
    """Track video generation metrics"""
    total_slides: int = 0
    processed_slides: int = 0
    failed_slides: int = 0
    total_duration: float = 0.0
    file_size_mb: float = 0.0
    generation_time: float = 0.0

class AdvancedVideoGenerator:
    """Professional-grade video generator for placement presentations"""
    
    def __init__(self, config: VideoConfig = None):
        self.config = config or VideoConfig()
        self.metrics = SlideMetrics()
        self.temp_files = []
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup professional logging"""
        logger = logging.getLogger('PlacementVideoGenerator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                self.logger.warning(f"Failed to cleanup {temp_file}: {e}")
        self.temp_files.clear()

    def _create_enhanced_slide(self, slide: Dict, template: str, slide_num: int, 
                             total_slides: int, company_logo: Any = None) -> Image.Image:
        """Create visually stunning slides with professional design"""
        width, height = self.config.resolution
        
        # Create base image with gradient background
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Professional gradient background
        if template == 'corporate':
            self._apply_corporate_template(img, draw, width, height)
        elif template == 'modern':
            self._apply_modern_template(img, draw, width, height)
        elif template == 'minimalist':
            self._apply_minimalist_template(img, draw, width, height)
        else:
            self._apply_default_template(img, draw, width, height)
        
        # Add company logo with proper positioning
        if company_logo:
            self._add_company_logo(img, company_logo, width, height)
        
        # Add slide content with smart text wrapping
        self._add_slide_content(img, draw, slide, width, height)
        
        # Add slide number and progress indicator
        self._add_slide_metadata(img, draw, slide_num, total_slides, width, height)
        
        # Apply professional effects
        img = self._apply_visual_effects(img, template)
        
        return img

    def _apply_corporate_template(self, img: Image.Image, draw: ImageDraw.Draw, 
                                width: int, height: int):
        """Apply corporate template with professional blue gradient"""
        # Create gradient from dark blue to light blue
        for y in range(height):
            gradient_factor = y / height
            r = int(25 + (70 * gradient_factor))
            g = int(50 + (120 * gradient_factor))  
            b = int(100 + (155 * gradient_factor))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add subtle geometric patterns
        self._add_geometric_patterns(draw, width, height, (255, 255, 255, 30))

    def _apply_modern_template(self, img: Image.Image, draw: ImageDraw.Draw,
                             width: int, height: int):
        """Apply modern template with dynamic gradients"""
        # Multi-color gradient
        for y in range(height):
            factor = y / height
            r = int(45 + (155 * factor))
            g = int(25 + (200 * factor))
            b = int(85 + (170 * factor))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add modern accent lines
        accent_color = (255, 255, 255, 100)
        for i in range(0, width, 150):
            draw.line([(i, 0), (i + 100, height)], fill=accent_color, width=2)

    def _apply_minimalist_template(self, img: Image.Image, draw: ImageDraw.Draw,
                                 width: int, height: int):
        """Apply clean minimalist template"""
        # Clean white background with subtle accent
        draw.rectangle([(0, 0), (width, height)], fill=(248, 249, 250))
        
        # Minimal accent bar
        accent_height = height // 20
        draw.rectangle([(0, 0), (width, accent_height)], fill=(59, 130, 246))

    def _apply_default_template(self, img: Image.Image, draw: ImageDraw.Draw,
                              width: int, height: int):
        """Apply default professional template"""
        # Professional gray gradient
        for y in range(height):
            factor = y / height
            gray = int(240 - (40 * factor))
            draw.line([(0, y), (width, y)], fill=(gray, gray, gray))

    def _add_geometric_patterns(self, draw: ImageDraw.Draw, width: int, height: int, 
                              color: Tuple[int, int, int, int]):
        """Add subtle geometric patterns for visual interest"""
        # Add diagonal lines pattern
        spacing = 100
        for x in range(-height, width, spacing):
            draw.line([(x, 0), (x + height, height)], fill=color, width=1)

    def _add_company_logo(self, img: Image.Image, logo: Any, width: int, height: int):
        """Add company logo with proper scaling and positioning"""
        try:
            if isinstance(logo, str) and os.path.exists(logo):
                logo_img = Image.open(logo)
            elif hasattr(logo, 'save'):
                logo_img = logo
            else:
                return
            
            # Scale logo proportionally
            logo_size = min(width // 8, height // 8)
            logo_img = logo_img.convert('RGBA')
            logo_img.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Position logo in top-right corner
            logo_x = width - logo_img.width - 50
            logo_y = 50
            
            img.paste(logo_img, (logo_x, logo_y), logo_img)
            
        except Exception as e:
            self.logger.warning(f"Failed to add company logo: {e}")

    def _add_slide_content(self, img: Image.Image, draw: ImageDraw.Draw, 
                          slide: Dict, width: int, height: int):
        """Add slide content with intelligent text layout"""
        try:
            # Load professional fonts
            title_font = self._get_font('title', width)
            content_font = self._get_font('content', width)
            
            # Title positioning and styling
            title = slide.get('title', '').strip()
            if title:
                title_y = height // 6
                self._draw_text_with_shadow(draw, title, title_font, width, title_y, 
                                          'center', (255, 255, 255), (0, 0, 0, 128))
            
            # Content positioning with smart wrapping
            content = slide.get('content', '').strip()
            if content:
                content_y = height // 3
                content_lines = self._wrap_text(content, content_font, width - 200)
                
                for i, line in enumerate(content_lines):
                    line_y = content_y + (i * 80)
                    if line_y < height - 100:  # Ensure text stays within bounds
                        self._draw_text_with_shadow(draw, line, content_font, width, 
                                                  line_y, 'center', (255, 255, 255), 
                                                  (0, 0, 0, 100))
                        
        except Exception as e:
            self.logger.error(f"Failed to add slide content: {e}")

    def _get_font(self, font_type: str, width: int) -> ImageFont.FreeTypeFont:
        """Get appropriate font with size scaling"""
        base_size = width // 25 if font_type == 'title' else width // 35
        
        font_paths = [
            '/System/Library/Fonts/Arial.ttf',  # macOS
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
            'C:/Windows/Fonts/arial.ttf',  # Windows
        ]
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, base_size)
            except:
                continue
        
        # Fallback to default font
        return ImageFont.load_default()

    def _draw_text_with_shadow(self, draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
                             width: int, y: int, align: str, text_color: Tuple[int, int, int],
                             shadow_color: Tuple[int, int, int, int]):
        """Draw text with shadow effect for better readability"""
        # Calculate text positioning
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        if align == 'center':
            x = (width - text_width) // 2
        elif align == 'right':
            x = width - text_width - 50
        else:
            x = 50
        
        # Draw shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, 
                 fill=shadow_color[:3])
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Intelligent text wrapping for better readability"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Single word too long
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def _add_slide_metadata(self, img: Image.Image, draw: ImageDraw.Draw,
                           slide_num: int, total_slides: int, width: int, height: int):
        """Add slide number and progress indicator"""
        # Progress bar
        progress_width = width - 100
        progress_height = 8
        progress_x = 50
        progress_y = height - 60
        
        # Background progress bar
        draw.rectangle([(progress_x, progress_y), 
                       (progress_x + progress_width, progress_y + progress_height)],
                      fill=(200, 200, 200))
        
        # Filled progress
        fill_width = int((slide_num / total_slides) * progress_width)
        draw.rectangle([(progress_x, progress_y),
                       (progress_x + fill_width, progress_y + progress_height)],
                      fill=(59, 130, 246))
        
        # Slide number
        slide_text = f"{slide_num} / {total_slides}"
        font = self._get_font('content', width)
        draw.text((progress_x, progress_y - 30), slide_text, font=font, fill=(100, 100, 100))

    def _apply_visual_effects(self, img: Image.Image, template: str) -> Image.Image:
        """Apply professional visual effects"""
        try:
            # Subtle sharpening
            img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            
            # Slight contrast enhancement
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.05)
            
            # Color enhancement for modern template
            if template == 'modern':
                color_enhancer = ImageEnhance.Color(img)
                img = color_enhancer.enhance(1.1)
                
        except Exception as e:
            self.logger.warning(f"Failed to apply visual effects: {e}")
        
        return img

    def _process_slide_audio(self, slide: Dict, tts_lang: str, speed_factor: float) -> Optional[str]:
        """Process audio for slide with enhanced TTS"""
        try:
            # Use the existing enhanced_text_to_speech function
            audio_file_path = enhanced_text_to_speech(
                slide["content"], tts_lang, speed_factor
            )
            
            if audio_file_path and os.path.exists(audio_file_path):
                self.temp_files.append(audio_file_path)
                return audio_file_path
            else:
                self.logger.warning(f"Audio file not generated or doesn't exist for slide")
                return None
            
        except Exception as e:
            self.logger.error(f"Failed to process audio for slide: {e}")
            return None

    def _create_slide_video_clip(self, slide: Dict, template: str, slide_num: int,
                               total_slides: int, company_logo: Any, tts_lang: str,
                               speed_factor: float) -> Optional[Any]:
        """Create individual video clip for slide"""
        try:
            # Generate slide image
            slide_img = self._create_enhanced_slide(slide, template, slide_num, 
                                                  total_slides, company_logo)
            
            # Save slide image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
                slide_img.save(tmp_img.name, 'PNG', quality=95)
                self.temp_files.append(tmp_img.name)
                
                # Process audio
                audio_file_path = self._process_slide_audio(slide, tts_lang, speed_factor)
                
                if audio_file_path and os.path.exists(audio_file_path):
                    try:
                        # Create video clip with audio
                        audio_clip = AudioFileClip(audio_file_path)
                        
                        # Apply audio effects - use crossfadein and crossfadeout for audio
                        audio_clip = audio_clip.fx(volumex, 1.0)  # Ensure proper volume
                        
                        # Calculate optimal duration
                        duration = max(
                            min(audio_clip.duration + 1.0, self.config.max_slide_duration),
                            self.config.min_slide_duration
                        )
                        
                        img_clip = ImageClip(tmp_img.name, duration=duration)
# Apply effects using the proper syntax
                        img_clip = fadein(img_clip, self.config.fade_duration)
                        img_clip = fadeout(img_clip, self.config.fade_duration)

# For audio effects
                        audio_clip = volumex(audio_clip, 1.0)  # Apply volume effect directly
                        video_clip = img_clip.set_audio(audio_clip)
                        
                        self.metrics.total_duration += duration
                        self.metrics.processed_slides += 1
                        
                        return video_clip
                    except Exception as audio_error:
                        self.logger.error(f"Failed to create audio clip: {audio_error}")
                        # Fall back to silent video
                        duration = self.config.min_slide_duration
                        img_clip = ImageClip(tmp_img.name, duration=duration)
                        img_clip = img_clip.fx(fadein, self.config.fade_duration)
                        img_clip = img_clip.fx(fadeout, self.config.fade_duration)
                        
                        self.metrics.total_duration += duration
                        self.metrics.processed_slides += 1
                        
                        return img_clip
                    
                else:
                    # Create silent video clip
                    duration = self.config.min_slide_duration
                    img_clip = ImageClip(tmp_img.name, duration=duration)
                    img_clip = img_clip.fx(fadein, self.config.fade_duration)
                    img_clip = img_clip.fx(fadeout, self.config.fade_duration)
                    
                    self.metrics.total_duration += duration
                    self.metrics.processed_slides += 1
                    
                    return img_clip
                    
        except Exception as e:
            self.logger.error(f"Failed to create video clip for slide {slide_num}: {e}")
            self.metrics.failed_slides += 1
            return None

    def _show_progress(self, stage: int, progress: float, total_stages: int, message: str):
        """Enhanced progress display"""
        if st:
            overall_progress = (stage + progress) / total_stages
            st.progress(overall_progress)
            st.text(f"Stage {stage + 1}/{total_stages}: {message}")
            
            # Show metrics in sidebar
            with st.sidebar:
                st.subheader("Video Generation Metrics")
                st.metric("Processed Slides", self.metrics.processed_slides)
                st.metric("Failed Slides", self.metrics.failed_slides)
                st.metric("Total Duration", f"{self.metrics.total_duration:.1f}s")

# Configure Streamlit page
st.set_page_config(
    page_title="Placement Cell - Company Info & Video Generator",
    page_icon="🎯",
    layout="wide"
)

# --- UI & APP LOGIC ---

# Title and description
st.title("🎯 Placement Cell - Company Information & Video Generator")
st.markdown("Generate comprehensive company information and create professional placement videos (YouTube Shorts format)")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# Get API key from environment variables with fallback to sidebar input
env_api_key = os.getenv("GEMINI_API_KEY")
if env_api_key:
    gemini_api_key = env_api_key
    st.sidebar.success("✅ Gemini API Key loaded from .env file")
else:
    st.sidebar.warning("⚠️ No API key found in .env file. Please enter it below.")
    gemini_api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key or add GEMINI_API_KEY to .env file"
    )

# WhatsApp configuration
st.sidebar.subheader("WhatsApp Settings")

# Get phone number from environment variables with fallback to sidebar input
env_phone = os.getenv("WHATSAPP_PHONE")
if env_phone:
    whatsapp_phone = env_phone
    st.sidebar.success("✅ WhatsApp phone loaded from .env file")
    # Option to override
    if st.sidebar.checkbox("Override phone number from .env"):
        whatsapp_phone = st.sidebar.text_input(
            "Override Phone Number",
            value=env_phone,
            placeholder="+91xxxxxxxxxx",
            help="Override the phone number from .env file"
        )
else:
    st.sidebar.warning("⚠️ No phone number found in .env file.")
    whatsapp_phone = st.sidebar.text_input(
        "Phone Number (for sharing)",
        placeholder="+91xxxxxxxxxx",
        help="Enter phone number with country code or add WHATSAPP_PHONE to .env file"
    )

whatsapp_method = st.sidebar.radio(
    "WhatsApp Method:",
    ["WhatsApp Web Link", "Auto-send (pywhatkit)"],
    help="Choose how to send messages. 'Web Link' is generally more reliable."
)

# Video Settings
if VIDEO_LIBS_AVAILABLE:
    st.sidebar.subheader("🎥 Video Settings")
    video_template = st.sidebar.selectbox(
        "Video Template:",
        ["Tech-Forward", "Professional", "Modern", "Colorful"],
        help="Choose video template style. 'Tech-Forward' is recommended."
    )

    tts_language = st.sidebar.selectbox(
        "Voice Language:",
        ["en-US", "en-GB", "en-AU", "en-IN"],
        help="Text-to-speech language/accent"
    )

    speech_speed = st.sidebar.slider(
        "Speech Speed:",
        min_value=1.0,
        max_value=2.0,
        value=1.4,
        step=0.1,
        help="Speech speed multiplier (1.4 is recommended for an energetic pace)"
    )

# Email content input
st.header("📧 Company Email Content")
email_content = st.text_area(
    "Paste the entire company email content here:",
    height=200,
    placeholder="Example: 'Subject: Invitation to interview for Software Engineer role at Innovate Inc...'"
)

# --- CORE FUNCTIONS ---

def show_advanced_progress(stage, substage, total_stages, details=""):
    """Advanced progress tracking with detailed stages"""
    stages = ["Script Analysis", "Company Research", "Slide Generation", "Logo Creation", "Audio Processing", "Video Assembly", "Final Export"]

    if 'progress_container' not in st.session_state:
        st.session_state.progress_container = st.empty()

    with st.session_state.progress_container.container():
        main_progress = st.progress(0)
        stage_text = st.empty()
        detail_text = st.empty()

        cols = st.columns(len(stages))
        stage_bars = []
        for i, col in enumerate(cols):
            with col:
                st.write(f"**{stages[i][:8]}**")
                st.caption(stages[i])
                bar = st.progress(0)
                stage_bars.append(bar)

        overall_progress = min((stage + substage) / total_stages, 1.0)
        main_progress.progress(overall_progress, f"Overall Progress: {overall_progress*100:.1f}%")
        stage_text.write(f"🔄 **Current Stage:** {stages[min(stage, len(stages)-1)]}")
        detail_text.write(f"📋 {details}")

        for i, bar in enumerate(stage_bars):
            if i < stage:
                bar.progress(1.0)  # Completed
            elif i == stage:
                bar.progress(min(substage, 1.0))  # Current
            else:
                bar.progress(0.0)  # Pending

def extract_company_logo(company_name):
    """Extract company logo using Clearbit API with a fallback to generated initials."""
    try:
        sanitized_name = company_name.lower().replace(' ', '').replace('ltd', '').replace('pvt', '').replace('.', '')
        search_url = f"https://logo.clearbit.com/{sanitized_name}.com"

        response = requests.get(search_url, timeout=5)
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            logo_img = Image.open(BytesIO(response.content))
            return logo_img.resize((200, 200), Image.Resampling.LANCZOS)
        else:
            return generate_initials_logo(company_name)
    except Exception:
        return generate_initials_logo(company_name)

def generate_initials_logo(company_name):
    """Generate a professional initials-based logo as a fallback."""
    words = company_name.replace('Ltd', '').replace('Pvt', '').replace('Inc', '').split()
    initials = ''.join([word[0].upper() for word in words[:2] if word])
    if not initials: initials = "CO"

    size = 200
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    colors = ['#00F260', '#0575E6', '#F2C94C', '#f2709c', '#4facfe', '#6A82FB', '#FC466B', '#38f9d7']
    color = colors[hash(company_name) % len(colors)]

    draw.ellipse([10, 10, size-10, size-10], fill=color)
    draw.ellipse([5, 5, size-5, size-5], outline='white', width=5)

    try:
        font = ImageFont.truetype("arialbd.ttf", 80)
    except IOError:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 80)
        except IOError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = (size - text_width) // 2, (size - text_height) // 2 - 10

    draw.text((x + 2, y + 2), initials, fill=(0, 0, 0, 76), font=font)
    draw.text((x, y), initials, fill='white', font=font)
    return img

def create_interactive_slide(slide_data, template, slide_num, total_slides, company_logo=None):
    """
    Overhauled function to create modern, attention-grabbing slides.
    """
    width, height = 1080, 1920

    # Define color schemes including the new 'Tech-Forward' theme
    color_schemes = {
        "Tech-Forward": {"bg": "#121212", "primary": "#FFFFFF", "secondary": "#AAAAAA", "accent": "#00F260", "card_bg": (34, 34, 34, 255)},
        "Professional": {"bg": "#2c3e50", "primary": "#ffffff", "secondary": "#ecf0f1", "accent": "#3498db", "card_bg": (255, 255, 255, 25)},
        "Modern": {"bg": "#1a1a2e", "primary": "#00d4aa", "secondary": "#ffffff", "accent": "#ff6b6b", "card_bg": (0, 212, 170, 25)},
        "Colorful": {"bg": "#667eea", "primary": "#ffffff", "secondary": "#ffffff", "accent": "#f5d76e", "card_bg": (255, 255, 255, 38)}
    }
    colors = color_schemes.get(template, color_schemes["Tech-Forward"])

    # Base image
    img = Image.new('RGB', (width, height), colors["bg"])
    draw = ImageDraw.Draw(img)

    # Fonts - Prioritize modern, clean fonts
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 80)
        font_regular = ImageFont.truetype("arial.ttf", 52)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # --- Slide Layout ---
    padding = 80

    # Header with Logo and Title
    if slide_num == 1 and company_logo:
        logo_size = 150
        logo_pos = ((width - logo_size) // 2, padding)
        logo_to_paste = company_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        if logo_to_paste.mode == 'RGBA':
            img.paste(logo_to_paste, logo_pos, logo_to_paste)
        else:
            img.paste(logo_to_paste, logo_pos)
        title_y = logo_pos[1] + logo_size + 40
    else:
        title_y = padding + 40

    # Slide Title
    title = slide_data["title"].upper()
    title_bbox = draw.textbbox((0, 0), title, font=font_bold)
    draw.text(((width - (title_bbox[2] - title_bbox[0])) / 2, title_y), title, fill=colors["accent"], font=font_bold)

    # Content Area
    y_start = title_y + 150
    content_text = slide_data["content"]
    points = [s.strip() for s in content_text.split('.') if s.strip()]

    for point in points[:4]: # Limit to 4 points for clarity
        # Card-based layout for each point
        card_x, card_y = padding, y_start
        card_width, card_height = width - 2 * padding, 180
        
        # Draw rounded rectangle for the card
        draw.rounded_rectangle([card_x, card_y, card_x + card_width, card_y + card_height], radius=20, fill=colors["card_bg"])
        
        # Icon placeholder (e.g., a simple circle)
        icon_x, icon_y = card_x + 30, card_y + (card_height // 2) - 15
        draw.ellipse([icon_x, icon_y, icon_x + 30, icon_y + 30], fill=colors["accent"])

        # Text inside the card with wrapping
        text_x = icon_x + 50
        text_y = card_y + 30
        
        avg_char_width = 22
        max_chars = (card_width - 100) // avg_char_width
        wrapped_lines = [point[i:i+max_chars] for i in range(0, len(point), max_chars)]
        
        for line in wrapped_lines[:2]: # Max 2 lines per card
            draw.text((text_x, text_y), line, fill=colors["primary"], font=font_regular)
            text_y += 60

        y_start += card_height + 30

    # Footer with Progress Bar
    footer_y = height - 120
    progress_width = width - 2 * padding
    # Background
    draw.line([(padding, footer_y), (width - padding, footer_y)], fill=colors["secondary"], width=8)
    # Progress
    fill_width = int((slide_num / total_slides) * progress_width)
    draw.line([(padding, footer_y), (padding + fill_width, footer_y)], fill=colors["accent"], width=8)
    
    # Slide number
    slide_text = f"{slide_num} / {total_slides}"
    draw.text((padding, footer_y + 20), slide_text, fill=colors["secondary"], font=font_small)

    return img

def enhanced_text_to_speech(text, lang="en-US", speed_factor=1.3):
    """
    Enhanced TTS using gTTS and pydub for stable speed control.
    """
    try:
        clean_text = text.replace('[SLIDE', '').replace(']', '').replace(':', '.').strip()
        if not clean_text: return None

        tts = gTTS(text=clean_text, lang=lang.split('-')[0], slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts_path = tmp_file.name
            tts.save(tts_path)

        sound = AudioSegment.from_mp3(tts_path)
        sound = sound + 6 # Increase volume
        if speed_factor != 1.0:
            sound = sound.speedup(playback_speed=speed_factor)

        with tempfile.NamedTemporaryFile(delete=False, suffix='_enhanced.mp3') as enhanced_tmp_file:
            enhanced_path = enhanced_tmp_file.name
            sound.export(enhanced_path, format="mp3")
        
        os.unlink(tts_path)
        return enhanced_path
            
    except Exception as e:
        st.error(f"Error in enhanced TTS: {str(e)}")
        return None

def generate_comprehensive_prompt(email_content):
    """Refined prompt for more engaging and student-focused content."""
    return f"""
    think about each stage and validate each link of yours using your search capabilities.
    make sure the link is working and relevant.
       As a placement cell assistant, analyze the following company email and extract the company name and role, then research and provide comprehensive information.

    Email Content:
    {email_content}

    First, identify the company name and role from the email content above, then provide information in the following structured format:

    also you act as an agent for a 4th year B.Tech, COMPUTER SCIENCE/AIML STREAM student who is preparing for placements and needs detailed information about the company and role. 
    keep in mind that the student is looking for specific details to prepare effectively for interviews and understand the company better.
    ORGANIZATION: [Extracted Company Name]

    ORGANIZATION DETAILS:
    1. Base Site: [Official website URL]
    2. LinkedIn: [LinkedIn company page URL]
    3. Facebook: [Facebook page URL if available]
    4. X (Twitter): [Twitter handle URL if available]
    5. Instagram: [Instagram page URL if available]
    6. Role/s Offered: [Extracted Role from email]
    7. Company Overview: [Brief description of what the company does]
    8. Company Size: [Number of employees if available]
    9. Headquarters: [Location]
    10. Founded: [Year if available]

    INTERVIEW REFERENCES:
    1. Interview Experiences and Questions from GeeksForGeeks: [Search for company-specific interview experiences, for example : https://www.glassdoor.co.in/Interview/Komprise-Interview-Questions-E1328184.htm
    4. LeetCode Company-specific Questions: [If available]

    ROLE-SPECIFIC PREPARATION:
    [Based on the extracted role, suggest specific technical topics, skills, and preparation areas and provide links to resources(one best fitting link for each topic):]
    eg:
    to get started with the preparation, you can refer to the following resources:
    the company requires candidates to have a strong understanding of the following topics:
    1. Programming Languages: [Link to resource]
    2. Data Structures and Algorithms: [Link to resource] and mention the important topics compulsarily and say its been asked before
    3. System Design: [Link to resource]
    4. Behavioral Interviews: [Link to resource]
    5. Company Culture and Values: [Link to resource]

    INTERVIEW HIGHLIGHTS (General Preparation):
    search for the following resources and provide links in the format example:
    based on the role and company, provide the following resources (not limited to just geeksforgeeks, but also include other reputable sources):
    if no role is extracted, just provide resources for entry level SDE/analyst roles.
    check for interview preperation resources for the specific company and role, and if not available, provide general resources for the role.
    make sure to include the best resources available for each topic.
    1. Interview Preparation Resources:
    - [Link to resource]
    - [Link to resource]
    - [Link to resource]
    - [Link to resource]

    ADDITIONAL RESOURCES:
    - GeeksForGeeks: [Link to GFG company page]
    - LeetCode: [Link to LeetCode company page]
    - AmbitionBox: [Link to AmbitionBox company page]
    - Glassdoor: [Link to Glassdoor company page]
    

    COMPANY CULTURE & VALUES:
    [Brief information about company culture, values, and work environment]

    do not include any salary information, even if it is mentioned in the email content.

    
    no placeholder text, just provide the information in the format specified above.
    also add the following:
    Best Regards,
    Professor Animesh Giri
    Linkedin: https://www.linkedin.com/in/animesh-giri-15272531/
    Youtube: https://www.youtube.com/channel/UCBFH7hssUsyipttqLxHU-cw

    Please use your search capabilities to find accurate and up-to-date information. Make sure all URLs are working and relevant. Focus on extracting the correct company name and role from the email content first, then research accordingly.
    do not include any personal opinions or unverified information. Provide the information in a clear and structured format.
    do not use any markdown formatting, just plain text.
    IMPORTANT : FOR EACH AND EVERY URL - MAKE SURE THAT THE URL IS JUST THE LINK, NOT THE TEXT.
    For example, if the company website is "https://www.example.com", then the output should be "Base Site: https://www.example.com" and NOT "Base Site: [Official website URL]". 
    The text should not include any placeholders or additional text,
    ALSO THE URL SHOULD WORK
    and for example  - this Base Site: [Official website URL] is just supposed to return "Base site :" the official website URL of the company, not the text "Base Site: [Official website URL]".
    """

def generate_shorts_script(company_info):
    """Refined script generator for a more dynamic, attention-grabbing video."""
    if not gemini_api_key: return None
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        script_prompt = f"""
        Create a high-energy, 60-second YouTube Shorts script for a tech placement opportunity based on the info below. The tone should be like a top tech influencer: fast, exciting, and packed with value.

        **Strict Rules:**
        - **6 Slides MAX.**
        - **Format:** `[SLIDE X: CATCHY TITLE]\n(The spoken text for the narrator for this slide goes here. Do NOT include the word "Narrator" or any colons.)`
        - **Language:** Use hooks, short sentences, and strong CTAs.

        **Company Info:**
        ---
        {company_info}
        ---

        **Script Blueprint:**
        [SLIDE 1: THE DROP]
        Stop scrolling! This is the opportunity you've been waiting for.

        [SLIDE 2: THE LOWDOWN]
        Quick facts about the company. What they do, their impact. Make them sound cool.

        [SLIDE 3: THE VALUE PROPOSITION]
        Highlight the unique benefits and growth opportunities this role offers.

        [SLIDE 4: THE TECH STACK]
        List the top 2-3 technologies they're looking for. "You need to know..."

        [SLIDE 5: THE HACKS]
        I've dropped the links. GFG, LeetCode... go grind.

        [SLIDE 6: THE DEADLINE]
        Create urgency. "The deadline is approaching. Your career is calling. Let's go!"

        Generate the script now. Make it punchy.
        """
        response = model.generate_content(script_prompt)
        cleaned_text = response.text.strip().strip('```').strip()
        return cleaned_text
    except Exception as e:
        st.error(f"Error generating shorts script: {str(e)}")
        return None

def parse_script_into_slides(script):
    """Parse the script into individual slides"""
    slides = []
    pattern = r'\[SLIDE \d+:\s*(.*?)\]\n(.*?)(?=\n\[SLIDE|\Z)'
    matches = re.findall(pattern, script, re.DOTALL)
    for match in matches:
        title = match[0].strip()
        content = match[1].strip().replace('\n', ' ').replace('Narrator:', '').replace('narrator:', '').strip()
        if title and content:
            slides.append({"title": title, "content": content})
    return slides

def create_professional_placement_video(
    slides: List[Dict], 
    company_name: str, 
    template: str = 'corporate',
    tts_lang: str = 'en',
    speed_factor: float = 1.0,
    config: VideoConfig = None,
    parallel_processing: bool = True
) -> Optional[str]:
    """
    Create professional placement video with industry-standard quality
    
    Args:
        slides: List of slide dictionaries with 'title' and 'content'
        company_name: Name of the company for branding
        template: Visual template ('corporate', 'modern', 'minimalist')
        tts_lang: Text-to-speech language
        speed_factor: Audio speed multiplier
        config: Video configuration settings
        parallel_processing: Enable parallel slide processing
    
    Returns:
        Path to generated video file or None if failed
    """
    if not VIDEO_LIBS_AVAILABLE:
        if st:
            st.error("❌ Video libraries not available. Please install moviepy and PIL.")
        return None
    
    if not slides:
        if st:
            st.error("❌ No slides provided for video generation.")
        return None
    
    # Initialize generator
    generator = AdvancedVideoGenerator(config)
    start_time = time.time()
    
    try:
        generator.metrics.total_slides = len(slides)
        generator._show_progress(0, 0.1, 8, "🚀 Initializing professional video generation...")
        
        # Extract/generate company logo
        company_logo = extract_company_logo(company_name) if 'extract_company_logo' in globals() else None
        generator._show_progress(0, 0.5, 8, "🏢 Processing company branding...")
        
        # Process slides
        video_clips = []
        
        if parallel_processing and len(slides) > 3:
            # Parallel processing for better performance
            generator._show_progress(1, 0.0, 8, "⚡ Processing slides in parallel...")
            
            with ThreadPoolExecutor(max_workers=min(4, len(slides))) as executor:
                future_to_slide = {
                    executor.submit(
                        generator._create_slide_video_clip,
                        slide, template, i + 1, len(slides), company_logo, tts_lang, speed_factor
                    ): i for i, slide in enumerate(slides)
                }
                
                for future in as_completed(future_to_slide):
                    slide_idx = future_to_slide[future]
                    try:
                        clip = future.result()
                        if clip:
                            video_clips.append((slide_idx, clip))
                        
                        progress = len(video_clips) / len(slides)
                        generator._show_progress(2, progress, 8, 
                                               f"📹 Generated {len(video_clips)}/{len(slides)} slides")
                        
                    except Exception as e:
                        generator.logger.error(f"Slide {slide_idx + 1} failed: {e}")
                        generator.metrics.failed_slides += 1
            
            # Sort clips by original order
            video_clips.sort(key=lambda x: x[0])
            video_clips = [clip for _, clip in video_clips]
            
        else:
            # Sequential processing
            for i, slide in enumerate(slides):
                generator._show_progress(2, i / len(slides), 8, 
                                       f"📹 Generating slide {i+1}/{len(slides)}...")
                
                clip = generator._create_slide_video_clip(
                    slide, template, i + 1, len(slides), company_logo, tts_lang, speed_factor
                )
                
                if clip:
                    video_clips.append(clip)
        
        if not video_clips:
            if st:
                st.error("❌ No video clips were generated successfully.")
            return None
        
        generator._show_progress(4, 0.2, 8, "🎬 Assembling final video...")
        
        # Create final video composition
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Apply final enhancements
        if generator.config.resolution != (1920, 1080):
            final_video = final_video.resize(generator.config.resolution)
        
        generator._show_progress(5, 0.6, 8, "🎨 Applying final enhancements...")
        
        # Export video with professional settings
        generator._show_progress(6, 0.1, 8, "💾 Exporting high-quality video...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video:
            final_video.write_videofile(
                tmp_video.name,
                fps=generator.config.fps,
                codec=generator.config.video_codec,
                audio_codec=generator.config.audio_codec,
                preset=generator.config.preset,
                ffmpeg_params=['-crf', str(generator.config.crf)],
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None,
                verbose=False
            )
            
            # Calculate final metrics
            generator.metrics.generation_time = time.time() - start_time
            if os.path.exists(tmp_video.name):
                generator.metrics.file_size_mb = os.path.getsize(tmp_video.name) / (1024 * 1024)
            
            generator._show_progress(7, 1.0, 8, 
                                   f"✅ Video created! Duration: {generator.metrics.total_duration:.1f}s | "
                                   f"Size: {generator.metrics.file_size_mb:.1f}MB | "
                                   f"Time: {generator.metrics.generation_time:.1f}s")
            
            # Cleanup
            final_video.close()
            for clip in video_clips:
                if hasattr(clip, 'audio') and clip.audio:
                    clip.audio.close()
                clip.close()
            
            generator._cleanup_temp_files()
            
            # Show final metrics
            if st:
                st.success(f"🎉 Professional video generated successfully!")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Duration", f"{generator.metrics.total_duration:.1f}s")
                with col2:
                    st.metric("File Size", f"{generator.metrics.file_size_mb:.1f}MB")
                with col3:
                    st.metric("Generation Time", f"{generator.metrics.generation_time:.1f}s")
            
            return tmp_video.name
    
    except Exception as e:
        generator.logger.error(f"Critical error in video generation: {e}")
        if st:
            st.error(f"❌ Video generation failed: {str(e)}")
        
        generator._cleanup_temp_files()
        return None

# Utility function for backward compatibility
def enhanced_create_placement_video(*args, **kwargs):
    """Enhanced wrapper function with default professional settings"""
    config = VideoConfig(
        resolution=(1920, 1080),
        fps=30,
        crf=20,  # Higher quality
        fade_duration=0.8,
        max_slide_duration=25.0
    )
    return create_professional_placement_video(*args, config=config, **kwargs)

def generate_whatsapp_web_link(message, phone_number=None):
    """Generate WhatsApp Web link as a reliable alternative"""
    import urllib.parse
    encoded_message = urllib.parse.quote(message)
    
    if phone_number:
        phone_number = "".join(filter(str.isdigit, phone_number))
        return f"https://wa.me/{phone_number}?text={encoded_message}"
    else:
        return f"https://web.whatsapp.com/send?text={encoded_message}"

# --- STREAMLIT UI FLOW ---

if 'generated_info' not in st.session_state:
    st.session_state.generated_info = ""
if 'video_script' not in st.session_state:
    st.session_state.video_script = ""
if 'progress_container' not in st.session_state:
    st.session_state.progress_container = None

if st.button("🔍 Generate Company Information", type="primary"):
    if not gemini_api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not email_content.strip():
        st.error("Please paste the company email content.")
    else:
        with st.spinner("Processing email and generating company information..."):
            try:
                genai.configure(api_key=gemini_api_key)
                research_prompt = generate_comprehensive_prompt(email_content)
                model = genai.GenerativeModel('gemini-2.5-pro')
                response = model.generate_content(research_prompt)
                st.session_state.generated_info = response.text
                st.success("✅ Company information generated successfully!")
            except Exception as e:
                st.error(f"An error occurred with the AI model: {str(e)}")

if st.session_state.generated_info:
    st.header("📋 Generated Company Information")
    st.text_area("Generated Content:", st.session_state.generated_info, height=400)
    
    company_name_match = re.search(r'ORGANIZATION:\s*(.+)', st.session_state.generated_info)
    company_name = company_name_match.group(1).strip() if company_name_match else "Company"
    
    if VIDEO_LIBS_AVAILABLE:
        st.header("🎥 Generate Professional Placement Video")
        st.info("📱 Creates a 60-90 second professional video optimized for mobile sharing.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Generate Video Script"):
                with st.spinner("Generating YouTube Shorts style script..."):
                    st.session_state.video_script = generate_shorts_script(st.session_state.generated_info)
                    if st.session_state.video_script:
                        st.success("🎬 Video script generated! Review below and create the video.")
        
        with col2:
            if st.session_state.video_script:
                if st.button("🎬 Create Professional Video", type="primary"):
                    if 'progress_container' in st.session_state and st.session_state.progress_container:
                        st.session_state.progress_container.empty()
                    st.session_state.progress_container = st.empty()
                    
                    with st.spinner("Creating video... This may take 2-4 minutes."):
                        slides = parse_script_into_slides(st.session_state.video_script)
                        if not slides:
                            st.error("Script parsing failed. Please check the script format or regenerate.")
                        else:
                            # Map UI template names to internal template names
                            template_mapping = {
                                "Tech-Forward": "corporate",
                                "Professional": "corporate", 
                                "Modern": "modern",
                                "Colorful": "modern"
                            }
                            internal_template = template_mapping.get(video_template, "corporate")
                            
                            video_path = create_professional_placement_video(
                                slides, company_name, internal_template, tts_language, speech_speed
                            )
                            if video_path:
                                st.session_state.progress_container.empty()
                                st.success("🎉 Professional placement video created successfully!")
                                
                                with open(video_path, 'rb') as video_file:
                                    st.video(video_file.read())
                                
                                with open(video_path, 'rb') as video_file:
                                    st.download_button(
                                        label="📥 Download Video (MP4)",
                                        data=video_file.read(),
                                        file_name=f"{company_name.lower().replace(' ', '_')}_placement_video.mp4",
                                        mime="video/mp4"
                                    )
                                os.unlink(video_path)
                            else:
                                st.error("Failed to create video. Please check the error messages above.")

    if st.session_state.video_script:
        with st.expander("📜 View/Edit Video Script"):
            edited_script = st.text_area(
                "Video Script:", st.session_state.video_script, height=300
            )
            if edited_script != st.session_state.video_script:
                st.session_state.video_script = edited_script
                st.info("Script updated! Click 'Create Video' to apply changes.")
    
    st.header("🚀 Share & Download")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📲 Share via WhatsApp")
        if whatsapp_method == "WhatsApp Web Link":
            whatsapp_link = generate_whatsapp_web_link(st.session_state.generated_info, whatsapp_phone)
            st.markdown(f"**[Click here to open WhatsApp]({whatsapp_link})**")
            st.info("The message will be pre-filled. Just click send!")
        else:
            if whatsapp_phone:
                if st.button("📤 Auto-send via pywhatkit"):
                    with st.spinner("Scheduling WhatsApp message..."):
                        try:
                            now = datetime.now() + timedelta(minutes=1)
                            kit.sendwhatmsg(whatsapp_phone, st.session_state.generated_info, now.hour, now.minute)
                            st.success("Message scheduled! WhatsApp will open shortly.")
                        except Exception as e:
                            st.error(f"PyWhatKit Error: {e}")
                            st.info("Try using the 'WhatsApp Web Link' method instead.")
            else:
                st.warning("Enter a phone number in the sidebar for auto-sending.")

    with col2:
        st.subheader("💾 Download Assets")
        st.download_button(
            label="📄 Download Company Info (.txt)",
            data=st.session_state.generated_info,
            file_name=f"{company_name.lower().replace(' ', '_')}_info.txt",
            mime="text/plain"
        )
        if st.session_state.video_script:
            st.download_button(
                label="🎬 Download Video Script (.txt)",
                data=st.session_state.video_script,
                file_name=f"{company_name.lower().replace(' ', '_')}_script.txt",
                mime="text/plain"
            )

st.markdown("---")
st.markdown("**Made with ❤️ for Students & Placement Teams | Transform placement preparation with AI**")
