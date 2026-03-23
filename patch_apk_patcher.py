import re

file_path = '/home/pc/Music/ApkPatcher-Modified/ApkPatcher-main/ApkPatcher/APK_PATCHER.py'
with open(file_path, 'r') as f:
    content = f.read()

# Add import
if 'from .Patch.Energy_Patch import Energy_Smali_Patch' not in content:
    content = content.replace('from .Patch.Ads_Patch import Ads_Smali_Patch', 
                              'from .Patch.Ads_Patch import Ads_Smali_Patch\nfrom .Patch.Energy_Patch import Energy_Smali_Patch')

# Add function call
if 'Energy_Smali_Patch(smali_folders)' not in content:
    content = content.replace('if args.Remove_Ads:\n            Ads_Smali_Patch(smali_folders)', 
                              'if args.Remove_Ads:\n            Ads_Smali_Patch(smali_folders)\n            Energy_Smali_Patch(smali_folders)')

with open(file_path, 'w') as f:
    f.write(content)

print("APK_PATCHER.py updated successfully")
