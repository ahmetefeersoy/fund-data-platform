import time
import datetime
import logging
import pandas as pd
from tefas import Crawler
from src.case_study.utils.db import engine
from sqlalchemy import text

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TefasCrawler:

    def __init__(
        self,
    ):
        """Initialize the TefasCrawler with database settings"""
        self.crawler = Crawler()
        
    def clean_oldest_data(self):
        """Clean oldest data from the database to maintain size"""
        
        logger.info("Cleaning oldest data from the database...")
        delete_query = text("""
            DELETE FROM fund_data
            WHERE date < CURRENT_DATE - INTERVAL '180 days';
        """)
        
        with engine.begin() as conn:
            result = conn.execute(delete_query)
            logger.info(f"Deleted {result.rowcount} oldest records from the database.")    

    def save_to_db(self, data):

        """Save fetched fund_data to the database"""

        if data is None or data.empty:
            logger.warning("No data to save to the database.")
            return
        
        fund_columns = [
            "date",
            "code",
            "price",
            "title",
            "market_cap",
            "number_of_shares",
            "number_of_investors",
            "bank_bills",
            "exchange_traded_fund",
            "other",
            "fx_payable_bills",
            "government_bond",
            "foreign_currency_bills",
            "eurobonds",
            "commercial_paper",
            "fund_participation_certificate",
            "real_estate_certificate",
            "venture_capital_investment_fund_participation",
            "real_estate_investment_fund_participation",
            "treasury_bill",
            "stock",
            "government_bonds_and_bills_fx",
            "participation_account",
            "participation_account_au",
            "participation_account_d",
            "participation_account_tl",
            "government_lease_certificates",
            "government_lease_certificates_d",
            "government_lease_certificates_tl",
            "government_lease_certificates_foreign",
            "precious_metals",
            "precious_metals_byf",
            "precious_metals_kba",
            "precious_metals_kks",
            "public_domestic_debt_instruments",
            "private_sector_lease_certificates",
            "private_sector_bond",
            "repo",
            "derivatives",
            "tmm",
            "reverse_repo",
            "asset_backed_securities",
            "term_deposit",
            "term_deposit_au",
            "term_deposit_d",
            "term_deposit_tl",
            "futures_cash_collateral",
            "foreign_debt_instruments",
            "foreign_domestic_debt_instruments",
            "foreign_private_sector_debt_instruments",
            "foreign_exchange_traded_funds",
            "foreign_equity",
            "foreign_securities",
            "foreign_investment_fund_participation_shares",
            "private_sector_international_lease_certificate",
            "private_sector_foreign_debt_instruments",
        ]

        logger.info("Saving data to the database...")

        insert_data = text(f"""
            INSERT INTO fund_data ({", ".join(fund_columns)})
            VALUES ({", ".join([f":{c}" for c in fund_columns])})
            ON CONFLICT (code, date) DO UPDATE SET
                price = EXCLUDED.price,
                market_cap = EXCLUDED.market_cap,
                number_of_shares = EXCLUDED.number_of_shares,
                number_of_investors = EXCLUDED.number_of_investors,
                stock = EXCLUDED.stock,
                precious_metals = EXCLUDED.precious_metals,
                government_bond = EXCLUDED.government_bond,
                foreign_currency_bills = EXCLUDED.foreign_currency_bills,
                eurobonds = EXCLUDED.eurobonds;
        """)

        with engine.begin() as conn:
            for _, row in data.iterrows():
                conn.execute(insert_data, row.to_dict())

        logger.info(f"Saved {len(data)} records to the database.")

        
               

    def fetch_historical_data(self, start_date, end_date=None, chunk_size=7):
        """
        Fetch historical data in chunks

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format, defaults to today
            chunk_size: Days per fetch, max 7 days
        """
        if end_date is None:
            end_date = datetime.date.today()
        else:
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        # Ensure we're not trying to get future data
        today = datetime.date.today()
        if end_date > today:
            error_message = "End date cannot be in the future"
            logger.error(error_message)
            raise ValueError(error_message)

        if start_date > end_date:
            error_message = "Start date cannot be after end date"
            logger.error(error_message)
            raise ValueError(error_message)

        # Calculate the number of days to fetch
        total_days = (end_date - start_date).days + 1

        logger.info(
            f"Fetching data from {start_date} to {end_date} ({total_days} days)"
        )

        # Create date ranges
        current_date = start_date
        all_data = []

        try:
            while current_date <= end_date:
                # Calculate chunk end date (not exceeding end_date)
                chunk_end = min(
                    current_date + datetime.timedelta(days=chunk_size - 1), end_date
                )

                logger.info(f"Processing from {current_date} to {chunk_end}")

                # Fetch data for the current chunk
                try:
                    data = self.crawler.fetch(
                        start=current_date.strftime("%Y-%m-%d"),
                        end=chunk_end.strftime("%Y-%m-%d"),
                    )

                    if not data.empty:
                        all_data.append(data)
                    else:
                        logger.warning(
                            f"No data returned for {current_date} to {chunk_end}"
                        )

                except Exception as e:
                    logger.error(
                        f"Error fetching data for {current_date} to {chunk_end}: {e}"
                    )

                # Move to the next chunk
                current_date = chunk_end + datetime.timedelta(days=1)

                # Sleep to avoid overloading the server
                time.sleep(1)

            return pd.concat(all_data)

        except Exception as e:
            logger.error(f"Error during historical data collection: {e}")
            raise e
