#!/usr/bin/env python3
"""
LEARNED GOTO POLICY - Verified Version (96.4% accuracy)
القاعدة المكتشفة التي طابقت 96.4% من قرارات Teacher
"""

def learned_goto(cursor, done_mask, num_cols=12):
    """
    القاعدة النهائية - الترتيب الدقيق:
    
    1) إذا num_nondone == 0: stay
    2) إذا num_nondone == 1: go to the only one
    3) إذا cursor == leftmost_nondone: jump to rightmost
    4) إذا done_mask[cursor] == 1: go back one
    5) else: go to leftmost
    
    96.4% accuracy test on Teacher GOTO decisions
    """
    
    # بحث عن أول وآخر عمود غير مكتمل
    leftmost_nondone = None
    for i in range(num_cols):
        if done_mask[i] == 0.0:
            leftmost_nondone = i
            break
    
    rightmost_nondone = None
    for i in range(num_cols - 1, -1, -1):
        if done_mask[i] == 0.0:
            rightmost_nondone = i
            break
    
    # عدد الأعمدة غير المكتملة
    num_nondone = sum(1 for dm in done_mask if dm == 0.0)
    
    # تطبيق القاعدة بالترتيب الصحيح (كما في final_rule_test.py التي أعطت 96.4%)
    if num_nondone == 0:
        # لا يوجد عمل، ابق في المكان
        return cursor
    elif num_nondone == 1:
        # عمود واحد فقط يحتاج عمل، اذهب إليه
        return leftmost_nondone if leftmost_nondone is not None else cursor
    elif cursor == leftmost_nondone and leftmost_nondone is not None:
        # cursor في أول عمود يحتاج عمل، اذهب إلى آخر واحد
        return rightmost_nondone if rightmost_nondone is not None else cursor
    elif done_mask[cursor] == 1.0:
        # العمود الحالي متم، ارجع واحد
        return cursor - 1 if cursor > 0 else 0
    else:
        # خلاف ذلك، اذهب إلى leftmost
        return leftmost_nondone if leftmost_nondone is not None else cursor
