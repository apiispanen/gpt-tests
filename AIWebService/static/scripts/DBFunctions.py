# CORE FUNCTIONS THAT SPINNY SHOULD HAVE ACCESS TO
# DATA WILL MIRROR THE SCHEMA IN SCHEMAS.PY
# BE SURE TO FEED THE CORRECT FUNCTIONS TO IT IN VIEWS.PY

from AIWebService import embedder, mysql_connect 

connection_local = None

connection_local = mysql_connect.ensure_connection()

database = "instadb"

# connection_local = mysql_connect.connection_local
dataset = []

def find_users(args, connection_local=connection_local, database=database):
    # Inputs user_id and interest
    # Returns a list of users with similar interests
    # Returns userid, username, firstname, lastname, location, interests 
    print('find_users', args)
    interest = args['keyword']
    
    sql = f"""
        USE {database};
        SELECT u.id as "User ID", u.username as "User Name", u.firstname as "First Name", u.lastname as "Last Name", i.name as "Interest"
        FROM user u
        INNER JOIN userinterest ui ON u.id = ui.userid
        INNER JOIN interest i ON ui.refid = i.refid
        WHERE i.name LIKE '%{interest}%'
        LIMIT 5;
    """
    user_id = args.get('user_id', None)
    print('find_users', user_id, interest, sql)
    
    results = mysql_connect.run_sql_script(sql, connection=connection_local)
    
    # # Format the results for GPT to better understand
    # for row in results:
    #     record = {
    #         'User ID': row[0],
    #         'User Name': row[1],
    #         'First Name': row[2],
    #         'Last Name': row[3],
    #         'Interest': row[4]
    #     }
    # dataset.append(record)

    #dataset
    # close connection_local
    return {'results': results}

def find_groups(args, connection_local=connection_local, database=database):
    # Inputs user_id and group_type
    # Returns a list of groups with similar interests
    # Returns group_id, group_name, group_type, location, description, interests, members
    print('find_groups', args)
    user_id = args.get('user_id', None)
    group_type = args['keyword']
    sql = f"""
        USE {database};
        SELECT squadid, description, city, state, country, title
        FROM squad
        where description like '%{group_type}%' OR title like '%{group_type}%'
        LIMIT 5;
    """
    # Updated query for find groups
    
    # USE {mysql_connect.cnx_local.database};
    # SELECT s.squadid as SquadID, s.title as Title, s.description as Description, s.city as City, s.state as State, s.country as Country
    # FROM squad s
    # INNER JOIN squadmedia sm on s.squadid = sm.squadid
    # WHERE sm.category LIKE '%{group_type}%'
    # LIMIT 5;

    print('find_groups', user_id, group_type, sql)
    results = mysql_connect.run_sql_script(sql, connection=connection_local)
    # close connection_local

    return {'results': results}

def find_events(args, connection_local=connection_local, database=database):
    # Inputs user_id, event_type, location, month
    # Returns a list of events nearby (don't worry about location initially) 
    # of a similar type (concert, festival, etc.)
    # Returns event_id, event_name, event_type, location, description, date, time, attendees
    print('find_events', args)
    event_type = args['keyword']

    sql = f"""
    USE {database};
    SELECT e.id, e.title, e.description, e.squad_id, e.address, e.event_type, e.location, i.name interest, i.description interest_description
    FROM events e
    JOIN event_interests ei ON ei.event_id = e.id
    JOIN interest i ON i.refid = ei.interest_id 
    WHERE e.visibility = "public" AND i.name LIKE '%{args['keyword']}%'
    LIMIT 5;
    """
    user_id = args.get('user_id', None)
    zip_code = args.get('zip_code', None)
    print('find_events', user_id, event_type, zip_code, sql)
    results = mysql_connect.run_sql_script(sql, connection=connection_local)
    # close connection_local

    return {'results': results}

def browse__docs(args):
    print('browse__docs', args)
    user_id = args.get('user_id', None)
    keyword = args['keyword']
    results = embedder.get_vector_results(keyword)
    print('browse__docs', user_id, keyword)
    return {'results': [results]}

# Return all of video urls for content moderation
def get_video_urls(connection_local=connection_local):
    sql = f"""
        USE {connection_local.database};
        SELECT id, userid, vidlink
        FROM usermedia;
    """
    results = mysql_connect.run_sql_script(sql, connection=connection_local)
    for row in results:
        record = {
            'ID': row[0],
            'User ID': row[1],
            'Video Link': row[2],
        }
    dataset.append(record)
    return dataset