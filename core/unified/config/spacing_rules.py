# -*- coding: utf-8 -*-
# Spacing rules - now sourced from hwp_proofread.spacing_rules
# This file is a thin import wrapper for backward compatibility.
# All spacing rules are maintained in hwp_proofread.spacing_rules as the single source of truth.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

from .nosplit_sets import *

from hwp_proofread.spacing_rules import (
    NARA_RULES, SPACING_RULES, CONTEXT_SPACING_RULES, QUOTE_RULES,
)

SPACING_NOSPLIT = GEOT_NOSPLIT | SU_NOSPLIT | TTAWI_NOSPLIT | SAI_NOSPLIT | PPUN_NOSPLIT

CONTEXT_NOSPLIT_EXACT = {
    "가운데", "한가운데", "가운데서", "한가운데서",
    "집안", "방안", "안방", "안쪽", "안전", "안정", "안내", "안녕", "안부", "안심",
    "평안", "보안", "치안", "편안", "불안", "공안", "차안",
    "바깥", "바깥쪽",
    "사이좋다", "사이사이",
    "뒷문", "뒷마당", "뒷산", "뒷모습", "뒷발", "뒷방", "뒷북", "뒷일",
    "앞날", "앞으로", "앞서", "앞뒤", "앞문", "앞길", "앞장",
}

DEPENDENT_NOUN_CATEGORIES = [
    ("것", GEOT_NOSPLIT, 1),
    ("수", SU_NOSPLIT, 1),
    ("따위", TTAWI_NOSPLIT, 2),
    ("사이", SAI_NOSPLIT, 2),
    ("뿐", PPUN_NOSPLIT, 1),
    ("척", CHUK_NOSPLIT, 1),
    ("이상", ISANG_NOSPLIT, 2),
    ("이하", IHA_NOSPLIT, 2),
    ("밑", MIT_NOSPLIT, 1),
    ("등", DEUNG_NOSPLIT, 1),
    ("때", TTE_NOSPLIT, 1),
    ("때문", TTAE_MUN_NOSPLIT, 2),
    ("번", BEON_NOSPLIT, 1),
    ("데", DE_NOSPLIT, 1),
    ("대로", DAERO_NOSPLIT, 2),
    ("만큼", MANKEUM_NOSPLIT, 2),
    ("줄", JUL_NOSPLIT, 1),
    ("듯", DEUT_NOSPLIT, 1),
    ("차례", CHARYE_NOSPLIT, 2),
    ("터", TEO_NOSPLIT, 1),
    ("채", CHAE_NOSPLIT, 1),
    ("적", JEOK_NOSPLIT, 1),
    ("지", JI_NOSPLIT, 1),
    ("바", BA_NOSPLIT, 1),
    ("중", JUNG_NOSPLIT, 1),
    ("상", SANG_NOSPLIT, 1),
    ("우", U_NOSPLIT, 1),
    ("하", HA_NOSPLIT, 1),
    ("같은", GAT_NOSPLIT, 2),
    ("고", GO_NOSPLIT, 1),
    ("앞", AP_NOSPLIT, 1),
    ("게", GE_NOSPLIT, 1),
    ("가운데", GAWUNDE_NOSPLIT, 3),
    ("안", AN_NOSPLIT, 1),
    ("밖", BAK_NOSPLIT, 1),
    ("뒤", DWI_NOSPLIT, 1),
    ("상(방위)", SANG_DIR_NOSPLIT, 2),
    ("하(방위)", HA_DIR_NOSPLIT, 2),
    ("뜻", DDUT_NOSPLIT, 1),
    ("모두", MODU_NOSPLIT, 2),
    ("척하다", CHEOK_NOSPLIT, 2),
    ("가운데(의존)", GAUNDE_NOSPLIT, 3),
]
