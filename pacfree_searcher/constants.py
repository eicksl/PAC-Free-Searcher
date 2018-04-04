ELECTIONS_HOME = open('txt/elections.txt').read()
GOOGLE_KEY = open('txt/google_key.txt').read()
GOOGLE_CX = open('txt/google_cx.txt').read()
GOOGLE_SEARCH = 'https://www.googleapis.com/customsearch/v1'
SENATE_CLASS = '1'
TWITTER = 'https://twitter.com'
FACEBOOK = 'https://www.facebook.com'
STATES = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
    'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}
AT_LARGE_STATES = set({
    'Alaska', 'Delaware', 'Montana', 'North Dakota', 'South Dakota',
    'Vermont', 'Wyoming'
})
SPECS = set({
    'pac money', 'corporate pac', 'corporate money', 'money in politics',
    'corporate influence', 'small dollar donations', 'small dollar donors',
    'grass roots funded', 'grass roots fundraising', 'corporate pacs',
    'campaign finance reform', 'special interest groups', 'big money'
})
