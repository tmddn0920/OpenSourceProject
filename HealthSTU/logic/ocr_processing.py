from PIL import Image, ImageOps, ImageFilter
import pytesseract

# 이미지 가공 준비
def preprocess_image(image_path):
    try:
        image = Image.open(image_path)
        image = ImageOps.grayscale(image)
        image = image.filter(ImageFilter.SHARPEN)
        image = image.point(lambda x: 0 if x < 128 else 255)
        return image
    except Exception as e:
        raise ValueError(f"이미지 전처리 중 오류가 발생했습니다: {e}")

# 이미지 가공 준비
def process_inbody_image(image_path):
    try:
        image = preprocess_image(image_path)
        custom_config = '--psm 6'
        return pytesseract.image_to_string(image, lang="kor", config=custom_config)
    except Exception as e:
        raise ValueError(f"OCR 처리 중 오류가 발생했습니다: {e}")

# 데이터 추출
def parse_inbody_data(ocr_text):
    import re
    try:
        matches = re.findall(r"[가-힣]+\s*([\d]+\.\d+)", ocr_text)
        numbers = [float(num) for num in matches]
        if len(numbers) >= 3:
            return {
                "weight_kg": numbers[0],
                "skeletal_muscle_mass": numbers[1],
                "body_fat_mass": numbers[2],
            }
        return None
    except Exception as e:
        raise ValueError(f"데이터 파싱 중 오류가 발생했습니다: {e}")
