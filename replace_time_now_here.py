# replace_time_now_here.py v1.3
import sublime
import sublime_plugin
import re
import datetime

print("= = = = = = = = = = Loading replace_time_now_here.py v1.3")

class ReplaceTimeNowHereCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("= = = = = = = = = = Running ReplaceTimeNowHereCommand v1.3")
        view = self.view
        print("View acquired:", view is not None)
        content = view.substr(sublime.Region(0, view.size()))
        
        # Debug: Print initial content
        print("Initial File Content:", content)
        
        # Remove trailing semicolon from ; Tools:
        content = re.sub(r'^; Tools:.*;+\s*(?:\n|$)', lambda m: m.group(0).rstrip(';'), content, flags=re.MULTILINE)
        view.replace(edit, sublime.Region(0, view.size()), content)
        content = view.substr(sublime.Region(0, view.size()))
        
        # Get current date/time
        now = datetime.datetime.now()
        time_str = now.strftime("%A %Y/%m/%d (%H:%M:%S)")  # e.g., Saturday 2025/04/12 (09:27:26)
        print("Current Date/Time:", time_str)
        
        # Initialize replacement flag
        replaced = False
        
        # Try RegReplace to find regions
        try:
            print("Running RegReplace: replace_time_now_here")
            view.run_command("reg_replace", {
                "replacements": ["replace_time_now_here"],
                "no_selection": True
            })
            
            # Get marked regions
            regions = view.get_regions("reg_replace")
            print("RegReplace Regions:", len(regions))
            if regions:
                # Replace each region in reverse to avoid offset issues
                for region in reversed(regions):
                    match_text = view.substr(region)
                    print("Region content:", match_text)
                    if re.match(r'(TimeNowHere', match_text):
                        view.replace(edit, region, f"{time_str}")
                        replaced = True
                view.erase_regions("reg_replace")
            
            # Check if replacement occurred
            if not replaced and re.search(r'(TimeNowHere', content):
                print("RegReplace failed to replace TimeNowHere")
                raise Exception("RegReplace missed matches")
            print("RegReplace Completed")
        
        except Exception as e:
            print("RegReplace Error:", str(e))
            print("Falling back to regex")
            # Fallback: Direct regex replace
            new_content = re.sub(r'TimeNowHere', f'{time_str}', content, flags=re.MULTILINE)
            if new_content == content:
                print("No TimeNowHere found")
                sublime.message_dialog("No TimeNowHere found in the G-code file!")
                return
            view.replace(edit, sublime.Region(0, view.size()), new_content)
            replaced = True
            print("Fallback Regex Completed")
        
        if replaced:
            print("Replacement successful")
        else:
            print("No replacements made")
        
        # Debug: Print final content
        final_content = view.substr(sublime.Region(0, view.size()))
        print("Final File Content:", final_content)