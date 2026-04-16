from typing import List, Dict, Union
from .models import ScratchBlock

def get_top_level_blocks(blocks: Dict[str, Union[ScratchBlock, list]]) -> List[str]:
    """
    Finds all top-level block IDs in a given Scratch target.
    This includes Green Flag clicked, events, clone starters, and My Block definitions.
    """
    top_level_ids = []
    for block_id, block in blocks.items():
        if isinstance(block, ScratchBlock) and block.topLevel:
            # We skip procedure prototypes directly, as they are shadowed by the definition
            if block.opcode != "procedures_prototype":
                top_level_ids.append(block_id)
    return top_level_ids

def build_block_sequence(start_id: str, blocks: Dict[str, Union[ScratchBlock, list]]) -> List[str]:
    """
    Traverses the 'next' pointers to build a linear sequence of block IDs.
    """
    sequence = []
    current_id = start_id
    
    while current_id and current_id in blocks:
        sequence.append(current_id)
        current_block = blocks[current_id]
        
        if isinstance(current_block, ScratchBlock):
            current_id = current_block.next
        else:
            break
            
    return sequence