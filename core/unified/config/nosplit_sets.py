# -*- coding: utf-8 -*-
# NOSPLIT exception sets - now sourced from hwp_proofread.spacing_rules
# This file is a thin import wrapper for backward compatibility.
# All NOSPLIT sets are maintained in hwp_proofread.spacing_rules as the single source of truth.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

from hwp_proofread.spacing_rules import (
    GEOT_NOSPLIT, SU_NOSPLIT, TTAWI_NOSPLIT, SAI_NOSPLIT, PPUN_NOSPLIT,
    CHUK_NOSPLIT, CHUK_NOSPLIT_PREFIXES, ISANG_NOSPLIT, MIT_NOSPLIT,
    AP_NOSPLIT, GE_NOSPLIT, DEUT_NOSPLIT, CHARYE_NOSPLIT,
    GAWUNDE_NOSPLIT, AN_NOSPLIT, BAK_NOSPLIT, DWI_NOSPLIT,
    DEUNG_NOSPLIT, TTE_NOSPLIT, TTAE_MUN_NOSPLIT, BEON_NOSPLIT,
    DE_NOSPLIT, DAERO_NOSPLIT, MANKEUM_NOSPLIT, JUL_NOSPLIT,
    TEO_NOSPLIT, CHAE_NOSPLIT, JEOK_NOSPLIT, JI_NOSPLIT,
    BA_NOSPLIT, IHA_NOSPLIT, SANG_NOSPLIT, U_NOSPLIT,
    JUNG_NOSPLIT, GAT_NOSPLIT, HA_NOSPLIT, GO_NOSPLIT,
    GAUNDE_NOSPLIT,
    SANG_DIR_NOSPLIT, HA_DIR_NOSPLIT,
    DDUT_NOSPLIT, MODU_NOSPLIT, CHEOK_NOSPLIT,
)
