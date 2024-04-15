import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def calculate_weighted_sentiment(sentiment_filename, keywords_filename):
    '''
    Args:
        sentiment_filename: Name of Excel file with sentiment results for a transcript.
                            Columns such as: 'Sentiment Score', 'Keyword', 'Paragraph' 

        keywords_filename:  Name of Excel file with keywords and their weights (under 'Proposed').
                            Must contain 'Proposed' (ie keyword weights) 

    Result:
        Adds (at least) columns 'Proposed' and 'Weighted Sentiment Score' to 'sentiment_filename'.
        'Weighted Sentiment Score' equals the original 'Sentiment Score' multiplied by 'Proposed' weight
        for relevant 'Keyword', scaled to between 0 and 1.

    Returns:
        None
    '''
    # Read the files
    sentiment_df = pd.read_excel(sentiment_filename)
    keywords_df = pd.read_excel(keywords_filename)

    # Map the qualitative assessments to quantitative weights
    importance_weights = {
        'Very Important': 1.5,
        'Important': 1.0,
        'Less Important': 0.5
    }
    keywords_df['Weight'] = keywords_df['Proposed'].map(importance_weights)

    # Merge the sentiment DataFrame with the keyword weights DataFrame and drop duplicate columns
    sentiment_df = pd.merge(sentiment_df, keywords_df, left_on='Keyword', right_on='Keyword', how='left', 
                            suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

    # Calculate the proposed sentiment score using keyword weights
    sentiment_df['Weighted Sentiment Score'] = sentiment_df['Sentiment Score'] * sentiment_df['Weight']

    # Normalize the weighted sentiment score to be between 0 and 1
    scaler = MinMaxScaler()
    sentiment_df['Weighted Sentiment Score'] = scaler.fit_transform(sentiment_df[['Weighted Sentiment Score']])

    # Save the DataFrame with the new column to the same Excel file
    sentiment_df.to_excel(sentiment_filename, index=False)
