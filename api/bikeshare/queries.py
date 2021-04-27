# TO DO: Pre-process DB with views for each station ID

od_query = """
    with origins as (
    select
        start_station as station_id,
        count(*) as origins
        from trips
        where end_station in ID_LIST
        group by start_station
    ),
    destinations as (
    select
        end_station as station_id,
        count(*) as destinations
        from trips
        where start_station in ID_LIST
        group by end_station
    ),
    numeric_data as (
        select o.station_id, o.origins, d.destinations
        from origins o
        full outer join destinations d on o.station_id = d.station_id
    )
    select ss.geom, ss.name, nd.* from station_shapes ss
    inner join numeric_data nd on ss.id = nd.station_id
"""
