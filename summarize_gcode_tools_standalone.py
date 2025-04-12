import sublime
import sublime_plugin
import re

print("= = = = = = = = = = Loading summarize_gcode_tools_standalone.py")

class SummarizeGcodeToolsStandaloneCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("= = = = = = = = = = Running SummarizeGcodeToolsStandaloneCommand")
        view = self.view
        content = view.substr(sublime.Region(0, view.size()))
        
        # Debug: Print full content
        print("Standalone Full Content:", content)
        
        # Find tools with broader regex
        tool_matches = re.findall(r'(?i)T\s*=?[\s;]*(\d+)', content, re.MULTILINE)
        
        # Debug: Print matches and regex details
        print("Standalone Regex Used: (?i)T\s*=?[\s;]*(\d+)")
        print("Standalone Tools Found:", tool_matches)
        
        if not tool_matches:
            print("No tools matched - showing dialog")
            sublime.message_dialog("No tools found in the G-code file!")
            return
        
        # Deduplicate and sort
        tools = sorted(set(int(tool) for tool in tool_matches))
        tools_summary = f"; Tools: {', '.join(str(tool) for tool in tools)}"
        
        # Debug: Print summary
        print("Standalone Tools Summary to Add:", tools_summary)
        
        # Find insertion point after ;Part#-123
        part_line = re.search(r'^;Part#-123\s*(?:\n|$)', content, re.MULTILINE | re.IGNORECASE)
        if part_line:
            insert_point = part_line.end()
            existing_summary = re.match(r'\s*; Tools:\s*[\d,\s]*(?:\n|$)', 
                                     content[insert_point:], re.MULTILINE | re.IGNORECASE)
            if existing_summary:
                print("Replacing existing summary")
                summary_region = sublime.Region(insert_point, 
                                             insert_point + existing_summary.end())
                view.replace(edit, summary_region, tools_summary)
            else:
                print("Inserting new summary")
                view.insert(edit, insert_point, tools_summary + "\n")
        else:
            print(";Part#-123 not found, using fallback")
            # Fallback: Insert at top
            existing_summary = re.match(r'^; Tools:\s*[\d,\s]*(?:\n|$)', 
                                      content, re.MULTILINE | re.IGNORECASE)
            if existing_summary:
                print("Replacing existing summary at top")
                view.replace(edit, sublime.Region(0, existing_summary.end()), 
                           tools_summary)
            else:
                print("Inserting new summary at top")
                view.insert(edit, 0, tools_summary + "\n")
        
        # Debug: Print final content
        final_content = view.substr(sublime.Region(0, view.size()))
        print("Standalone Final Content:", final_content)