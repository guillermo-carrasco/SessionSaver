import sublime
import sublime_plugin
import os

if not os.path.exists(sublime.packages_path() + '/SessionSaver/sessions/'):
	try:
		os.makedirs(sublime.packages_path() + '/SessionSaver/sessions/')
	except OSError as e:
		sublime.error_message('Could not create sessions folder!\n' + e.strerror)


class SaveAsCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Name of this session:", "", self.on_done, None, None)

	def on_done(self, sessionName):
		session = sublime.packages_path() + '/SessionSaver/sessions/' + sessionName
		if os.path.exists(session):
			question = 'There is another session saved with this name, do you want to replace it? (yes/no):'
			self.window.show_input_panel(question, 'No', lambda s: self.handle_response(s, session), None, None)
		else:
			self.handle_response('yes', session)

	def handle_response(self, answer, session):
		if answer.upper() in ['YES', 'Y']:
			views = self.window.views()
			f = open(session, 'w')
			for v in views:
				f.write(v.file_name() + '\n')
			f.close()
			sublime.status_message("Session saved succefully as " + session.split('/')[-1] + '!')
		else:
			sublime.status_message("No session saved")


class LoadSessionCommand(sublime_plugin.WindowCommand):
	def run(self):
		sessionsDir = os.path.join(sublime.packages_path(), 'SessionSaver/sessions')
		if not os.listdir(sessionsDir):
			sublime.status_message("There are no sessions saved")
		else:
			self.window.show_quick_panel(os.listdir(sessionsDir), self.on_done)

	def on_done(self, session):
		if session != -1:
			session = sublime.packages_path() + '/SessionSaver/sessions/' + os.listdir(sublime.packages_path() + '/SessionSaver/sessions/')[session]
			#Close current views
			self.window.run_command("close_all")
			#Open saved documents
			s = open(session, 'r')
			for l in s.readlines():
				self.window.open_file(l.rstrip())
			s.close()


class RemoveSessionCommand(sublime_plugin.WindowCommand):
	def run(self):
		sessionsDir = os.path.join(sublime.packages_path(), 'SessionSaver/sessions')
		if not os.listdir(sessionsDir):
			sublime.status_message("There are no sessions saved")
		else:
			self.window.show_quick_panel(os.listdir(sessionsDir), self.on_done)

	def on_done(self, session):
		session = sublime.packages_path() + '/SessionSaver/sessions/' + os.listdir(sublime.packages_path() + '/SessionSaver/sessions/')[session]
		self.window.show_input_panel('Do you really want to remove this session (yes/no):', 'No', lambda s: self.handle_response(s, session), None, None)

	def handle_response(self, answer, session):
		if answer.upper() in ['Y', 'YES']:
			try:
				os.remove(session)
			except OSError as e:
				sublime.status_message(e.strerror)
			else:
				sublime.status_message("Session succefully removed")
		else:
			sublime.status_message("Session not removed")