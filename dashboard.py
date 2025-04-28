import streamlit as st
import pandas as pd

# Load your scraped CSV
df = pd.read_csv('supercharged_keyword_links.csv')

# Set up the Streamlit app
st.title('Community College Resource Finder')

# Search box to filter
search_term = st.text_input('Search for a keyword or college name:')

# Filter the DataFrame
if search_term:
    filtered_df = df[
        df['matched_text'].str.contains(search_term, case=False, na=False) |
        df['page_url'].str.contains(search_term, case=False, na=False)
    ]
else:
    filtered_df = df

# Show the table
st.dataframe(filtered_df)

# Optionally download the data
st.download_button("Download data as CSV", data=filtered_df.to_csv(index=False), file_name='filtered_results.csv', mime='text/csv')
