import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "scenare"
EXPECTED_DEFAULTS = {
    "maly-partak-na-palube.html": {"video-views", "engagement", "traffic-sk", "traffic-international", "english-version"},
    "sziget-nalahko.html": {"video-views", "engagement", "traffic-sk", "traffic-international", "english-version"},
    "travel-pass-menej-ako-kava.html": {"video-views", "engagement", "traffic-sk", "traffic-international", "english-version"},
    "vodici-odovzdavanie-autobusu.html": {"video-views", "engagement"},
}
ALL_VALUES = {"video-views", "engagement", "traffic-sk", "traffic-international", "english-version"}


class CampaignControlsTests(unittest.TestCase):
    def test_each_scenario_has_clickable_campaign_and_language_controls(self):
        self.assertEqual(set(EXPECTED_DEFAULTS), {path.name for path in SCENARIOS.glob("*.html")})
        for name, expected_checked in EXPECTED_DEFAULTS.items():
            text = (SCENARIOS / name).read_text(encoding="utf-8")
            self.assertIn('class="distribution-panel"', text, name)
            self.assertIn('data-distribution-form', text, name)
            controls = re.findall(
                r'<input\s+type="checkbox"\s+name="distribution"\s+value="([^"]+)"([^>]*)>',
                text,
            )
            self.assertEqual(ALL_VALUES, {value for value, _ in controls}, name)
            checked = {value for value, attrs in controls if re.search(r'\bchecked\b', attrs)}
            self.assertEqual(expected_checked, checked, name)
            self.assertIn('Vytvoriť anglickú jazykovú mutáciu', text, name)
            self.assertIn('../assets/campaign-controls.js', text, name)

    def test_shared_script_persists_each_scenario_selection(self):
        script = (ROOT / "assets" / "campaign-controls.js").read_text(encoding="utf-8")
        self.assertIn("sl-scenario-distribution:", script)
        self.assertIn("addEventListener('change'", script)
        self.assertIn("localStorage.setItem", script)
        self.assertIn("localStorage.getItem", script)
        self.assertIn("data-distribution-summary", script)


if __name__ == "__main__":
    unittest.main()
