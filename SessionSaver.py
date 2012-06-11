import sublime
import sublime_plugin
import os

if not os.path.exists(sublime.packages_path() + '/SessionSaver/sessions/'):
	os.makedirs(sublime.packages_path() + '/SessionSaver/sessions/')


class SaveAsCommand(sublime_plugin.WindowCommand):
	"""
	Basically saves the current session with the given name. By the moment, and until ok_cancel_dialog is available
	in the stable version of sublime, if a session with the same name than the entered by the user exists, it will
	be overwritten.
	"""
	def run(self):
		self.window.show_input_panel("Name of this session:", "", self.on_done, None, None)
		pass

	def on_done(self, sessionName):
		views = self.window.views()
		packageDir = sublime.packages_path() + '/SessionSaver/sessions/'
		f = open(packageDir + sessionName, 'w')
		for v in views:
			f.write(v.file_name() + '\n')
		f.close()
		sublime.status_message("Session saved succefully as " + sessionName + '!')


class LoadSessionCommand(sublime_plugin.WindowCommand):
	"""
	Close all currently opened tabs and open the document(s) oh the selected session
	"""
	def run(self):
		sessionsDir = os.path.join(sublime.packages_path(), 'SessionSaver/sessions')
		if not os.listdir(sessionsDir):
			sublime.status_message("There are no sessions saved")
		else:
			self.window.show_quick_panel(os.listdir(sessionsDir), self.on_done)

	def on_done(self, session):
		session = sublime.packages_path() + '/SessionSaver/sessions/' + os.listdir(sublime.packages_path() + '/SessionSaver/sessions/')[session]
		#Close current views
		self.window.run_command("close_all")
		#Open saved documents
		s = open(session, 'r')
		for l in s.readlines():
			self.window.open_file(l.rstrip())
		s.close()


class RemoveSessionCommand(sublime_plugin.WindowCommand):
	"""
	Removes a stored session WITHOUT confirmation
	"""
	def run(self):
		sessionsDir = os.path.join(sublime.packages_path(), 'SessionSaver/sessions')
		if not os.listdir(sessionsDir):
			sublime.status_message("There are no sessions saved")
		else:
			self.window.show_quick_panel(os.listdir(sessionsDir), self.on_done)

	def on_done(self, session):
		session = sublime.packages_path() + '/SessionSaver/sessions/' + os.listdir(sublime.packages_path() + '/SessionSaver/sessions/')[session]
		#Remove the session file
		os.remove(session)
		sublime.status_message("Session succefully removed")