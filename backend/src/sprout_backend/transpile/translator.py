import re
from typing import Dict, Union, Any, Callable
from ..scratch.models import ScratchProject, ScratchBlock
from ..scratch.block_index import get_top_level_blocks, build_block_sequence
from .emitter import PythonEmitter


class ProjectTranslator:
    def __init__(self, project: ScratchProject):
        self.project = project
        self.emitter = PythonEmitter()
        self.blocks: Dict[str, Union[ScratchBlock, list]] = {}

        # CENTRAL HANDLER MAP
        self.handlers: Dict[str, Callable] = {
            # EVENTS
            "event_whenflagclicked": self._handle_green_flag,
            "event_whenkeypressed": self._handle_key_pressed,
            "event_whenbroadcastreceived": self._handle_broadcast_received,

            # CONTROL
            "control_wait": self._handle_wait,
            "control_repeat": self._handle_repeat,
            "control_if": self._handle_if,
            "control_if_else": self._handle_if_else,
            "control_forever": self._handle_forever,

            # MOTION
            "motion_movesteps": self._handle_move,
            "motion_turnright": self._handle_turn_right,
            "motion_turnleft": self._handle_turn_left,
            "motion_gotoxy": self._handle_goto_xy,
            "motion_goto": self._handle_goto,
            "motion_pointtowards": self._handle_point_towards,

            # LOOKS
            "looks_say": self._handle_say,
            "looks_show": self._handle_show,
            "looks_hide": self._handle_hide,
            "looks_switchcostumeto": self._handle_switch_costume,

            # VARIABLES
            "data_setvariableto": self._handle_set_var,
            "data_changevariableby": self._handle_change_var,

            # SOUND
            "sound_play": self._handle_play_sound,

            # SENSING (statement)
            "sensing_askandwait": self._handle_ask,
        }

    # =========================
    # MAIN ENTRY
    # =========================
    def translate(self) -> Dict[str, Any]:
        self.emitter.emit_line("import time", "meta", "import")
        self.emitter.emit_line("import random", "meta", "import")
        self.emitter.lines.append("")

        for target in self.project.targets:
            self.blocks = target.blocks

            for start_id in get_top_level_blocks(self.blocks):
                sequence = build_block_sequence(start_id, self.blocks)
                self._translate_sequence(sequence)
                self.emitter.lines.append("")

        return {
            "python_code": self.emitter.get_code(),
            "mappings": self.emitter.mappings,
            "warnings": self.emitter.warnings
        }

    # =========================
    # CORE DISPATCH
    # =========================
    def _translate_sequence(self, sequence: list[str]):
        for block_id in sequence:
            block = self.blocks.get(block_id)
            if isinstance(block, ScratchBlock):
                self._dispatch(block_id, block)

    def _dispatch(self, block_id: str, block: ScratchBlock):
        opcode = block.opcode

        # Skip reporters
        if opcode.startswith("operator_"):
            return

        handler = self.handlers.get(opcode)

        if handler:
            handler(block_id, block)
        else:
            self._warn(f"Unsupported block: {opcode}", block_id)
            self.emitter.emit_line(f"# TODO: {opcode}", block_id, opcode)

    # =========================
    # UTILITIES
    # =========================
    def _warn(self, message: str, block_id: str = ""):
        self.emitter.add_warning({
            "message": message,
            "block_id": block_id
        })

    def _resolve_input(self, block: ScratchBlock, name: str, default="0"):
        raw = block.inputs.get(name)
        if not isinstance(raw, list) or len(raw) < 2:
            return default

        value = raw[1]

        if isinstance(value, str):
            return self._evaluate_reporter(value)

        if isinstance(value, list) and len(value) > 1:
            return self._format_literal(value[1])

        return default

    def _format_literal(self, val):
        try:
            float(val)
            return str(val)
        except:
            return f'"{val}"'

    def _get_field(self, block, name, default=""):
        return str(block.fields.get(name, [default])[0])

    def _sanitize(self, name: str):
        return re.sub(r'\W|^(?=\d)', '_', name).lower()

    # =========================
    # REPORTERS
    # =========================
    def _evaluate_reporter(self, block_id: str) -> str:
        block = self.blocks.get(block_id)
        if not isinstance(block, ScratchBlock):
            return "None"

        op = block.opcode

        if op == "operator_add":
            return f"({self._resolve_input(block,'NUM1')} + {self._resolve_input(block,'NUM2')})"

        if op == "operator_gt":
            return f"({self._resolve_input(block,'OPERAND1')} > {self._resolve_input(block,'OPERAND2')})"

        if op == "sensing_mousex":
            return "sprite.mouse_x"

        if op == "data_variable":
            return f"var_{self._sanitize(self._get_field(block,'VARIABLE'))}"

        self._warn(f"Unknown reporter: {op}")
        return "None"

    # =========================
    # HANDLERS
    # =========================

    # --- EVENTS ---
    def _handle_green_flag(self, bid, block):
        self.emitter.emit_line("@event.green_flag", bid, block.opcode)
        self.emitter.emit_line("def start():", bid, block.opcode)
        self.emitter.indent()

    def _handle_key_pressed(self, bid, block):
        key = self._get_field(block, "KEY_OPTION")
        self.emitter.emit_line(f"@event.key('{key}')", bid, block.opcode)
        self.emitter.emit_line(f"def on_{key}():", bid, block.opcode)
        self.emitter.indent()

    def _handle_broadcast_received(self, bid, block):
        msg = self._get_field(block, "BROADCAST_OPTION")
        self.emitter.emit_line(f"@event.broadcast('{msg}')", bid, block.opcode)
        self.emitter.emit_line(f"def on_{self._sanitize(msg)}():", bid, block.opcode)
        self.emitter.indent()

    # --- CONTROL ---
    def _handle_wait(self, bid, block):
        secs = self._resolve_input(block, "DURATION")
        self.emitter.emit_line(f"time.sleep({secs})", bid, block.opcode)

    def _handle_repeat(self, bid, block):
        times = self._resolve_input(block, "TIMES")
        self.emitter.emit_line(f"for _ in range(int({times})):", bid, block.opcode)
        self._handle_substack(block, "SUBSTACK")

    def _handle_if(self, bid, block):
        cond = self._resolve_input(block, "CONDITION", "False")
        self.emitter.emit_line(f"if {cond}:", bid, block.opcode)
        self._handle_substack(block, "SUBSTACK")

    def _handle_if_else(self, bid, block):
        cond = self._resolve_input(block, "CONDITION", "False")
        self.emitter.emit_line(f"if {cond}:", bid, block.opcode)
        self._handle_substack(block, "SUBSTACK")
        self.emitter.emit_line("else:", bid, block.opcode)
        self._handle_substack(block, "SUBSTACK2")

    def _handle_forever(self, bid, block):
        self.emitter.emit_line("while True:", bid, block.opcode)
        self._handle_substack(block, "SUBSTACK")

    # --- MOTION ---
    def _handle_move(self, bid, block):
        steps = self._resolve_input(block, "STEPS")
        self.emitter.emit_line(f"sprite.move({steps})", bid, block.opcode)

    def _handle_turn_right(self, bid, block):
        deg = self._resolve_input(block, "DEGREES")
        self.emitter.emit_line(f"sprite.turn_right({deg})", bid, block.opcode)

    def _handle_turn_left(self, bid, block):
        deg = self._resolve_input(block, "DEGREES")
        self.emitter.emit_line(f"sprite.turn_left({deg})", bid, block.opcode)

    def _handle_goto_xy(self, bid, block):
        x = self._resolve_input(block, "X")
        y = self._resolve_input(block, "Y")
        self.emitter.emit_line(f"sprite.goto({x}, {y})", bid, block.opcode)

    def _handle_goto(self, bid, block):
        target = self._resolve_input(block, "TO")
        self.emitter.emit_line(f"sprite.goto_target({target})", bid, block.opcode)

    def _handle_point_towards(self, bid, block):
        target = self._resolve_input(block, "TOWARDS")
        self.emitter.emit_line(f"sprite.point_towards({target})", bid, block.opcode)

    # --- LOOKS ---
    def _handle_say(self, bid, block):
        msg = self._resolve_input(block, "MESSAGE")
        self.emitter.emit_line(f"sprite.say({msg})", bid, block.opcode)

    def _handle_show(self, bid, block):
        self.emitter.emit_line("sprite.show()", bid, block.opcode)

    def _handle_hide(self, bid, block):
        self.emitter.emit_line("sprite.hide()", bid, block.opcode)

    def _handle_switch_costume(self, bid, block):
        c = self._resolve_input(block, "COSTUME")
        self.emitter.emit_line(f"sprite.costume = {c}", bid, block.opcode)

    # --- VARIABLES ---
    def _handle_set_var(self, bid, block):
        name = self._sanitize(self._get_field(block, "VARIABLE"))
        val = self._resolve_input(block, "VALUE")
        self.emitter.emit_line(f"var_{name} = {val}", bid, block.opcode)

    def _handle_change_var(self, bid, block):
        name = self._sanitize(self._get_field(block, "VARIABLE"))
        val = self._resolve_input(block, "VALUE")
        self.emitter.emit_line(f"var_{name} += {val}", bid, block.opcode)

    # --- SOUND ---
    def _handle_play_sound(self, bid, block):
        s = self._resolve_input(block, "SOUND_MENU")
        self.emitter.emit_line(f"sprite.play_sound({s})", bid, block.opcode)

    # --- SENSING ---
    def _handle_ask(self, bid, block):
        q = self._resolve_input(block, "QUESTION")
        self.emitter.emit_line(f"sprite.ask({q})", bid, block.opcode)

    # =========================
    # SUBSTACK
    # =========================
    def _handle_substack(self, block, key):
        sub = block.inputs.get(key)

        if isinstance(sub, list) and isinstance(sub[1], str):
            seq = build_block_sequence(sub[1], self.blocks)
            self._translate_sequence(seq)
        else:
            self.emitter.emit_line("pass", "", "pass")

        self.emitter.dedent()