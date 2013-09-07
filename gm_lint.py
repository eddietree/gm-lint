# GameMonkey Linter: https://github.com/eddietree/gm-lint

import sublime, sublime_plugin
import subprocess, os, re

class GmLintCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# erase previous status and regions
		self.view.erase_status("gm-lint")   	
		self.view.erase_regions("compile_error_regions")

		# find the fullpath of the gm byte code exe
		plugin_fullpath = os.path.realpath(__file__)
		plugin_dir = os.path.dirname(plugin_fullpath)
		gm_exe_path = plugin_dir + "\GmByteCodeGen.exe"
		
		# script file
		script_filename = self.view.file_name()
		
		# generate the string to be executed
		exe_string =  "\"" + gm_exe_path + "\" -i " + "\"" + script_filename + "\""
		foo = subprocess.Popen(exe_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		# wait for compile to finish and listen to emitted return code
		foo.wait()
		return_code = foo.returncode

		# if error code
		if return_code == 1:

			# show the console if error
			#sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

			output_bytes = foo.stdout.read()
			output_string = output_bytes.decode("utf-8")
			#print( "output: " + output_string)

			# grab the line number and error
			pattern = re.compile('.*Compile error[ \t]*\(([0-9]*)\)(.*)\r?\n')
			match = pattern.match( output_string )
			line_number = int(match.group(1))
			compile_error_msg = match.group(2)
			
			#print( "LINE: " + str(line_number))
			#print( "ERROR: " + compile_error_msg)

			# set the status
			output_msg = "Compile error: Line " + str(line_number) + ": " + compile_error_msg
			print ( "[gm-lint] " + output_msg)
			self.view.set_status("gm-lint", output_msg)

			# grabs region that has the compile error
			line_pt = self.view.text_point(line_number-1, 0)
			line_region = self.view.line(line_pt)
			compile_error_regions = [line_region]

			# highlight the region
			self.view.add_regions("compile_error_regions", compile_error_regions, "comment", "bookmark",  sublime.DRAW_NO_FILL )
			self.view.show_at_center( line_region )

			# goto error line
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(line_pt))
			self.view.show(line_pt)
		
		else:
			print ("[GM-Lint] Successfully compiled '" + script_filename + "'!")

  
class ListenSaveGameMonkeyFile(sublime_plugin.EventListener):
    def on_post_save(self, view):

    	# what operating system?
    	os_platform = sublime.platform()

    	# get file extension of the file we just saved
    	extension = os.path.splitext(view.file_name())[1] 

    	# run only on .gm files and on windows
    	if extension == ".gm" and os_platform == "windows" :
    		view.run_command("gm_lint")