import streamlit as st
import pandas as pd
import plotly.express as px

github_data = pd.read_csv('github_dataset.csv')
repository_data = pd.read_csv('repository_data.csv')

github_data_cleaned = github_data.drop_duplicates(subset='repositories')
repository_data_cleaned = repository_data.drop_duplicates(subset='name')

github_data_cleaned['stars_count'] = pd.to_numeric(github_data_cleaned['stars_count'], errors='coerce')
github_data_cleaned = github_data_cleaned.dropna(subset=['stars_count'])

st.title('GitHub Repository Data Analysis')

st.sidebar.header('Customize Display')
top_n = st.sidebar.slider('Select the number of top repositories to display:', min_value=5, max_value=50, value=10, step=5)

valid_stars_repos = repository_data_cleaned[repository_data_cleaned['stars_count'].notna() & (repository_data_cleaned['stars_count'] > 0)]
available_repos = min(top_n, len(valid_stars_repos))

st.subheader(f'Top {available_repos} Repositories by Stars')
valid_stars_repos = valid_stars_repos.drop_duplicates(subset='name').dropna(subset=['stars_count'])
top_stars = valid_stars_repos.nlargest(available_repos, 'stars_count').sort_values('stars_count', ascending=False)
top_stars_display = top_stars[['name', 'stars_count', 'forks_count', 'primary_language']].rename(columns={
    'name': 'Repository Name', 'stars_count': 'Stars', 'forks_count': 'Forks', 'primary_language': 'Primary Language'}).reset_index(drop=True)
st.dataframe(top_stars_display)

st.subheader(f'Top {available_repos} Repositories by Stars (Bar Chart)')
fig = px.bar(top_stars, x='name', y='stars_count', color='primary_language',
             labels={'name': 'Repository Name', 'stars_count': 'Stars', 'primary_language': 'Language'},
             title=f'Top {available_repos} Repositories by Stars')
st.plotly_chart(fig)

available_forks_repos = min(top_n, len(github_data_cleaned))
st.subheader(f'Top {available_forks_repos} Repositories by Forks')
top_forks = github_data_cleaned.nlargest(available_forks_repos, 'forks_count').sort_values('forks_count', ascending=False)
top_forks_display = top_forks[['repositories', 'forks_count', 'stars_count', 'language']].rename(columns={
    'repositories': 'Repository Name', 'forks_count': 'Forks', 'stars_count': 'Stars', 'language': 'Language'}).reset_index(drop=True)
st.dataframe(top_forks_display)

st.subheader(f'Top {available_forks_repos} Repositories by Forks (Bar Chart)')
fig2 = px.bar(top_forks, x='repositories', y='forks_count', color='language',
              labels={'repositories': 'Repository Name', 'forks_count': 'Forks', 'language': 'Language'},
              title=f'Top {available_forks_repos} Repositories by Forks')
st.plotly_chart(fig2)

available_languages = min(top_n, len(repository_data_cleaned['primary_language'].value_counts()))
st.subheader(f'Top {available_languages} Most Common Programming Languages')
language_count = repository_data_cleaned['primary_language'].value_counts().nlargest(available_languages)
st.dataframe(language_count.rename_axis('Language').reset_index(name='Count').reset_index(drop=True))

st.subheader(f'Top {available_languages} Most Common Programming Languages (Bar Chart)')
fig3 = px.bar(language_count, x=language_count.index, y=language_count.values,
              labels={'x': 'Language', 'y': 'Count'},
              title=f'Top {available_languages} Most Common Programming Languages')
st.plotly_chart(fig3)

available_comparison_repos = min(top_n, len(github_data_cleaned))
st.subheader(f'Top {available_comparison_repos} Repositories - Stars vs Forks Comparison')
comparison_data = github_data_cleaned[['repositories', 'stars_count', 'forks_count', 'language']].nlargest(available_comparison_repos, 'stars_count').sort_values('stars_count', ascending=False)
comparison_data = comparison_data.rename(columns={'repositories': 'Repository Name', 'stars_count': 'Stars', 'forks_count': 'Forks', 'language': 'Language'})
st.dataframe(comparison_data)

st.subheader(f'Top {available_comparison_repos} Repositories - Stars vs Forks (Scatter Plot)')
fig4 = px.scatter(comparison_data, x='Stars', y='Forks',
                  size='Forks', color='Language',
                  labels={'Stars': 'Stars', 'Forks': 'Forks', 'Language': 'Language'},
                  title=f'Top {available_comparison_repos} Repositories - Stars vs Forks Comparison')
st.plotly_chart(fig4)

available_contributors_repos = min(top_n, len(github_data_cleaned))
st.subheader(f'Top {available_contributors_repos} Repositories by Contributors')
top_contributors = github_data_cleaned.nlargest(available_contributors_repos, 'contributors')
st.dataframe(top_contributors[['repositories', 'contributors', 'stars_count', 'language']].rename(columns={
    'repositories': 'Repository Name', 'contributors': 'Contributors', 'stars_count': 'Stars', 'language': 'Language'}).reset_index(drop=True))

st.subheader(f'Top {available_contributors_repos} Repositories by Contributors (Bar Chart)')
fig5 = px.bar(top_contributors, x='repositories', y='contributors', color='language',
              labels={'repositories': 'Repository Name', 'contributors': 'Contributors', 'language': 'Language'},
              title=f'Top {available_contributors_repos} Repositories by Contributors')
st.plotly_chart(fig5)
