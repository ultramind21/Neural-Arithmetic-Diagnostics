#!/usr/bin/env python3
"""
LEARNED GOTO POLICY
تطبيق القاعدة المكتشفة من Teacher
96.4% تطابق مع Teacher GOTO
"""

def learned_goto(cursor, done_mask, num_cols=12):
    """
    القاعدة النهائية المكتشفة (مع ترتيب صحيح):
    
    1) إذا done_mask[cursor] == 1: ارجع واحد للخلف (الأولوية القصوى)
    2) إذا num_nondone == 0: ابق في المكان
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
    
    # **أولاً**: إذا كان العمود الحالي متم، ارجع واحد للخلف
    if done_mask[cursor] == 1.0:
        return cursor - 1 if cursor > 0 else 0
    
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
    
    # تطبيق القاعدة
    if num_nondone == 0:
        # لا يوجد عمل، ابق في المكان
        return cursor
    elif num_nondone == 1:
        # عمود واحد فقط، اذهب إليه
        return leftmost_nondone if leftmost_nondone is not None else cursor
    elif cursor == leftmost_nondone and leftmost_nondone is not None:
        # cursor في أول عمود يحتاج عمل، اذهب إلى آخر واحد
        return rightmost_nondone if rightmost_nondone is not None else cursor
    else:
        # خلاف ذلك، اذهب إلى leftmost
        return leftmost_nondone if leftmost_nondone is not None else cursor


if __name__ == "__main__":
    # توضيح سريع
    print("Learned GOTO Policy - Quick Test")
    print("=" * 50)
    
    # حالة 1: عمود واحد غير مكتمل
    done_mask = [1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    result = learned_goto(0, done_mask)
    print(f"Done mask: {['✓' if x else '○' for x in done_mask]}")
    print(f"Cursor: 0 → GOTO: {result} (expected: 1)")
    print()
    
    # حالة 2: cursor == leftmost_nondone
    done_mask = [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    result = learned_goto(1, done_mask)
    print(f"Done mask: {['✓' if x else '○' for x in done_mask]}")
    print(f"Cursor: 1 → GOTO: {result} (expected: 3, rightmost_nondone)")
    print()
    
    # حالة 3: cursor متم، ارجع واحد
    done_mask = [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    result = learned_goto(3, done_mask)
    print(f"Done mask: {['✓' if x else '○' for x in done_mask]}")
    print(f"Cursor: 3 → GOTO: {result} (expected: 2, back one)")
