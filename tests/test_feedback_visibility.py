import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ACTIVE_SCENARIOS = {
    "vodici-odovzdavanie-autobusu": ROOT / "scenare" / "vodici-odovzdavanie-autobusu.html",
    "sziget-nalahko": ROOT / "scenare" / "sziget-nalahko.html",
}


class FeedbackVisibilityTests(unittest.TestCase):
    def test_active_catalog_cards_mark_imported_feedback(self):
        html = INDEX.read_text(encoding="utf-8")
        for slug in ACTIVE_SCENARIOS:
            marker = f'data-scenario-id="{slug}" data-static-feedback="true"'
            self.assertIn(marker, html, f"{slug} nemá trvalý feedback marker")

    def test_catalog_combines_static_and_browser_feedback(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("card.dataset.staticFeedback === 'true'", html)
        self.assertIn("summary.hasFeedback || hasStaticFeedback", html)

    def test_active_scenario_details_show_naty_feedback(self):
        for slug, path in ACTIVE_SCENARIOS.items():
            html = path.read_text(encoding="utf-8")
            self.assertEqual(html.count("data-imported-feedback"), 1, slug)
            self.assertIn("Feedback od Naty", html, slug)
            self.assertIn("Zapracované", html, slug)
            self.assertIn("samostatné označenie anglickej mutácie", html, slug)
            self.assertIn("feedback aj v katalógu", html, slug)

    def test_driver_feedback_preserves_exact_production_note_requests(self):
        html = ACTIVE_SCENARIOS["vodici-odovzdavanie-autobusu"].read_text(encoding="utf-8")
        self.assertIn("odstavenom autobuse", html)
        self.assertIn("objednaní vodičov cez Martinku", html)

    def test_removed_internal_notes_do_not_return(self):
        banned = ("v odstavenom autobuse", "objednať cez Martinku", "objednať vopred cez Martinku")
        for slug, path in ACTIVE_SCENARIOS.items():
            html = path.read_text(encoding="utf-8").lower()
            for phrase in banned:
                self.assertNotIn(phrase.lower(), html, f"{slug}: {phrase}")


if __name__ == "__main__":
    unittest.main()
