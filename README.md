## What ?
An attempt at creating one database of *(almost)* all knowledge I gather online / offline. Leveraging the simple ETL method.  
- `Extract` data from across platforms where you read, write or interact with
- `Transform` this data into form usable by the database
- `Load` into the database

## Why ?
- Link knowledge gained across platforms
- Organized knowledge lake to dive into for writing references, project ideas
- Stats about interactions in past week to motivate and become better

## Where ?
### From
Reading -
- Pocket  
*(I know there are better tools out there, but for first iteration pocket works flawlessly. Focus on getting a prototype out first than concentrating on the intricacies.)*
- Kindle
- Twitter Threads

Podcast -
*(Search for podcast player with official / good unofficial API support)*

Videos -
- Youtube

Vocabulary -
- TBD

### To
For now using Google Sheets to create a quick prototype to test POC.
In final rendition, maybe use Notion API *(Once it is out)* or store locally

## How ?
### Extract
Everything is extracted into `source/` folder, from where it is transformed and loaded by appropriate jobs.  

Reading -
- Pocket : 
- - Using [pockexport](https://github.com/karlicoss/pockexport) as it gives annotations as well
- Kindle : 
- - Kindle allows you to export your highlights. Both for official as well as mailed documents.  
- - Extraction phase for Kindle is manual, transform and load phase will be automated
- Twitter Threads :
- - For now, use https://threadreaderapp.com/ and export to pocket
- - Repeat the pocket workflow

Podcast
- TBD

Videos
- TBD

Vocabulary
- TBD

### Transform
- Reading data from `source/`. JSON, txt, pickled, all forms of data ...
- Compare and check which data is new
- Transform new data as per needs
- Move to loading phase

### Load
- Finally call the append call to the particular google sheet

## Misc
### Config
- API keys kept in `env/`
- Google Sheet IDs and range in `env/`

### Future Features *(Probable)*
- Weekly email containing stats
- Weekly email containg past posts for spaced repition and nostalgia
- Linting and Testing
- Github Workflows


