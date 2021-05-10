import requests
import pandas as pd

def writeToFile(teams):
    df = pd.DataFrame(teams)
    df.to_csv('kivaTeams.csv', sep=',', mode='a', index=False)

def callApi(query):
    baseUrl = 'https://api.kivaws.org/graphql?query='
    r = requests.post(baseUrl + query )
    if r.status_code == 200:
        print(r)
        return r.json()
    else:
        print(r)
        print(r.json()['errors'])

# get the total number of teams
# teamCountQuery = '{community {teams {totalCount}}}'
# teamCountResponse = callApi(teamCountQuery)
# if not teamCountResponse:
#     exit()
# totalCount = teamCountResponse['data']['community']['teams']['totalCount']

totalCount = 200
start = 0
limit = 100     # since the API does not allow more than 100 rows per query  
while start <= totalCount:
    teamsQuery = f'''
    {{
        community {{
            teams(offset:{start},limit:{limit}) {{
                values {{
                    name
                    id
                    createdDate
                    teamPublicId
                    url
                    category
                    lentAmount
                    loanCount
                    membershipType
                    loanBecause
                    description
                    whereabouts
                    lenderCount
                }}
            }}
        }}
    }}
    '''
    teamsResponse = callApi(teamsQuery)
    if not teamsResponse:
        break
    teams = teamsResponse['data']['community']['teams']['values']
    writeToFile(teams)
    start += limit  

