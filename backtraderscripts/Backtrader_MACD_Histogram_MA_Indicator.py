import backtrader as bt

class MacdHistoThresholdIndicator(bt.Indicator):
    lines = ('macd', 'macd_signal', 'macd_histo', 'signal')
    params = (
        ('fast', 12),
        ('slow', 26),
        ('signal', 9),
        # ('histogram_ma_period', 5),  # Moving average period for the histogram
        ('histogram_threshold', 15),  # Percentage threshold for MACD histogram to cross signal line
        ('look_back_bars', 3),  # Number of bars to check if histogram is consistently above MA
    )

    # clean up plot lines display
    plotlines = dict(
        # macd=dict(_plotskip='False', ),
        # macd_signal=dict(_plotskip='False', ),
        macd_histo=dict(_plotskip='True', ),
        signal=dict(_plotskip='True', ),
        histogram_ma=dict(_plotskip='True', ),
        strong_buy_signal=dict(_plotskip='True', ),
        strong_sell_signal=dict(_plotskip='True', )
    )

    def __init__(self, logger=None):
        self.logger = logger
        # Calculate EMAs
        self.macd = bt.indicators.MACDHisto(self.data.close,
                                  period_me1=self.p.fast,
                                  period_me2=self.p.slow,
                                  period_signal=self.p.signal)
        self.lines.macd = self.macd.lines.macd
        self.lines.macd_signal = self.macd.lines.signal
        self.lines.macd_histo = self.macd.lines.histo

        # Moving average of the histogram
        # self.lines.histogram_ma = bt.indicators.MovingAverageSimple(self.macd.lines.histo,
        #                                                             period=self.p.histogram_ma_period)
    def next(self):
        bar_seq_number = len(self.data)
        if bar_seq_number < self.p.look_back_bars:
            return
        # Check if histogram is above its MA for the past 'bars' bars
        strong_buy_signal = True
        for i in range(-self.p.look_back_bars + 1, 1):
            if self.macd.lines.histo[i] < 0 or abs(self.macd.lines.histo[i]) < abs(self.lines.macd_signal[i]*self.p.histogram_threshold/100):
                strong_buy_signal = False
                break

        strong_sell_signal = True
        for i in range(-self.p.look_back_bars + 1, 1):
            if self.macd.lines.histo[i] > 0 or abs(self.macd.lines.histo[i]) < abs(self.lines.macd_signal[i]*self.p.histogram_threshold/100):
                strong_sell_signal = False
                break

        self.signal[0] = 1 if strong_buy_signal else -1 if strong_sell_signal else 0

        if self.logger:
            current_datetime = bt.num2date(self.data.datetime[0])
            self.logger.debug("Date:"+current_datetime.strftime('%Y-%m-%d %H:%M:%S')+"\t Macro_Histogram_MA_Indicator: " + str(self.signal[0]))
