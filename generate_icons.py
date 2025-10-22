#!/usr/bin/env python3
"""
A.U.R.A Icon Generator
Creates PWA icons with the A.U.R.A branding colors
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_aura_icon(size, filename):
    """Create an A.U.R.A icon with the branding colors"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle with orange gradient effect
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(232, 80, 2, 255), outline=(193, 8, 1, 255), width=2)
    
    # Inner circle with lighter orange
    inner_margin = size // 4
    draw.ellipse([inner_margin, inner_margin, size-inner_margin, size-inner_margin], 
                 fill=(241, 96, 1, 200))
    
    # Add "A" text in the center
    try:
        # Try to use a system font
        font_size = size // 3
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Get text size for centering
    bbox = draw.textbbox((0, 0), "A", font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 2  # Slight adjustment for visual centering
    
    # Draw white "A" text
    draw.text((x, y), "A", fill=(249, 249, 249, 255), font=font)
    
    # Save the icon
    img.save(filename, 'PNG')
    print(f"Created icon: {filename} ({size}x{size})")

def main():
    """Generate all required PWA icons"""
    print("🎨 Generating A.U.R.A PWA icons...")
    
    # Icon sizes for PWA
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    for size in sizes:
        filename = f"icons/icon-{size}x{size}.png"
        create_aura_icon(size, filename)
    
    print("✅ All A.U.R.A PWA icons generated successfully!")
    print("📱 Icons are ready for Progressive Web App installation")

if __name__ == "__main__":
    main()
