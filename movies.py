import os
from imdbpie import Imdb
import shutil

imdb=Imdb()
# path = "/media/neel/New Volume/Movies/Superhero/"
# dest = "../Test/"
# genre= "Superhero/"
# for i in os.listdir(path):
# 	# print (path+i)
# 	if not os.path.exists(dest+genre):
# 	    os.makedirs(dest+genre)
# 	destination = dest+genre+i
# 	# shutil.move(path+i,dest+genre)
# 	os.symlink(path+i,destination)

paths=['/media/neel/New Volume/ToWatchASAP/Movie/',
		'/media/neel/New Volume/Movies/To Watch/',
		'/media/neel/New Volume/Movies/Superhero/']
dest = "/media/neel/New Volume/WatchList/"
for file in os.listdir(paths[1]):
	movie_name=[]
	flag=False
	year=[]
	for i in file:
		if not flag:
			if ord(i)>=48 and ord(i)<=57:
				flag=True
				year.append(i)
			else:
				movie_name.append(i)
		else:
			if ord(i)>=48 and ord(i)<=57:
				year.append(i)
			else:
				flag=False
				break
	if len(year)>0:
		if int("".join(year))>=1980 and int("".join(year))<=2018:
			search_term="".join(movie_name + year)
			try:
				mov_id=imdb.search_for_title(search_term)[0]['imdb_id']
				rating = imdb.get_title_ratings(mov_id)["rating"]
				genres = imdb.get_title_genres(mov_id)["genres"]
				print (file, rating, genres)
				for j in genres:
					if not os.path.exists(dest+j):
					    os.makedirs(dest+j)
					if not os.path.exists(dest+j+"/"+str(int(rating))+"+"):
					    os.makedirs(dest+j+"/"+str(int(rating))+"+")
					os.symlink(paths[1]+file,dest+j+"/"+str(int(rating))+"+"+"/"+file)
			except:
				print ("no movies")