import json
import threading
import shutil
import os

# تعريف المتغيرات التي سنستخدمها لتخزين المواقع
data_mappings = {
    "bot_location": {},
    "floor1_location": {},
    "floor2_location": {},
    "floor3_location": {},
}

# تحديث المتغيرات في البيئة العامة
globals().update(data_mappings)

# حفظ البيانات في ملفات JSON
def save_data():
    try:
        total, used, free = shutil.disk_usage("/")
        if free < 1024 * 1024:
            print("Not enough disk space to save data.")
            return

        for var_name in data_mappings.keys():
            filename = f"{var_name}.json"
            try:
                with open(filename, "w") as f:
                    json.dump(globals()[var_name], f)
            except Exception as e:
                print(f"Error saving {filename}: {e}")

    except Exception as e:
        print("Disk usage check failed:", e)

    # إعادة جدولة الحفظ التلقائي بعد 100 ثانية
    threading.Timer(100, save_data).start()

# تحميل البيانات من ملفات JSON عند التشغيل
def load_data():
    for var_name, default_value in data_mappings.items():
        filename = f"{var_name}.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    globals()[var_name] = json.load(f)
            else:
                globals()[var_name] = default_value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {filename}: {e}")
            globals()[var_name] = default_value

# تحميل البيانات عند بدء تشغيل البوت
load_data()

# بدء الحفظ التلقائي
save_data()
