import os
import re
from ..ANSI_COLORS import ANSI; C = ANSI()
from ..MODULES import IMPORT; M = IMPORT()

C_Line = f"{C.CC}{'_' * 61}"

def Energy_Smali_Patch(smali_folders):
    """
    Patch untuk n1master (com.aicyteadev.n1master):
    1. Bypass isPro() -> always return true  (Energy Unlimited)
    2. Bypass hasEnoughEnergy() -> always return true
    3. DummyAdDialog countdown timer -> 1ms (instant reward, no need to watch ad)
    """
    print(f"\n{C.CC}{'_' * 61}\n")
    print(f"\n{C.S} Energy Patch {C.E} {C.OG}->  {C.P}Scanning Smali Files {C.G}...", end="", flush=True)

    Smali_Paths = []
    for smali_folder in smali_folders:
        for root, _, files in M.os.walk(smali_folder):
            for file in files:
                if file.endswith('.smali'):
                    Smali_Paths.append(M.os.path.join(root, file))

    print(f" {C.G} OK", flush=True)
    print(f'\n{C_Line}\n')

    # NOTE: Smali yang dihasilkan apktool memiliki blank line (\n\n) di antara instruksi
    patches = [
        # PATCH 1: isPro() -> always return true (Energy Unlimited)
        (
            re.compile(
                r'(\.method public final isPro\(\)Z\n    \.locals \d+\n\n(?:    \.line \d+\n)?    )'
                r'iget-boolean ([vp]\d+), p0, L[^;]+;->isPro:Z\n\n    return \2\n(\.end method)',
                re.MULTILINE
            ),
            r'\1const/4 v0, 0x1\n\n    return v0\n\3',
            "isPro() -> always return true [Energy Unlimited]",
        ),
        # PATCH 2: hasEnoughEnergy() -> always return true

        # PATCH 3: DummyAdDialog countdown timer -> 1ms (instant reward)
        # Mengubah delay dari 1000ms (0x3E8) menjadi 1ms (0x1)
        # Efek: dialog iklan langsung selesai tanpa perlu menunggu

    ]

    total_patched = 0

    for pattern, replacement, description in patches:
        Count_Applied = 0
        Applied_Files = set()

        for file_path in Smali_Paths:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                new_content = pattern.sub(replacement, content)
                if new_content != content:
                    Applied_Files.add(file_path)
                    Count_Applied += 1
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(new_content)
            except Exception:
                pass

        if Count_Applied > 0:
            total_patched += Count_Applied
            print(f"\n{C.S} Tag {C.E} {C.G}{description}")
            for fp in Applied_Files:
                print(f"{C.G}  |\n  +---- {C.CC}~{C.G}$ {C.Y}{M.os.path.basename(fp)} {C.G} OK")
            print(f"\n{C.S} Applied {C.E} {C.OG}-> {C.PN}{Count_Applied} {C.C}file(s) {C.G} OK\n{C_Line}\n")
        else:
            print(f"\n{C.WARN} {description} -> {C.Y}Not matched (different version or already patched)\n")

    if total_patched == 0:
        print(f"\n{C.WARN} Energy Patch: No patterns matched. Check APK version.\n")
    else:
        print(f"\n{C.S} Energy Patch Complete {C.E} {C.OG}-> {C.PN}{total_patched} {C.C}total patches {C.G} OK\n")
