import sublime, sublime_plugin  

class ExampleCommand(sublime_plugin.TextCommand):  
    def run(self, edit):  
        self.view.insert(edit, 0, "Hello, World!") 


class SaveCurrentSessionCommand(sublime_plugin.TextCommand):
	def run(self):
		sublime.error_message("Current session saved succefully!")