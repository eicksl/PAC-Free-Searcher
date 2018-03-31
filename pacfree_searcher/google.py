class GoogleParser():
    """Handles the details of sending search requests to google and parsing
    results for info on a specific candidate's stance with regards to PAC
    money."""
    def __init__(self, data=None):
        """Initializes google search and parsing process using the data for
        the candidate."""
        self.data = data
        if self.data['campaign_url'] is None:
            self.find_campaign_url()


    def find_campaign_url(self):
        pass


    def _get_campaign_url_search_string(self):
        office = self.data['office'].split('-')
        str_search = '\"{}\" \"{}\" {}'.format(
                self.data['name'], self.data['state'], office[0])
        if office[0] == 'House':
            str_search += ' district ' + office[1]
        return str_search.replace(' ', '+')
