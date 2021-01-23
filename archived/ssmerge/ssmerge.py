import os
import numpy as np
from PIL import Image

def joinImages(ss,showName,ssNo):
    ssName = showName+"-"+str(ssNo)+".jpg"
    print("XXXXX")
    print(ss,ssName)
    list_im = ss
    imgs    = [ Image.open(i) for i in list_im ]

    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    # # save that beautiful picture
    # imgs_comb = Image.fromarray( imgs_comb)
    # imgs_comb.save( 'Trifecta.jpg' )    

    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save( ssName )

imgFormats = set(["png","jpg","gif"])
files = os.listdir('.')
files.sort()


breaks = [[i for i, x in enumerate(j) if x =="."] for j in files]


ss = []
ssbreaks = []
for i in range(len(files)):
    if len(breaks[i]) == 3 and files[i][breaks[i][-1]+1:] in imgFormats:
        ss.append(files[i])
        ssbreaks.append(breaks[i])


shows = {}
for i in range(len(ss)):
    show = ss[i][:ssbreaks[i][0]]
    ssNo = int(ss[i][ssbreaks[i][0]+1:ssbreaks[i][1]])
    seqNo = ss[i][ssbreaks[i][1]+1:ssbreaks[i][2]]

    if show in shows.keys():
        if len(shows[show]) == ssNo:
            shows[show][ssNo-1].append(ss[i])
        else:
            shows[show].append([ss[i]])
    else:
        shows[show] = [[ss[i]]]

print(shows)
for show in shows.keys():
    for i in range(len(shows[show])):
        joinImages(shows[show][i],show,i+1)

