import sublime
import sublime_plugin
import os
from os.path import join as pjoin

packages_path = sublime.packages_path()
plugin_dir = pjoin(packages_path, 'SessionSaver')
sessions_dir = pjoin(plugin_dir, 'sessions')

if not os.path.exists(sessions_dir):
	try:
		os.makedirs(sessions_dir)
	except OSError as e:
		raise OSError('Could not create sessions folder!\n' + e.strerror)


class SaveAsCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel('Name for this session:', '', self.on_done, None, None)

	def on_done(self, sessionName):
		session = pjoin(sessions_dir, sessionName)
		answer = True
		if os.path.exists(session):
			message = 'There is another session saved with this name, do you want to replace it?'
			answer = sublime.ok_cancel_dialog(message)
		self.handle_response(answer, session)

	def handle_response(self, answer, session):
		if answer:
			views = self.window.views()
			with open(session, 'w') as f:
				for v in views:
					f.write(v.file_name() + '\n')
			sublime.status_message('Session saved successfully as ' + os.path.basename(session))
		else:
			sublime.status_message('Saving session canceled')


class LoadSessionCommand(sublime_plugin.WindowCommand):
	def run(self):
		if not os.listdir(sessions_dir):
			sublime.message_dialog('There are no sessions saved')
		else:
			self.window.show_quick_panel(os.listdir(sessions_dir), self.on_done)

	def on_done(self, session):
		if session != -1:
			session = pjoin(sessions_dir, os.listdir(sessions_dir)[session])
			self.window.run_command("close_all")
			with open(session, 'r') as s:
				for l in s.readlines():
					self.window.open_file(l.rstrip())


class RemoveSessionCommand(sublime_plugin.WindowCommand):
	def run(self):
		if not os.listdir(sessions_dir):
			sublime.message_dialog('There are no sessions saved')
		else:
			self.window.show_quick_panel(os.listdir(sessions_dir), self.on_done)

	def on_done(self, session):
		session_path = pjoin(sessions_dir, os.listdir(sessions_dir)[session])
		session_name = os.path.basename(session_path)
		message = "Do you really want to remove the session %s?" % session_name
		answer = sublime.ok_cancel_dialog(message)
		self.handle_response(answer, session_path, session_name)

	def handle_response(self, answer, session_path, session_name):
		if answer:
			os.remove(session_path)
			sublime.status_message('Session \"%s\" removed' % session_name)
		else:
			sublime.status_message('Session not removed')