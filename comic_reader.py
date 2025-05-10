import os
import json
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.utils import platform

# 配置应用窗口
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')
Config.set('kivy', 'default_font', ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC'])

# 支持的图片格式
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')


class ComicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_page = 0
        self.images = []
        self.scatter = None
        self.image = None
        self.comic_path = None

    def load_comic(self, comic_path):
        self.comic_path = comic_path
        self.images = []

        # 获取目录下所有支持的图片文件
        for file in sorted(os.listdir(comic_path)):
            if file.lower().endswith(SUPPORTED_FORMATS):
                self.images.append(os.path.join(comic_path, file))

        if not self.images:
            popup = Popup(title="错误", content=Label(text="该文件夹中没有支持的图片格式！"), size_hint=(0.8, 0.4))
            popup.open()
            return

        self.current_page = 0
        self.show_image()

    def show_image(self):
        if not self.images:
            return

        # 清除当前图片
        if self.scatter:
            self.remove_widget(self.scatter)

        # 创建新的图片组件
        self.image = Image(source=self.images[self.current_page])
        self.scatter = Scatter(scale=1, do_rotation=False, size_hint=(None, None))
        self.scatter.add_widget(self.image)

        # 计算图片显示尺寸，保持宽高比
        win_ratio = Window.width / Window.height
        img_ratio = self.image.texture_size[0] / self.image.texture_size[1]

        if img_ratio > win_ratio:
            self.scatter.size = (Window.width, Window.width / img_ratio)
        else:
            self.scatter.size = (Window.height * img_ratio, Window.height)

        self.scatter.pos = ((Window.width - self.scatter.width) / 2,
                            (Window.height - self.scatter.height) / 2)
        self.add_widget(self.scatter)

        # 更新标题
        self.manager.get_screen('main').update_title(
            f"{os.path.basename(self.comic_path)} ({self.current_page + 1}/{len(self.images)})")

    def next_page(self):
        if self.current_page < len(self.images) - 1:
            self.current_page += 1
            self.show_image()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_image()

    def on_touch_up(self, touch):
        # 检测滑动手势
        if touch.grab_current is None:
            if touch.dx > 50:  # 右滑
                self.prev_page()
                return True
            elif touch.dx < -50:  # 左滑
                self.next_page()
                return True
        return super().on_touch_up(touch)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comic_folders = []
        self.load_saved_folders()

        # 创建UI组件
        self.layout = FloatLayout()

        # 标题
        self.title_label = Label(
            text="漫画阅读器",
            font_size=24,
            pos_hint={'center_x': 0.5, 'top': 0.98},
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)

        # 添加文件夹按钮
        self.add_button = Button(
            text="添加漫画文件夹",
            pos_hint={'center_x': 0.5, 'y': 0.02},
            size_hint=(0.8, 0.08),
            background_color=(0.2, 0.6, 0.9, 1)
        )
        self.add_button.bind(on_press=self.show_file_chooser)
        self.layout.add_widget(self.add_button)

        # 漫画文件夹列表
        self.folder_buttons = []
        self.update_folder_list()

        self.add_widget(self.layout)

    def update_title(self, title):
        self.title_label.text = title

    def load_saved_folders(self):
        try:
            if platform == 'android':
                from android.storage import app_storage_path
                storage_path = app_storage_path()
            else:
                storage_path = os.path.dirname(os.path.abspath(__file__))

            config_path = os.path.join(storage_path, 'comic_folders.json')

            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.comic_folders = json.load(f)
        except Exception as e:
            print(f"加载保存的文件夹失败: {e}")

    def save_folders(self):
        try:
            if platform == 'android':
                from android.storage import app_storage_path
                storage_path = app_storage_path()
            else:
                storage_path = os.path.dirname(os.path.abspath(__file__))

            config_path = os.path.join(storage_path, 'comic_folders.json')

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.comic_folders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件夹失败: {e}")

    def update_folder_list(self):
        # 移除旧的按钮
        for btn in self.folder_buttons:
            self.layout.remove_widget(btn)
        self.folder_buttons = []

        # 创建新的按钮
        if not self.comic_folders:
            no_folder_label = Label(
                text="没有添加漫画文件夹\n点击下方按钮添加",
                font_size=18,
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(1, 0.2)
            )
            self.layout.add_widget(no_folder_label)
            self.folder_buttons.append(no_folder_label)
        else:
            for i, folder in enumerate(self.comic_folders):
                btn = Button(
                    text=os.path.basename(folder),
                    pos_hint={'center_x': 0.5, 'center_y': 0.85 - i * 0.12},
                    size_hint=(0.8, 0.1),
                    background_color=(0.3, 0.7, 0.4, 1)
                )
                btn.bind(on_press=lambda instance, f=folder: self.open_comic(f))
                self.layout.add_widget(btn)
                self.folder_buttons.append(btn)

    def show_file_chooser(self, instance):
        # 创建文件选择器弹窗
        box = FloatLayout()

        file_chooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*'],
            dirselect=True,
            size_hint=(1, 0.9),
            pos_hint={'x': 0, 'y': 0.1}
        )
        box.add_widget(file_chooser)

        select_btn = Button(
            text="选择",
            size_hint=(0.4, 0.08),
            pos_hint={'x': 0.1, 'y': 0.01},
            background_color=(0.2, 0.6, 0.9, 1)
        )
        select_btn.bind(on_press=lambda x: self.select_folder(file_chooser.selection, popup))
        box.add_widget(select_btn)

        cancel_btn = Button(
            text="取消",
            size_hint=(0.4, 0.08),
            pos_hint={'x': 0.5, 'y': 0.01},
            background_color=(0.8, 0.3, 0.3, 1)
        )
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        box.add_widget(cancel_btn)

        popup = Popup(title="选择漫画文件夹", content=box, size_hint=(0.9, 0.9))
        popup.open()

    def select_folder(self, selection, popup):
        if selection and os.path.isdir(selection[0]):
            folder_path = selection[0]
            if folder_path not in self.comic_folders:
                self.comic_folders.append(folder_path)
                self.save_folders()
                self.update_folder_list()
            popup.dismiss()

    def open_comic(self, folder_path):
        self.manager.get_screen('comic').load_comic(folder_path)
        self.manager.current = 'comic'


class ComicReaderApp(App):
    def build(self):
        # 创建屏幕管理器
        self.sm = ScreenManager()

        # 添加主屏幕
        main_screen = MainScreen(name='main')
        self.sm.add_widget(main_screen)

        # 添加漫画阅读屏幕
        comic_screen = ComicScreen(name='comic')
        self.sm.add_widget(comic_screen)

        # 返回按钮事件
        Window.bind(on_keyboard=self.on_back_button)

        return self.sm

    def on_back_button(self, window, key, *args):
        if key == 27:  # 安卓返回键
            if self.sm.current == 'comic':
                self.sm.current = 'main'
                return True  # 拦截返回事件
        return False  # 不拦截其他按键事件


if __name__ == '__main__':
    ComicReaderApp().run()