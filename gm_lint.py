# GameMonkey Linter: https://github.com/eddietree/gm-lint
import subprocess, os, re, sys
import sublime, sublime_plugin


class LintCommandBase(sublime_plugin.TextCommand):
	def highlight_line(self, line_number):

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

	def reset(self):
		# erase previous status and regions
		self.view.erase_status(self.command_name)   	
		self.view.erase_regions("compile_error_regions")

	def handle_compile_fail(self, line_number, compile_error_msg):

		output_msg = self.command_name + ": Compile error: Line " + str(line_number) + " - " + compile_error_msg
		print ( output_msg )

		self.view.set_status(self.command_name, output_msg)
		self.highlight_line(line_number)

	# overwrite this function!
	def get_line_and_error_msg(self, edit):
		return None

	def run(self, edit):

		self.reset()

		line_number, compile_error_msg = self.get_line_and_error_msg(edit)

		if ( line_number == None ):
			success_msg = self.command_name + ": Compiled success!"
			print (success_msg)
			self.view.set_status(self.command_name, success_msg)

		else:
			self.handle_compile_fail( line_number, compile_error_msg )


########################## GAMEMONKEY 
class GmLintCommand(LintCommandBase):

	command_name = "gm_lint"

	def get_line_and_error_msg(self, edit):

		# find the fullpath of the gm byte code exe
		plugin_fullpath = os.path.realpath(__file__)
		plugin_dir = os.path.dirname(plugin_fullpath)
		gm_exe_path = plugin_dir + "\GmByteCodeGen.exe"
		
		# script file
		script_filename = self.view.file_name()
		
		# generate the string to be executed
		exe_string =  "\"" + gm_exe_path + "\" -i " + "\"" + script_filename + "\""
		process = subprocess.Popen(exe_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		# wait for compile to finish and listen to emitted return code
		process.wait()
		return_code = process.returncode

		if return_code == 1: # if error in compiling

			# read the stdout
			output_bytes = process.stdout.read()
			output_string = output_bytes.decode("utf-8")
			#print( "output: " + output_string)

			# grab the line number and error
			pattern = re.compile('.*Compile error[ \t]*\(([0-9]*)\)(.*)\r?\n')
			match = pattern.match( output_string )
			line_number = int(match.group(1))
			compile_error_msg = match.group(2)

			return line_number, compile_error_msg	

		else: # success

			return None, None


class ListenSaveGameMonkeyFile(sublime_plugin.EventListener):

    def on_post_save(self, view):

    	# this plugin only works on windows!
    	if sublime.platform() != "windows":
    		print ("gm-lint works only on Windows!")

    	# get file extension of the file we just saved
    	extension = os.path.splitext(view.file_name())[1] 

    	# run only on .gm files and on windows
    	if extension == ".gm":
    		view.run_command("gm_lint")