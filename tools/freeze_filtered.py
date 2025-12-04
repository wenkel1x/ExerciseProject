import re
import subprocess

# 读取 requirements.txt 中的包名（忽略版本和注释）
def get_required_packages(file_path):
    packages = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('-r'):
                included_file = line.split(maxsplit=1)[1]
                packages += get_required_packages(included_file)
            elif line.startswith('--'):
                packages.append(line)
            else:
                pkg = re.split(r'\s+#', line)[0].strip()
                packages.append(pkg)
    return packages

# 获取 pip freeze 的结果
freeze = subprocess.check_output(['pip', 'freeze'], text=True).splitlines()
freeze_dict = {}
for line in freeze:
    if '==' in line:
        name, version = line.split('==', 1)
        freeze_dict[name.lower()] = version

# 处理 requirements.txt
required = get_required_packages('requirements.txt')
output = []

for pkg in required:
    if pkg.startswith('--'):
        output.append(pkg)
        continue
    base = re.split(r'[<>=!~]', pkg)[0].strip()
    base_clean = re.sub(r'\[.*\]', '', base).lower()
    extras = re.search(r'(\[.*\])', pkg)
    extras_str = extras.group(1) if extras else ''
    if base_clean in freeze_dict:
        version = freeze_dict[base_clean]
        output.append(f"{base}{extras_str}=={version}")
    else:
        print(f"未找到已安装的包:{pkg}")

# 写入结果
with open('requirement_convert.txt', 'w') as f:
    f.write('\n'.join(output))

print("requirement_convert.txt done")