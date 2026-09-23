"""
src/extract_features.py
Feature Extraction Module for EndpointShield AI

Ingests raw byte data and extracts 256-bin Byte Histograms and 
256-bin Entropy Histograms matching the EMBER 2018 schema.
"""

import math
import numpy as np
import pandas as pd


class ByteHistogramExtractor:
    """Calculates 256-bin byte counts normalized across raw bytes."""

    def process(self, byte_data: bytes) -> list:
        counts = np.bincount(np.frombuffer(byte_data, dtype=np.uint8), minlength=256)
        return counts.tolist()


class ByteEntropyHistogramExtractor:
    """Calculates byte entropy distribution across sliding windows."""

    def process(self, byte_data: bytes, window_size: int = 1024, step: int = 256) -> list:
        if len(byte_data) < window_size:
            return [0] * 256

        entropies = []
        for i in range(0, len(byte_data) - window_size + 1, step):
            window = byte_data[i : i + window_size]
            counts = np.bincount(np.frombuffer(window, dtype=np.uint8), minlength=256)
            probs = counts / window_size
            probs = probs[probs > 0]
            entropy = -np.sum(probs * np.log2(probs))
            entropies.append(entropy)

        hist, _ = np.histogram(entropies, bins=256, range=(0, 8))
        return hist.tolist()


def extract_pe_features_from_bytes(byte_data: bytes) -> pd.DataFrame:
    """
    Reads raw bytes of an executable and outputs a single-row DataFrame 
    matching the 512 static features expected by src/predict.py.
    """
    hist_extractor = ByteHistogramExtractor()
    byte_hist = hist_extractor.process(byte_data)

    entropy_extractor = ByteEntropyHistogramExtractor()
    byte_entropy = entropy_extractor.process(byte_data)

    feature_dict = {}
    for i in range(256):
        feature_dict[f"byte_hist_{i}"] = byte_hist[i]
    for i in range(256):
        feature_dict[f"entropy_{i}"] = byte_entropy[i]

    return pd.DataFrame([feature_dict])
