from app.core.text_utils import normalize_code


def test_strips_diacritics_and_uppercases():
    assert normalize_code("Khoa Xét Nghiệm") == "KHOA-XET-NGHIEM"


def test_handles_dd_special_case():
    assert normalize_code("Đơn vị Đặc biệt") == "DON-VI-DAC-BIET"


def test_leaves_already_clean_code_untouched():
    assert normalize_code("TB-001") == "TB-001"


def test_collapses_punctuation_and_spaces():
    assert normalize_code("  tb   001 !! ") == "TB-001"
