import os
import sys
import argparse

# Add src directory to Python Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from netguard.config import DATA_DIR, MODEL_DIR, OUTPUT_DIR
from netguard.models.trainer import ModelTrainer
from netguard.utils.logger import logger

def main():
    parser = argparse.ArgumentParser(description="NetGuard AI Model Training Pipeline")
    parser.add_argument("--data-dir", type=str, default=str(DATA_DIR), help="Path to data directory")
    parser.add_argument("--model-dir", type=str, default=str(MODEL_DIR), help="Path to output models directory")
    parser.add_argument("--output-dir", type=str, default=str(OUTPUT_DIR), help="Path to outputs directory")

    args = parser.parse_args()

    trainer = ModelTrainer(
        data_dir=args.data_dir,
        model_dir=args.model_dir,
        output_dir=args.output_dir
    )

    summary = trainer.run_pipeline()
    logger.info(f"Training completed successfully. Summary: {summary}")

if __name__ == "__main__":
    main()