import rustworkxGraph as rx
import time
import tracemalloc
import csv


def functionRuntime(count, function, *argv):
    totaltime = 0

    for x in range(count):
        startTime = time.time()
        function(*argv)
        endTime = time.time()
        timeTaken = endTime - startTime
        totaltime += timeTaken

    avgExecution = totaltime / count

    return avgExecution


def functionMemory(function, *argv):
    tracemalloc.start()
    function(*argv)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stats = stats[1] - stats[0]

    return stats


def csvMaker(fileName, n, dim, count, graphGen, graphGenPar, graphFilt, graphFiltPar, shortPath, shortPathPar):
    row = [n, (n ** dim)]
    totalTime = 0
    totalMem = 0

    graphGenRuntime = functionRuntime(count, graphGen, *graphGenPar)
    graphFiltRuntime = functionRuntime(count, graphFilt, *graphFiltPar)
    shortPathRuntime = functionRuntime(count, shortPath, *shortPathPar)

    totalTime = graphGenRuntime + graphFiltRuntime + shortPathRuntime
    totalTime = round(totalTime, 20)

    graphGenMem = functionMemory(graphGen, *graphGenPar)
    graphFiltMem = functionMemory(graphFilt, *graphFiltPar)
    shortPathMem = functionMemory(shortPath, *shortPathPar)

    totalMem = graphGenMem + graphFiltMem + shortPathMem
    totalMem = round(totalMem, 20)

    row.append(graphGenRuntime)
    row.append(graphFiltRuntime)
    row.append(shortPathRuntime)
    row.append(totalTime)
    row.append(totalMem)

    with open(fileName, 'a', newline="\n") as file:
        writer = csv.writer(file)
        writer.writerow(row)


fileName = "tests/10x10.txt"
g = rx.createGraph(fileName)
fg = rx.filterGraph(g, False)

csvMaker("RustworkX_Test_Results.csv", 10, 2, 3, rx.createGraph, [fileName], rx.filterGraph, [g],
         rx.shortest_path, [fg])

fileName = "tests/50x50.txt"
g = rx.createGraph(fileName)
fg = rx.filterGraph(g, False)

csvMaker("RustworkX_Test_Results.csv", 50, 2, 3, rx.createGraph, [fileName], rx.filterGraph, [g],
         rx.shortest_path, [fg])

fileName = "tests/100x100.txt"
g = rx.createGraph(fileName)
fg = rx.filterGraph(g, False)

csvMaker("RustworkX_Test_Results.csv", 100, 2, 3, rx.createGraph, [fileName], rx.filterGraph, [g],
         rx.shortest_path, [fg])

fileName = "tests/500x500.txt"
g = rx.createGraph(fileName)
fg = rx.filterGraph(g, False)

csvMaker("RustworkX_Test_Results.csv", 500, 2, 3, rx.createGraph, [fileName], rx.filterGraph, [g],
         rx.shortest_path, [fg])

fileName = "tests/1000x1000.txt"
g = rx.createGraph(fileName)
fg = rx.filterGraph(g, False)

csvMaker("RustworkX_Test_Results.csv", 1000, 2, 3, rx.createGraph, [fileName], rx.filterGraph, [g],
         rx.shortest_path, [fg])