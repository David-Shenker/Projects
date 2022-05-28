from logger.logger import log
from mongo.mongo import Mongo
from smtp.emailSender import Email
from stocksAPI.finnhubAPI import FinnhubAPI
from utils.utils import Utils

class TheInvestor():

    # Consts
    DB_NAME = 'theInvestor'

    def __init__(self) -> None:
        self.mongo = Mongo(TheInvestor.DB_NAME)
        self.utils = Utils()

        self.__emailCredsDict = self.mongo.runQuery('config', 'find', {},{'credentials': 1, '_id': 0})
        self.__sourceEmailAddress = self.__emailCredsDict.get('credentials').get('DEV_EMAIL_ADDRESS')
        self.__sourceEmailPassword = self.utils.decodeBase64(self.__emailCredsDict.get('credentials').get('DEV_EMAIL_PASSWORD'))

        self.smtp = Email(self.__sourceEmailAddress, self.__sourceEmailPassword)

        queryResult = self.mongo.runQuery('config', 'find', {'configName': 'FINNHUB_API_KEY'}, {'_id': 0, 'configValue': 1})
        self.finnhubAPIKey = self.utils.decodeBase64(queryResult.get('configValue'))

        stockQueryResponse = self.mongo.runQuery('stocks', 'find', {}, {'_id': 0})
        cryptoQueryResponse = self.mongo.runQuery('crypto', 'find', {}, {'_id': 0})

        self.finnhubAPI = FinnhubAPI(self.finnhubAPIKey, stockQueryResponse, cryptoQueryResponse)

        self.destEmails = self.mongo.runQuery('destenationEmails', 'find', {}, {'_id': 0})

        log.debug('TheInvestor initiliazed')

    def main(self) -> None:
        log.info('Get best investment from finnhub API')
        stockName, dailyPercentage = self.finnhubAPI.getSuggestions(checkStocks=True, checkCrypto=True)

        for receiver in self.destEmails:
            receiverEmail = self.destEmails[receiver]

            subject = 'The Investor'
            msg = f'Hi, {receiver}\n\n Our suggestion for today is:\n    Stock Name -> {stockName}\n    Daily Percentage -> {dailyPercentage}%\n\nGood luck!\nMay we all be rich =]'

            self.smtp.sendEmail(receiverEmail, subject, msg)
            log.info(f'Email sent to - {receiverEmail}')


if __name__ == '__main__':

    log.info('-------------------- TheInvestor --------------------')
    TheInvestor().main()
    log.info('-------------------- Done --------------------')

