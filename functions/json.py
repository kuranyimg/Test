import json
import threading
import shutil

# تعريف المتغيرات التي سيتم حفظها في JSON
data_mappings = {
    "bot_location": {}  # لحفظ موقع البوت
}

# ربط المتغيرات العامة بالمحتوى
globals().update(data_mappings)

def save_data():
    """حفظ كل البيانات في ملفات JSON."""
    total, used, free = shutil.disk_usage("/")
    if free < 1024 * 1024:
        print("لا توجد مساحة كافية على القرص لحفظ البيانات.")
        return

    for var_name in data_mappings.keys():
        filename = f"{var_name}.json"
        try:
            with open(filename, "w") as f:
                json.dump(globals()[var_name], f)
        except Exception as e:
            print(f"خطأ أثناء حفظ {filename}: {e}")

    # إعادة تشغيل الحفظ كل 100 ثانية
    threading.Timer(100, save_data).start()

def load_data():
    """تحميل كل البيانات من ملفات JSON."""
    for var_name, default_value in data_mappings.items():
        filename = f"{var_name}.json"
        try:
            with open(filename, "r") as f:
                globals()[var_name] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            globals()[var_name] = default_value

# تحميل وحفظ البيانات عند التشغيل
load_data()
save_data()
