import sys
import lldb
import enum


class TextColorType(enum.Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


class ColoredText:
    def __init__(self, text, color):
        self.text = text
        self.color = color

    def __str__(self):
        color_ctl = None
        if self.color == TextColorType.BLACK:
            color_ctl = "\033[30m"
        elif self.color == TextColorType.RED:
            color_ctl = "\033[31m"
        elif self.color == TextColorType.GREEN:
            color_ctl = "\033[32m"
        elif self.color == TextColorType.YELLOW:
            color_ctl = "\033[33m"
        elif self.color == TextColorType.BLUE:
            color_ctl = "\033[34m"
        elif self.color == TextColorType.MAGENTA:
            color_ctl = "\033[35m"
        elif self.color == TextColorType.CYAN:
            color_ctl = "\033[36m"
        elif self.color == TextColorType.WHITE:
            color_ctl = "\033[37m"
        else:
            color_ctl = "\033[37m"

        t = "%s%s%s" % (color_ctl, self.text, "\033[0m")
        return t


class Frame:
    def __init__(self, frame):
        self.frame = frame
        self.id = self.frame.GetFrameID()
        self.module = self.frame.GetModule()
        self.function_name = self.frame.GetFunctionName()
        self.pc = "0x%016x" % self.frame.GetPC()

    def __str__(self):
        return "Frame #%03d %s %s" % (self.id, ColoredText(self.pc, TextColorType.YELLOW), self.frame.GetPCAddress())

class Register:
    def __init__(self, r_value):
        self.r_value = r_value

    def __str__(self):
        return "%s" % self.r_value.GetName()

class RegisterSet:
    def __init__(self, rs_value):
        self.rs_value = rs_value
        self.name = self.rs_value.GetName()
        self.general_registers = []
        self._parse()

    def _parse(self):
        for r in self.general_registers:
            self.general_registers.append(Register(r))

    def __str__(self):
        return "%d" %len(self.general_registers)


class FrameCommand:
    def __init__(self, debugger, session_dict):
        pass

    def __call__(self, debugger, command, exe_ctx, result):
        target = debugger.GetSelectedTarget()
        process = target.GetProcess()
        thread = process.GetSelectedThread()

        thread_index = thread.GetIndexID()
        thread_id = thread.GetThreadID()
        thread_name = thread.GetName()
        queue_name = thread.GetQueueName()
        queue_id = thread.GetQueueID()
        stop_reason = thread.GetStopReason()
        stop_desc = thread.GetStopDescription(thread.GetStopReasonDataAtIndex(stop_reason))

        desc = "Thread #%02d, ID: 0x%x, queue = %s" % (thread_index, thread_id, ColoredText(queue_name, TextColorType.GREEN))
        if thread_name is not None:
            desc += ", name = %s" % (ColoredText(thread_name, TextColorType.BLUE))
        desc += ", stop reason = %s" % (ColoredText(stop_desc, TextColorType.RED))
        print(desc, file=result)

        for f in thread:
            frame = Frame(f)
            print(" %s" % (str(frame)), file=result)

        registers = thread.GetFrameAtIndex(0).GetRegisters()
        register_objects = []
        for r in registers:
            register_objects.append(RegisterSet(r))

        print("%s" % register_objects[0], file=result)

    def get_short_help(self):
        help_str = "Display current frame"

    def get_long_help(self):
        pass


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("command script add --class lldbinit.FrameCommand f")
