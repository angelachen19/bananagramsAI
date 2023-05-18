import matplotlib.pyplot as plt
from IPython import display

plt.ion()

# Number of board resets


def plot_resets(num_board_resets):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Number of Board Shuffles')
    plt.plot(num_board_resets)
    plt.ylim(ymin=0)
    plt.text(len(num_board_resets)-1,
             num_board_resets[-1], str(num_board_resets[-1]))
    plt.show(block=False)
    plt.pause(.1)


# Time until completion
def plot_gametime(gametimes):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Time (s)')
    plt.plot(gametimes)
    plt.ylim(ymin=0)
    plt.text(len(gametimes)-1,
             gametimes[-1], str(gametimes[-1]))
    plt.show(block=False)
    plt.pause(.1)
