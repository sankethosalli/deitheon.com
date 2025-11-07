#!/usr/bin/env python3
"""
Generate a simple favicon.png for DeiTheon
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a 512x512 image with transparency
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient circle background
    # We'll approximate a gradient by drawing concentric circles
    center = size // 2
    radius = size // 2 - 20
    
    # Draw main circle with blue color
    draw.ellipse([center - radius, center - radius, center + radius, center + radius], 
                 fill='#3b82f6')
    
    # Try to load a font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 300)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 300)
        except:
            font = ImageFont.load_default()
    
    # Draw the letter "D"
    text = "D"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 20
    
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    # Save as PNG
    output_dir = '/home/un6/github/sankethosalli/deitheon.com/assets/images'
    os.makedirs(output_dir, exist_ok=True)
    img.save(f'{output_dir}/favicon.png', 'PNG')
    
    # Also save a smaller 32x32 version for .ico
    img_small = img.resize((32, 32), Image.LANCZOS)
    img_small.save(f'{output_dir}/favicon.ico', 'ICO')
    
    print("✅ Favicon generated successfully!")
    print(f"   - favicon.png (512x512)")
    print(f"   - favicon.ico (32x32)")
    
except ImportError:
    print("⚠️  PIL/Pillow not installed. Creating simple text-based favicon marker...")
    # Create a simple marker file
    with open('/home/un6/github/sankethosalli/deitheon.com/assets/images/favicon.png', 'w') as f:
        f.write('<!-- Favicon placeholder - replace with actual PNG -->')
    print("✅ Placeholder created. Install Pillow with: pip install Pillow")
