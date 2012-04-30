import sublime, sublime_plugin, re

class XtoyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				line = self.view.line(region)
				line_contents = '\n' + self.view.substr(line)
				self.view.insert(edit, line.end(), self.replace(line_contents))
			else:
				self.view.insert(edit, region.end(), self.replace(self.view.substr(region)))

	def replace(self, content):
		patterns = {
			"WIDTH"  :"HEIGHT",
			"HEIGHT" :"WIDTH",
			"X"      :"Y",
			"Y"      :"X",
			"width"  :"height",
			"Width"  :"Height",
			"Height" :"Width",
			"x"      :"y",
			"y"      :"x"
		}
		regex = re.compile("|".join(map(re.escape, patterns.keys())))
		return regex.sub(lambda match: patterns[match.group(0)], content)
