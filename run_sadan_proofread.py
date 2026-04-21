# -*- coding: utf-8 -*-
import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\AMD\AJ\hwp_proofreading_package"

sys.path.insert(0, BASE)

import importlib.util
spec = importlib.util.spec_from_file_location("proofread", os.path.join(BASE, "hwp_ollama_proofread.py"))
mod = importlib.util.module_from_spec(spec)

mod.RULES_FILE = os.path.join(BASE, "hwp_proofreading", "config", "rules_documentation.txt")
mod.CHINA_PLACE_FILE = os.path.join(BASE, "hwp_proofreading", "config", "rules_china_place.txt")
mod.HWP_DIR = r"C:\사전"

spec.loader.exec_module(mod)