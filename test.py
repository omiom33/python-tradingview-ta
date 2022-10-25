from colorama import Fore, Style
from tradingview_ta import TA_Handler, Interval, get_multiple_analysis
import tradingview_ta, requests, argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("--proxy", help="Use HTTP proxy")
arg_parser.add_argument("--secureproxy", help="Use HTTPS proxy")

args = arg_parser.parse_args()
proxies = {}
if args.proxy:
    proxies["http"] = args.proxy
if args.secureproxy:
    proxies["https"] = args.secureproxy

print("------------------------------------------------")
print(
    f"Testing {Fore.CYAN}Tradingview-TA{Fore.MAGENTA} v{tradingview_ta.__version__}{Style.RESET_ALL}"
)

print(
    f"This test is {Fore.LIGHTRED_EX}semi-automatic{Style.RESET_ALL}. Please compare with tradingview's data manually."
)

print("------------------------------------------------")

COUNT = 7
success = 0

print(
    f"{Fore.BLUE}#0{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing invalid symbol{Style.RESET_ALL}"
)

handler = TA_Handler(
    symbol="ThisSymbolIsInvalid",
    interval="1m",
    screener="america",
    exchange="NASDAQ",
    proxies = proxies
)
try:
    if analysis := handler.get_analysis():
        print(
            f"{Fore.BLUE}#0{Style.RESET_ALL} Invalid symbol test {Fore.RED}failed{Style.RESET_ALL}. No exception occured."
        )

except Exception as e:
    if str(e) == "Exchange or symbol not found.":
        print(
            f"{Fore.BLUE}#0{Style.RESET_ALL} Invalid symbol test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1
    else:
        print(
            f"{Fore.BLUE}#0{Style.RESET_ALL} Invalid symbol test {Fore.RED}failed{Style.RESET_ALL}. An exception occured, but the symbol is valid."
        )



print(
    f"{Fore.BLUE}#1{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing invalid exchange{Style.RESET_ALL}"
)

handler = TA_Handler(
    symbol="TSLA",
    interval="1m",
    screener="america",
    exchange="binance",
    proxies = proxies
)
try:
    if analysis := handler.get_analysis():
        print(
            f"{Fore.BLUE}#1{Style.RESET_ALL} Invalid exchange test {Fore.RED}failed{Style.RESET_ALL}. No exception occured."
        )

except Exception as e:
    if str(e) == "Exchange or symbol not found.":
        print(
            f"{Fore.BLUE}#1{Style.RESET_ALL} Invalid exchange test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1
    else:
        print(
            f"{Fore.BLUE}#1{Style.RESET_ALL} Invalid exchange test {Fore.RED}failed{Style.RESET_ALL}. An exception occured, but symbol is valid."
        )


print(
    f"{Fore.BLUE}#2{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing timeout{Style.RESET_ALL}"
)

handler = TA_Handler(
    symbol="AAPL",
    interval=Interval.INTERVAL_1_DAY,
    screener="america",
    exchange="NASDAQ",
    timeout=0.0001,
    proxies = proxies
)
try:
    if analysis := handler.get_analysis():
        print(
            f"{Fore.BLUE}#2{Style.RESET_ALL} Timeout test {Fore.RED}failed{Style.RESET_ALL}."
        )

except Exception as e:
    if type(e) == requests.exceptions.ConnectTimeout:
        print(
            f"{Fore.BLUE}#2{Style.RESET_ALL} Timeout test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1


print(
    f"{Fore.BLUE}#3{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing invalid interval{Style.RESET_ALL}"
)

handler = TA_Handler(
    symbol="TSLA",
    interval="1 minute",
    screener="america",
    exchange="NASDAQ",
    proxies = proxies
)
try:
    analysis = handler.get_analysis()
    if (
        analysis
        and input(
            f'{Fore.BLUE}#3{Style.RESET_ALL} Did you see a "defaulting to 1 day" {Fore.YELLOW}warning{Style.RESET_ALL}? (Y/N) '
        ).lower()
        == "y"
    ):
        print(
            f"{Fore.BLUE}#3{Style.RESET_ALL} Invalid interval test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1
    else:
        print(
            f"{Fore.BLUE}#3{Style.RESET_ALL} Invalid interval test {Fore.RED}failed{Style.RESET_ALL}"
        )


except Exception as e:
    print(
        f"{Fore.BLUE}#3{Style.RESET_ALL} Invalid interval test {Fore.RED}failed{Style.RESET_ALL}. An exception occured: {e}"
    )


print(
    f"{Fore.BLUE}#4{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing stock (NASDAQ:AAPL){Style.RESET_ALL}"
)

handler = TA_Handler(
    symbol="AAPL",
    interval=Interval.INTERVAL_1_DAY,
    screener="america",
    exchange="NASDAQ",
    proxies = proxies
)
try:
    analysis = handler.get_analysis()
    print(
        f"{Fore.BLUE}#4{Style.RESET_ALL} Please compare with {Fore.LIGHTMAGENTA_EX}https://www.tradingview.com/symbols/NASDAQ-AAPL/technicals/{Style.RESET_ALL}."
    )

    print(
        f'{Fore.BLUE}#4{Style.RESET_ALL} (Summary) Rec: {analysis.summary["RECOMMENDATION"]}, Sell: {analysis.summary["SELL"]}, Neutral: {analysis.summary["NEUTRAL"]}, Buy: {analysis.summary["BUY"]}'
    )

    if (
        input(
            f"{Fore.BLUE}#4{Style.RESET_ALL} Are the results the same? (Y/N) "
        ).lower()
        == "y"
    ):
        print(
            f"{Fore.BLUE}#4{Style.RESET_ALL} Stock test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1
    else:
        print(
            f"{Fore.BLUE}#4{Style.RESET_ALL} Stock test {Fore.RED}failed{Style.RESET_ALL}"
        )

except Exception as e:
    print(
        f"{Fore.BLUE}#4{Style.RESET_ALL} Stock test {Fore.RED}failed{Style.RESET_ALL}. An exception occured: {e}"
    )


print(
    f"{Fore.BLUE}#5{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing multiple analysis (NASDAQ:TSLA and NYSE:DOCN){Style.RESET_ALL}"
)

try:
    analysis = get_multiple_analysis(screener="america", interval=Interval.INTERVAL_1_HOUR, symbols=["nasdaq:tsla", "nyse:docn"])
    for key, value in analysis.items():
        print(
            f"{Fore.BLUE}#5{Style.RESET_ALL} Please compare with {Fore.LIGHTMAGENTA_EX}https://www.tradingview.com/symbols/{key}/technicals/{Style.RESET_ALL}. (Switch to 1 hour tab)"
        )

        print(
            f'{Fore.BLUE}#5{Style.RESET_ALL} (Summary) Rec: {value.summary["RECOMMENDATION"]}, Sell: {value.summary["SELL"]}, Neutral: {value.summary["NEUTRAL"]}, Buy: {value.summary["BUY"]}'
        )

    if (
        input(
            f"{Fore.BLUE}#5{Style.RESET_ALL} Are the results the same? (Y/N) "
        ).lower()
        == "y"
    ):
        print(
            f"{Fore.BLUE}#5{Style.RESET_ALL} Multiple analysis test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1
    else:
        print(
            f"{Fore.BLUE}#5{Style.RESET_ALL} Multiple analysis test {Fore.RED}failed{Style.RESET_ALL}"
        )

except Exception as e:
    print(
        f"{Fore.BLUE}#5{Style.RESET_ALL} Multiple analysis test {Fore.RED}failed{Style.RESET_ALL}. An exception occured: {e}"
    )


print(
    f"{Fore.BLUE}#6{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Testing get indicators (BINANCE:BTCUSDT){Style.RESET_ALL}"
)

handler = TA_Handler(
    symbol="BTCUSDT",
    interval=Interval.INTERVAL_1_DAY,
    screener="crypto",
    exchange="binance",
    proxies = proxies
)
try:
    print(
        f"{Fore.BLUE}#6{Style.RESET_ALL} Please compare with {Fore.LIGHTMAGENTA_EX}https://www.tradingview.com/symbols/BINANCE:BTCUSDT/technicals/{Style.RESET_ALL}. (Check for indicators)"
    )

    print(f"{Fore.BLUE}#6{Style.RESET_ALL} {handler.get_indicators()}")
    if (
        input(
            f"{Fore.BLUE}#6{Style.RESET_ALL} Are the results the same? (Y/N) "
        ).lower()
        == "y"
    ):
        print(
            f"{Fore.BLUE}#6{Style.RESET_ALL} Get indicators test {Fore.GREEN}success{Style.RESET_ALL}."
        )

        success += 1
    else:
        print(
            f"{Fore.BLUE}#6{Style.RESET_ALL} Get indicators test {Fore.RED}failed{Style.RESET_ALL}"
        )

except Exception as e:
    print(
        f"{Fore.BLUE}#6{Style.RESET_ALL} Get indicators test {Fore.RED}failed{Style.RESET_ALL}. An exception occured: {e}"
    )



print("------------------------------------------------")
print(
    f"Test finished. Result: {Fore.LIGHTWHITE_EX}{success}/{COUNT}{Style.RESET_ALL}."
)
