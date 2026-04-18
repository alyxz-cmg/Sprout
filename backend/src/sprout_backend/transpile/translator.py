import re
from typing import Dict, Union, Any, Tuple
from ..scratch.models import ScratchProject, ScratchBlock
from ..scratch.block_index import get_top_level_blocks, build_block_sequence
from .emitter import PythonEmitter

class ProjectTranslator:
    """
    Translates a parsed ScratchProject into a deterministic Python script,
    supporting Motion, Looks, Sound, Events, Control, Sensing, Operators, Variables, and My Blocks.
    """
    def __init__(self, project: ScratchProject):
        self.project = project
        self.emitter = PythonEmitter()
        self.blocks: Dict[str, Union[ScratchBlock, list]] = {}

    def translate(self) -> Dict[str, Any]:
        self.emitter.emit_line("import time", "meta", "import", "Imported for wait blocks.")
        self.emitter.emit_line("import random", "meta", "import", "Imported for math blocks.")
        self.emitter.lines.append("")

        for target in self.project.targets:
            self.blocks = target.blocks
            top_level_ids = get_top_level_blocks(self.blocks)
            
            if top_level_ids:
                sprite_type = "Stage" if target.isStage else "Sprite"
                self.emitter.emit_line(f"# --- {sprite_type}: {target.name} ---", "meta", "comment")
                
            for start_id in top_level_ids:
                self.emitter.current_indent = 0
                start_block = self.blocks.get(start_id)

                if isinstance(start_block, ScratchBlock):
                    section_name = self._generate_section_name(start_block)
                    self.emitter.emit_line(f"### SECTION: {section_name}", "meta", "section")

                sequence = build_block_sequence(start_id, self.blocks)
                self._translate_sequence(sequence)
                self.emitter.lines.append("") 
                
        return {
            "python_code": self.emitter.get_code(),
            "mappings": self.emitter.mappings,
            "warnings": self.emitter.warnings
        }

    def _generate_section_name(self, block: ScratchBlock) -> str:
        """Determines a readable section name based on the starting block."""
        opcode = block.opcode
        if opcode == "event_whenflagclicked":
            return "Green Flag Setup"
        elif opcode == "event_whenkeypressed":
            return f"Key Pressed: {self._get_field(block, 'KEY_OPTION')}"
        elif opcode == "event_whenthisspriteclicked":
            return "Sprite Clicked"
        elif opcode == "event_whenbroadcastreceived":
            return f"Message Received: {self._get_field(block, 'BROADCAST_OPTION')}"
        elif opcode == "procedures_definition":
            return "Custom Block Definition"
        elif opcode == "control_start_as_clone":
            return "Clone Startup"
        return "General Logic"

    def _translate_sequence(self, sequence: list[str]):
        for block_id in sequence:
            block = self.blocks.get(block_id)
            if isinstance(block, ScratchBlock):
                self._translate_block(block_id, block)

    def _resolve_input(self, block: ScratchBlock, input_name: str, default: str = "0") -> str:
        """
        Recursively resolves an input. It might be a simple number/string,
        or it might be a nested block (like an Operator or Variable).
        """
        if input_name not in block.inputs:
            return default
            
        input_data = block.inputs[input_name]
        if not isinstance(input_data, list) or len(input_data) < 2:
            return default
            
        val_data = input_data[1]
        
        # If it's a string, it's likely a reference to another block (a reporter)
        if isinstance(val_data, str):
            return self._evaluate_reporter(val_data)
            
        # If it's a list, it's a literal value (e.g., [4, "10"], [10, "hello"])
        if isinstance(val_data, list) and len(val_data) > 1:
            val = str(val_data[1])
            # Quote strings, leave numbers
            if not val.replace('.', '', 1).isdigit() and not val.startswith(('sprite.', 'var_')):
                return f'"{val}"'
            return val
            
        return default

    def _get_field(self, block: ScratchBlock, field_name: str, default: str = "") -> str:
        """Extracts field selections (e.g., dropdown menus)."""
        if field_name in block.fields:
            return str(block.fields[field_name][0])
        return default

    def _sanitize_name(self, name: str) -> str:
        """Sanitizes Scratch variable or custom block names to valid Python identifiers."""
        clean = re.sub(r'\W|^(?=\d)', '_', name)
        return clean.lower()

    def _evaluate_reporter(self, block_id: str) -> str:
        """Recursively evaluates Operator, Sensing, and Variable blocks into Python expressions."""
        if block_id not in self.blocks:
            return "None"
            
        block = self.blocks[block_id]
        if not isinstance(block, ScratchBlock):
            # In Scratch, top-level variables are sometimes stored as lists directly
            return f"var_{self._sanitize_name(str(block[1]))}" if isinstance(block, list) else "None"
            
        opcode = block.opcode

        # --- OPERATORS ---
        if opcode == "operator_add":
            return f"({self._resolve_input(block, 'NUM1')} + {self._resolve_input(block, 'NUM2')})"
        elif opcode == "operator_subtract":
            return f"({self._resolve_input(block, 'NUM1')} - {self._resolve_input(block, 'NUM2')})"
        elif opcode == "operator_multiply":
            return f"({self._resolve_input(block, 'NUM1')} * {self._resolve_input(block, 'NUM2')})"
        elif opcode == "operator_divide":
            return f"({self._resolve_input(block, 'NUM1')} / {self._resolve_input(block, 'NUM2')})"
        elif opcode == "operator_random":
            return f"random.randint({self._resolve_input(block, 'FROM')}, {self._resolve_input(block, 'TO')})"
        elif opcode == "operator_gt":
            return f"({self._resolve_input(block, 'OPERAND1')} > {self._resolve_input(block, 'OPERAND2')})"
        elif opcode == "operator_lt":
            return f"({self._resolve_input(block, 'OPERAND1')} < {self._resolve_input(block, 'OPERAND2')})"
        elif opcode == "operator_equals":
            return f"({self._resolve_input(block, 'OPERAND1')} == {self._resolve_input(block, 'OPERAND2')})"
        elif opcode == "operator_and":
            return f"({self._resolve_input(block, 'OPERAND1')} and {self._resolve_input(block, 'OPERAND2')})"
        elif opcode == "operator_or":
            return f"({self._resolve_input(block, 'OPERAND1')} or {self._resolve_input(block, 'OPERAND2')})"
        elif opcode == "operator_not":
            return f"(not {self._resolve_input(block, 'OPERAND')})"
        elif opcode == "operator_join":
            return f"f'{{{self._resolve_input(block, 'STRING1').strip(chr(34))}}}{{{self._resolve_input(block, 'STRING2').strip(chr(34))}}}'"
        elif opcode == "operator_length":
            return f"len(str({self._resolve_input(block, 'STRING')}))"

        # --- SENSING ---
        elif opcode == "sensing_touchingobject":
            return f"sprite.sensing.is_touching({self._resolve_input(block, 'TOUCHINGOBJECTMENU')})"
        elif opcode == "sensing_mousedown":
            return "sprite.sensing.mouse_down()"
        elif opcode == "sensing_mousex":
            return "sprite.sensing.mouse_x"
        elif opcode == "sensing_mousey":
            return "sprite.sensing.mouse_y"
        elif opcode == "sensing_timer":
            return "sprite.sensing.timer()"
        elif opcode == "sensing_answer":
            return "sprite.sensing.answer"

        # --- VARIABLES & LISTS & MOTION REPORTERS ---
        elif opcode == "data_variable":
            return f"var_{self._sanitize_name(self._get_field(block, 'VARIABLE'))}"
        elif opcode == "data_itemoflist":
            return f"list_{self._sanitize_name(self._get_field(block, 'LIST'))}[{self._resolve_input(block, 'INDEX')} - 1]"
        elif opcode == "data_lengthoflist":
            return f"len(list_{self._sanitize_name(self._get_field(block, 'LIST'))})"
        elif opcode == "motion_xposition":
            return "sprite.x"
        elif opcode == "motion_yposition":
            return "sprite.y"
        elif opcode == "motion_direction":
            return "sprite.direction"
            
        # --- MY BLOCKS ARGUMENTS ---
        elif opcode in ["argument_reporter_string_number", "argument_reporter_boolean"]:
            return self._sanitize_name(self._get_field(block, 'VALUE'))

        self.emitter.add_warning(f"Approximated reporter block: {opcode}")
        return f"None # {opcode}"

    def _translate_block(self, block_id: str, block: ScratchBlock):
        opcode = block.opcode

        # ==========================================
        # 1. EVENTS
        # ==========================================
        if opcode == "event_whenflagclicked":
            self.emitter.emit_line("@event.on_green_flag", block_id, opcode)
            self.emitter.emit_line("def green_flag_script():", block_id, opcode)
            self.emitter.indent()
        elif opcode == "event_whenkeypressed":
            key = self._get_field(block, "KEY_OPTION")
            self.emitter.emit_line(f"@event.on_key_pressed('{key}')", block_id, opcode)
            self.emitter.emit_line(f"def key_pressed_{self._sanitize_name(key)}():", block_id, opcode)
            self.emitter.indent()
        elif opcode == "event_whenthisspriteclicked":
            self.emitter.emit_line("@event.on_sprite_clicked", block_id, opcode)
            self.emitter.emit_line("def sprite_clicked_script():", block_id, opcode)
            self.emitter.indent()
        elif opcode == "event_whenbroadcastreceived":
            msg = self._get_field(block, "BROADCAST_OPTION")
            self.emitter.emit_line(f"@event.on_broadcast_received('{msg}')", block_id, opcode)
            self.emitter.emit_line(f"def receive_{self._sanitize_name(msg)}():", block_id, opcode)
            self.emitter.indent()
        elif opcode == "event_broadcast":
            msg = self._resolve_input(block, "BROADCAST_INPUT", '""')
            self.emitter.emit_line(f"sprite.events.broadcast({msg})", block_id, opcode)
        elif opcode == "event_broadcastandwait":
            msg = self._resolve_input(block, "BROADCAST_INPUT", '""')
            self.emitter.emit_line(f"await sprite.events.broadcast_and_wait({msg})", block_id, opcode, "Requires async logic in Python")

        # ==========================================
        # 2. CONTROL
        # ==========================================
        elif opcode == "control_wait":
            secs = self._resolve_input(block, "DURATION")
            self.emitter.emit_line(f"time.sleep({secs})", block_id, opcode)
        elif opcode == "control_repeat":
            times = self._resolve_input(block, "TIMES")
            self.emitter.emit_line(f"for _ in range(int({times})):", block_id, opcode)
            self._handle_substack(block, "SUBSTACK")
        elif opcode == "control_forever":
            self.emitter.emit_line("while True:", block_id, opcode)
            self._handle_substack(block, "SUBSTACK")
        elif opcode == "control_if":
            cond = self._resolve_input(block, "CONDITION", "False")
            self.emitter.emit_line(f"if {cond}:", block_id, opcode)
            self._handle_substack(block, "SUBSTACK")
        elif opcode == "control_if_else":
            cond = self._resolve_input(block, "CONDITION", "False")
            self.emitter.emit_line(f"if {cond}:", block_id, opcode)
            self._handle_substack(block, "SUBSTACK")
            self.emitter.emit_line("else:", block_id, opcode)
            self._handle_substack(block, "SUBSTACK2")
        elif opcode == "control_repeat_until":
            cond = self._resolve_input(block, "CONDITION", "False")
            self.emitter.emit_line(f"while not ({cond}):", block_id, opcode)
            self._handle_substack(block, "SUBSTACK")
        elif opcode == "control_wait_until":
            cond = self._resolve_input(block, "CONDITION", "False")
            self.emitter.emit_line(f"while not ({cond}):", block_id, opcode)
            self.emitter.indent()
            self.emitter.emit_line("time.sleep(0.01) # Yield to event loop", block_id, opcode)
            self.emitter.dedent()
        elif opcode == "control_stop":
            self.emitter.emit_line("return # Stops the current script", block_id, opcode)
            self.emitter.add_warning("Stop blocks are approximated as 'return'.")
        elif opcode == "control_create_clone_of":
            target = self._resolve_input(block, "CLONE_OPTION", '"_myself_"')
            self.emitter.emit_line(f"sprite.control.create_clone({target})", block_id, opcode)
        elif opcode == "control_start_as_clone":
            self.emitter.emit_line("@event.on_clone_start", block_id, opcode)
            self.emitter.emit_line("def clone_startup_script():", block_id, opcode)
            self.emitter.indent()
        elif opcode == "control_delete_this_clone":
            self.emitter.emit_line("sprite.control.delete_clone()", block_id, opcode)

        # ==========================================
        # 3. MOTION
        # ==========================================
        elif opcode == "motion_movesteps":
            self.emitter.emit_line(f"sprite.motion.move({self._resolve_input(block, 'STEPS')})", block_id, opcode)
        elif opcode == "motion_turnright":
            self.emitter.emit_line(f"sprite.motion.turn_right({self._resolve_input(block, 'DEGREES')})", block_id, opcode)
        elif opcode == "motion_turnleft":
            self.emitter.emit_line(f"sprite.motion.turn_left({self._resolve_input(block, 'DEGREES')})", block_id, opcode)
        elif opcode == "motion_pointindirection":
            self.emitter.emit_line(f"sprite.direction = {self._resolve_input(block, 'DIRECTION')}", block_id, opcode)
        elif opcode == "motion_gotoxy":
            self.emitter.emit_line(f"sprite.motion.go_to(x={self._resolve_input(block, 'X')}, y={self._resolve_input(block, 'Y')})", block_id, opcode)
        elif opcode == "motion_glidesecstoxy":
            self.emitter.emit_line(f"sprite.motion.glide(secs={self._resolve_input(block, 'SECS')}, x={self._resolve_input(block, 'X')}, y={self._resolve_input(block, 'Y')})", block_id, opcode)
        elif opcode == "motion_setx":
            self.emitter.emit_line(f"sprite.x = {self._resolve_input(block, 'X')}", block_id, opcode)
        elif opcode == "motion_sety":
            self.emitter.emit_line(f"sprite.y = {self._resolve_input(block, 'Y')}", block_id, opcode)
        elif opcode == "motion_changexby":
            self.emitter.emit_line(f"sprite.x += {self._resolve_input(block, 'DX')}", block_id, opcode)
        elif opcode == "motion_changeyby":
            self.emitter.emit_line(f"sprite.y += {self._resolve_input(block, 'DY')}", block_id, opcode)
        elif opcode == "motion_ifonedgebounce":
            self.emitter.emit_line("sprite.motion.bounce_if_on_edge()", block_id, opcode)

        # ==========================================
        # 4. LOOKS
        # ==========================================
        elif opcode == "looks_sayforsecs":
            self.emitter.emit_line(f"sprite.looks.say({self._resolve_input(block, 'MESSAGE')}, secs={self._resolve_input(block, 'SECS')})", block_id, opcode)
        elif opcode == "looks_say":
            self.emitter.emit_line(f"sprite.looks.say({self._resolve_input(block, 'MESSAGE')})", block_id, opcode)
        elif opcode == "looks_thinkforsecs":
            self.emitter.emit_line(f"sprite.looks.think({self._resolve_input(block, 'MESSAGE')}, secs={self._resolve_input(block, 'SECS')})", block_id, opcode)
        elif opcode == "looks_think":
            self.emitter.emit_line(f"sprite.looks.think({self._resolve_input(block, 'MESSAGE')})", block_id, opcode)
        elif opcode == "looks_show":
            self.emitter.emit_line("sprite.looks.show()", block_id, opcode)
        elif opcode == "looks_hide":
            self.emitter.emit_line("sprite.looks.hide()", block_id, opcode)
        elif opcode == "looks_switchcostumeto":
            self.emitter.emit_line(f"sprite.costume = {self._resolve_input(block, 'COSTUME')}", block_id, opcode)
        elif opcode == "looks_nextcostume":
            self.emitter.emit_line("sprite.looks.next_costume()", block_id, opcode)
        elif opcode == "looks_changesizeby":
            self.emitter.emit_line(f"sprite.size += {self._resolve_input(block, 'CHANGE')}", block_id, opcode)
        elif opcode == "looks_setsize":
            self.emitter.emit_line(f"sprite.size = {self._resolve_input(block, 'SIZE')}", block_id, opcode)
        elif opcode == "looks_cleargraphiceffects":
            self.emitter.emit_line("sprite.looks.clear_effects()", block_id, opcode)

        # ==========================================
        # 5. SOUND
        # ==========================================
        elif opcode == "sound_playuntildone":
            self.emitter.emit_line(f"sprite.sound.play_until_done({self._resolve_input(block, 'SOUND_MENU')})", block_id, opcode)
        elif opcode == "sound_play":
            self.emitter.emit_line(f"sprite.sound.play({self._resolve_input(block, 'SOUND_MENU')})", block_id, opcode)
        elif opcode == "sound_stopallsounds":
            self.emitter.emit_line("sprite.sound.stop_all()", block_id, opcode)
        elif opcode == "sound_changevolumeby":
            self.emitter.emit_line(f"sprite.volume += {self._resolve_input(block, 'VOLUME')}", block_id, opcode)
        elif opcode == "sound_setvolumeto":
            self.emitter.emit_line(f"sprite.volume = {self._resolve_input(block, 'VOLUME')}", block_id, opcode)

        # ==========================================
        # 6. SENSING (Action blocks)
        # ==========================================
        elif opcode == "sensing_askandwait":
            self.emitter.emit_line(f"sprite.sensing.ask_and_wait({self._resolve_input(block, 'QUESTION')})", block_id, opcode)
        elif opcode == "sensing_resettimer":
            self.emitter.emit_line("sprite.sensing.reset_timer()", block_id, opcode)

        # ==========================================
        # 7. VARIABLES & LISTS
        # ==========================================
        elif opcode == "data_setvariableto":
            var_name = self._sanitize_name(self._get_field(block, "VARIABLE"))
            val = self._resolve_input(block, "VALUE")
            self.emitter.emit_line(f"var_{var_name} = {val}", block_id, opcode)
        elif opcode == "data_changevariableby":
            var_name = self._sanitize_name(self._get_field(block, "VARIABLE"))
            val = self._resolve_input(block, "VALUE")
            self.emitter.emit_line(f"var_{var_name} += {val}", block_id, opcode)
        elif opcode == "data_showvariable":
            var_name = self._sanitize_name(self._get_field(block, "VARIABLE"))
            self.emitter.emit_line(f"sprite.ui.show_variable('var_{var_name}')", block_id, opcode)
        elif opcode == "data_hidevariable":
            var_name = self._sanitize_name(self._get_field(block, "VARIABLE"))
            self.emitter.emit_line(f"sprite.ui.hide_variable('var_{var_name}')", block_id, opcode)
            
        elif opcode == "data_addtolist":
            list_name = self._sanitize_name(self._get_field(block, "LIST"))
            val = self._resolve_input(block, "ITEM")
            self.emitter.emit_line(f"list_{list_name}.append({val})", block_id, opcode)
        elif opcode == "data_deleteoflist":
            list_name = self._sanitize_name(self._get_field(block, "LIST"))
            index = self._resolve_input(block, "INDEX")
            # Scratch is 1-indexed, Python is 0-indexed
            self.emitter.emit_line(f"del list_{list_name}[{index} - 1]", block_id, opcode)
        elif opcode == "data_deletealloflist":
            list_name = self._sanitize_name(self._get_field(block, "LIST"))
            self.emitter.emit_line(f"list_{list_name}.clear()", block_id, opcode)
        elif opcode == "data_insertatlist":
            list_name = self._sanitize_name(self._get_field(block, "LIST"))
            index = self._resolve_input(block, "INDEX")
            val = self._resolve_input(block, "ITEM")
            self.emitter.emit_line(f"list_{list_name}.insert({index} - 1, {val})", block_id, opcode)
        elif opcode == "data_replaceitemoflist":
            list_name = self._sanitize_name(self._get_field(block, "LIST"))
            index = self._resolve_input(block, "INDEX")
            val = self._resolve_input(block, "ITEM")
            self.emitter.emit_line(f"list_{list_name}[{index} - 1] = {val}", block_id, opcode)

        # ==========================================
        # 8. MY BLOCKS (Procedures)
        # ==========================================
        elif opcode == "procedures_definition":
            # The custom block definition points to a 'procedures_prototype' which holds the signature
            custom_block_id = block.inputs.get("custom_block", [])[1]
            if isinstance(custom_block_id, str) and custom_block_id in self.blocks:
                prototype = self.blocks[custom_block_id]
                # 'proccode' contains the Scratch signature, e.g., "jump %s %n"
                proc_code = prototype.inputs.get("proccode", ["", "custom_function"])[1]
                # We sanitize the first word to use as the function name
                func_name = self._sanitize_name(str(proc_code).split()[0])
                
                # Get arguments if they exist
                args = prototype.inputs.get("argumentids", ["", "[]"])[1]
                import json
                try:
                    arg_list = json.loads(str(args))
                    arg_str = ", ".join([f"arg_{i}" for i in range(len(arg_list))])
                except:
                    arg_str = ""
                    
                self.emitter.emit_line(f"def {func_name}({arg_str}):", block_id, opcode)
                self.emitter.indent()
                
        elif opcode == "procedures_call":
            # The mutation object stores the proccode for calls
            mutation = block.inputs.get("mutation", {})
            proccode = mutation.get("proccode", "custom_function") if isinstance(mutation, dict) else str(mutation)
            func_name = self._sanitize_name(proccode.split()[0])
            
            # Extract arguments being passed
            passed_args = []
            for key, val in block.inputs.items():
                if key != "mutation":
                    passed_args.append(self._resolve_input(block, key))
            
            arg_str = ", ".join(passed_args)
            self.emitter.emit_line(f"{func_name}({arg_str})", block_id, opcode)

        # ==========================================
        # UNSUPPORTED FALLBACK
        # ==========================================
        else:
            self.emitter.add_warning(f"Unsupported block type: {opcode}")
            self.emitter.emit_line(f"# TODO: Translate '{opcode}'", block_id, opcode, "This block is not fully supported yet.")

    def _handle_substack(self, block: ScratchBlock, input_key: str):
        """Helper to traverse nested code blocks within control structures like 'if' and 'repeat'."""
        if input_key in block.inputs:
            substack_id = block.inputs[input_key][1]
            if isinstance(substack_id, str):
                sub_sequence = build_block_sequence(substack_id, self.blocks)
                self._translate_sequence(sub_sequence)
            else:
                self.emitter.emit_line("pass # Empty block", "", "pass")
        else:
            self.emitter.emit_line("pass # Empty block", "", "pass")
            
        self.emitter.dedent()