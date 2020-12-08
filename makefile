all: compile_ui
	py GuiClicker.py

compile_ui: gui.ui
	pyuic5 gui.ui -o gui.py
