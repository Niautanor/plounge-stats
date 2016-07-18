#!/usr/bin/python3 -u
# Prints out PLounge stats and stuff
import sqlite3
import time

def log(msg):
	print(("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), str(msg))))

def main():
	while True:
		s = process()
		time.sleep(s)

def getfile(filename):
	return open("/var/www/plounge/stats_files/" + filename, 'wb')

def make_stats(db, query, line_format, f):
	"""
	Executes the specified query on the database, formats the results
	according to line_format and writes the lines to the file specified
	by f.

	Important things to consider when using this function:
	1. Nothing is escaped.
	2. Make sure that your format string uses exactly the results of
	   the query
	"""
	l = db.execute(query).fetchall()
	with f:
		stats = [line_format.format(i+1, *e)
		         for i, e in enumerate(l)]
		f.write(bytes('\n'.join(stats), 'UTF-8'))

# Connects to the database. Creates it if it needs to.
def init_db(filename):
	return sqlite3.connect(filename)

def process():
	db = None
	try:
		db = init_db('data/plounge.db')

		log("Building stats list...")
		# statsWeek (comments)
		make_stats(db, """SELECT author, count(*) FROM comments
		                  WHERE udate > datetime('now','-7 days', 'localtime')
		                  AND author != '[deleted]' AND body != ';-;'
		                  GROUP BY author ORDER BY count(*) DESC""",
		           "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>",
		           getfile("statsWeek.txt"))

		# statsDay (comments)
		make_stats(db, """SELECT author, count(*) FROM comments
		                  WHERE udate > datetime('now','-1 days', 'localtime')
		                  AND author != '[deleted]' AND body != ';-;'
		                  GROUP BY author ORDER BY count(*) DESC""",
		           "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>",
		           getfile("statsDay.txt"))

		# statsWeek (submissions)
		make_stats(db, """SELECT author, count(*) FROM submissions
		                  WHERE udate > datetime('now','-7 days', 'localtime')
		                  AND author != '[deleted]'
		                  GROUP BY author ORDER BY count(*) DESC""",
		           "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>",
		           getfile("statsWeekS.txt"))

		# statsDay (submissions)
		make_stats(db, """SELECT author, count(*) FROM submissions
		                  WHERE udate > datetime('now','-1 days', 'localtime')
		                  AND author != '[deleted]'
		                  GROUP BY author ORDER BY count(*) DESC""",
		           "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>",
		           getfile("statsDayS.txt"))

		# beesWeek
		make_stats(db, """SELECT author, COUNT(*) N, permalink FROM comments
		                  WHERE udate > datetime('now','-7 days', 'localtime')
		                  AND author != '[deleted]' AND (id LIKE '%5r')
		                  GROUP BY author ORDER BY n DESC""",
		           "<tr><td>{1}</td><td>{2}</td><td><a href=\"{3}\">Latest</a></td></tr>",
		           getfile("beesWeek.txt"))

		# beesAll
		make_stats(db, """SELECT author, COUNT(*) N, permalink FROM comments
		                  WHERE author != '[deleted]' AND (id LIKE '%5r')
		                  GROUP BY author ORDER BY n DESC""",
		           "<tr><td>{1}</td><td>{2}</td><td><a href=\"{3}\">Latest</a></td></tr>",
		           getfile("beesAll.txt"))

		# beesRecent
		make_stats(db, """SELECT author, udate, permalink FROM comments
		                  WHERE author != '[deleted]' AND (id LIKE '%5r')
		                  ORDER BY udate DESC""",
		           "<tr><td>{1}</td><td>{2}</td><td><a href=\"{3}\">Latest</a></td></tr>",
		           getfile("beesRecent.txt"))

		# ;-;
		make_stats(db, """SELECT author, count(*) FROM comments
		                  WHERE udate > datetime('now','-7 days', 'localtime')
		                  AND author != '[deleted]'
		                  AND body = ';-;'
		                  GROUP BY author ORDER BY count(*) DESC""",
		           "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>",
		           getfile(";-;.txt"))

		with getfile("lastUpdated.txt") as f:
			f.write(bytes(time.strftime("%Y-%m-%d %X") + " UTC", 'UTF-8'))

	except Exception as ex:
		print(ex)
		return 45
	finally:
		if db:
			db.close()
	log("Sleeping...")
	return 300

if __name__ == '__main__':
	main()
