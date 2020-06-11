CREATE TABLE public.hourly_weather (
    id serial PRIMARY KEY,
    datetime timestamp  without time zone,
    location varchar(10),
    temp integer,
    dwpt integer,
    heat_idx integer,
    rh integer,
    pressure integer,
    vis integer,
    wc integer,
    wdir integer,
    wspd integer,
    prcp integer,
    t_app integer,
    uv_idx integer,
    clds varchar(10)
    );