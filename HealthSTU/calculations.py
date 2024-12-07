def calculate_bmi(height, weight):
    """BMI 계산"""
    if height <= 0 or weight <= 0:
        raise ValueError("키와 체중은 0보다 큰 값이어야 합니다.")
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def calculate_body_fat_percentage(weight, body_fat_mass):
    """체지방률 계산"""
    if weight <= 0 or body_fat_mass < 0:
        raise ValueError("체중은 0보다 커야 하며, 체지방량은 음수가 될 수 없습니다.")
    return round((body_fat_mass / weight) * 100, 2)

def classify_body_type(bmi, body_fat_percentage):
    """BMI와 체지방률을 기반으로 체형 분류"""
    if bmi > 23.0:
        if body_fat_percentage > 16.0:
            return "비만"
        elif 13.0 < body_fat_percentage <= 16.0:
            return "과체중"
        else:
            return "운동선수"
    elif 20.75 <= bmi <= 23.0:
        if body_fat_percentage > 16.0:
            return "경도 비만"
        elif 13.0 < body_fat_percentage <= 16.0:
            return "적정"
        else:
            return "근육형"
    elif 18.5 <= bmi < 20.75:
        if body_fat_percentage > 16.0:
            return "마른 비만"
        elif 13.0 < body_fat_percentage <= 16.0:
            return "적정"
        elif 10.0 < body_fat_percentage <= 13.0:
            return "날씬"
        else:
            return "근육형 날씬"
    else:
        if body_fat_percentage > 16.0:
            return "마른 비만"
        elif 10.0 < body_fat_percentage <= 16.0:
            return "약간 마름"
        else:
            return "마름"