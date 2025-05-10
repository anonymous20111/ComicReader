[app]
# (str) 应用名称
title = 漫画阅读器

# (str) 应用包名 (如: org.kivy.myapp)
package.name = comicreader

# (str) 应用包ID (如: org.kivy.myapp)
package.domain = org.kivy

# (str) 源目录
source.dir = .

# (list) 源文件包含的扩展名
source.include_exts = py,png,jpg,kv,atlas,json

# (list) 需要排除的目录和文件
source.exclude_dirs = tests, bin, venv

# (list) 应用需要的权限
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) 应用版本 (integer)
version = 1

# (str) 应用图标路径
# android.icon = %(source.dir)s/data/icon.png

# (str) 应用启动画面路径
# android.splash = %(source.dir)s/data/splash.png

# (list) 应用依赖
requirements = python3,kivy,pillow

# (str) 窗口方向: portrait 或 landscape
orientation = portrait

# (bool) 是否使用 Kivy 语言
fullscreen = 0

# (list) 安卓平台需要的额外权限
android.extra_permissions = INTERNET

# (bool) 是否支持平板
android.arch = armeabi-v7a,arm64-v8a

# (str) 构建工具链
android.build_toolchain = sdl2

# (str) 安卓 SDK 路径 (如果已安装)
# android.sdk_path = /path/to/android-sdk

# (str) 安卓 NDK 路径 (如果已安装)
# android.ndk_path = /path/to/android-ndk

# (str) 安卓 SDK 版本
android.sdk_version = 31

# (str) 安卓 NDK 版本
android.ndk_version = 25b

# (str) 构建模式
android.build_mode = debug

# (str) 签名配置 (发布版本需要)
# android.release = 1
# android.keyalias = mykey
# android.keystore = my-release-key.keystore
# android.keystore_pass = your_password
# android.keyalias_pass = your_password

[buildozer]

# (int) 日志级别 (0 = 错误 only, 1 = 正常, 2 = 详细)
log_level = 2

# (int) 并行编译数
warn_on_root = 1