
UI = gui_ui.py


run : $(UI) gui_rc.py

%_ui.py : %_ui.ui
	@echo "compiling $<"
	pyuic5 $< > $@

gui_rc.py : gui.qrc icons/*
	pyrcc5 gui.qrc > gui_rc.py
