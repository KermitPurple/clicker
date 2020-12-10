all: gui.ui
	pyuic5 gui.ui -o gui.py

test: all
	py GuiClicker.py
