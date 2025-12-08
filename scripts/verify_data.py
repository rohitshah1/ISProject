"""
verify_data.py

Computes and verifies checksums for data files.
Ensures data integrity throughout the pipeline.

Author: Dev Rishi Udata
Project: Climate Variability and Agricultural Productivity in Illinois
Course: IS477
"""

import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def compute_sha256(filepath: str):
    """Compute SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    
    with open(filepath, "rb") as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def generate_checksums():
    """Generate checksums for all data files."""
    logger.info("Generating checksums...")
    logger.info("="*60)
    
    checksums = {
        'generated_at': datetime.now().isoformat(),
        'files': {}
    }
    
    # Define all data files
    data_files = [
        "data/raw/noaa_full.csv",
        "data/raw/usda_yields.csv",
        "data/processed/noaa_clean.csv",
        "data/processed/usda_clean.csv",
        "data/processed/integrated.csv"
    ]
    
    base_dir = Path("/Users/dru/ISProject")
    
    for rel_path in data_files:
        filepath = base_dir / rel_path
        
        if filepath.exists():
            logger.info(f"Computing checksum: {rel_path}")
            
            checksum = compute_sha256(str(filepath))
            file_size = filepath.stat().st_size
            
            checksums['files'][rel_path] = {
                'sha256': checksum,
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024**2), 2),
                'modified': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            }
            
            logger.info(f"  SHA-256: {checksum}")
            logger.info(f"  Size: {checksums['files'][rel_path]['size_mb']} MB")
        else:
            logger.warning(f"File not found: {rel_path}")
    
    return checksums


def verify_checksums(checksum_file: str):
    """Verify data files against stored checksums."""
    logger.info("\nVerifying checksums...")
    logger.info("="*60)
    
    if not Path(checksum_file).exists():
        logger.error(f"Checksum file not found: {checksum_file}")
        return False
    
    with open(checksum_file, 'r') as f:
        stored_checksums = json.load(f)
    
    base_dir = Path("/Users/dru/ISProject")
    all_valid = True
    
    for rel_path, file_info in stored_checksums['files'].items():
        filepath = base_dir / rel_path
        
        if not filepath.exists():
            logger.error(f"MISSING: {rel_path}")
            all_valid = False
            continue
        
        logger.info(f"Verifying: {rel_path}")
        
        current_checksum = compute_sha256(str(filepath))
        stored_checksum = file_info['sha256']
        
        if current_checksum == stored_checksum:
            logger.info(f"  OK - Checksum matches")
        else:
            logger.error(f"  MISMATCH - File has been modified!")
            logger.error(f"    Expected: {stored_checksum}")
            logger.error(f"    Got: {current_checksum}")
            all_valid = False
    
    if all_valid:
        logger.info("\nAll files verified successfully!")
    else:
        logger.error("\nVerification failed - some files are missing or modified")
    
    return all_valid


def save_checksums(checksums: dict, output_file: str):
    """Save checksums to file."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(checksums, f, indent=2)
    
    logger.info(f"\nChecksums saved to: {output_file}")


def main():
    """Run checksum generation or verification."""
    import sys
    
    checksum_file = "/Users/dru/ISProject/data/checksums.json"
    
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        # Verify mode
        verify_checksums(checksum_file)
    else:
        # Generate mode
        checksums = generate_checksums()
        save_checksums(checksums, checksum_file)
        
        logger.info("\n" + "="*60)
        logger.info("Checksum generation complete!")
        logger.info("="*60)
        logger.info("\nTo verify data integrity later, run:")
        logger.info("  python scripts/verify_data.py verify")


if __name__ == "__main__":
    main()

