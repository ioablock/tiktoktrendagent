create table runs (
    id uuid default gen_random_uuid () primary key,
    niche text not null,
    created_at timestamp
    with
        time zone default now(),
        video_count int,
        viral_count int,
        used_fallback boolean default false,
        notion_url text,
        status text,
        videos jsonb
);