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
):
    return ScratchBlock(
        id=block_id,
        opcode=opcode,
        next=None,
        parent=None,
        inputs=inputs or {},
        fields=fields or {},
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