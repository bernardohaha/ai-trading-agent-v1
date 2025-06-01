import numpy as np
import pandas as pd


class SupportResistanceEngine:
    def __init__(self, ohlcv, bin_size=0.002):  # bin_size = 0.2% do preço
        self.ohlcv = ohlcv
        self.bin_size = bin_size

    def clusterize_levels(self):
        closes = self.ohlcv["close"].values
        price_min, price_max = closes.min(), closes.max()

        # Calcula o tamanho do bin com base no preço atual
        bin_width = (price_max - price_min) * self.bin_size
        if bin_width == 0:
            bin_width = price_min * self.bin_size

        bins = np.arange(price_min, price_max + bin_width, bin_width)
        hist, edges = np.histogram(closes, bins=bins)

        # Seleciona os bins mais populares
        threshold = np.percentile(hist, 70)  # só bins com >= 70% de frequência relativa
        levels = []

        for count, edge in zip(hist, edges[:-1]):
            if count >= threshold:
                level = edge + bin_width / 2
                levels.append(level)

        # Ordena para dividir entre suportes e resistências
        levels = sorted(levels)
        return levels

    def classify_levels(self, current_price, levels):
        supports = [l for l in levels if l <= current_price]
        resistances = [l for l in levels if l > current_price]

        closest_support = max(supports) if supports else None
        closest_resistance = min(resistances) if resistances else None

        return closest_support, closest_resistance

    def suggest_trade_zone(self, current_price, support, resistance):
        if support and current_price <= support * 1.01:
            return "BUY ZONE", support, resistance
        elif resistance and current_price >= resistance * 0.99:
            return "SELL ZONE", support, resistance
        else:
            return "NEUTRAL ZONE", support, resistance
