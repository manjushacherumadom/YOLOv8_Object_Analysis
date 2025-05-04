import pytest
from app.detector import ObjectTracker

def test_detection():
    """Test detector functionality"""
    tracker = ObjectTracker()  # No argument passed
    result = tracker.model.predict(r"C:\Manjusha\AI by SRM\SEMESTER 4\ADL\project3\uploads\cafe_cut.mp4")

    assert result is not None  # Modify assertion based on expected output