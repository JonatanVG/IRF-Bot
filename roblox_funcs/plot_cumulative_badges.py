import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

from roblox_funcs.convert_date_to_datetime import convertDateToDatetime

def plot_cumulative_badges(username: str, user_id: str, dates: list[str]):
    """
    Graph the cumulative total of badges over time
    """
    # Sort badges by awarded date
    y_values = [convertDateToDatetime(date) for date in dates]
    y_values.sort()

    # Calculate cumulative count at each date and store into a list
    curr_count = 0
    cumulative_counts = []
    for date in y_values:
        curr_count += 1
        cumulative_counts.append(curr_count)
    # Plot the cumulative count over time
    plt.style.use('dark_background')
    plt.xlabel('Badge Earned Date')
    plt.ylabel('Total Badges')
    plt.title(f'Badges over Time for {username} ({user_id})')
    plt.scatter(y_values, cumulative_counts, marker='o', alpha=0.2)

    # Set the X-axis format to 'Year' only
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())

    plt.figtext(0.05, 0.95, f"Badge Count: {len(y_values)}", ha="left", va="top", color="white", transform=ax.transAxes)

    # Save the image, if desired. Must be ran before plt.show()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)
    plt.close()
    return buf