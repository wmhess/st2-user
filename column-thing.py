import sublime, sublime_plugin

class ShiftSelections(sublime_plugin.TextCommand):
    def run(self, edit, forward=True):
        view = self.view
        sels = view.sel()

        for sel in (reversed if forward else iter)(sels):
            substr = view.substr(sel)

            if forward:
                pt          = sel.end()
                after       = view.substr(pt)
                replacement = after + substr
                replace_sel = sel.begin(),     pt + 1
                after_sel   = sel.begin() + 1, pt + 1
            else:
                pt          = sel.begin()   - 1
                b4          = view.substr(pt)
                replacement = substr + b4
                replace_sel = pt, sel.end()
                after_sel   = pt, sel.end() - 1

            if pt < 0 or pt >= view.size(): continue

            sels.subtract(sel)
            view.replace(edit, sublime.Region(*replace_sel), replacement)
            sels.add(sublime.Region(*after_sel))