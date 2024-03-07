Our task is to implement a production-grade signal computation system.

We will be computing the same set of signals for multiple assets (symbols) over a set of dates. From run to run, the set of symbols may change, and so can the set of signals.

We'd like it to be easy to add new signals, such as "volatility-scaled price change", illustrated in the following pseudocode:

    dTradePriceMeanSqr = StreamingEMA(dTraderice * dTradePrice, Alpha)  # EMA_{t} = Alpha * EMA_{t-1} + (1 - Alpha) * x_{t}
    dTradePriceVolScaled = dTradePrice / sqrt(dTradePriceMeanSqr)

We'd also like to be able to test different values of the decay parameter `Alpha` above, or test different implementations of a signal, e.g.:

    dTradePriceMeanAbs = StreamingEMA(abs(dTradePrice), Alpha)
    dTradePriceVolScaled = dTradePrice / dTradePriceMeanAbs

We'd like to be able to quickly compute hundreds of features for hundreds of symbols over hundreds of days. After the signal computation is done, we'll be collecting the time series and fitting models over them. After we're done experimenting with fitting, we'd like the same exact code to be used in live trading that was used to produce the fit chosen for production.

A couple examples are provided. The code in `example-inline.py` computes two simple temporal difference signals. The code is short and easy to understand. However as the set of features grows one could imagine the code becoming difficult to maintain. The code in `example-ops.py` contains the initial steps for implementing the same logic using operator classes that provide a standard interface to specify dependencies and maintain state. We find the latter more amenable to generating the implementation code from a compact configuration file, however you are welcome to use whatever paradigm you find the most fitting.

We'd like you to deliver the following:

 * A way to specify the set of symbols and the computations to be performed on them over a set of dates.
 * A way to distribute the workload of computing the signals. Can (and should) we use caching? The working implementation can be local but do provide a detailed explanation of how it would be distributed.
 * Collect the signals:
   - Combine the individual symbol signals into a collective signal, such as "median `dTradePriceVolScaled` across the chosen symbols".
   - A way to collect the computed signals and present them to a fitting system. As a placeholder model, you can do a linear regression of `dTradePrice` accumulated N steps into the future over the last `M` values of `dTradePrice` (or `dTradePriceVolScaled`), `M >= 1`. You're welcome to use any fitting libraries you find convenient, such as `sklearn`. Evaluation should be done using a rolling fit window.
 * A way to package the above signal computation logic (with fitting parameters if applicable) for deployment on a real-time production system.

The script in `download.sh` will get a sample of 12 days of data for 3 symbols.
