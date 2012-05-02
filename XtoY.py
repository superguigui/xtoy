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
			"WIDTH"  	:"HEIGHT",
			"HEIGHT" 	:"WIDTH",
			"X"      	:"Y",
			"Y"      	:"X",
			"width"  	:"height",
			"Width"  	:"Height",
			"Height" 	:"Width",
			"x"      	:"y",
			"y"      	:"x",
			"-left"		:"-right",
			"-right"	:"-left",
			"-top"		:"-bottom",
			"-bottom"	:"-top",
			"left"		:"right",
			"right"		:"left",
			"top"		:"bottom",
			"bottom"	:"top"
		}

		ignoredSyntaxRegex = re.compile("(.*)[\d][p][x](.*)")

		# I don't know why it's not working with ignoredSyntaxRegex.match(content) each time it returns None...
		# That's why I'm using findall.
		if len(ignoredSyntaxRegex.findall(content)) > 0:
			del patterns['x']

		regex = re.compile("|".join(map(re.escape, patterns.keys())))

		return regex.sub(lambda match: patterns[match.group(0)], content)