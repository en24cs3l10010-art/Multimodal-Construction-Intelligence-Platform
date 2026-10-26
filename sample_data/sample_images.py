"""
Sample image generators and base64 assets for instant 1-click testing
in Site Safety PPE Audit and Crack Diagnostics tabs.
"""

import os
from PIL import Image, ImageDraw, ImageFont

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")
os.makedirs(SAMPLE_DIR, exist_ok=True)

PPE_SAMPLE_PATH = os.path.join(SAMPLE_DIR, "sample_construction_ppe.jpg")
CRACK_SAMPLE_PATH = os.path.join(SAMPLE_DIR, "sample_concrete_crack.jpg")
CRACK_HAIRLINE_PATH = os.path.join(SAMPLE_DIR, "sample_hairline_crack.jpg")


def create_sample_ppe_image() -> str:
    """Generates an illustrative construction site scene image if not already present."""
    if os.path.exists(PPE_SAMPLE_PATH):
        return PPE_SAMPLE_PATH

    img = Image.new("RGB", (900, 600), color="#1A202C")
    draw = ImageDraw.Draw(img)

    # Sky and background construction silhouette
    draw.rectangle([0, 0, 900, 240], fill="#2D3748")
    
    # Tower Crane silhouette
    draw.line([(700, 40), (700, 380)], fill="#F59E0B", width=6)
    draw.line([(550, 80), (880, 80)], fill="#F59E0B", width=5)
    draw.line([(550, 80), (700, 40)], fill="#F59E0B", width=3)
    draw.line([(700, 40), (820, 80)], fill="#F59E0B", width=3)
    draw.line([(780, 80), (780, 220)], fill="#CBD5E0", width=2)

    # Scaffolding & Concrete building structure
    for x in range(50, 500, 90):
        draw.line([(x, 120), (x, 480)], fill="#718096", width=4)
    for y in range(120, 500, 80):
        draw.line([(50, y), (410, y)], fill="#A0AEC0", width=4)
        # Cross bracing
        draw.line([(50, y), (140, y + 80)], fill="#4A5568", width=2)
        draw.line([(140, y), (50, y + 80)], fill="#4A5568", width=2)
        draw.line([(140, y), (230, y + 80)], fill="#4A5568", width=2)

    # Concrete slab floor
    draw.rectangle([0, 480, 900, 600], fill="#374151")
    # Ground soil/rebar markings
    draw.rectangle([0, 530, 900, 600], fill="#4A453A")
    for rx in range(600, 880, 30):
        draw.line([(rx, 530), (rx, 460)], fill="#9CA3AF", width=4) # Rebar protruding

    # Worker 1 (Compliant - Helmet + Orange Vest)
    # Head & Helmet
    draw.ellipse([200, 360, 240, 400], fill="#F6E05E") # Yellow Hard Hat
    draw.ellipse([205, 380, 235, 410], fill="#E2E8F0") # Face
    # Body & Hi-Vis Vest
    draw.rectangle([195, 410, 245, 480], fill="#DD6B20") # Orange Vest
    draw.line([(195, 435), (245, 435)], fill="#EDF2F7", width=6) # Reflective stripe
    draw.line([(195, 455), (245, 455)], fill="#EDF2F7", width=6) # Reflective stripe
    # Legs & Steel boots
    draw.rectangle([200, 480, 218, 540], fill="#2B6CB0") # Denim Jeans
    draw.rectangle([222, 480, 240, 540], fill="#2B6CB0")
    draw.rectangle([196, 535, 220, 550], fill="#2D3748") # Safety boots
    draw.rectangle([222, 535, 246, 550], fill="#2D3748")

    # Worker 2 (Compliant - Green Vest + White Helmet)
    draw.ellipse([340, 350, 380, 390], fill="#FFFFFF") # White Engineer Helmet
    draw.ellipse([345, 370, 375, 400], fill="#ED8936")
    draw.rectangle([335, 400, 385, 470], fill="#38A169") # Green Hi-Vis Vest
    draw.line([(335, 425), (385, 425)], fill="#EDF2F7", width=6)
    draw.rectangle([340, 470, 358, 530], fill="#1A202C")
    draw.rectangle([362, 470, 380, 530], fill="#1A202C")
    draw.rectangle([336, 525, 360, 540], fill="#4A5568")
    draw.rectangle([362, 525, 386, 540], fill="#4A5568")

    # Worker 3 (Non-compliant - Scaffolding at height, no harness, missing hardhat)
    draw.ellipse([100, 190, 130, 220], fill="#2D3748") # Dark hair, NO HELMET!
    draw.rectangle([95, 220, 135, 270], fill="#4A5568") # Plain dark shirt, NO VEST!
    draw.rectangle([100, 270, 115, 320], fill="#2B6CB0")
    draw.rectangle([118, 270, 133, 320], fill="#2B6CB0")

    # Informational Watermark
    draw.rectangle([20, 20, 440, 70], fill="#0F172A", outline="#F59E0B", width=2)
    draw.text((35, 28), "SAMPLE SITE PHOTO: PPE & HAZARD AUDIT", fill="#F59E0B")
    draw.text((35, 46), "OSHA 1926 & IS 15844 Compliance Verification", fill="#CBD5E0")

    img.save(PPE_SAMPLE_PATH, quality=92)
    return PPE_SAMPLE_PATH


def create_sample_crack_images():
    """Generates sample crack images (Structural Shear & Hairline) for crack diagnostics."""
    if not os.path.exists(CRACK_SAMPLE_PATH):
        # 1. Structural Shear Crack on Concrete Beam
        img1 = Image.new("RGB", (800, 600), color="#718096")
        draw1 = ImageDraw.Draw(img1)
        # Concrete aggregate texture
        import random
        for _ in range(1200):
            rx = random.randint(0, 800)
            ry = random.randint(0, 600)
            c = random.choice(["#4A5568", "#A0AEC0", "#2D3748", "#8B95A5"])
            draw1.point((rx, ry), fill=c)

        # Draw 45-degree prominent structural shear crack
        crack_points = [
            (150, 100), (220, 160), (270, 190), (340, 270), (410, 320),
            (480, 380), (550, 430), (630, 520)
        ]
        # Main jagged fracture
        for i in range(len(crack_points) - 1):
            p1 = crack_points[i]
            p2 = crack_points[i + 1]
            draw1.line([p1, p2], fill="#1A202C", width=8)
            draw1.line([p1, p2], fill="#000000", width=4)
            # Secondary branch
            if i in [2, 4]:
                draw1.line([p1, (p1[0] + 45, p1[1] + 15)], fill="#2D3748", width=3)

        # Scale ruler
        draw1.rectangle([50, 520, 250, 560], fill="#FFFFFF", outline="#000000", width=2)
        for tick in range(60, 240, 20):
            draw1.line([(tick, 540), (tick, 560)], fill="#000000", width=2)
        draw1.text((70, 525), "SCALE: 100 mm", fill="#000000")

        draw1.rectangle([20, 20, 480, 65], fill="#0F172A", outline="#EF4444", width=2)
        draw1.text((35, 28), "SAMPLE: RCC BEAM STRUCTURAL SHEAR CRACK", fill="#EF4444")
        draw1.text((35, 46), "Width: ~2.4mm | Angle: 45° | High Urgency", fill="#E2E8F0")

        img1.save(CRACK_SAMPLE_PATH, quality=92)

    if not os.path.exists(CRACK_HAIRLINE_PATH):
        # 2. Superficial Hairline Crack
        img2 = Image.new("RGB", (800, 600), color="#CBD5E0")
        draw2 = ImageDraw.Draw(img2)
        # Faint micro-crack line
        points = [(100, 300), (250, 290), (380, 310), (520, 285), (700, 305)]
        for i in range(len(points) - 1):
            draw2.line([points[i], points[i + 1]], fill="#4A5568", width=2)

        draw2.rectangle([20, 20, 480, 65], fill="#0F172A", outline="#10B981", width=2)
        draw2.text((35, 28), "SAMPLE: CONCRETE SURFACE HAIRLINE SHRINKAGE", fill="#10B981")
        draw2.text((35, 46), "Width: ~0.15mm | Non-structural | Low Urgency", fill="#E2E8F0")
        img2.save(CRACK_HAIRLINE_PATH, quality=92)


# Pre-generate samples immediately on module import
create_sample_ppe_image()
create_sample_crack_images()
