#!/bin/sh
pyuic4 ./src/graph-dialog.ui -o ./ui_graph_dialog.py
pyuic4 ./src/main-window.ui -o ./ui_main_window.py
pyuic4 ./src/sensor-edit-dialog.ui -o ./ui_sensor_edit_dialog.py
pyuic4 ./src/settings-dialog.ui -o ./ui_settings_dialog.py

pyrcc4 -py3 res/icon.qrc -o ../icon_rc.py
