import datetime
import json


def process_user_data(user_data_file, bar_plot_file, map_plot_file, markdown_file):
    """
    Reads user data from a JSON file and writes it to a markdown file.

    Args:
        user_data_file: Path to the JSON file containing user data.
        markdown_file: Path to the output markdown file.
    """
    now = datetime.datetime.now()

    with open(user_data_file, 'r') as f:
        user_data = json.load(f)

    # Write processed data to markdown file
    with open(markdown_file, 'w') as f:
        f.write('# Metrics \n\n')
        f.write(f'Last Updated: {now}\n\n')
        f.write('Total Users:\n\n')
        for key in user_data:
            f.write(f'{key}: {(user_data[key])}\n')
        f.write('\n')
        f.write(f'![Top Pages]({bar_plot_file})')
        f.write('\n\n')
        f.write(f'![Users by Country]({map_plot_file})')
        f.write('\n')
    f.close()


if __name__ == '__main__':
    user_data_file = 'user_metrics.json'
    bar_plot_file = '_static/bypage.png'
    map_plot_file = '_static/bycountry.png'
    markdown_file = 'portal/metrics.md'
    process_user_data(user_data_file, bar_plot_file, map_plot_file, markdown_file)
