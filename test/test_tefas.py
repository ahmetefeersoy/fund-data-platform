from src.dagster.ingestion.tefas_parser import TefasCrawler

crawler = TefasCrawler()

print("Crawling TEFAS…")

df = crawler.fetch_historical_data("2025-07-07", "2025-07-08")

print("Rows:", len(df))
print("Columns:")
print(df.columns)

print("Sample:")
print(df.head().to_string())
