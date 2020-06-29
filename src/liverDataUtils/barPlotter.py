import matplotlib.pyplot as plt
import numpy as np

def showPercentageBarPlot(labels, diceResults, falsePositive, falseNegative, title):
    _, ax = plt.subplots()
    ax.bar(labels, diceResults, label='Dice coefficient')
    ax.bar(labels, falseNegative, bottom=diceResults, label='False negative')
    ax.bar(labels, falsePositive, bottom=np.array(falseNegative) + np.array(diceResults), label='False positive')
    ax.legend()
    ax.set_title(title)
    plt.show()