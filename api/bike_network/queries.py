startup_commands = [
    """
    create table if not exists
    bikenetwork_mods (
        link_id int,
        design int
    );
    """,
    """
    create or replace view
    mods_with_geom as (
        select 
            mods.*,
            st_transform(nl.geom, 4326) as geom
        from
            bikenetwork_mods mods 
        left join
            network_links nl
        on
            mods.link_id = nl.gid
    )
    """,
]
