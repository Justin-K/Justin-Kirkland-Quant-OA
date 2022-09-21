from argparse import ArgumentParser
from datetime import datetime
from time import perf_counter
from scraper import SubredditScraper
from subreddit_parser import SubredditProcessor, SubredditJSONSerializer
"""
    A command-line-interface to scrape data from a subreddit into a JSON file.
"""

cli_parser = ArgumentParser(description="Subreddit scraper to scrape a given subreddit to obtain the top 5 posts and the top 6 replies to each post"
                                        "between two dates.")

cli_parser.add_argument("subreddit", type=str, help="Name of a subreddit to scrape (r/{subreddit} or {subreddit} is acceptable.)")

cli_parser.add_argument("start_date", type=str, help="Date to start collecting data from, in the format \"YYYY-MM-DD\".")

cli_parser.add_argument("end_date", type=str, help="Date to collect data to, in the format \"YYYY-MM-DD\".")

cli_parser.add_argument("-config_site", type=str, help="Site in praw.ini to use. Defaults to \"quant_oa_bot\"")

cli_parser.add_argument("-output_file", type=str, help="Output JSON file to serialize data to. Defaults to \"subreddit_data.json\"")

cli_parser.add_argument("-comments", type=int, help="Number of comments to fetch when calculating the number of accounts"
                                                    "that are younger than 3 months. Defaults to \"200\"")
args = cli_parser.parse_args()
subreddit = args.subreddit
start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

if args.config_site:
    config_site = args.config_site
else:
    config_site = "quant_oa_bot"

if args.output_file:
    out_file = args.output_file
else:
    out_file = "subreddit_data.json"

if args.comments:
    comments = args.comments
else:
    comments = 200

start = perf_counter()

scraper = SubredditScraper(config_site)
top_subs_and_comms = scraper.get_top_submissions_and_comments(subreddit, start_date, end_date)
young_accounts = scraper.num_new_accounts(subreddit, comments_to_scan=comments)
sub_proc = SubredditProcessor(top_subs_and_comms, young_accounts)
sub_serializer = SubredditJSONSerializer(sub_proc.parsed_subreddit_data, file=out_file)
sub_serializer.write_as_json()

end = perf_counter()

print(f"[*] Fetched and stored results in \"{out_file}\". Total time elapsed: {round((end-start)/60, 1)} minute(s).")
