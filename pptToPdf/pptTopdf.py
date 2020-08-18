import comtypes.client
import os

def PPTtoPDF(inputFileName, outputFileName, formatType = 32):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName + ".pdf"
    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, formatType) # formatType = 32 for ppt to pdf
    deck.Close()
    powerpoint.Quit()

relPath = os.path.abspath('../../College/Notes')
files = os.listdir(relPath)

for i in files:
    subject = i
    subjectFiles = os.listdir(relPath+"/"+i)
    for j in subjectFiles:
        if j[-3:] == "ppt":
            inpFile = relPath+"/"+i+"/"+j
            outFile = relPath+"/"+i+"/"+j[:-3]+"pdf"
            # print(inpFile)
            # print(outFile)
            PPTtoPDF(inpFile,outFile)
        elif j[-4:] == "pptx":
            inpFile = relPath+"/"+i+"/"+j
            outFile = relPath+"/"+i+"/"+j[:-4]+"pdf"
            # print(inpFile)
            # print(outFile)
            PPTtoPDF(inpFile,outFile)