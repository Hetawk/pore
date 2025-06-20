#!/usr/bin/env python3
"""
Configuration Override Validation Script

This script validates that the configuration override system is working correctly
by testing various parameter combinations and checking the generated configurations.
"""

import sys
import os
import tempfile
import subprocess
import json
from pathlib import Path

# Add app directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir / 'app'))


def test_config_override():
    """Test the configuration override functionality."""

    print("🧪 Testing Configuration Override System")
    print("=" * 50)

    # Test cases using actual config.py values
    test_cases = [
        {
            "name": "Default Board Dimensions (160x160x40mm)",
            "args": ["--length", "160", "--width", "160", "--thickness", "40", "--dry-run"],
            "expected_outputs": ["Board length: 160mm", "Board width: 160mm", "Board thickness: 40mm"]
        },
        {
            "name": "Default Pore Counts",
            "args": ["--pores-individual", "600", "--pores-comparative", "400", "--pores-density", "500", "--dry-run"],
            "expected_outputs": ["Individual pores: 600", "Comparative pores: 400", "Density pores: 500"]
        },
        {
            "name": "Default Matrix and Hybrid Pore Counts",
            "args": ["--pores-matrix", "800", "--pores-hybrid", "800", "--dry-run"],
            "expected_outputs": ["Matrix pores: 800", "Hybrid pores: 800"]
        },
        {
            "name": "Default Pore Size Range",
            "args": ["--min-pore-radius", "0.03", "--max-pore-radius", "0.08", "--dry-run"],
            "expected_outputs": ["Min pore radius: 0.03", "Max pore radius: 0.08"]
        },
        {
            "name": "Default Visualization Settings",
            "args": ["--dpi", "300", "--figure-size", "12,8", "--elevation", "30", "--azimuth", "60", "--dry-run"],
            "expected_outputs": ["DPI: 300", "Figure size: 12,8", "View elevation: 30°", "View azimuth: 60°"]
        },
        {
            "name": "Default Transparency and Format",
            "args": ["--alpha", "0.9", "--format", "png", "--dry-run"],
            "expected_outputs": ["Alpha transparency: 0.9", "Output format: png"]
        },
        {
            "name": "Small Specimen Configuration (10mm diameter)",
            "args": ["--diameter", "10", "--tolerance", "1", "--dry-run"],
            "expected_outputs": ["Specimen diameter: 10mm", "Specimen tolerance: ±1mm"]
        },
        {
            "name": "Scale Factor Test (10±1mm equivalent: 0.0625 scale)",
            "args": ["--scale", "0.0625", "--dry-run"],
            "expected_outputs": ["Scale factor: 0.0625", "Scaled board: 10", "Scaled pore size:"]
        }
    ]

    script_path = script_dir / "config_override.sh"

    # Run tests
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 40)

        try:
            # Run the configuration script
            result = subprocess.run(
                [str(script_path)] + test_case["args"],
                cwd=script_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                print(f"❌ Test failed: Script returned non-zero exit code")
                print(f"   stderr: {result.stderr}")
                all_passed = False
                continue

            # Check expected outputs
            output = result.stdout
            test_passed = True

            for expected in test_case["expected_outputs"]:
                if expected not in output:
                    print(f"❌ Expected output not found: '{expected}'")
                    test_passed = False
                else:
                    print(f"✅ Found expected output: '{expected}'")

            if test_passed:
                print(f"✅ Test {i} PASSED")
            else:
                print(f"❌ Test {i} FAILED")
                all_passed = False

        except subprocess.TimeoutExpired:
            print(f"❌ Test {i} FAILED: Timeout")
            all_passed = False
        except Exception as e:
            print(f"❌ Test {i} FAILED: {e}")
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests PASSED! Configuration override system is working correctly.")
    else:
        print("❌ Some tests FAILED. Please check the configuration override script.")

    return all_passed


def test_quick_config():
    """Test the quick configuration presets."""

    print("\n🚀 Testing Quick Configuration Presets")
    print("=" * 50)

    quick_script = script_dir / "quick_config.sh"

    # Test help output
    try:
        result = subprocess.run(
            [str(quick_script)],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        if "Simple Pore Analysis - Quick Presets" in result.stdout:
            print("✅ Quick config help system working")
        else:
            print("❌ Quick config help system not working properly")
            return False

    except Exception as e:
        print(f"❌ Quick config test failed: {e}")
        return False

    print("✅ Quick configuration system is working correctly.")
    return True


def demonstrate_usage():
    """Demonstrate common usage patterns."""

    print("\n📚 Usage Demonstration")
    print("=" * 50)

    print("\n1. Default Configuration Test:")
    print("   ./config_override.sh --length 160 --width 160 --thickness 40")
    print("   # Tests default board dimensions from config.py")

    print("\n2. Default Pore Counts Test:")
    print("   ./config_override.sh --pores-individual 600 --pores-comparative 400")
    print("   # Tests default pore counts from config.py")

    print("\n3. Small Specimen Analysis (Your Use Case):")
    print("   ./config_override.sh --diameter 10 --tolerance 1")
    print("   # OR using preset:")
    print("   ./quick_config.sh small-specimen")

    print("\n4. Default Visualization Settings Test:")
    print("   ./config_override.sh --dpi 300 --figure-size 12,8 --elevation 30")
    print("   # Tests default visualization parameters from config.py")

    print("\n5. Default Pore Size Range Test:")
    print("   ./config_override.sh --min-pore-radius 0.03 --max-pore-radius 0.08")
    print("   # Tests default pore size range from config.py")


if __name__ == "__main__":
    print("🔧 Simple Pore Analysis - Configuration Override Validation")
    print("=" * 60)

    # Check if scripts exist
    config_script = script_dir / "config_override.sh"
    quick_script = script_dir / "quick_config.sh"

    if not config_script.exists():
        print("❌ config_override.sh not found!")
        sys.exit(1)

    if not quick_script.exists():
        print("❌ quick_config.sh not found!")
        sys.exit(1)

    # Run tests
    success = True
    success &= test_config_override()
    success &= test_quick_config()

    # Demonstrate usage
    demonstrate_usage()

    print("\n" + "=" * 60)
    if success:
        print("🎉 Configuration override system is ready to use!")
        print("\nDefault configuration values from config.py can be tested:")
        print("  ./config_override.sh --length 160 --width 160 --thickness 40")
        print("  ./config_override.sh --pores-individual 600 --pores-comparative 400")
        print("\nYour specific use case (Small specimens with 10 ± 1 mm diameter):")
        print("  ./config_override.sh --diameter 10 --tolerance 1")
        print("  # OR")
        print("  ./quick_config.sh small-specimen")
    else:
        print("❌ Configuration override system has issues that need to be resolved.")
        sys.exit(1)
