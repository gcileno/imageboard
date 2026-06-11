import cv2
import numpy as np
from typing import Dict, Any, List
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

def process_to_grayscale(image_bytes: bytes) -> np.ndarray:
    """
    Converts raw image bytes to a grayscale numpy array.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    return img

def calculate_histogram(image: np.ndarray) -> np.ndarray:
    """
    Calculates the grayscale histogram of an image.
    Returns a normalized histogram.
    """
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

def get_basic_stats(image: np.ndarray) -> Dict[str, float]:
    """
    Returns basic statistical measures of the grayscale image:
    Mean intensity and Standard Deviation.
    """
    mean, std = cv2.meanStdDev(image)
    return {
        "mean": float(mean[0][0]),
        "std": float(std[0][0])
    }

def calculate_ssim(imageA: np.ndarray, imageB: np.ndarray) -> float:
    """
    Calculates the Structural Similarity Index (SSIM) between two images.
    Note: Both images must have the same dimensions.
    """
    if imageA.shape != imageB.shape:
        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    
    score, _ = ssim(imageA, imageB, full=True)
    return float(score)

def calculate_psnr(imageA: np.ndarray, imageB: np.ndarray) -> float:
    """
    Calculates the Peak Signal-to-Noise Ratio (PSNR) between two images.
    """
    if imageA.shape != imageB.shape:
        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    
    return float(psnr(imageA, imageB))

def calculate_contrast(image: np.ndarray) -> float:
    """
    Calculates the contrast of the image (standard deviation of pixels).
    """
    return float(np.std(image))

def calculate_mean_intensity(image: np.ndarray) -> float:
    """
    Calculates the mean intensity (brightness) of the image.
    """
    return float(np.mean(image))

def calculate_sharpness(image: np.ndarray) -> float:
    """
    Calculates the sharpness of the image using the Laplacian variance.
    Also known as the Tenengrad method for focus measure.
    """
    return float(cv2.Laplacian(image, cv2.CV_64F).var())

def calculate_snr(image: np.ndarray) -> float:
    """
    Calculates a simple Signal-to-Noise Ratio (mean / std).
    """
    mean = np.mean(image)
    std = np.std(image)
    if std == 0:
        return 0.0
    return float(mean / std)

def draw_grid_overlay(image: np.ndarray, grid_size: int) -> np.ndarray:
    """
    Draws a grid on the image for visualization.
    Returns a copy of the image with the grid drawn.
    """
    # Convert to BGR so we can draw colored lines (or just keep grayscale if preferred)
    grid_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    h, w = image.shape
    cell_h, cell_w = h // grid_size, w // grid_size

    color = (0, 255, 0) # Green lines
    thickness = 1

    for row in range(1, grid_size):
        y = row * cell_h
        cv2.line(grid_img, (0, y), (w, y), color, thickness)

    for col in range(1, grid_size):
        x = col * cell_w
        cv2.line(grid_img, (x, 0), (x, h), color, thickness)

    return grid_img

def analyze_grid_stats(image: np.ndarray, grid_size: int) -> List[Dict[str, Any]]:
    """
    Divides the image into a grid of (grid_size x grid_size) cells
    and calculates statistics for each cell.
    """
    h, w = image.shape
    cell_h, cell_w = h // grid_size, w // grid_size
    
    grid_results = []
    for row in range(grid_size):
        for col in range(grid_size):
            y1, y2 = row * cell_h, (row + 1) * cell_h
            x1, x2 = col * cell_w, (col + 1) * cell_w
            
            cell = image[y1:y2, x1:x2]
            stats = get_basic_stats(cell)
            stats.update({
                "sharpness": calculate_sharpness(cell),
                "snr": calculate_snr(cell),
                "cell": f"({row}, {col})",
                "row": row,
                "col": col
            })
            grid_results.append(stats)
            
    return grid_results
