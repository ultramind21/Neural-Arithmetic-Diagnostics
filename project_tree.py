import os

# المجلدات المراد تخطيها
SKIP_FOLDERS = {'.git', '__pycache__', '.venv', 'node_modules', '.env', '.idea', 'venv', '.pytest_cache', 'dist', 'build'}

def get_file_size(filepath):
    """الحصول على حجم الملف بصيغة قابلة للقراءة"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    except:
        return "?"

def build_tree(directory, prefix="", is_root=False, show_sizes=False, file_extensions=None):
    """
    بناء هيكل المجلدات والملفات بشكل هرمي مشابه لأمر tree في Windows.
    
    Args:
        directory: المسار المراد البحث فيه
        prefix: البادئة للمحاذاة
        is_root: هل هذا المجلد الجذر
        show_sizes: عرض حجم الملفات
        file_extensions: قائمة الامتدادات المسموحة (None = الكل)
    """
    lines = []
    try:
        items = os.listdir(directory)
    except PermissionError:
        return lines

    # فرز المجلدات أولاً ثم الملفات
    folders = sorted([
        item for item in items 
        if os.path.isdir(os.path.join(directory, item)) and item not in SKIP_FOLDERS
    ])
    files = sorted([item for item in items if os.path.isfile(os.path.join(directory, item))])
    
    # تصفية الملفات حسب الامتداد إذا طُلب
    if file_extensions:
        files = [f for f in files if any(f.endswith(ext) for ext in file_extensions)]

    # دمج المجلدات والملفات
    all_items = folders + files

    for i, item in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            # إذا كان مجلد
            if is_root:
                lines.append(f"{prefix}+---{item}/")
                lines.extend(build_tree(item_path, prefix + "|   ", False, show_sizes, file_extensions))
            elif is_last:
                lines.append(f"{prefix}\\---{item}/")
                lines.extend(build_tree(item_path, prefix + "    ", False, show_sizes, file_extensions))
            else:
                lines.append(f"{prefix}+---{item}/")
                lines.extend(build_tree(item_path, prefix + "|   ", False, show_sizes, file_extensions))
        else:
            # إذا كان ملف
            file_info = item
            if show_sizes:
                size = get_file_size(item_path)
                file_info = f"{item} ({size})"
            
            if is_root:
                lines.append(f"{prefix}|   {file_info}")
            elif is_last:
                lines.append(f"{prefix}\\---{file_info}")
            else:
                lines.append(f"{prefix}+---{file_info}")

    return lines

def count_items(directory, file_extensions=None):
    """عد الملفات والمجلدات"""
    total_files = 0
    total_folders = 0
    
    for root, dirs, files in os.walk(directory):
        # تخطي المجلدات المحظورة
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]
        
        total_folders += len(dirs)
        
        if file_extensions:
            total_files += len([f for f in files if any(f.endswith(ext) for ext in file_extensions)])
        else:
            total_files += len(files)
    
    return total_files, total_folders

if __name__ == "__main__":
    # الحصول على المسار الحالي
    current_dir = os.getcwd()
    
    # خيارات العرض
    show_file_sizes = True  # عرض حجم الملفات
    file_extensions = None  # None = عرض جميع الملفات، أو ["*.py", "*.txt"] لتصفية معينة
    
    # بناء المحتوى
    output_lines = []
    output_lines.append(f"{'='*60}")
    output_lines.append(f"Folder PATH listing for: {current_dir}")
    output_lines.append(f"{'='*60}")
    output_lines.append("")
    
    # عد العناصر
    file_count, folder_count = count_items(current_dir, file_extensions)
    output_lines.append(f"Total Folders: {folder_count}")
    output_lines.append(f"Total Files: {file_count}")
    output_lines.append("")
    output_lines.append(f"{os.path.basename(current_dir)}/")
    output_lines.append("")
    
    # بناء الشجرة
    output_lines.extend(build_tree(current_dir, "", True, show_file_sizes, file_extensions))
    
    # كتابة إلى ملف
    output_file = "project_tree_output.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print(f"✓ تم حفظ هيكل المشروع في الملف: {output_file}")
        print(f"✓ عدد المجلدات: {folder_count}")
        print(f"✓ عدد الملفات: {file_count}")
    except Exception as e:
        print(f"✗ حدث خطأ: {e}")
