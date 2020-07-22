import lldb


class Frame:
    def __init__(self, id, cfa, module):
        self.id = id
        self.cfa = cfa
        self.module = module

    def __str__(self):
        return "Frame #%03d 0x%x %s" %(self.id, self.cfa, self.module)

class FrameCommand:
    def __init__(self, debugger, session_dict):
        pass

    def __call__(self, debugger, command, exe_ctx, result):
        
        target = debugger.GetSelectedTarget()
        process = target.GetProcess()
        thread = process.GetSelectedThread()

        for f in thread:

            frame = Frame(f.GetFrameID(), f.GetCFA(), f.GetModule())
            print(str(frame), file=result)

    def get_short_help(self):
        help_str = "Display current frame"

    def get_long_help(self):
        pass


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("command script add --class lldbinit.FrameCommand f")
