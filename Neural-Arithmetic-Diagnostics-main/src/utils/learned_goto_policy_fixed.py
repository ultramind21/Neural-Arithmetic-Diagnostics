#!/usr/bin/env python3
"""
LEARNED GOTO POLICY - Fixed Version
تطبيق القاعدة المكتشفة من Teacher
"""

def learned_goto(cursor, done_mask, num_cols=12):
    """
    القاعدة النهائية المكتشفة:
    
    بحث عن أول وآخر عمود غير مكتمل أولاً
    ثم تطبيق القاعدة بترتيب:
    
    1) إذا num_nondone == 0: ابق في المكان
    2) إذا done_mask[cursor] == 1: ارجع واحد للخلف
    3) إذا num_nondone == 1: اذهب للعمود الوحيد غير المكتمل
    4) إذا cursor == leftmost_nondone: اذهب إلى rightmost_nondone
    5) وإلا: اذهب إلى leftmost_nondone
    
    Args:
        cursor: الموقع الحالي
        done_mask: قائمة بقيمة 1.0 للأعمدة المكتملة و 0.0 للأخرى
        num_cols: عدد الأعمدة (افتراضي 12)
    
    Returns:
        العمود الذي يجب الانتقال إليه
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
    
    # تطبيق القاعدة بالترتيب الصحيح
    if num_nondone == 0:
        # لا يوجد عمل، ابق في المكان
        return cursor
    elif num_nondone == 1:
        # عمود واحد فقط، اذهب إليه (الأولوية رقم 1)
        return leftmost_nondone if leftmost_nondone is not None else cursor
    elif done_mask[cursor] == 1.0:
        # العمود الحالي متم وهناك أكثر من واحد متبقي، ارجع واحد
        return cursor - 1 if cursor > 0 else 0
    elif cursor == leftmost_nondone and leftmost_nondone is not None:
        # cursor في أول عمود يحتاج عمل، اذهب إلى آخر واحد
        return rightmost_nondone if rightmost_nondone is not None else cursor
    else:
        # خلاف ذلك (cursor في منتصف)، اذهب إلى leftmost
        return leftmost_nondone if leftmost_nondone is not None else cursor
