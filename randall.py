import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import praw, time, pickle, random

# This is another python file on a higher level that contains the passwords for the bod
import tokens

from pyfiglet import Figlet
from colorama import init, Fore, Style
init(autoreset=True)

r = praw.Reddit(user_agent="Replies \'Woosh\' to random comments by Felolis /u/Felolis")
print("Logging in...")
r.login(tokens.randall_username, tokens.randall_password, disable_warning=True)
print(Style.BRIGHT + Fore.GREEN + "Success!")

f = Figlet(font='doom')
print("\n" + Style.BRIGHT + Fore.BLUE + f.renderText('Randall'))

# These MUST be lower case
words_to_match = ["randall", "amazing", "xkcd"]

cacheFile = 'cache.bcf'

cache = ["d50cskt", "d50c2cq", "d5005yj"]

responses = [
	"*[Woosh](https://xkcd.com/1627/)*",
	"*[Comment of the year](https://xkcd.com/1627/)*",
	"*[Are you for real](https://xkcd.com/1627/)*",
	"*[I'm taking a screenshot so I can remember this moment forever](https://xkcd.com/1627/)*"
]

sleep_time = 600

try:
	print("Opening cache file")
	with open(cacheFile, 'rb') as f:
		cache = pickle.load(f)
except:
	print(Fore.MAGENTA + "Failed to open cache file.\nCreating one instead...")
	with open(cacheFile, 'wb') as f:
		pickle.dump(cache, f)

print(Fore.MAGENTA + "Cache:\n" + str(cache))

def run_bot():
	print("Grabbing subreddit...")
	subreddit = r.get_subreddit("felolis")

	print("Grabbing comments...")
	comments = subreddit.get_comments(limit=50)

	for comment in comments:
		comment_text = comment.body.lower()
		is_match = any(string in comment_text for string in words_to_match)

		if comment.id not in cache and is_match:
			print(Style.BRIGHT + Fore.GREEN + "Match found! Comment ID: " + comment.id)
			reply = random.choice(responses)
			try:
				comment.reply(reply + '\n\n&nbsp;\n\n*^^^I ^^^am ^^^a ^^^bot ^^^created ^^^by ^^^/u/Felolis*')
			except praw.errors.RateLimitExceeded as err:
				print(Style.BRIGHT + Fore.RED + str(err))
				return

			print(Style.BRIGHT + Fore.GREEN + "Replied succesful")
			print("Replied with: \"" + random.choice(responses) + "\"")
			cache.append(comment.id)

			print("Opening cache file...")
			with open(cacheFile, 'wb') as f:
				pickle.dump(cache, f)
			return


while True:
	run_bot()

	try:
		print("Comment loops finished sleeping for " + str(sleep_time / 60) + " minutes...")
		time.sleep(sleep_time)
	except:
		print(Style.BRIGHT + Fore.RED + "Failed to sleep or program terminated")
		break
