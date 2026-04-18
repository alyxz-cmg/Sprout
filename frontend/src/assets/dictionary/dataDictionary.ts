export interface DictionaryItem {
  id: string;
  category: string;
  scratchText: string;
  pythonCode: string;
  colorClass: string;
}

export const dictionaryData: DictionaryItem[] = [
  // ==========================================
  // 1. EVENTS (Yellow)
  // ==========================================
  { id: "evt_1", category: "Events", scratchText: "When ⚑ clicked", pythonCode: "@event.on_green_flag\ndef green_flag_script():", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_2", category: "Events", scratchText: "when [space] key pressed", pythonCode: "@event.on_key_pressed('space')\ndef key_pressed_space():", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_3", category: "Events", scratchText: "when this sprite clicked", pythonCode: "@event.on_sprite_clicked\ndef sprite_clicked_script():", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_4", category: "Events", scratchText: "when I receive [message1]", pythonCode: "@event.on_broadcast_received('message1')\ndef receive_message1():", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_5", category: "Events", scratchText: "broadcast [message1]", pythonCode: "sprite.events.broadcast('message1')", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_6", category: "Events", scratchText: "broadcast [message1] and wait", pythonCode: "sprite.events.broadcast_and_wait('message1')", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_7", category: "Events", scratchText: "when backdrop switches to [backdrop1]", pythonCode: "@event.on_backdrop_switched('backdrop1')\ndef backdrop_switched_backdrop1():", colorClass: "bg-yellow-400 text-yellow-900" },
  { id: "evt_8", category: "Events", scratchText: "when [timer] > (10)", pythonCode: "@event.on_greater_than('timer', 10)\ndef greater_than_timer():", colorClass: "bg-yellow-400 text-yellow-900" },

  // ==========================================
  // 2. CONTROL (Orange)
  // ==========================================
  { id: "ctrl_1", category: "Control", scratchText: "wait (1) seconds", pythonCode: "time.sleep(1)", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_2", category: "Control", scratchText: "repeat (10)", pythonCode: "for _ in range(int(10)):", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_3", category: "Control", scratchText: "forever", pythonCode: "while True:", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_4", category: "Control", scratchText: "if <condition> then", pythonCode: "if condition:", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_5", category: "Control", scratchText: "if <condition> then ... else", pythonCode: "if condition:\n    ...\nelse:", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_6", category: "Control", scratchText: "wait until <condition>", pythonCode: "while not (condition):\n    time.sleep(0.01)", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_7", category: "Control", scratchText: "repeat until <condition>", pythonCode: "while not (condition):", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_8", category: "Control", scratchText: "stop [all]", pythonCode: "raise SystemExit()", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_9", category: "Control", scratchText: "stop [this script]", pythonCode: "return", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_10", category: "Control", scratchText: "when I start as a clone", pythonCode: "@event.on_clone_start\ndef clone_startup_script():", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_11", category: "Control", scratchText: "create clone of [myself]", pythonCode: "sprite.control.create_clone('_myself_')", colorClass: "bg-orange-400 text-orange-950" },
  { id: "ctrl_12", category: "Control", scratchText: "delete this clone", pythonCode: "sprite.control.delete_clone()", colorClass: "bg-orange-400 text-orange-950" },

  // ==========================================
  // 3. MOTION (Blue)
  // ==========================================
  { id: "mot_1", category: "Motion", scratchText: "move (10) steps", pythonCode: "sprite.motion.move(10)", colorClass: "bg-blue-500 text-white" },
  { id: "mot_2", category: "Motion", scratchText: "turn ↻ (15) degrees", pythonCode: "sprite.motion.turn_right(15)", colorClass: "bg-blue-500 text-white" },
  { id: "mot_3", category: "Motion", scratchText: "turn ↺ (15) degrees", pythonCode: "sprite.motion.turn_left(15)", colorClass: "bg-blue-500 text-white" },
  { id: "mot_4", category: "Motion", scratchText: "point in direction (90)", pythonCode: "sprite.direction = 90", colorClass: "bg-blue-500 text-white" },
  { id: "mot_5", category: "Motion", scratchText: "point towards [mouse-pointer]", pythonCode: "sprite.motion.point_towards('_mouse_')", colorClass: "bg-blue-500 text-white" },
  { id: "mot_6", category: "Motion", scratchText: "go to [random position]", pythonCode: "sprite.motion.go_to(target='_random_')", colorClass: "bg-blue-500 text-white" },
  { id: "mot_7", category: "Motion", scratchText: "go to x: (0) y: (0)", pythonCode: "sprite.motion.go_to(x=0, y=0)", colorClass: "bg-blue-500 text-white" },
  { id: "mot_8", category: "Motion", scratchText: "glide (1) secs to [random position]", pythonCode: "sprite.motion.glide_to(target='_random_')", colorClass: "bg-blue-500 text-white" },
  { id: "mot_9", category: "Motion", scratchText: "glide (1) secs to x: (0) y: (0)", pythonCode: "sprite.motion.glide(secs=1, x=0, y=0)", colorClass: "bg-blue-500 text-white" },
  { id: "mot_10", category: "Motion", scratchText: "change x by (10)", pythonCode: "sprite.x += 10", colorClass: "bg-blue-500 text-white" },
  { id: "mot_11", category: "Motion", scratchText: "set x to (0)", pythonCode: "sprite.x = 0", colorClass: "bg-blue-500 text-white" },
  { id: "mot_12", category: "Motion", scratchText: "change y by (10)", pythonCode: "sprite.y += 10", colorClass: "bg-blue-500 text-white" },
  { id: "mot_13", category: "Motion", scratchText: "set y to (0)", pythonCode: "sprite.y = 0", colorClass: "bg-blue-500 text-white" },
  { id: "mot_14", category: "Motion", scratchText: "if on edge, bounce", pythonCode: "sprite.motion.bounce_if_on_edge()", colorClass: "bg-blue-500 text-white" },
  { id: "mot_15", category: "Motion", scratchText: "set rotation style [left-right]", pythonCode: "sprite.rotation_style = \"left-right\"", colorClass: "bg-blue-500 text-white" },
  { id: "mot_16", category: "Motion (Reporter)", scratchText: "(x position)", pythonCode: "sprite.x", colorClass: "bg-blue-500/80 border-2 border-blue-500 text-white rounded-full" },
  { id: "mot_17", category: "Motion (Reporter)", scratchText: "(y position)", pythonCode: "sprite.y", colorClass: "bg-blue-500/80 border-2 border-blue-500 text-white rounded-full" },
  { id: "mot_18", category: "Motion (Reporter)", scratchText: "(direction)", pythonCode: "sprite.direction", colorClass: "bg-blue-500/80 border-2 border-blue-500 text-white rounded-full" },

  // ==========================================
  // 4. LOOKS (Purple)
  // ==========================================
  { id: "lks_1", category: "Looks", scratchText: "say [Hello!] for (2) seconds", pythonCode: "sprite.looks.say('Hello!', secs=2)", colorClass: "bg-purple-500 text-white" },
  { id: "lks_2", category: "Looks", scratchText: "say [Hello!]", pythonCode: "sprite.looks.say('Hello!')", colorClass: "bg-purple-500 text-white" },
  { id: "lks_3", category: "Looks", scratchText: "think [Hmm...] for (2) seconds", pythonCode: "sprite.looks.think('Hmm...', secs=2)", colorClass: "bg-purple-500 text-white" },
  { id: "lks_4", category: "Looks", scratchText: "think [Hmm...]", pythonCode: "sprite.looks.think('Hmm...')", colorClass: "bg-purple-500 text-white" },
  { id: "lks_5", category: "Looks", scratchText: "switch costume to [costume2]", pythonCode: "sprite.costume = 'costume2'", colorClass: "bg-purple-500 text-white" },
  { id: "lks_6", category: "Looks", scratchText: "next costume", pythonCode: "sprite.looks.next_costume()", colorClass: "bg-purple-500 text-white" },
  { id: "lks_7", category: "Looks", scratchText: "switch backdrop to [backdrop1]", pythonCode: "stage.looks.switch_backdrop('backdrop1')", colorClass: "bg-purple-500 text-white" },
  { id: "lks_8", category: "Looks", scratchText: "next backdrop", pythonCode: "stage.looks.next_backdrop()", colorClass: "bg-purple-500 text-white" },
  { id: "lks_9", category: "Looks", scratchText: "change size by (10)", pythonCode: "sprite.size += 10", colorClass: "bg-purple-500 text-white" },
  { id: "lks_10", category: "Looks", scratchText: "set size to (100) %", pythonCode: "sprite.size = 100", colorClass: "bg-purple-500 text-white" },
  { id: "lks_11", category: "Looks", scratchText: "change [color] effect by (25)", pythonCode: "sprite.looks.change_effect('color', 25)", colorClass: "bg-purple-500 text-white" },
  { id: "lks_12", category: "Looks", scratchText: "set [color] effect to (0)", pythonCode: "sprite.looks.set_effect('color', 0)", colorClass: "bg-purple-500 text-white" },
  { id: "lks_13", category: "Looks", scratchText: "clear graphic effects", pythonCode: "sprite.looks.clear_effects()", colorClass: "bg-purple-500 text-white" },
  { id: "lks_14", category: "Looks", scratchText: "show", pythonCode: "sprite.looks.show()", colorClass: "bg-purple-500 text-white" },
  { id: "lks_15", category: "Looks", scratchText: "hide", pythonCode: "sprite.looks.hide()", colorClass: "bg-purple-500 text-white" },
  { id: "lks_16", category: "Looks", scratchText: "go to [front] layer", pythonCode: "sprite.looks.go_to_layer('front')", colorClass: "bg-purple-500 text-white" },
  { id: "lks_17", category: "Looks", scratchText: "go [forward] (1) layers", pythonCode: "sprite.looks.change_layer('forward', 1)", colorClass: "bg-purple-500 text-white" },
  { id: "lks_18", category: "Looks (Reporter)", scratchText: "(costume [number])", pythonCode: "sprite.looks.costume('number')", colorClass: "bg-purple-500/80 border-2 border-purple-500 text-white rounded-full" },
  { id: "lks_19", category: "Looks (Reporter)", scratchText: "(backdrop [name])", pythonCode: "stage.looks.backdrop('name')", colorClass: "bg-purple-500/80 border-2 border-purple-500 text-white rounded-full" },
  { id: "lks_20", category: "Looks (Reporter)", scratchText: "(size)", pythonCode: "sprite.size", colorClass: "bg-purple-500/80 border-2 border-purple-500 text-white rounded-full" },

  // ==========================================
  // 5. SOUND (Fuchsia)
  // ==========================================
  { id: "snd_1", category: "Sound", scratchText: "play sound [Meow] until done", pythonCode: "sprite.sound.play_until_done('Meow')", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_2", category: "Sound", scratchText: "start sound [Meow]", pythonCode: "sprite.sound.play('Meow')", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_3", category: "Sound", scratchText: "stop all sounds", pythonCode: "sprite.sound.stop_all()", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_4", category: "Sound", scratchText: "change [pitch] effect by (10)", pythonCode: "sprite.sound.change_effect('pitch', 10)", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_5", category: "Sound", scratchText: "set [pitch] effect to (100)", pythonCode: "sprite.sound.set_effect('pitch', 100)", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_6", category: "Sound", scratchText: "clear sound effects", pythonCode: "sprite.sound.clear_effects()", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_7", category: "Sound", scratchText: "change volume by (-10)", pythonCode: "sprite.volume += -10", colorClass: "bg-fuchsia-500 text-white" },
  { id: "snd_8", category: "Sound", scratchText: "set volume to (100) %", pythonCode: "sprite.volume = 100", colorClass: "bg-fuchsia-500 text-white" },

  // ==========================================
  // 6. SENSING (Cyan)
  // ==========================================
  { id: "sen_1", category: "Sensing", scratchText: "ask [What's your name?] and wait", pythonCode: "sprite.sensing.ask_and_wait(\"What's your name?\")", colorClass: "bg-cyan-500 text-cyan-950" },
  { id: "sen_2", category: "Sensing", scratchText: "reset timer", pythonCode: "sprite.sensing.reset_timer()", colorClass: "bg-cyan-500 text-cyan-950" },
  { id: "sen_3", category: "Sensing", scratchText: "set drag mode [draggable]", pythonCode: "sprite.draggable = True", colorClass: "bg-cyan-500 text-cyan-950" },
  { id: "sen_4", category: "Sensing (Reporter)", scratchText: "<touching [mouse-pointer]?>", pythonCode: "sprite.sensing.is_touching('_mouse_')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_5", category: "Sensing (Reporter)", scratchText: "<touching color [#ffffff]?>", pythonCode: "sprite.sensing.touching_color('#ffffff')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_6", category: "Sensing (Reporter)", scratchText: "<color [#ffffff] is touching [#000000]?>", pythonCode: "sprite.sensing.color_touching_color('#ffffff', '#000000')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_7", category: "Sensing (Reporter)", scratchText: "(distance to [mouse-pointer])", pythonCode: "sprite.sensing.distance_to('_mouse_')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_8", category: "Sensing (Reporter)", scratchText: "(answer)", pythonCode: "sprite.sensing.answer", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_9", category: "Sensing (Reporter)", scratchText: "<key [space] pressed?>", pythonCode: "sprite.sensing.key_pressed('space')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_10", category: "Sensing (Reporter)", scratchText: "<mouse down?>", pythonCode: "sprite.sensing.mouse_down()", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_11", category: "Sensing (Reporter)", scratchText: "(mouse x)", pythonCode: "sprite.sensing.mouse_x", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_12", category: "Sensing (Reporter)", scratchText: "(mouse y)", pythonCode: "sprite.sensing.mouse_y", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_13", category: "Sensing (Reporter)", scratchText: "(loudness)", pythonCode: "sprite.sensing.loudness()", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_14", category: "Sensing (Reporter)", scratchText: "(timer)", pythonCode: "sprite.sensing.timer()", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_15", category: "Sensing (Reporter)", scratchText: "([x position] of [Sprite1])", pythonCode: "sprite.sensing.attribute_of('x position', 'Sprite1')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_16", category: "Sensing (Reporter)", scratchText: "(current [year])", pythonCode: "sprite.sensing.current('YEAR')", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_17", category: "Sensing (Reporter)", scratchText: "(days since 2000)", pythonCode: "sprite.sensing.days_since_2000()", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },
  { id: "sen_18", category: "Sensing (Reporter)", scratchText: "(username)", pythonCode: "sprite.sensing.username", colorClass: "bg-cyan-500/80 border-2 border-cyan-500 text-cyan-950 rounded-full" },

  // ==========================================
  // 7. OPERATORS (Green)
  // ==========================================
  { id: "op_1", category: "Operators", scratchText: "((1) + (1))", pythonCode: "(1 + 1)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_2", category: "Operators", scratchText: "((1) - (1))", pythonCode: "(1 - 1)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_3", category: "Operators", scratchText: "((1) * (1))", pythonCode: "(1 * 1)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_4", category: "Operators", scratchText: "((1) / (1))", pythonCode: "(1 / 1)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_5", category: "Operators", scratchText: "(pick random (1) to (10))", pythonCode: "random.randint(1, 10)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_6", category: "Operators", scratchText: "<(50) > (50)>", pythonCode: "(50 > 50)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_7", category: "Operators", scratchText: "<(50) < (50)>", pythonCode: "(50 < 50)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_8", category: "Operators", scratchText: "<(50) = (50)>", pythonCode: "(50 == 50)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_9", category: "Operators", scratchText: "< <> and <> >", pythonCode: "(cond1 and cond2)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_10", category: "Operators", scratchText: "< <> or <> >", pythonCode: "(cond1 or cond2)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_11", category: "Operators", scratchText: "<not <>>", pythonCode: "(not cond1)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_12", category: "Operators", scratchText: "(join [apple] [banana])", pythonCode: "f'{apple}{banana}'", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_13", category: "Operators", scratchText: "(letter (1) of [apple])", pythonCode: "str('apple')[1 - 1]", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_14", category: "Operators", scratchText: "(length of [apple])", pythonCode: "len(str('apple'))", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_15", category: "Operators", scratchText: "<[apple] contains [a]?>", pythonCode: "('a' in 'apple')", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_16", category: "Operators", scratchText: "((10) mod (3))", pythonCode: "(10 % 3)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_17", category: "Operators", scratchText: "(round (1.5))", pythonCode: "round(1.5)", colorClass: "bg-green-500 text-white rounded-full" },
  { id: "op_18", category: "Operators", scratchText: "([abs] of (10))", pythonCode: "abs(10) # or math.sin, math.log, etc.", colorClass: "bg-green-500 text-white rounded-full" },

  // ==========================================
  // 8. VARIABLES & LISTS (Dark Orange/Red)
  // ==========================================
  { id: "var_1", category: "Variables", scratchText: "set [score] to (0)", pythonCode: "var_score = 0", colorClass: "bg-orange-500 text-white" },
  { id: "var_2", category: "Variables", scratchText: "change [score] by (1)", pythonCode: "var_score += 1", colorClass: "bg-orange-500 text-white" },
  { id: "var_3", category: "Variables", scratchText: "show variable [score]", pythonCode: "sprite.ui.show_variable('var_score')", colorClass: "bg-orange-500 text-white" },
  { id: "var_4", category: "Variables", scratchText: "hide variable [score]", pythonCode: "sprite.ui.hide_variable('var_score')", colorClass: "bg-orange-500 text-white" },
  { id: "var_5", category: "Variables (Reporter)", scratchText: "(score)", pythonCode: "var_score", colorClass: "bg-orange-500/80 border-2 border-orange-500 text-white rounded-full" },
  
  { id: "lst_1", category: "Lists", scratchText: "add [thing] to [list]", pythonCode: "list_list.append('thing')", colorClass: "bg-orange-600 text-white" },
  { id: "lst_2", category: "Lists", scratchText: "delete (1) of [list]", pythonCode: "del list_list[1 - 1]", colorClass: "bg-orange-600 text-white" },
  { id: "lst_3", category: "Lists", scratchText: "delete all of [list]", pythonCode: "list_list.clear()", colorClass: "bg-orange-600 text-white" },
  { id: "lst_4", category: "Lists", scratchText: "insert [thing] at (1) of [list]", pythonCode: "list_list.insert(1 - 1, 'thing')", colorClass: "bg-orange-600 text-white" },
  { id: "lst_5", category: "Lists", scratchText: "replace item (1) of [list] with [thing]", pythonCode: "list_list[1 - 1] = 'thing'", colorClass: "bg-orange-600 text-white" },
  { id: "lst_6", category: "Lists (Reporter)", scratchText: "(item (1) of [list])", pythonCode: "list_list[1 - 1]", colorClass: "bg-orange-600/80 border-2 border-orange-600 text-white rounded-full" },
  { id: "lst_7", category: "Lists (Reporter)", scratchText: "(length of [list])", pythonCode: "len(list_list)", colorClass: "bg-orange-600/80 border-2 border-orange-600 text-white rounded-full" },

  // ==========================================
  // 9. MY BLOCKS (Pink)
  // ==========================================
  { id: "myb_1", category: "My Blocks", scratchText: "define custom_block (arg)", pythonCode: "def custom_block(arg_0):", colorClass: "bg-pink-500 text-white" },
  { id: "myb_2", category: "My Blocks", scratchText: "custom_block (10)", pythonCode: "custom_block(10)", colorClass: "bg-pink-500 text-white" },
];