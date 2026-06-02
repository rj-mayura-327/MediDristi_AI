"""
MediDrishti AI - Unit Tests

Tests for the backend modules of the MediDrishti AI application.
Run with: pytest tests/test_backend.py
"""

import pytest
from backend.report_parser import (
    validate_report_file,
    parse_medical_parameters,
)
from backend.analyzer import analyze_parameters
from backend.health_score import calculate_health_score, risk_level
from backend.diet_engine import generate_diet_recommendations
from backend.precaution_engine import generate_precaution_plan


class TestReportParser:
    """Test report parsing functionality."""
    
    def test_validate_report_file_pdf(self):
        """Test PDF file validation."""
        assert validate_report_file("report.pdf") == True
    
    def test_validate_report_file_jpg(self):
        """Test JPG file validation."""
        assert validate_report_file("report.jpg") == True
    
    def test_validate_report_file_png(self):
        """Test PNG file validation."""
        assert validate_report_file("report.png") == True
    
    def test_validate_report_file_invalid(self):
        """Test invalid file validation."""
        assert validate_report_file("report.txt") == False
    
    def test_parse_medical_parameters_hemoglobin(self):
        """Test extraction of hemoglobin values."""
        text = "Hemoglobin: 14.5 g/dL"
        result = parse_medical_parameters(text)
        assert "hemoglobin" in result
    
    def test_parse_medical_parameters_blood_sugar(self):
        """Test extraction of blood sugar values."""
        text = "Blood Sugar: 95 mg/dL"
        result = parse_medical_parameters(text)
        assert "blood sugar" in result or len(result) > 0
    
    def test_parse_medical_parameters_empty_text(self):
        """Test parsing empty text."""
        result = parse_medical_parameters("")
        assert result == {}


class TestAnalyzer:
    """Test parameter analysis functionality."""
    
    def test_analyze_parameters_normal(self):
        """Test analysis of normal parameters."""
        parsed = {"hemoglobin": "14.5"}
        results = analyze_parameters(parsed)
        assert len(results) > 0
        assert results[0]["status"] == "Normal"
    
    def test_analyze_parameters_high(self):
        """Test analysis of high parameters."""
        parsed = {"cholesterol": "250"}
        results = analyze_parameters(parsed)
        assert len(results) > 0
        assert results[0]["status"] == "High"
    
    def test_analyze_parameters_low(self):
        """Test analysis of low parameters."""
        parsed = {"hemoglobin": "7.0"}
        results = analyze_parameters(parsed)
        assert len(results) > 0
        assert results[0]["status"] == "Low"
    
    def test_analyze_parameters_multiple(self):
        """Test analysis of multiple parameters."""
        parsed = {
            "hemoglobin": "12.0",
            "cholesterol": "150",
            "blood sugar": "100"
        }
        results = analyze_parameters(parsed)
        assert len(results) == 3


class TestHealthScore:
    """Test health score calculation."""
    
    def test_calculate_health_score_all_normal(self):
        """Test health score with all normal parameters."""
        parameters = [
            {"parameter": "Hemoglobin", "status": "Normal"},
            {"parameter": "Cholesterol", "status": "Normal"},
        ]
        score = calculate_health_score(parameters)
        assert score == 100
    
    def test_calculate_health_score_one_abnormal(self):
        """Test health score with one abnormal parameter."""
        parameters = [
            {"parameter": "Hemoglobin", "status": "Normal"},
            {"parameter": "Cholesterol", "status": "High"},
        ]
        score = calculate_health_score(parameters)
        assert score < 100
        assert score > 0
    
    def test_calculate_health_score_empty(self):
        """Test health score with no parameters."""
        score = calculate_health_score([])
        assert score == 70
    
    def test_risk_level_low(self):
        """Test risk level classification - Low."""
        assert risk_level(85) == "Low"
    
    def test_risk_level_moderate(self):
        """Test risk level classification - Moderate."""
        assert risk_level(65) == "Moderate"
    
    def test_risk_level_high(self):
        """Test risk level classification - High."""
        assert risk_level(35) == "High"


class TestDietEngine:
    """Test diet recommendation engine."""
    
    def test_generate_diet_recommendations_empty(self):
        """Test diet recommendations with no parameters."""
        recommendations = generate_diet_recommendations([])
        assert "include" in recommendations
        assert "limit" in recommendations
        assert "hydration" in recommendations
        assert "nutrition" in recommendations
    
    def test_generate_diet_recommendations_with_parameters(self):
        """Test diet recommendations with parameters."""
        parameters = [
            {
                "parameter": "Hemoglobin",
                "status": "Low",
            },
        ]
        recommendations = generate_diet_recommendations(parameters)
        assert len(recommendations["include"]) > 0
        assert "Spinach" in recommendations["include"]
    
    def test_generate_diet_recommendations_cholesterol(self):
        """Test diet recommendations for high cholesterol."""
        parameters = [
            {
                "parameter": "Cholesterol",
                "status": "High",
            },
        ]
        recommendations = generate_diet_recommendations(parameters)
        assert len(recommendations["include"]) > 0


class TestPrecautionEngine:
    """Test precaution recommendation engine."""
    
    def test_generate_precaution_plan_empty(self):
        """Test precautions with no parameters."""
        plan = generate_precaution_plan([])
        assert "daily_precautions" in plan
        assert "lifestyle_changes" in plan
        assert "monitoring_recommendations" in plan
        assert "medical_follow_up" in plan
    
    def test_generate_precaution_plan_with_parameters(self):
        """Test precautions with parameters."""
        parameters = [
            {
                "parameter": "Hemoglobin",
                "status": "Low",
            },
        ]
        plan = generate_precaution_plan(parameters)
        assert len(plan["daily_precautions"]) > 0
        assert len(plan["lifestyle_changes"]) > 0
    
    def test_generate_precaution_plan_normal_values(self):
        """Test precautions ignore normal values."""
        parameters = [
            {
                "parameter": "Blood Sugar",
                "status": "Normal",
            },
        ]
        plan = generate_precaution_plan(parameters)
        # Should still have default precautions
        assert len(plan["daily_precautions"]) > 0


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_complete_workflow(self):
        """Test a complete analysis workflow."""
        # Parse parameters
        text = "Hemoglobin: 10.0 g/dL\nCholesterol: 240 mg/dL"
        parsed = parse_medical_parameters(text)
        assert len(parsed) > 0
        
        # Analyze parameters
        analysis = analyze_parameters(parsed)
        assert len(analysis) > 0
        
        # Calculate health score
        score = calculate_health_score(analysis)
        assert 0 <= score <= 100
        
        # Get risk level
        level = risk_level(score)
        assert level in ["Low", "Moderate", "High"]
        
        # Get recommendations
        diet = generate_diet_recommendations(analysis)
        precautions = generate_precaution_plan(analysis)
        
        assert len(diet["include"]) > 0
        assert len(precautions["daily_precautions"]) > 0


# Fixtures for common test data
@pytest.fixture
def sample_parameters():
    """Provide sample parsed parameters."""
    return {
        "hemoglobin": "12.5",
        "rbc": "4.5",
        "wbc": "7.5",
        "platelets": "250",
        "blood sugar": "95",
        "cholesterol": "180",
    }


@pytest.fixture
def sample_analysis_results():
    """Provide sample analysis results."""
    return [
        {
            "parameter": "Hemoglobin",
            "value": "12.5",
            "normal_range": "12.0 - 17.5 g/dL",
            "status": "Normal",
            "medical_explanation": "Normal hemoglobin level",
            "simple_explanation": "Your hemoglobin is normal",
        },
        {
            "parameter": "Blood Sugar",
            "value": "95",
            "normal_range": "70 - 110 mg/dL",
            "status": "Normal",
            "medical_explanation": "Normal blood sugar",
            "simple_explanation": "Your blood sugar is normal",
        },
    ]


if __name__ == "__main__":
    # Run tests with: python -m pytest tests/test_backend.py -v
    pytest.main([__file__, "-v"])
