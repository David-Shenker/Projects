import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s %(message)s',
                    filename='Projects/theInvestor/TheInvestor.log'
                    )
log = logging.getLogger()
