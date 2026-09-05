from netguard.config import BASE_DIR, DATA_DIR, MODEL_DIR, OUTPUT_DIR, DEFAULT_THRESHOLD, RISK_LEVELS

def test_config_paths():
    assert BASE_DIR.exists()
    assert DATA_DIR.exists()

def test_risk_levels():
    assert "CRITICAL" in RISK_LEVELS
    assert "HIGH" in RISK_LEVELS
    assert "MEDIUM" in RISK_LEVELS
    assert "LOW" in RISK_LEVELS
    assert RISK_LEVELS["CRITICAL"]["min_prob"] == 0.80
