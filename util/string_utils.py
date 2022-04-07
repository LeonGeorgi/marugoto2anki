def convert_lesson(lesson_string: str) -> str:
    return lesson_string.removesuffix("ス")


def calculate_topic(lesson: str):
    converted_lesson = convert_lesson(lesson)
    return str((int(converted_lesson) + 1) // 2)
