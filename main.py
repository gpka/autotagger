import btreemodel as bt
from odd import oddityDot
od = oddityDot()
namelist = ["Google","Microsoft","Computer","Laptop","Stanford University","Harvard University","Bachelor's degree", "Master's degree","Salt","Chili pepper","Sugar","Sushi","Wasabi","Espresso","Cappucino","Pizza","Spaghetti"]

print "Retrieving %d articles ..." % len(namelist)
for i in range(len(namelist)):
    od.addArticle(namelist[i])
print "Making data set ... ~%d tokens expected" % (len(namelist)*(len(namelist)-1)*(len(namelist)-2)/6)
dataset = od.getFullTrainingSet()
print "Start solving ..."
tree = bt.DichotomousTree(namelist, dataset)
tree.treeSolve()
print tree.listform()
print "Finished solving. Calculating accuracy..."
total = 0
for x in dataset:
    total += x[2]
print "Approximately %d/%d of conditions satisfied." % (tree.reward, total)
