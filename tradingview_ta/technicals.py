# Tradingview Technical Analysis (tradingview-ta)
# Author: deathlyface (https://github.com/deathlyface)
# Rewritten from https://www.tradingview.com/static/bundles/technicals.f2e6e6a51aebb6cd46f8.js
# License: MIT

class Recommendation:
    buy = "BUY"
    strong_buy = "STRONG_BUY"
    sell = "SELL"
    strong_sell = "STRONG_SELL"
    neutral = "NEUTRAL"
    error = "ERROR"

class Compute:
    def MA(self, close):
        """Compute Moving Average

        Args:
            ma (float): MA value
            close (float): Close value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self < close:
            return Recommendation.buy
        elif self > close:
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def RSI(self, rsi1):
        """Compute Relative Strength Index

        Args:
            rsi (float): RSI value
            rsi1 (float): RSI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self < 30 and rsi1 < self:
            return Recommendation.buy
        elif self > 70 and rsi1 > self:
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Stoch(self, d, k1, d1):
        """Compute Stochastic

        Args:
            k (float): Stoch.K value
            d (float): Stoch.D value
            k1 (float): Stoch.K[1] value
            d1 (float): Stoch.D[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self < 20 and d < 20 and self > d and k1 < d1:
            return Recommendation.buy
        elif self > 80 and d > 80 and self < d and k1 > d1:
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def CCI20(self, cci201):
        """Compute Commodity Channel Index 20

        Args:
            cci20 (float): CCI20 value
            cci201 ([type]): CCI20[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self < -100 and self > cci201:
            return Recommendation.buy
        elif self > 100 and self < cci201:
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def ADX(self, adxpdi, adxndi, adxpdi1, adxndi1):
        """Compute Average Directional Index

        Args:
            adx (float): ADX value
            adxpdi (float): ADX+DI value
            adxndi (float): ADX-DI value
            adxpdi1 (float): ADX+DI[1] value
            adxndi1 (float): ADX-DI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self > 20 and adxpdi1 < adxndi1 and adxpdi > adxndi:
            return Recommendation.buy
        elif self > 20 and adxpdi1 > adxndi1 and adxpdi < adxndi:
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def AO(self, ao1, ao2):
        """Compute Awesome Oscillator

        Args:
            ao (float): AO value
            ao1 (float): AO[1] value
            ao2 (float): AO[2] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (
            self > 0
            and ao1 < 0
            or self > 0
            and ao1 > 0
            and self > ao1
            and ao2 > ao1
        ):
            return Recommendation.buy
        elif (
            self < 0
            and ao1 > 0
            or self < 0
            and ao1 < 0
            and self < ao1
            and ao2 < ao1
        ):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Mom(self, mom1):
        """Compute Momentum

        Args:
            mom (float): Mom value
            mom1 (float): Mom[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self < mom1:
            return Recommendation.sell
        elif self > mom1:
            return Recommendation.buy
        else:
            return Recommendation.neutral

    def MACD(self, signal):
        """Compute Moving Average Convergence/Divergence

        Args:
            macd (float): MACD.macd value
            signal (float): MACD.signal value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self > signal:
            return Recommendation.buy
        elif self < signal:
            return Recommendation.sell
        else:
            return Recommendation.neutral
        
    def BBBuy(self, bblower):
        """Compute Bull Bear Buy

        Args:
            close (float): close value
            bblower (float): BB.lower value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        return Recommendation.buy if self < bblower else Recommendation.neutral

    def BBSell(self, bbupper):
        """Compute Bull Bear Sell

        Args:
            close (float): close value
            bbupper (float): BB.upper value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        return Recommendation.sell if self > bbupper else Recommendation.neutral

    def PSAR(self, open):
        """Compute Parabolic Stop-And-Reverse

        Args:
            psar (float): P.SAR value
            open (float): open value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self < open:
            return Recommendation.buy
        elif self > open:
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Recommend(self):
        """Compute Recommend

        Args:
            value (float): recommend value

        Returns:
            string: "STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL", or "ERROR"
        """
        if self >= -1 and self < -0.5:
            return Recommendation.strong_sell
        elif self >= -0.5 and self < -0.1:
            return Recommendation.sell
        elif self >= -0.1 and self <= 0.1:
            return Recommendation.neutral
        elif self > 0.1 and self <= 0.5:
            return Recommendation.buy
        elif self > 0.5 and self <= 1:
            return Recommendation.strong_buy
        else:
            return Recommendation.error

    def Simple(self):
        """Compute Simple

        Args:
            value (float): Rec.X value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if self == -1:
            return Recommendation.sell
        elif self == 1:
            return Recommendation.buy
        else:
            return Recommendation.neutral
