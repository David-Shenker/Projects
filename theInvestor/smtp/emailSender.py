import smtplib
from logger.logger import log


class Email():

    def __init__(self, sourceEmailAddress: str, sourceEmailPassword: str) -> None:
        self.__sourceEmailAddress = sourceEmailAddress
        self.__sourceEmailPassword = sourceEmailPassword

        log.debug('Email initiliaze')

    def sendEmail(self, destinationEmail: list, subject: str, body: str):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            log.debug('SMTP connection Created')


            smtp.login(self.__sourceEmailAddress, self.__sourceEmailPassword)
            log.debug(f'Logged in to {self.__sourceEmailAddress} email')

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(self.__sourceEmailAddress, destinationEmail, msg)
            log.debug(f'Email sent to {destinationEmail} | Message: {msg}')

            smtp.quit()


