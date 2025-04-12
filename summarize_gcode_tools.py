import sublime
import sublime_plugin
import re

print("= = = = = = = = = = Loading summarize_gcode_tools.py")

class SummarizeGcodeToolsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("= = = = = = = = = = Running SummarizeGcodeToolsCommand")
        view = self.view
        print("View acquired:", view is not None)
        content = view.substr(sublime.Region(0, view.size()))
        
        # Debug: Print full content
        print("Initial File Content:", content)
        
        # Find tools
        tool_matches = []
        try:
            print("Running RegReplace: find_gcode_tools")
            view.run_command("reg_replace", {
                "replacements": ["find_gcode_tools"],
                "no_selection": true
            })
            
            # Get highlighted regions
            regions = view.get_regions("reg_replace")
            print("RegReplace Regions:", len(regions))
            tool_matches = []
            for region in regions:
                match_text = view.substr(region)
                print("Region content:", match_text)
                match = re.match(r'(?i)T\s*=?[\s;]*(\d+)', match_text)
                if match:
                    tool_matches.append(match.group(1))
            print("RegReplace Tools Found:", tool_matches)
            
            # Clear highlights
            view.erase_regions("reg_replace")
        except Exception as e:
            print("RegReplace Error:", str(e))
            print("Falling back to regex")
            tool_matches = re.findall(r'(?i)T\s*=?[\s;]*(\d+)', content, re.MULTILINE)
            print("Fallback Regex Tools Found:", tool_matches)
        
        if not tool_matches:
            print("No tools matched")
            sublime.message_dialog("No tools found in the G-code file!")
            return
        
        # Deduplicate and sort
        tools = sorted(set(int(tool) for tool in tool_matches))
        tools_summary = f"; Tools: {', '.join(str(tool) for tool in tools)}"
        
        # Debug: Print summary
        print("Tools Summary to Add:", tools_summary)
        
        # Find insertion point after ;Part#-123
        part_line = re.search(r'^;Part#-123\s*(?:\n|$)', content, re.MULTILINE | re.IGNORECASE)
        if part_line:
            insert_point = part_line.end()
            print(f"Found ;Part#-123 at position {insert_point}")
            # Check for existing summary after ;Part#-123
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
        print("Final File Content:", final_content)