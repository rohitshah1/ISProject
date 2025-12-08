


import os


def setup_keys():
    
    print("="*70)
    print(" Climate & Agriculture Project - API Key Setup")
    print("="*70)
    print()
    print("This script will help you configure your API keys for data acquisition.")
    print()
    print("You need:")
    print("  1. NOAA Climate Data Online API Token")
    print("     Get it at: https://www.ncdc.noaa.gov/cdo-web/token")
    print()
    print("  2. USDA NASS QuickStats API Key")
    print("     Get it at: https://quickstats.nass.usda.gov/api")
    print()
    print("-"*70)
    print()
    
  
    print("Enter your NOAA API Token:")
    print("(or press Enter to skip)")
    noaa_token = input("NOAA Token: ").strip()
    
    if not noaa_token:
        noaa_token = "YOUR_NOAA_TOKEN_HERE"
        print("Skipped NOAA token")
    else:
        print("NOAA token set")
    
    print()
    
    
    print("Enter your USDA NASS API Key:")
    print("(or press Enter to skip)")
    usda_key = input("USDA Key: ").strip()
    
    if not usda_key:
        usda_key = "YOUR_USDA_KEY_HERE"
        print("Skipped USDA key")
    else:
        print("USDA key set")
    
    print()
    print("-"*70)
    print()
    
    
    config_path = "/Users/dru/ISProject/config.py"
    with open(config_path, 'r') as f:
        config_content = f.read()
    
    
    config_content = config_content.replace(
        "NOAA_API_TOKEN = os.getenv('NOAA_API_TOKEN', 'YOUR_NOAA_TOKEN_HERE')",
        f"NOAA_API_TOKEN = os.getenv('NOAA_API_TOKEN', '{noaa_token}')"
    )
    
    config_content = config_content.replace(
        "USDA_API_KEY = os.getenv('USDA_API_KEY', 'YOUR_USDA_KEY_HERE')",
        f"USDA_API_KEY = os.getenv('USDA_API_KEY', '{usda_key}')"
    )
    
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print("Configuration updated!")
    print(f"File: {config_path}")
    print()
    
    
    noaa_set = noaa_token != "YOUR_NOAA_TOKEN_HERE"
    usda_set = usda_key != "YOUR_USDA_KEY_HERE"
    
    if noaa_set and usda_set:
        print("All API keys configured!")
        print()
        print("Next steps:")
        print("  1. Download NOAA data:  python scripts/get_noaa_data.py")
        print("  2. Download USDA data:  python scripts/get_usda_data.py")
        print("  3. Run full pipeline:   ./workflow/run_all.sh")
    else:
        print("Some API keys are missing:")
        if not noaa_set:
            print("  - NOAA token not set")
        if not usda_set:
            print("  - USDA key not set")
        print()
        print("You can:")
        print("  1. Run this script again to add keys")
        print("  2. Manually edit config.py")
        print("  3. Set environment variables:")
        print("     export NOAA_API_TOKEN='your_token'")
        print("     export USDA_API_KEY='your_key'")
    
    print()
    print("="*70)
    print("test")


if __name__ == "__main__":
    try:
        setup_keys()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please manually edit config.py to add your API keys.")

