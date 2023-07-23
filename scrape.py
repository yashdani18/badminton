import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate


# df_results = pd.DataFrame(
#     {
#         'year': [],
#         'month': [],
#         'tournament_link': [],
#         'tournament_name': [],
#         'tournament_dates': [],
#         'tournament_prize_money': [],
#         'tournament_super_level': [],
#         'city': [],
#         'country': [],
#         'men_singles_winner': [],
#         'men_singles_runner_up': [],
#         'men_singles_third_place_1': [],
#         'men_singles_third_place_2': [],
#         'women_singles_winner': [],
#         'women_singles_runner_up': [],
#         'women_singles_third_place_1': [],
#         'women_singles_third_place_2': [],
#         'men_doubles_winner_1': [],
#         'men_doubles_winner_2': [],
#         'men_doubles_runner_up_1': [],
#         'men_doubles_runner_up_2': [],
#         'men_doubles_third_place_1_1': [],
#         'men_doubles_third_place_1_2': [],
#         'men_doubles_third_place_2_1': [],
#         'men_doubles_third_place_2_2': [],
#         'women_doubles_third_place_1_1': [],
#         'women_doubles_third_place_1_2': [],
#         'women_doubles_third_place_2_1': [],
#         'women_doubles_third_place_2_2': [],
#         'mixed_doubles_third_place_1_1': [],
#         'mixed_doubles_third_place_1_2': [],
#         'mixed_doubles_third_place_2_1': [],
#         'mixed_doubles_third_place_2_2': [],
#     }
# )


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


df_results = pd.DataFrame(
    {
        'year': [],
        'month': [],
        'tournament_link': [],
        'tournament_name': [],
        'tournament_dates': [],
        'tournament_prize_money': [],
        'tournament_super_level': [],
        'city': [],
        'country': [],
        'men_singles_winner': [],
        'men_singles_runner_up': [],
        'men_singles_third_place_1': [],
        'men_singles_third_place_2': [],
        'women_singles_winner': [],
        'women_singles_runner_up': [],
        'women_singles_third_place_1': [],
        'women_singles_third_place_2': [],
        'men_doubles_winner_1': [],
        'men_doubles_winner_2': [],
        'men_doubles_runner_up_1': [],
        'men_doubles_runner_up_2': [],
        'men_doubles_third_place_1_1': [],
        'men_doubles_third_place_1_2': [],
        'men_doubles_third_place_2_1': [],
        'men_doubles_third_place_2_2': [],
        'women_doubles_winner_1': [],
        'women_doubles_winner_2': [],
        'women_doubles_runner_up_1': [],
        'women_doubles_runner_up_2': [],
        'women_doubles_third_place_1_1': [],
        'women_doubles_third_place_1_2': [],
        'women_doubles_third_place_2_1': [],
        'women_doubles_third_place_2_2': [],
        'mixed_doubles_winner_1': [],
        'mixed_doubles_winner_2': [],
        'mixed_doubles_runner_up_1': [],
        'mixed_doubles_runner_up_2': [],
        'mixed_doubles_third_place_1_1': [],
        'mixed_doubles_third_place_1_2': [],
        'mixed_doubles_third_place_2_1': [],
        'mixed_doubles_third_place_2_2': [],
    }
)

years = ['2018', '2019', '2020', '2021', '2022', '2023']

dictionary = {}

# years = ['2023']

for year in years:
    dictionary[year] = {}
    url = f'https://bwfworldtour.bwfbadminton.com/calendar/?cyear={year}&rstate=completed'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    months = soup.find_all(class_="item-results")
    print(len(months))

    for index_month, month in enumerate(months):
        # if index_month == len(months) - 1:
        #     continue
        # if index_month > 0:
        #     continue
        month_name = month.find(class_="title-nolink").text
        print(month_name)
        tournaments = month.find(class_="tblResultLanding").find_all('a')
        for index_tournament, tournament in enumerate(tournaments):
            if index_month == len(months) - 1 and index_tournament == len(tournaments) - 1:
                continue
            tournament_link = tournament['href']
            if tournament_link == '#':
                continue
            print('tournament_link:', tournament_link)
            tournament_detail = tournament.find(class_='inner-tournament-detail')

            tournament_info = tournament_detail.find(class_='info')
            tournament_name = tournament_detail.find('h2').text.strip()
            tournament_dates = tournament_detail.find('h3').text.strip()
            tournament_prize_money = tournament_detail.find(class_='prize').text.strip()
            print('tournament_name:', tournament_name)
            if tournament_name[-11:] == '(Cancelled)':
                continue
            print('tournament_dates:', tournament_dates)
            print('tournament_prize_money:', tournament_prize_money)

            country_detail = tournament_detail.find(class_='country-detail')
            tournament_super_level_logo_link = country_detail.find('img')['src']
            print('tournament_type_logo_link:', tournament_super_level_logo_link)
            venue = country_detail.find_all(class_="country_code")
            city = venue[0].text.strip()
            country = venue[1].text.strip()
            print('city:', city)
            print('country:', country)

            df_results.loc[len(df_results.index)] = [year, month_name, tournament_link, tournament_name,
                                                     tournament_dates, tournament_prize_money,
                                                     tournament_super_level_logo_link, city, country,
                                                     '', '', '', '',
                                                     '', '', '', '',
                                                     '', '', '', '', '', '', '', '',
                                                     '', '', '', '', '', '', '', '',
                                                     '', '', '', '', '', '', '', '']

            tournament_results = requests.get(tournament_link + '/results/podium/').text
            inner_soup = BeautifulSoup(tournament_results, 'lxml')

            men_singles = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-single')[0]
            men_singles_entries = men_singles.find(class_="title").find('span').text.strip()
            tournament_type_players = men_singles.find('ul').find_all('li')
            tournament_type_players_keys = ['men_singles_winner', 'men_singles_runner_up',
                                            'men_singles_third_place_1', 'men_singles_third_place_2']
            for player_index, tournament_type_player in enumerate(tournament_type_players):
                player_name = tournament_type_player.find(class_='flag-name-wrap').find('a')['title']
                print(f'{player_index}: {player_name}')
                df_results[tournament_type_players_keys[player_index]][len(df_results.index) - 1] = player_name

            women_singles = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-single')[1]
            women_singles_entries = women_singles.find(class_="title").find('span').text.strip()
            tournament_type_players = women_singles.find('ul').find_all('li')
            tournament_type_players_keys = ['women_singles_winner', 'women_singles_runner_up',
                                            'women_singles_third_place_1', 'women_singles_third_place_2']
            for player_index, tournament_type_player in enumerate(tournament_type_players):
                player_name = tournament_type_player.find(class_='flag-name-wrap').find('a')['title']
                print(f'{player_index}: {player_name}')
                df_results[tournament_type_players_keys[player_index]][len(df_results.index) - 1] = player_name

            # # SINGLES
            # tournament_types = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-single')
            # # print(len(tournament_types))
            # tournament_type_singles = ["MEN'S SINGLES", "WOMEN'S SINGLES"]
            # for index, tournament_type in enumerate(tournament_types):
            #     tournament_type_category = tournament_type_singles[index]
            #     tournament_type_entries = tournament_type.find(class_="title").find('span').text.strip()
            #     print('tournament_type_category:', tournament_type_category)
            #     print('tournament_type_entries:', tournament_type_entries)
            #
            #     tournament_type_players = tournament_type.find('ul').find_all('li')
            #     tournament_type_players_keys = ['men_singles_winner', 'men_singles_runner_up',
            #                                     'men_singles_third_place_1', 'men_singles_third_place_2']
            #     for player_index, tournament_type_player in enumerate(tournament_type_players):
            #         player_name = tournament_type_player.find(class_='flag-name-wrap').find('a')['title']
            #         print(f'{player_index}: {player_name}')
            #         df_results[tournament_type_players_keys[player_index]][len(df_results.index) - 1] = player_name

            #  MENS DOUBLES
            men_doubles = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-double')[0]
            men_doubles_entries = men_doubles.find(class_="title").find('span').text.strip()
            tournament_type_players = men_doubles.find('ul').find_all('li')
            tournament_type_players_keys = [['men_doubles_winner_1', 'men_doubles_winner_2'],
                                            ['men_doubles_runner_up_1', 'men_doubles_runner_up_2'],
                                            ['men_doubles_third_place_1_1', 'men_doubles_third_place_1_2'],
                                            ['men_doubles_third_place_2_1', 'men_doubles_third_place_2_2']]
            for player_index, tournament_type_player in enumerate(tournament_type_players):
                # player_name = tournament_type_player.find(class_='flag-name-wrap').find('a')['title']
                # print(f'{player_index}: {player_name}')
                players = tournament_type_player.find_all(class_='flag-name-wrap')
                df_results[tournament_type_players_keys[player_index][0]][len(df_results.index) - 1] = \
                players[0].find("a")["title"]
                df_results[tournament_type_players_keys[player_index][1]][len(df_results.index) - 1] = \
                    players[1].find("a")["title"]

            #  WOMEN DOUBLES
            women_doubles = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-double')[1]
            women_doubles_entries = women_doubles.find(class_="title").find('span').text.strip()
            tournament_type_players = women_doubles.find('ul').find_all('li')
            tournament_type_players_keys = [['women_doubles_winner_1', 'women_doubles_winner_2'],
                                            ['women_doubles_runner_up_1', 'women_doubles_runner_up_2'],
                                            ['women_doubles_third_place_1_1', 'women_doubles_third_place_1_2'],
                                            ['women_doubles_third_place_2_1', 'women_doubles_third_place_2_2']]
            for player_index, tournament_type_player in enumerate(tournament_type_players):
                # player_name = tournament_type_player.find(class_='flag-name-wrap').find('a')['title']
                # print(f'{player_index}: {player_name}')
                players = tournament_type_player.find_all(class_='flag-name-wrap')
                df_results[tournament_type_players_keys[player_index][0]][len(df_results.index) - 1] = \
                    players[0].find("a")["title"]
                df_results[tournament_type_players_keys[player_index][1]][len(df_results.index) - 1] = \
                    players[1].find("a")["title"]

            #  MIXED DOUBLES
            women_doubles = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-double')[2]
            women_doubles_entries = women_doubles.find(class_="title").find('span').text.strip()
            tournament_type_players = women_doubles.find('ul').find_all('li')
            tournament_type_players_keys = [['mixed_doubles_winner_1', 'mixed_doubles_winner_2'],
                                            ['mixed_doubles_runner_up_1', 'mixed_doubles_runner_up_2'],
                                            ['mixed_doubles_third_place_1_1', 'mixed_doubles_third_place_1_2'],
                                            ['mixed_doubles_third_place_2_1', 'mixed_doubles_third_place_2_2']]
            for player_index, tournament_type_player in enumerate(tournament_type_players):
                # player_name = tournament_type_player.find(class_='flag-name-wrap').find('a')['title']
                # print(f'{player_index}: {player_name}')
                players = tournament_type_player.find_all(class_='flag-name-wrap')
                df_results[tournament_type_players_keys[player_index][0]][len(df_results.index) - 1] = \
                    players[0].find("a")["title"]
                df_results[tournament_type_players_keys[player_index][1]][len(df_results.index) - 1] = \
                    players[1].find("a")["title"]

            # # DOUBLES
            # tournament_type_singles = ["MEN'S DOUBLES", "WOMEN'S DOUBLES", "MIXED DOUBLES"]
            # tournament_types = inner_soup.find(class_='item-results-podium').find_all('div', class_='men-double')
            # # print(len(tournament_types))
            # for index, tournament_type in enumerate(tournament_types):
            #     tournament_type_category = tournament_type_singles[index]
            #     tournament_type_entries = tournament_type.find(class_="title").find('span').text.strip()
            #     print('tournament_type_category:', tournament_type_category)
            #     print('tournament_type_entries:', tournament_type_entries)
            #
            #     tournament_type_players = tournament_type.find('ul').find_all('li')
            #     for player_index, tournament_type_player in enumerate(tournament_type_players):
            #         players = tournament_type_player.find_all(class_='flag-name-wrap')
            #         print(f'{player_index}: {players[0].find("a")["title"]}')
            #         print(f'{player_index}: {players[1].find("a")["title"]}')

            print()

print_dataframe(df_results)
df_results.to_csv('results.csv')
