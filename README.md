# CeneoScraper

##Libraries used in project
- Requests
- BeautifiulSoup4
- Json
- Os

##CSS selectors of components of opinions in [Ceneo.pl](https://www.ceneo.pl/) service
| Component | Name | Selector | Data type |
| --- | --- | --- | --- |
| opinion ID | id | [data-entry-id] | string / int |
| opinion's author | author | span.user-post\_\_author-name | string |
| author's recommendation | recommendation | span.user-post\_\_author-recommendation \> em | bool |
| score expressed in number of stars | stars | span.user-post\_\_score-count | float |
| opinion's content | content | div.user-post\_\_text | string |
| list of product advantages | pros | div.review-feature\_\_title--positives ~ div.review-feature\_\_item | list of string |
| list of product disadvantages | cons | div.review-feature\_\_title--negatives ~ div.review-feature\_\_item | list of string |
| how many users think that opinion was helpful | upvote | button.vote-yes \> spanbutton.vote-yes[data-total-vote] | int |
| how many users think that opinion was unhelpful | downvote | button.vote-no \> spanbutton.vote-no[data-total-vote] | int |
| publishing date | posted | span.user-post\_\_published \> time:nth-child(1)[datetime] | string |
| purchase date | purchased | span.user-post\_\_published \> time:nth-child(2)[datetime] | string |