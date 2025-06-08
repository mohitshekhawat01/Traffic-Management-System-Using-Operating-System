import matplotlib.pyplot as plt

def plot_traffic(roads):
    names = [road.name for road in roads]
    traffic_counts = [road.traffic for road in roads]

    plt.bar(names, traffic_counts, color=['blue', 'green', 'red', 'orange'])
    plt.xlabel('Roads')
    plt.ylabel('Remaining Traffic')
    plt.title('Traffic After Simulation')
    plt.show()
 
