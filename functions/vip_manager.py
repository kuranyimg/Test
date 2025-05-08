import json
from typing import List

VIP_FILE = "vips.json"  # اسم الملف الذي سنخزن فيه الـ VIP

class VIPManager:
    def __init__(self):
        self.vips = self.load_vips()  # تحميل قائمة الـ VIP عند بداية التشغيل

    def load_vips(self) -> List[str]:
        """تحميل الـ VIP من ملف JSON"""
        try:
            with open(VIP_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # إذا لم يتم العثور على الملف، إرجاع قائمة فارغة
            return []

    def save_vips(self) -> None:
        """حفظ قائمة الـ VIP في ملف JSON"""
        with open(VIP_FILE, "w") as file:
            json.dump(self.vips, file)
    
    def add_vip(self, user_id: str) -> None:
        """إضافة مستخدم إلى قائمة الـ VIP"""
        if user_id not in self.vips:
            self.vips.append(user_id)
            self.save_vips()

    def remove_vip(self, user_id: str) -> None:
        """إزالة مستخدم من قائمة الـ VIP"""
        if user_id in self.vips:
            self.vips.remove(user_id)
            self.save_vips()

    def is_vip(self, user_id: str) -> bool:
        """التحقق ما إذا كان المستخدم VIP"""
        return user_id in self.vips
