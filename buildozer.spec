[app]

title = School Management System

package.name = schoolmanagement

package.domain = org.jhad

source.dir = .

source.include_exts = py,png,jpg,kv,atlas

source.include_patterns = assets/*,images/*.png

source.exclude_exts = spec

source.exclude_dirs = tests, bin, venv

version = 1.0.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf,pillow,plyer
orientation = portrait

osx.python_version = 3

osx.kivy_version = 2.2.1

fullscreen = 0

android.presplash_color = #FFFFFF

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 31

android.minapi = 21

android.skip_update = False

[buildozer]

log_level = 2

warn_on_root = 1

bin_dir = ./bin
