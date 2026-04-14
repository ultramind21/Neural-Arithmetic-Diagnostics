"""
action_factorizer.py - تحويل بين (column, micro_action) و action_id
"""

from typing import Tuple

# Micro-action enum
MICRO_ADD1 = 0
MICRO_ADD5 = 1
MICRO_DONE = 2
MICRO_GOTO = 3  # Special: navigate to column without operation
NUM_MICRO = 4


def encode_factored_action(column: int, micro_action: int, num_columns: int) -> int:
    """
    تحويل (column, micro_action) → action_id
    
    الفكرة:
    - نرسل GOTO_column أولاً
    - ثم micro_action بعده
    
    لكن بما أننا نريد action واحد في step واحد:
    نخزن state: إذا كنا بحاجة GOTO، نرسله في هذه الخطوة
    وإلا نرسل الـ micro_action
    
    للبساطة: نترجم مباشرة:
    - إذا micro == ADD1: action = ADD1 (W)
    - إذا micro == ADD5: action = ADD5 (W+1)
    - إذا micro == DONE: action = DONE (W+2)
    والـ column مسؤول عن state البيئة بنفسها
    """
    if micro_action == MICRO_ADD1:
        return num_columns  # ADD1
    elif micro_action == MICRO_ADD5:
        return num_columns + 1  # ADD5
    elif micro_action == MICRO_DONE:
        return num_columns + 2  # DONE
    else:
        raise ValueError(f"Unknown micro_action: {micro_action}")


def decode_factored_action(action: int, num_columns: int) -> Tuple[int, int]:
    """
    تحويل action_id → (column, micro_action)
    
    الـ action id يحدد micro_action فقط
    الـ column يجب نأخذه من البيئة (cursor الحالي)
    """
    if action < num_columns:
        # GOTO action - ليس micro، ده selection مباشر للعمود
        return (action, None)  # Column هو رقم الـ GOTO
    elif action == num_columns:
        return (None, MICRO_ADD1)  # Micro is ADD1, column من البيئة
    elif action == num_columns + 1:
        return (None, MICRO_ADD5)
    elif action == num_columns + 2:
        return (None, MICRO_DONE)
    else:
        raise ValueError(f"Unknown action: {action}")


def micro_to_string(micro: int) -> str:
    """Convert micro_action to string."""
    if micro == MICRO_ADD1:
        return "ADD1"
    elif micro == MICRO_ADD5:
        return "ADD5"
    elif micro == MICRO_DONE:
        return "DONE"
    return "UNKNOWN"


def teacher_action_to_factored(action: int, num_columns: int) -> Tuple[int, int]:
    """
    تحويل teacher action → (column, micro_action)
    
    Teacher يطلع action من البيئة الحالية
    نستخرج منها الـ column والـ micro
    """
    col, micro = decode_factored_action(action, num_columns)
    
    if col is not None:
        # GOTO action
        return (col, MICRO_DONE)  # Dummy micro، الـ column محدد
    else:
        # Micro action، لكن نحتاج العمود الحالي من البيئة state
        # هذا سيجي من البيئة نفسها (cursor)
        return (None, micro)  # Column سيحدد من state الحالي
