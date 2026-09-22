import os
from PIL import Image

def optimize_image(input_path, output_path=None, max_width=1920, max_height=1080, quality=75, format="WebP"):
    """
    Optimizes an image by resizing, compressing, and removing unnecessary metadata.
    """
    if not os.path.exists(input_path):
        print(f"Error: Could not find image at {input_path}")
        return

    # Original size in KB
    original_size_kb = os.path.getsize(input_path) / 1024

    print(f"\n--- Original Image Stats ---")
    print(f"Path: {input_path}")
    print(f"File Size: {original_size_kb:.2f} KB")

    try:
        # 1. Open the image
        img = Image.open(input_path)
        
        # Strip metadata by completely discarding the info dictionary
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.paste(img)
        img = image_without_exif

        print(f"Dimensions: {img.size[0]}x{img.size[1]}")

        # 2. Check dimensions & Resize if necessary
        # We use LANCZOS for high quality downsampling
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        print(f"New Dimensions after resize: {img.size[0]}x{img.size[1]}")

        # 3. Determine output format and path
        if not output_path:
            filename, _ = os.path.splitext(input_path)
            output_path = f"{filename}_optimized.{format.lower()}"

        # 4. Save with Compression (and no EXIF data to save space)
        # We ensure no exif parameter is passed, so metadata is dropped
        if img.mode in ("RGBA", "P") and format.upper() == "JPEG":
            # JPEG doesn't support alpha channel, convert to RGB
            img = img.convert("RGB")

        print(f"\n[Processing...] Saving as {format.upper()} with Quality={quality}...")
        
        img.save(output_path, format=format, quality=quality, optimize=True)

        # 5. Output comparison
        optimized_size_kb = os.path.getsize(output_path) / 1024
        saved_kb = original_size_kb - optimized_size_kb
        saved_percent = (saved_kb / original_size_kb) * 100

        print(f"\n--- Optimized Image Stats ---")
        print(f"Path: {output_path}")
        print(f"New File Size: {optimized_size_kb:.2f} KB")
        print(f"Saved: {saved_kb:.2f} KB ({saved_percent:.2f}% reduction)")
        print("-" * 30)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("=" * 50)
    print("IMAGE OPTIMIZATION TOOL")
    print("=" * 50)

    input_img = input("Enter the path to your high-resolution image:\n> ").strip()
    
    # Remove quotes if user drag-drops the file in terminal
    input_img = input_img.strip('"').strip("'")

    if not input_img:
        print("Path is required! Exiting...")
        return
        
    print("\nSelect Output Format (default is WebP for best compression):")
    print("1. WebP (Recommended)")
    print("2. JPEG")
    print("3. PNG (Lossless, larger size)")
    
    choice = input("Enter choice (1/2/3) or press Enter for default: ").strip()
    fmt = "WebP"
    if choice == "2":
        fmt = "JPEG"
    elif choice == "3":
        fmt = "PNG"
        
    quality_input = input("\nEnter compression quality (1-100) [Default=75]: ").strip()
    quality = int(quality_input) if quality_input.isdigit() else 75

    optimize_image(input_img, quality=quality, format=fmt)

if __name__ == "__main__":
    main()
