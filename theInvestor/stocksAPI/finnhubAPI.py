import finnhub
import datetime
from typing import Union
from logger.logger import log


class FinnhubAPI():

    # Consts
    ONE_DAY = 86400
    RESOLUTION = 'D'
    STATUS = 's'

    def __init__(self, APIKey: str, stockNameDict: str, cryptoDict: str) -> None:
        self.finnhubAPIKey = APIKey
        self.__setupAPIClient()

        self.stockNameDict = stockNameDict
        self.cryptoDict = cryptoDict

        self.bestInvestment = {'stockName': '', 'dailyPercentage': 0}
        self.investmentsDict = {}

        log.debug('FinnhubAPI initiliazed')

    def __getTimeStamp(self) -> Union[int, int]:
        presentDate = datetime.datetime.now()
        unixTimestampToday = round(datetime.datetime.timestamp(presentDate))
        log.debug(f'Now time stamp is - {unixTimestampToday}')
        unixTimestampYestarday = unixTimestampToday - FinnhubAPI.ONE_DAY
        log.debug(f'Yestarday time stamp is - {unixTimestampYestarday}')

        return unixTimestampYestarday, unixTimestampToday

    def __setupAPIClient(self) -> None:
        global finnhubClient
        finnhubClient = finnhub.Client(api_key=self.finnhubAPIKey)
        log.debug('Finnhub API client was set successfully')

    def __getCryptoQuote(self) -> None:
        unixTimestampYestarday, unixTimestampToday = self.__getTimeStamp()

        for coin in self.cryptoDict:
            log.debug(f'Sending API request to finnhub for crypto quote- {coin}')
            cryptoData = finnhubClient.crypto_candles(self.cryptoDict[coin], FinnhubAPI.RESOLUTION, unixTimestampYestarday, unixTimestampToday)

            if cryptoData.get(FinnhubAPI.STATUS) == 'ok':
                openingPrice = cryptoData.get('o')[0]
                closingPrice = cryptoData.get('c')[0]
                dailyChange = openingPrice - closingPrice
                dailyPercentage = round((dailyChange / openingPrice) * 100, 3)

                if dailyPercentage > 0:
                    log.debug(f'{coin} -> +{dailyPercentage}%')
                else:
                    log.debug(f'{coin} -> {dailyPercentage}%')

                self.investmentsDict[coin] = dailyPercentage

    def __getStockQuote(self) -> None:
        for stock in self.stockNameDict:
            log.debug(f'Sending API request to finnhub for stock quote- {stock}')
            dailyPercentage = finnhubClient.quote(self.stockNameDict[stock])['dp']

            if dailyPercentage:
                if dailyPercentage > 0:
                    log.debug(f"{stock} -> {self.stockNameDict[stock]} -> +{dailyPercentage}%")
                else:
                    log.debug(f"{stock} -> {self.stockNameDict[stock]} -> {dailyPercentage}%")

                self.investmentsDict[stock] = dailyPercentage

    def getSuggestions(self, checkStocks: bool = False, checkCrypto: bool = False) -> None:
        if checkStocks:
            self.__getStockQuote()
        if checkCrypto:
            self.__getCryptoQuote()

        for stock in self.investmentsDict:
            if self.investmentsDict[stock] > self.bestInvestment['dailyPercentage']:
                self.bestInvestment['stockName'] = stock
                self.bestInvestment['dailyPercentage'] = self.investmentsDict[stock]

        log.debug(f"Best Investment: {self.bestInvestment['stockName']} -> {self.bestInvestment['dailyPercentage']}%")

        return self.bestInvestment['stockName'], self.bestInvestment['dailyPercentage']
