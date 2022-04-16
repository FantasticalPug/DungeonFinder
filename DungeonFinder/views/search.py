"""DungeonFinder Search Algorithm."""
import flask
import DungeonFinder
from DungeonFinder.views.accounts import check_session

@DungeonFinder.app.route('/search/')
def show_results():
    """Perform the search and display the results page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    campaign = flask.request.args['campaign']
    system = flask.request.args['system']
    tags = flask.request.args['tags']
    days = flask.request.args.getlist('day[]')
    begin = flask.request.args['begin']
    end = flask.request.args['end']
    frequency = flask.request.args['frequency']
    fil = flask.request.args.get('filter', False)
    days_str = ""
    if len(days) == 7:
        days_str = "Anyday"
    else:
        for day in days:
            if len(days_str) == 0:
                days_str = f"{day}"
            else:
                days_str = f"{days_str} {day}"
    if begin != '' and end != '':
        begin_time = begin.split(':')
        begin = f"{begin_time[0]}{begin_time[1]}"
        begin = int(begin)
        end_time = end.split(':')
        end = f"{end_time[0]}{end_time[1]}"
        end = int(end)
        if end < begin:
            end += 2400
    tags = tags.split(',')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE owner != ?",
        (logname, )
    )
    data = cur.fetchall()
    games = []
    for game in data:
        count = 0
        for tag in tags:
            if tag.lower() in game['tags'].lower():
                count += 1
        game['count'] = count
        cur = connection.execute(
            "SELECT * FROM sessions WHERE gameid = ?",
            (game['gameid'], )
        )
        filled = len(cur.fetchall())
        added = False
        if len(campaign) > 0 and len(system) > 0 and campaign.lower() in game['name'].lower() and game['system'] == system and filled < game['slots']:
            games.append(game)
            added = True
        elif len(campaign) > 0 and len(system) == 0 and campaign.lower() in game['name'].lower() and filled < game['slots']:
            games.append(game)
            added = True
        elif len(system) > 0 and len(campaign) == 0 and game['system'] == system and filled < game['slots']:
            games.append(game)
            added = True
        elif len(campaign) == 0 and len(system) == 0 and filled < game['slots']:
            games.append(game)
            added = True
        if count == 0 and fil == 'Y' and len(tags) > 0 and added:
            games.remove(game)
            added = False
            continue
        if days_str != "Anyday" and days_str != '' and added:
            days_list = days_str.split()
            day_found = False
            for day in days_list:
                if day in game['avail'] or "Anyday" in game['avail']:
                    day_found = True
            if not day_found:
                games.remove(game)
                added = False
                continue
        if begin != '' and end != '' and added:
            game_times = game['avail'].split(' from ')
            game_times = game_times[1]
            game_times = game_times.split(' until ')
            game_begin = ''
            game_end = ''
            if 'AM' in game_times[0]:
                game_begin = game_times[0].replace(' AM', '')
                game_begin = game_begin.replace(':', '')
                game_begin = int(game_begin)
            else:
                game_begin = game_times[0].replace(' PM', '')
                game_begin = game_begin.replace(':', '')
                game_begin = int(game_begin)
                game_begin += 1200
            if 'AM' in game_times[1]:
                game_end = game_times[1].replace(' AM', '')
                game_end = game_end.replace(':', '')
                game_end = int(game_end)
            else:
                game_end = game_times[1].replace(' PM', '')
                game_end = game_end.replace(':', '')
                game_end = int(game_end)
                game_end += 1200
            if game_end < game_begin:
                game_end += 2400
            if begin >= game_end or end <= game_begin:
                games.remove(game)
                added = False
                continue
        if frequency != game['frequency'] and frequency != '':
            games.remove(game)
            added = False
            continue
    games_found = True
    if len(games) == 0:
        games_found = False
    games = sorted(games, key=lambda game: game['count'], reverse=True)
    context = {
        "logname": logname,
        "games": games,
        "found": games_found,
        "page": "Search Results"
    }
    return flask.render_template("results.html", **context)
