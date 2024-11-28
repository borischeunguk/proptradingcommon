import backtrader as bt
from datetime import timedelta

class BacktraderMacdSltpStrategy(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        # MACD factors
        pfast=12,  # period for the fast moving average
        pslow=26,   # period for the slow moving average
        psignal=9,   # period for the signal moving average

        # Stop Loss and Take Profit Control: risk reward ratio 1:2 - 1:3
        pstoploss=5,  # stop loss % percentage
        ptakeprofit=15,  # take profit % percentage

        pcapitalShare=0.95,  # percentage of capital to use for each trade
        pvalidDuration=7,  # number of days the order is valid for

        ptradecooldown=0  # trade cool down in bars (hours) to avoid over trading
    )

    def __init__(self, logger=None):
        self.logger = logger
        self.logger.info("Input Param: pfast: " + str(self.p.pfast) + "\t pslow: " + str(self.p.pslow) + "\t psignal: " + str(self.p.psignal))

        # record all closed trades information
        self.trades = []

        self.macd = bt.indicators.MACDHisto(self.data.close, period_me1=self.p.pfast, period_me2=self.p.pslow,
                                       period_signal=self.p.psignal)

        # Additional attributes to manage stop loss and take profit
        self.order = None
        self.stop_loss_order = None
        self.take_profit_order = None

        self.trade_cooldown = 0
    def notify_order(self, order):
        current_datetime = bt.num2date(self.data.datetime[0])
        order_type = order.ExecTypes[order.exectype]
        order_status = order.Status[order.status]
        order_side = 'buy' if order.isbuy() else 'sell'
        order_price = order.price
        order_size = order.size

        if order.status in [bt.Order.Completed]:
            self.trade_cooldown = self.p.ptradecooldown
            order_price = order.executed.price
            order_size = order.executed.size

        self.logger.info("Date:" + current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                         + '\t order_ref: ' + str(order.ref)
                         + '\t order_type: ' + str(order_type)
                         + '\t order_status: ' + str(order_status)
                         + '\t order_price: ' + str(order_price)
                         + '\t order_size: ' + str(order_size)
                         + '\t order_side: ' + str(order_side))

        if order.status in [bt.Order.Completed]:
            self.trade_cooldown = self.p.ptradecooldown

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades.append({
                'tradeid': trade.tradeid,
                'pnl': trade.pnl,
                'pnl_net': trade.pnlcomm,
                'size': trade.size,
                'price': trade.price,
                'value': trade.value,
                'commission': trade.commission,
                'bar_open': trade.baropen,
                'bar_close': trade.barclose
            })
            self.logger.info(f'Trade ID: {trade.tradeid}, PnL Gross: {trade.pnl}, PnL Net: {trade.pnlcomm}'
                             f' Size: {trade.size}, Price: {trade.price}, Value: {trade.value}, Commission: {trade.commission}'
                             f' Bar Open: {trade.baropen}, Bar Close: {trade.barclose}')
    def next(self):
        # Convert the internal float datetime to a datetime object
        current_datetime = bt.num2date(self.data.datetime[0])
        cash = self.broker.get_cash()
        position_size = self.position.size
        bar_seq_number = len(self.data)
        self.logger.info("Date:"+current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                         + "\t close: " + str(self.data.close[0])
                         + "\t cash: " + str(cash)
                         + "\t position_size: " + str(position_size)
                         + "\t bar_no: " + str(bar_seq_number)
                         + "\t current_trade_cooldown: " + str(self.trade_cooldown))

        self.logger.debug("Date:"+current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                         + "\t macd: " + str(self.macd.lines.macd[0])
                         + "\t signal: " + str(self.macd.lines.signal[0])
                         + "\t macd_histo: " + str(self.macd.lines.histo[0]))

        if self.trade_cooldown > 0:
            self.trade_cooldown -= 1
            return

        if not self.position:  # not in the market
            if self.macd.lines.histo[0] > 0:  # macd crosses signal to the upside

                # Calculate how much you can buy
                current_close_price = self.data.close[0]  # current close price
                # order price should be next open price, but sometimes may not exist, thus use close price instead
                order_price = self.data.open[1] if bar_seq_number < self.data.buflen() else current_close_price
                long_size = self.p.pcapitalShare * cash // order_price  # This gives the number of shares you can buy

                # Buy that quantity
                # calculate the size of the order based on the next available price (usually the opening price of the next bar) and the available cash in the account
                self.order = self.buy(size=long_size, exectype=bt.Order.Market)

                # Implement Stop Loss and Take Profit
                stop_loss_price = current_close_price * (1 - (self.p.pstoploss / 100))
                take_profit_price = current_close_price * (1 + (self.p.ptakeprofit / 100))
                valid_duration = timedelta(days=self.p.pvalidDuration)

                # Create Stop Loss and Take Profit Sell Orders to limit the loss and lock in profit
                self.stop_loss_order = self.sell(size=long_size, exectype=bt.Order.Stop, price=stop_loss_price
                                                 , valid=current_datetime + valid_duration)
                self.take_profit_order = self.sell(size=long_size, exectype=bt.Order.Limit, price=take_profit_price
                                                 , valid=current_datetime + valid_duration)

                self.logger.debug("Date:"+current_datetime.strftime('%Y-%m-%d %H:%M:%S') + " \t Quantity:" + str(long_size)
                                 + "\t Setup Stop Loss Order:" + str(self.stop_loss_order)
                                 + "\t Setup Take Profit Order:" + str(self.take_profit_order))
        elif self.macd.lines.histo[0] < 0:  # in the market & cross to the downside
            if self.position:
                self.close()  # close long position

                # Cancel Stop Loss and Take Profit Orders if they haven't been executed
                if self.stop_loss_order:
                    self.cancel(self.stop_loss_order)
                    self.logger.debug("Date:"+current_datetime.strftime('%Y-%m-%d %H:%M:%S') + "\t Cancel Stop Loss Order:" + str(self.stop_loss_order))
                if self.take_profit_order:
                    self.cancel(self.take_profit_order)
                    self.logger.debug("Date:"+current_datetime.strftime('%Y-%m-%d %H:%M:%S') + "\t Cancel Take Profit Order:" + str(self.take_profit_order))