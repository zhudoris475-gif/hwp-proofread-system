__version__ = "4.0.0"

from .pipeline import ProofreadPipeline
from .io.hwp_reader import HWPReader
from .io.hwp_writer import HWPWriter
from .io.binary_editor import binary_proofread, file_hash, extract_text
from .rules import build_all_rules, load_china_place_rules
from .rules.dependent_nouns import (
    BOTH_FORMS_DEP_NOUNS,
    apply_dependent_noun_inspection,
    apply_text_corrections,
)
from .rules.spacing_rules import SPACING_RULES, CONTEXT_SPACING_RULES, QUOTE_RULES
from .rules.nara_rules import NARA_RULES, generate_dynamic_nara_rules
from .correctors import (
    MiddleDotCorrector,
    QuoteCorrector,
    PlaceNameConverter,
    SpacingCorrector,
)
from .com_editor import COMEditor
from .rule_engine import RuleEngine
from .report import CorrectionReport
from .config import Config
from .analysis.text_analyzer import analyze_text
from .analysis.change_detector import classify_entry
from .analysis.noise_filter import filter_noise_text

__all__ = [
    "ProofreadPipeline",
    "HWPReader",
    "HWPWriter",
    "binary_proofread",
    "file_hash",
    "extract_text",
    "build_all_rules",
    "load_china_place_rules",
    "BOTH_FORMS_DEP_NOUNS",
    "apply_dependent_noun_inspection",
    "apply_text_corrections",
    "SPACING_RULES",
    "CONTEXT_SPACING_RULES",
    "QUOTE_RULES",
    "NARA_RULES",
    "generate_dynamic_nara_rules",
    "MiddleDotCorrector",
    "QuoteCorrector",
    "PlaceNameConverter",
    "SpacingCorrector",
    "COMEditor",
    "RuleEngine",
    "CorrectionReport",
    "Config",
    "analyze_text",
    "classify_entry",
    "filter_noise_text",
]
