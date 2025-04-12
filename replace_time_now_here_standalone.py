import sublime
import sublime_plugin
import re
import datetime

print("= = = = = = = = = = Loading replace_time_now_here_standalone.py")

class ReplaceTimeNowHereStandaloneCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("= = = = = = = = = = Running ReplaceTimeNowHereStandaloneCommand")
        view = self.view
        content = view.substr(sublime.Region(0, view.size()))
        
        # Debug: Print initial content
        print("Standalone Full Content:", content)
        
        # Get current date/time
        now = datetime.datetime.now()
        time_str = now.strftime("%A %Y/%m/%d (%H:%M:%S)")  # e.g., Saturday 2025/04/12 (09:04:56)
        print("Current Date/Time:", time_str)
        
        # Replace TimeNowHere
        new_content = re.sub(r'TimeNowHere', time_str, content)
        
        # Debug: Check if replaced
        if new_content == content:
            print("No TimeNowHere found")
            sublime.message_dialog("No TimeNowHere found in the G-code file!")
            return
        
        print("Replacing TimeNowHere with:", time_str)
        view.replace(edit, sublime.Region(0, view.size()), new_content)
        
        # Debug: Print final content
        final_content = view.substr(sublime.Region(0, view.size()))
        print("Standalone Final Content:", final_content)