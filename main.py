import os
import sys
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import platform

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.database.db_manager import DatabaseManager
    from src.modules.auth import AuthManager
    from src.modules.license import LicenseManager
    from src.utils.helpers import StorageHelper
except ImportError:
    from database.db_manager import DatabaseManager
    from modules.auth import AuthManager
    from modules.license import LicenseManager
    from utils.helpers import StorageHelper


class LicenseScreen(MDScreen):
    """License activation screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        title = MDLabel(
            text='تفعيل الترخيص',
            halign='center',
            font_style='H4',
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(title)
        
        info = MDLabel(
            text='هذا التطبيق محمي برخصة فريدة لكل جهاز.\nيرجى تفعيل الترخيص قبل الاستمرار.',
            halign='center',
            theme_text_color='Secondary'
        )
        layout.add_widget(info)
        
        self.device_id = LicenseManager.generate_device_id()
        device_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(60),
            md_bg_color=(0.95, 0.95, 0.95, 1)
        )
        device_label = MDLabel(
            text='معرف الجهاز: %s' % self.device_id,
            halign='center',
            font_style='Caption'
        )
        device_card.add_widget(device_label)
        layout.add_widget(device_card)
        
        self.license_input = MDTextField(
            hint_text='أدخل مفتاح الترخيص',
            helper_text='XXXX-XXXX-XXXX-XXXX',
            helper_text_mode='on_focus',
            halign='center'
        )
        layout.add_widget(self.license_input)
        
        btn_layout = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50), pos_hint={'center_x': 0.5})
        btn_layout.add_widget(MDRaisedButton(text='إنشاء مفتاح', on_release=self.show_generated_key))
        btn_layout.add_widget(MDRaisedButton(text='تفعيل', on_release=self.activate_license))
        layout.add_widget(btn_layout)
        
        self.status_label = MDLabel(
            text='اضغط على "إنشاء مفتاح" لإنشاء مفتاح فريد لجهازك',
            halign='center',
            theme_text_color='Hint'
        )
        layout.add_widget(self.status_label)
        layout.add_widget(MDBoxLayout())
        self.add_widget(layout)
    
    def show_generated_key(self, *args):
        license_key = LicenseManager.generate_license_key(self.device_id)
        self.license_input.text = license_key
        self.status_label.text = 'تم إنشاء المفتاح. اضغط "تفعيل" لتفعيل التطبيق.'
        self.status_label.theme_text_color = 'Primary'
    
    def activate_license(self, *args):
        license_key = self.license_input.text.strip()
        if not license_key:
            self.status_label.text = 'يرجى إدخال مفتاح الترخيص'
            self.status_label.theme_text_color = 'Error'
            return
        success, message = LicenseManager.activate_license(license_key)
        if success:
            self.manager.current = 'login'
        else:
            self.status_label.text = message
            self.status_label.theme_text_color = 'Error'


class LoginScreen(MDScreen):
    """Login screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        layout.add_widget(MDLabel(text='نظام إدارة المدرسة', halign='center', font_style='H4', size_hint_y=None, height=dp(60)))
        layout.add_widget(MDLabel(text='تسجيل الدخول', halign='center', theme_text_color='Secondary'))
        
        card = MDCard(padding=dp(20), spacing=dp(15), size_hint_y=None, height=dp(280), elevation=4)
        card_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        self.username_input = MDTextField(hint_text='اسم المستخدم', icon_right='account')
        self.password_input = MDTextField(hint_text='كلمة المرور', icon_right='lock', password=True)
        card_layout.add_widget(self.username_input)
        card_layout.add_widget(self.password_input)
        
        card_layout.add_widget(MDRaisedButton(text='دخول', pos_hint={'center_x': 0.5}, on_release=self.login))
        card_layout.add_widget(MDLabel(text='البيانات الافتراضية: admin / admin123', halign='center', theme_text_color='Hint', font_style='Caption'))
        card.add_widget(card_layout)
        layout.add_widget(card)
        layout.add_widget(MDBoxLayout())
        self.add_widget(layout)
    
    def login(self, *args):
        username = self.username_input.text
        password = self.password_input.text
        if not username or not password:
            self.show_error('يرجى إدخال اسم المستخدم وكلمة المرور')
            return
        app = MDApp.get_running_app()
        success, message = app.auth.login(username, password)
        if success:
            self.manager.current = 'main'
            self.username_input.text = ''
            self.password_input.text = ''
        else:
            self.show_error(message)
    
    def show_error(self, message):
        dialog = MDDialog(title='خطأ', text=message,
                          buttons=[MDFlatButton(text='موافق', on_release=lambda x: dialog.dismiss())])
        dialog.open()


class StudentsTab(MDBoxLayout):
    """Students management tab content"""
    
    def __init__(self, **kwargs):
        self.dialog = None
        super().__init__(orientation='vertical', **kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.add_widget(MDToolbar(title='إدارة الطلاب', elevation=10,
                                   right_action_items=[['plus', lambda x: self.show_add_dialog()]]))
        self.scroll = MDScrollView()
        self.list_layout = MDList()
        self.scroll.add_widget(self.list_layout)
        self.add_widget(self.scroll)
        Clock.schedule_once(lambda dt: self.load_students(), 0.5)
    
    def load_students(self):
        self.list_layout.clear_widgets()
        app = MDApp.get_running_app()
        try:
            students = app.db.fetch_all('SELECT s.id, s.name, s.email, s.phone, c.name, s.status, s.parent_name, s.parent_phone FROM students s LEFT JOIN classes c ON s.class_id = c.id ORDER BY s.name')
        except Exception:
            students = []
        if not students:
            self.list_layout.add_widget(OneLineListItem(text='لا يوجد طلاب مسجلين'))
            return
        for student in students:
            item = ThreeLineListItem(
                text=student[1] or 'بدون اسم',
                secondary_text='الفصل: %s | الحالة: %s' % (student[4] or 'غير محدد', student[5] or 'active'),
                tertiary_text='ولي الأمر: %s | هاتف الولي: %s' % (student[6] or '-', student[7] or '-'),
                on_release=lambda x, s=student: self.show_options(s)
            )
            self.list_layout.add_widget(item)
    
    def show_options(self, student):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        
        def edit_callback(*args):
            nonlocal self
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None
            self.show_student_dialog(student)
        
        def delete_callback(*args):
            nonlocal self
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None
            self.confirm_delete(student)
        
        self.dialog = MDDialog(
            title='خيارات الطالب', text='الطالب: %s' % student[1],
            buttons=[
                MDFlatButton(text='تعديل', on_release=edit_callback),
                MDRaisedButton(text='حذف', md_bg_color=(0.9, 0.3, 0.3, 1), on_release=delete_callback),
                MDFlatButton(text='إغلاق', on_release=lambda x: self.dialog.dismiss() if self.dialog else None),
            ]
        )
        self.dialog.open()
    
    def confirm_delete(self, student):
        def do_delete(*args):
            app = MDApp.get_running_app()
            app.db.execute_query('DELETE FROM students WHERE id = ?', (student[0],))
            self.load_students()
            confirm_dialog.dismiss()
        confirm_dialog = MDDialog(
            title='تأكيد الحذف', text='هل أنت متأكد من حذف الطالب %s؟' % student[1],
            buttons=[MDFlatButton(text='إلغاء', on_release=lambda x: confirm_dialog.dismiss()),
                     MDRaisedButton(text='حذف', on_release=do_delete)]
        )
        confirm_dialog.open()
    
    def show_add_dialog(self, *args):
        self.show_student_dialog()
    
    def show_student_dialog(self, student=None):
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(400))
        name_input = MDTextField(hint_text='الاسم *', text=student[1] if student else '')
        email_input = MDTextField(hint_text='البريد الإلكتروني', text=student[2] if student else '')
        phone_input = MDTextField(hint_text='الهاتف', text=student[3] if student else '')
        parent_input = MDTextField(hint_text='اسم الولي', text=student[6] if student else '')
        parent_phone_input = MDTextField(hint_text='هاتف الولي', text=student[7] if student else '')
        for w in [name_input, email_input, phone_input, parent_input, parent_phone_input]:
            content.add_widget(w)
        
        dialog = MDDialog(
            title='تعديل طالب' if student else 'إضافة طالب', type='custom', content_cls=content,
            buttons=[
                MDFlatButton(text='إلغاء', on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text='حفظ', on_release=lambda x: self.save_student(dialog, name_input, email_input, phone_input, parent_input, parent_phone_input, student))
            ]
        )
        dialog.open()
    
    def save_student(self, dialog, name_input, email_input, phone_input, parent_input, parent_phone_input, student=None):
        if not name_input.text.strip():
            MDDialog(title='خطأ', text='الاسم مطلوب', buttons=[MDFlatButton(text='موافق', on_release=lambda x: dialog.dismiss())]).open()
            return
        app = MDApp.get_running_app()
        if student:
            app.db.execute_query('UPDATE students SET name=?, email=?, phone=?, parent_name=?, parent_phone=? WHERE id=?',
                                  (name_input.text.strip(), email_input.text.strip(), phone_input.text.strip(),
                                   parent_input.text.strip(), parent_phone_input.text.strip(), student[0]))
        else:
            class_result = app.db.fetch_one('SELECT id FROM classes LIMIT 1')
            class_id = class_result[0] if class_result else 1
            app.db.execute_query('INSERT INTO students (name, email, phone, class_id, parent_name, parent_phone, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                  (name_input.text.strip(), email_input.text.strip(), phone_input.text.strip(), class_id,
                                   parent_input.text.strip(), parent_phone_input.text.strip(), 'active'))
        self.load_students()
        dialog.dismiss()


class TeachersTab(MDBoxLayout):
    """Teachers management tab content"""
    
    def __init__(self, **kwargs):
        self.dialog = None
        super().__init__(orientation='vertical', **kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.add_widget(MDToolbar(title='إدارة المعلمين', elevation=10,
                                   right_action_items=[['plus', lambda x: self.show_add_dialog()]]))
        self.scroll = MDScrollView()
        self.list_layout = MDList()
        self.scroll.add_widget(self.list_layout)
        self.add_widget(self.scroll)
        Clock.schedule_once(lambda dt: self.load_teachers(), 0.5)
    
    def load_teachers(self):
        self.list_layout.clear_widgets()
        app = MDApp.get_running_app()
        try:
            teachers = app.db.fetch_all('SELECT id, name, email, phone, specialization FROM teachers ORDER BY name')
        except Exception:
            teachers = []
        if not teachers:
            self.list_layout.add_widget(OneLineListItem(text='لا يوجد معلمون مسجلون'))
            return
        for teacher in teachers:
            item = TwoLineListItem(
                text=teacher[1] or 'بدون اسم',
                secondary_text='التخصص: %s | الهاتف: %s' % (teacher[4] or '-', teacher[3] or '-'),
                on_release=lambda x, t=teacher: self.show_options(t)
            )
            self.list_layout.add_widget(item)
    
    def show_options(self, teacher):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        
        def edit_callback(*args):
            nonlocal self
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None
            self.show_teacher_dialog(teacher)
        
        def delete_callback(*args):
            nonlocal self
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None
            self.confirm_delete(teacher)
        
        self.dialog = MDDialog(
            title='خيارات المعلم', text='المعلم: %s' % teacher[1],
            buttons=[
                MDFlatButton(text='تعديل', on_release=edit_callback),
                MDRaisedButton(text='حذف', md_bg_color=(0.9, 0.3, 0.3, 1), on_release=delete_callback),
                MDFlatButton(text='إغلاق', on_release=lambda x: self.dialog.dismiss() if self.dialog else None),
            ]
        )
        self.dialog.open()
    
    def confirm_delete(self, teacher):
        def do_delete(*args):
            app = MDApp.get_running_app()
            app.db.execute_query('DELETE FROM teachers WHERE id = ?', (teacher[0],))
            self.load_teachers()
            confirm_dialog.dismiss()
        confirm_dialog = MDDialog(
            title='تأكيد الحذف', text='هل أنت متأكد من حذف المعلم %s؟' % teacher[1],
            buttons=[MDFlatButton(text='إلغاء', on_release=lambda x: confirm_dialog.dismiss()),
                     MDRaisedButton(text='حذف', on_release=do_delete)]
        )
        confirm_dialog.open()
    
    def show_add_dialog(self, *args):
        self.show_teacher_dialog()
    
    def show_teacher_dialog(self, teacher=None):
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(300))
        name_input = MDTextField(hint_text='الاسم *', text=teacher[1] if teacher else '')
        email_input = MDTextField(hint_text='البريد', text=teacher[2] if teacher else '')
        phone_input = MDTextField(hint_text='الهاتف', text=teacher[3] if teacher else '')
        spec_input = MDTextField(hint_text='التخصص', text=teacher[4] if teacher else '')
        for w in [name_input, email_input, phone_input, spec_input]:
            content.add_widget(w)
        
        dialog = MDDialog(
            title='تعديل معلم' if teacher else 'إضافة معلم', type='custom', content_cls=content,
            buttons=[
                MDFlatButton(text='إلغاء', on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text='حفظ', on_release=lambda x: self.save_teacher(dialog, name_input, email_input, phone_input, spec_input, teacher))
            ]
        )
        dialog.open()
    
    def save_teacher(self, dialog, name_input, email_input, phone_input, spec_input, teacher=None):
        if not name_input.text.strip():
            MDDialog(title='خطأ', text='الاسم مطلوب', buttons=[MDFlatButton(text='موافق', on_release=lambda x: dialog.dismiss())]).open()
            return
        app = MDApp.get_running_app()
        if teacher:
            app.db.execute_query('UPDATE teachers SET name=?, email=?, phone=?, specialization=? WHERE id=?',
                                  (name_input.text.strip(), email_input.text.strip(), phone_input.text.strip(),
                                   spec_input.text.strip(), teacher[0]))
        else:
            app.db.execute_query('INSERT INTO teachers (name, email, phone, specialization) VALUES (?, ?, ?, ?)',
                                  (name_input.text.strip(), email_input.text.strip(), phone_input.text.strip(), spec_input.text.strip()))
        self.load_teachers()
        dialog.dismiss()


class GradesTab(MDBoxLayout):
    """Grades management tab content"""
    
    def __init__(self, **kwargs):
        self.dialog = None
        self.menu = None
        super().__init__(orientation='vertical', **kwargs)
        self.build_ui()
    
    def build_ui(self):
        toolbar = MDToolbar(title='إدارة الدرجات', elevation=10,
                            right_action_items=[['plus', lambda x: self.show_add_dialog()]])
        self.add_widget(toolbar)
        
        self.scroll = MDScrollView()
        self.list_layout = MDList()
        self.scroll.add_widget(self.list_layout)
        self.add_widget(self.scroll)
        Clock.schedule_once(lambda dt: self.load_grades(), 0.5)
    
    def load_grades(self):
        self.list_layout.clear_widgets()
        app = MDApp.get_running_app()
        try:
            grades = app.db.fetch_all('SELECT g.id, s.name, g.subject, g.exam_type, g.score, g.total_marks FROM grades g JOIN students s ON g.student_id = s.id ORDER BY s.name')
        except Exception:
            grades = []
        if not grades:
            self.list_layout.add_widget(OneLineListItem(text='لا يوجد درجات مسجلة'))
            return
        for grade in grades:
            item = ThreeLineListItem(
                text='%s - %s' % (grade[1] or 'بدون اسم', grade[2] or '-'),
                secondary_text='الامتحان: %s' % (grade[3] or '-'),
                tertiary_text='الدرجة: %s/%s' % (grade[4] or 0, grade[5] or 100)
            )
            self.list_layout.add_widget(item)
    
    def show_add_dialog(self, *args):
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(350))
        app = MDApp.get_running_app()
        try:
            students = app.db.fetch_all('SELECT id, name FROM students')
        except Exception:
            students = []
        if not students:
            MDDialog(title='خطأ', text='لا يوجد طلاب مسجلون').open()
            return
        student_data = [(s[0], s[1]) for s in students]
        
        student_input = MDTextField(hint_text='الطالب (اختر من القائمة)')
        subject_input = MDTextField(hint_text='المادة')
        exam_input = MDTextField(hint_text='نوع الامتحان')
        score_input = MDTextField(hint_text='الدرجة', input_filter='float')
        total_input = MDTextField(hint_text='النهاية', text='100', input_filter='float')
        for w in [student_input, subject_input, exam_input, score_input, total_input]:
            content.add_widget(w)
        
        dialog = MDDialog(
            title='إضافة درجة', type='custom', content_cls=content,
            buttons=[
                MDFlatButton(text='إلغاء', on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text='حفظ', on_release=lambda x: self.save_grade(dialog, student_data, student_input, subject_input, exam_input, score_input, total_input))
            ]
        )
        dialog.open()
    
    def save_grade(self, dialog, student_data, student_input, subject_input, exam_input, score_input, total_input):
        try:
            student_id = student_data[0][0] if student_data else 1
            app = MDApp.get_running_app()
            app.db.execute_query('INSERT INTO grades (student_id, subject, exam_type, score, total_marks) VALUES (?, ?, ?, ?, ?)',
                                  (student_id, subject_input.text.strip(), exam_input.text.strip(),
                                   float(score_input.text or 0), float(total_input.text or 100)))
            self.load_grades()
            dialog.dismiss()
        except Exception as e:
            MDDialog(title='خطأ', text=str(e)).open()


class ReportsTab(MDBoxLayout):
    """Reports tab content"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.add_widget(MDToolbar(title='التقارير', elevation=10))
        self.report_type = MDTextField(hint_text='نوع التقرير', text='ملخص نتائج الفصل')
        self.add_widget(self.report_type)
        self.class_input = MDTextField(hint_text='اختر الفصل')
        self.add_widget(self.class_input)
        btn_layout = MDBoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10), padding=dp(10))
        btn_layout.add_widget(MDRaisedButton(text='إنشاء', on_release=self.generate_report))
        self.add_widget(btn_layout)
        self.report_label = MDLabel(
            text='اختر نوع التقرير والفصل ثم اضغط إنشاء',
            halign='center', theme_text_color='Secondary'
        )
        self.add_widget(self.report_label)
        self.add_widget(MDScrollView())
    
    def generate_report(self, *args):
        app = MDApp.get_running_app()
        class_name = self.class_input.text.strip()
        if not class_name:
            self.report_label.text = 'يرجى إدخال اسم الفصل'
            return
        class_info = app.db.fetch_one('SELECT id FROM classes WHERE name = ?', (class_name,))
        if not class_info:
            self.report_label.text = 'الفصل غير موجود'
            return
        class_id = class_info[0]
        students = app.db.fetch_all('SELECT id, name FROM students WHERE class_id = ?', (class_id,))
        lines = ['ملخص نتائج الفصل - %s\n' % class_name, 'اسم الطالب\t\tالمتوسط\tالحالة', '-' * 40]
        for student_id, student_name in students:
            grades = app.db.fetch_all('SELECT AVG(score) FROM grades WHERE student_id = ?', (student_id,))
            avg_score = grades[0][0] if grades and grades[0][0] else 0
            status = 'نجح' if avg_score >= 50 else 'رسب'
            lines.append('%s\t\t%.2f\t%s' % (student_name, avg_score, status))
        self.report_label.text = '\n'.join(lines) if lines else 'لا توجد بيانات'


class SettingsTab(MDBoxLayout):
    """Settings tab content"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(20), spacing=dp(15), **kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.add_widget(MDToolbar(title='الإعدادات', elevation=10))
        self.add_widget(MDLabel(text='تغيير كلمة المرور', font_style='H6'))
        self.old_pass = MDTextField(hint_text='كلمة المرور الحالية', password=True)
        self.new_pass = MDTextField(hint_text='كلمة المرور الجديدة', password=True)
        self.confirm_pass = MDTextField(hint_text='تأكيد كلمة المرور', password=True)
        for w in [self.old_pass, self.new_pass, self.confirm_pass]:
            self.add_widget(w)
        self.add_widget(MDRaisedButton(text='تغيير كلمة المرور', on_release=self.change_password))
        self.add_widget(MDRaisedButton(text='تسجيل الخروج', md_bg_color=(0.9, 0.3, 0.3, 1), on_release=self.logout))
        self.add_widget(MDBoxLayout())
    
    def change_password(self, *args):
        if not self.old_pass.text or not self.new_pass.text:
            self.show_message('يرجى ملء جميع الحقول')
            return
        if self.new_pass.text != self.confirm_pass.text:
            self.show_message('كلمات المرور الجديدة غير متطابقة')
            return
        app = MDApp.get_running_app()
        success, message = app.auth.change_password(self.old_pass.text, self.new_pass.text)
        if success:
            self.old_pass.text = ''
            self.new_pass.text = ''
            self.confirm_pass.text = ''
        self.show_message(message)
    
    def logout(self, *args):
        app = MDApp.get_running_app()
        app.auth.logout()
        app.root.current = 'login'
    
    def show_message(self, message):
        dialog = MDDialog(title='تنبيه', text=message,
                          buttons=[MDFlatButton(text='موافق', on_release=lambda x: dialog.dismiss())])
        dialog.open()


class MainScreen(MDScreen):
    """Main screen with bottom navigation"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        bottom_nav = MDBottomNavigation()
        
        students_item = MDBottomNavigationItem(name='students', text='الطلاب', icon='school')
        students_item.add_widget(StudentsTab())
        bottom_nav.add_widget(students_item)
        
        teachers_item = MDBottomNavigationItem(name='teachers', text='المعلمين', icon='account-tie')
        teachers_item.add_widget(TeachersTab())
        bottom_nav.add_widget(teachers_item)
        
        grades_item = MDBottomNavigationItem(name='grades', text='الدرجات', icon='chart-bar')
        grades_item.add_widget(GradesTab())
        bottom_nav.add_widget(grades_item)
        
        reports_item = MDBottomNavigationItem(name='reports', text='التقارير', icon='file-document')
        reports_item.add_widget(ReportsTab())
        bottom_nav.add_widget(reports_item)
        
        settings_item = MDBottomNavigationItem(name='settings', text='الإعدادات', icon='cog')
        settings_item.add_widget(SettingsTab())
        bottom_nav.add_widget(settings_item)
        
        layout.add_widget(bottom_nav)
        self.add_widget(layout)


class SchoolManagementApp(MDApp):
    """Main application class"""
    
    def build(self):
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.theme_style = 'Light'
        
        # Initialize database with dynamic path
        db_path = StorageHelper.get_storage_path('data/school.db')
        StorageHelper.ensure_dir(db_path)
        self.db = DatabaseManager(db_path)
        
        # Initialize auth
        self.auth = AuthManager(self.db)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Check license
        if not LicenseManager.is_licensed():
            sm.add_widget(LicenseScreen(name='license'))
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'license'
        else:
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'login'
        
        # Handle Android back button
        Window.bind(on_keyboard=self.on_keyboard)
        
        return sm
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard events including Android back button"""
        if key == 27:  # ESC key / Android back button
            sm = self.root
            if sm.current == 'main':
                # Exit confirmation on main screen
                dialog = MDDialog(
                    title='خروج',
                    text='هل تريد الخروج من التطبيق؟',
                    buttons=[
                        MDFlatButton(text='إلغاء', on_release=lambda x: dialog.dismiss()),
                        MDRaisedButton(text='خروج', on_release=lambda x: self.stop())
                    ]
                )
                dialog.open()
                return True
            elif sm.current == 'login':
                # Go back to license if not licensed
                if not LicenseManager.is_licensed():
                    sm.current = 'license'
                    return True
            return False
        return False
    
    def on_stop(self):
        """Clean up on app stop"""
        if hasattr(self, 'db') and self.db:
            self.db.close()


if __name__ == '__main__':
    SchoolManagementApp().run()
