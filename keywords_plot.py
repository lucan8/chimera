import matplotlib.pyplot as plt
import re
from probUtils import getSelectedWords

res_files = {
    'Rust': 'results/rs_results.txt',
    'Java': 'results/java_results.txt',
    'C++': 'results/cpp_results.txt'
}

language_colors = {
    'Rust': '#dea584',
    'Java': '#b07219',
    'C++': '#f34b7d'
}

keywords = getSelectedWords()
keyword_counts = {language: {keyword: 0 for keyword in keywords} for language in res_files}

def read_keyword_counts(file_name):
    counts = {keyword: 0 for keyword in keywords}
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.split()

            # Keyword lines
            if len(parts) == 2:
                keyword, count = parts
                if keyword in counts:
                    counts[keyword] = int(count)
    return counts

def plot_keywords():
    for keyword in keywords:
        print(f"Plotting '{keyword}' keyword...")

        counts = {language: keyword_counts[language][keyword] for language in res_files}

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(counts.keys(), counts.values(), color=[language_colors[language] for language in counts])
        ax.set_title(f'Keyword: {keyword}')
        ax.set_ylabel("Occurrences")


        img_path = f"{keyword}.png"
        invalid_chars = r'[<>:"/\\|?*]'
        sanitized_path = re.sub(invalid_chars, '_', img_path)
        plt.savefig(f"plots/{sanitized_path}", dpi=300)

        plt.close()

def main():
    for language, file_name in res_files.items():
        keyword_counts[language] = read_keyword_counts(file_name)

    plot_keywords()

main()
