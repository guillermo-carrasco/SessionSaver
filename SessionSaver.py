import sublime
import sublime_plugin
import os


class SaveCurrentSessionCommand(sublime_plugin.WindowCommand):
	## TODO: Ask for a session name if no session is loaded
	def run(self):
		activeWindow = self.window.views()
		packageDir = os.getcwd()
		f = open(packageDir + '/session', 'w')
		for v in activeWindow:
			f.write(v.file_name() + '\n')
		f.close()
		sublime.status_message("Current session saved succefully! :-)")


class SaveAsCommand(sublime_plugin.WindowCommand):
	#TODO: If there is another session with the same name... do something
	def run(self):
		self.window.show_input_panel("Name of this session:", "", self.on_done, None, None)
		pass

	def on_done(self, sessionName):
		activeWindow = self.window.views()
		packageDir = os.getcwd() + '/sessions/'
		f = open(packageDir + sessionName, 'w')
		for v in activeWindow:
			f.write(v.file_name() + '\n')
		f.close()
		sublime.status_message("Session saved succefully as " + sessionName + "! :-)")

class LoadSession(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_quick_panel(os.listdir(os.getcwd() + '/sessions'), self.on_done)

	def on_done(self, session):
		print os.listdir(os.getcwd() + '/sessions')[session]

## General TODOs: Remove sessions (asking if sure...), check things... 