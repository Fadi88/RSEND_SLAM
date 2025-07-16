import cv2
import numpy as np
from PIL import Image, ImageDraw
import os

def modify_map_replace_tables_with_feet(
    input_pgm_path,
    output_pgm_path,
    min_table_dimension_pixels=30,
    max_table_dimension_pixels=400,
    min_aspect_ratio=1.0,
    max_aspect_ratio=1.5,
    foot_size=5,
    debug_output_path="debug_contours.png"
):
    try:
        img_cv = cv2.imread(input_pgm_path, cv2.IMREAD_GRAYSCALE)

        if img_cv is None:
            print(f"Error: Could not open or find the image '{input_pgm_path}'. Please ensure the file exists and is a valid image.")
            return

        debug_img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2BGR)
        
        # Use a stricter threshold (all non-white pixels become black, then invert)
        # This can help eliminate faint gray connections.
        _, binary_img = cv2.threshold(img_cv, 250, 255, cv2.THRESH_BINARY_INV) # Thresh at 250 to catch very dark pixels
                                                                               # Invert so black objects are white for contour finding

        # --- IMPORTANT CHANGE HERE: cv2.RETR_EXTERNAL changed to cv2.RETR_LIST ---
        contours, _ = cv2.findContours(binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
        # RETR_LIST retrieves all contours without any hierarchical relationships

        img_pil = Image.fromarray(img_cv)
        draw = ImageDraw.Draw(img_pil)

        detected_tables_count = 0
        
        print("\n--- Debugging Contour Properties ---")
        print(f"Filtering with min_dim={min_table_dimension_pixels}, max_dim={max_table_dimension_pixels}, min_AR={min_aspect_ratio:.2f}, max_AR={max_aspect_ratio:.2f}")

        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate aspect ratio
            aspect_ratio = float(w) / h if h != 0 else float('inf')
            normalized_aspect_ratio = max(aspect_ratio, 1.0 / aspect_ratio)

            # Check if dimensions are within range
            is_valid_dimension = (w >= min_table_dimension_pixels and w <= max_table_dimension_pixels and
                                  h >= min_table_dimension_pixels and h <= max_table_dimension_pixels)
            
            if is_valid_dimension:
                print(f"Contour {i} Candidate: x={x}, y={y}, w={w}, h={h}, NormAR={normalized_aspect_ratio:.2f}")
                
                # Draw green rectangle for candidates that meet dimension criteria
                cv2.rectangle(debug_img_cv, (x, y), (x + w, y + h), (0, 255, 0), 2) 

                # Apply aspect ratio filter
                if (normalized_aspect_ratio >= min_aspect_ratio and 
                    normalized_aspect_ratio <= max_aspect_ratio):
                    
                    detected_tables_count += 1
                    cv2.rectangle(debug_img_cv, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue for ACCEPTED
                    
                    # Fill table area with white
                    draw.rectangle([x, y, x + w, y + h], fill=255) 

                    # Draw feet
                    foot_half = foot_size // 2
                    draw.rectangle([x - foot_half, y - foot_half, x + foot_half, y + foot_half], fill=0)
                    draw.rectangle([x + w - foot_half, y - foot_half, x + w + foot_half, y + foot_half], fill=0)
                    draw.rectangle([x - foot_half, y + h - foot_half, x + foot_half, y + h + foot_half], fill=0)
                    draw.rectangle([x + w - foot_half, y + h - foot_half, x + w + foot_half, y + h + foot_half], fill=0)
                else:
                    cv2.rectangle(debug_img_cv, (x, y), (x + w, y + h), (0, 0, 255), 2) # Red for REJECTED by AR
            # Else (if not even dimension range is met), don't draw or print as a candidate

        print("------------------------------------\n")

        if detected_tables_count == 0:
            print(f"No tables detected matching all criteria.")
            print(f"  - Dimensions: {min_table_dimension_pixels}x{min_table_dimension_pixels} to {max_table_dimension_pixels}x{max_table_dimension_pixels} pixels")
            print(f"  - Aspect ratio: {min_aspect_ratio:.2f} to {max_aspect_ratio:.2f}")
            print("Please adjust filter parameters based on the debug output above, or verify your 'map.pgm' file.")
        else:
            print(f"Successfully processed {detected_tables_count} tables.")

        img_pil.save(output_pgm_path)
        print(f"Modified map saved to: {output_pgm_path}")

        cv2.imwrite(debug_output_path, debug_img_cv)
        print(f"Debug contours image saved to: {debug_output_path}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_pgm_path}' not found. Make sure 'map.pgm' is in the same directory as the script.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    input_file = os.path.join(script_dir, "map.pgm")
    output_file = os.path.join(script_dir, "new_map.pgm")
    debug_file = os.path.join(script_dir, "debug_contours.png")

    min_table_dim = 30
    max_table_dim = 400
    min_ar = 1.0  
    max_ar = 2.0 

    foot_pixel_size = 5

    modify_map_replace_tables_with_feet(
        input_file,
        output_file,
        min_table_dimension_pixels=min_table_dim,
        max_table_dimension_pixels=max_table_dim,
        min_aspect_ratio=min_ar,
        max_aspect_ratio=max_ar,
        foot_size=foot_pixel_size,
        debug_output_path=debug_file
    )