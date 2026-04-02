"""اختبار الـ parser الجديد على الـ raw output الموجود"""
import re
from pathlib import Path

# قراءة الـ raw output
output_file = Path('step1d_killer_test_raw_output.txt')
output_text = output_file.read_text()

# Parser الجديد
def parse_patterns(output_text):
    lines = output_text.splitlines()
    parsed = {}
    current_pattern = None

    for line in lines:
        line_stripped = line.strip()
        
        # Match "Testing: <pattern_description>"
        m_pat = re.match(r"Testing:\s*(.+)", line_stripped)
        if m_pat:
            current_pattern = m_pat.group(1)
            parsed[current_pattern] = {}
            continue

        if current_pattern is None:
            continue

        # Match "Digit Accuracy: XX.XX%"
        m_digit = re.match(r"Digit Accuracy:\s*([0-9.]+)%", line_stripped)
        if m_digit:
            parsed[current_pattern]["digit_accuracy"] = float(m_digit.group(1))
            continue

        # Match "Carry Accuracy: XX.XX%"
        m_carry = re.match(r"Carry Accuracy:\s*([0-9.]+)%", line_stripped)
        if m_carry:
            parsed[current_pattern]["carry_accuracy"] = float(m_carry.group(1))
            continue

        # Match "Exact Match: XX.XX%"
        m_exact = re.match(r"Exact Match:\s*([0-9.]+)%", line_stripped)
        if m_exact:
            parsed[current_pattern]["exact_match"] = float(m_exact.group(1))
            continue

    return parsed

# اختبار الـ parser
parsed = parse_patterns(output_text)

print("✓ تم استخراج الأنماط:")
print()
for pattern_name, metrics in parsed.items():
    print(f"  {pattern_name}")
    for k, v in metrics.items():
        print(f"    {k}: {v:.2f}%")
    print()

print(f"\nعدد الأنماط المستخرجة: {len(parsed)}")
