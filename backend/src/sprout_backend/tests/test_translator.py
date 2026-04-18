# backend/tests/test_translator.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from transpile.translator import ProjectTranslator
from scratch.models import ScratchProject, ScratchBlock


class DummyTarget:
    def __init__(self, name, isStage, blocks):
        self.name = name
        self.isStage = isStage
        self.blocks = blocks


# --- Helpers ---

def make_block(
    block_id,
    opcode,
    inputs=None,
    fields=None,
    mutation=None,
):
    return ScratchBlock(
        id=block_id,
        opcode=opcode,
        next=None,
        parent=None,
        inputs=inputs or {},
        fields=fields or {},
        mutation=mutation or {},
        shadow=False,
        topLevel=True,
    )


# --- Monkeypatch block traversal ---

@pytest.fixture(autouse=True)
def patch_block_helpers(monkeypatch):
    """
    Patch block_index helpers inside transpile.translator
    """

    def fake_get_top_level_blocks(blocks):
        return list(blocks.keys())

    def fake_build_block_sequence(start_id, blocks):
        return [start_id]

    monkeypatch.setattr(
        "transpile.translator.get_top_level_blocks",
        fake_get_top_level_blocks,
    )

    monkeypatch.setattr(
        "transpile.translator.build_block_sequence",
        fake_build_block_sequence,
    )


# --- TESTS ---


def test_basic_motion_translation():
    block = make_block(
        "b1",
        "motion_movesteps",
        inputs={"STEPS": [1, [4, "10"]]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    code = result["python_code"]

    assert "sprite.motion.move(10)" in code
    assert len(result["warnings"]) == 0
    assert len(result["mappings"]) > 0


def test_event_block_creates_function():
    block = make_block("b1", "event_whenflagclicked")

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    code = result["python_code"]

    assert "@event.on_green_flag" in code
    assert "def green_flag_script()" in code


def test_control_repeat_generates_loop():
    block = make_block(
        "b1",
        "control_repeat",
        inputs={"TIMES": [1, [4, "5"]]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    code = result["python_code"]

    assert "for _ in range(int(5)):" in code


def test_operator_add_expression():
    add_block = make_block(
        "b1",
        "operator_add",
        inputs={
            "NUM1": [1, [4, "3"]],
            "NUM2": [1, [4, "4"]],
        },
    )

    target = DummyTarget("Sprite1", False, {"b1": add_block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)

    expr = translator._evaluate_reporter("b1")

    assert expr == "(3 + 4)"


def test_unsupported_block_adds_warning():
    block = make_block("b1", "unknown_block_type")

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert len(result["warnings"]) > 0
    assert "Unsupported block type" in result["warnings"][0]


def test_variable_set_translation():
    block = make_block(
        "b1",
        "data_setvariableto",
        inputs={"VALUE": [1, [4, "42"]]},
        fields={"VARIABLE": ["Score", None]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    code = result["python_code"]

    assert "var_score = 42" in code


def test_menu_backed_input_resolves_to_literal():
    sound_menu = make_block(
        "menu1",
        "sound_sounds_menu",
        fields={"SOUND_MENU": ["Meow", None]},
    )
    play_sound = make_block(
        "b1",
        "sound_play",
        inputs={"SOUND_MENU": [1, "menu1"]},
    )

    target = DummyTarget("Sprite1", False, {"b1": play_sound, "menu1": sound_menu})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert 'sprite.sound.play("Meow")' in result["python_code"]
    assert len(result["warnings"]) == 0


def test_control_stop_uses_stop_option_field():
    block = make_block(
        "b1",
        "control_stop",
        fields={"STOP_OPTION": ["all", None]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert "raise SystemExit()" in result["python_code"]
    assert any("Stop block 'all'" in warning for warning in result["warnings"])


def test_broadcast_and_wait_avoids_invalid_await_in_sync_code():
    menu = make_block(
        "menu1",
        "event_broadcast_menu",
        fields={"BROADCAST_OPTION": ["game over", None]},
    )
    block = make_block(
        "b1",
        "event_broadcastandwait",
        inputs={"BROADCAST_INPUT": [1, "menu1"]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block, "menu1": menu})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert 'sprite.events.broadcast_and_wait("game over")' in result["python_code"]
    assert "await " not in result["python_code"]
    assert any("Broadcast-and-wait" in warning for warning in result["warnings"])


def test_motion_goto_uses_menu_target_literal():
    menu = make_block(
        "menu1",
        "motion_goto_menu",
        fields={"TO": ["_random_", None]},
    )
    block = make_block(
        "b1",
        "motion_goto",
        inputs={"TO": [1, "menu1"]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block, "menu1": menu})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert 'sprite.motion.go_to(target="_random_")' in result["python_code"]
    assert len(result["warnings"]) == 0


def test_motion_setrotationstyle_maps_to_sprite_property():
    block = make_block(
        "b1",
        "motion_setrotationstyle",
        fields={"STYLE": ["left-right", None]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert 'sprite.rotation_style = "left-right"' in result["python_code"]
    assert len(result["warnings"]) == 0


def test_sensing_setdragmode_maps_to_sprite_draggable_flag():
    block = make_block(
        "b1",
        "sensing_setdragmode",
        fields={"DRAG_MODE": ["draggable", None]},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert "sprite.draggable = True" in result["python_code"]
    assert len(result["warnings"]) == 0


def test_procedure_call_uses_block_mutation_metadata():
    block = make_block(
        "b1",
        "procedures_call",
        inputs={"input0": [1, [4, "7"]]},
        mutation={"proccode": "jump %n"},
    )

    target = DummyTarget("Sprite1", False, {"b1": block})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert "jump(7)" in result["python_code"]


def test_procedure_definition_uses_prototype_mutation_metadata():
    definition = make_block(
        "def1",
        "procedures_definition",
        inputs={"custom_block": [1, "proto1"]},
    )
    prototype = make_block(
        "proto1",
        "procedures_prototype",
        mutation={"proccode": "jump %n", "argumentids": "[\"arg1\"]"},
    )

    target = DummyTarget("Sprite1", False, {"def1": definition, "proto1": prototype})
    project = ScratchProject(targets=[target], meta={})

    translator = ProjectTranslator(project)
    result = translator.translate()

    assert "def jump(arg_0):" in result["python_code"]
