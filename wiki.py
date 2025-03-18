from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import wikipedia
import warnings
from collections import Counter
import re

# Suppressing unnecessary warnings
warnings.filterwarnings("ignore")

# Function to clean and count word frequencies
def get_top_words(text, stopwords, n=10):
    words = re.findall(r'\b\w+\b', text.lower())
    filtered = [word for word in words if word not in stopwords and len(word) > 2]
    return Counter(filtered).most_common(n)

# Function to search the Wikipedia article and generate the word cloud
def gen_cloud(topic):
    try:
        page = wikipedia.page(topic)
        content = str(page.content)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"⚠️ Topic is ambiguous. Try being more specific. Suggestions: {e.options[:5]}")
        return None, None
    except wikipedia.exceptions.PageError:
        print("❌ Page not found. Try another topic.")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

    STOPWORDS.add('==')
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        stopwords=stopwords,
        max_words=200,
        background_color="black",
        width=600,
        height=350
    ).generate(content)
    return wordcloud, content

# Function to save the word cloud to the current directory
def save_cloud(wordcloud, topic):
    filename = f"./{topic.lower().replace(' ', '_')}_wordcloud.png"
    wordcloud.to_file(filename)
    print(f"✅ Wordcloud saved as: {filename}")

# Function to display the word cloud with matplotlib
def show_cloud(wordcloud):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Main driver code
if __name__ == '__main__':
    while True:
        topic = input("🔍 What do you want to search: ").strip()
        wordcloud, content = gen_cloud(topic)
        
        if wordcloud:
            save_cloud(wordcloud, topic)

            # Optional: Show top 10 words
            show_words = input("📊 Do you want to see the top 10 most frequent words? (y/n): ").strip().lower()
            if show_words == 'y' and content:
                top_words = get_top_words(content, set(STOPWORDS))
                print("\nTop 10 Words:")
                for word, freq in top_words:
                    print(f"{word}: {freq}")

            # Show the word cloud
            desc = input("🖼️ Do you wish to see the wordcloud image? (y/n): ").strip().lower()
            if desc == 'y':
                show_cloud(wordcloud)

        again = input("\n🔁 Do you want to try another topic? (y/n): ").strip().lower()
        if again != 'y':
            print("👋 Exiting... Thanks for using the WordCloud Generator!")
            break
