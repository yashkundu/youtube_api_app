-- creating video table
create table if not exists mydb.videos
(
    video_id varchar(50) primary key,
    title varchar(150) not null,
    description text,
    published_at timestamp not null,
    thumbnail_url varchar(150)
);


-- creating index on videos (published_at) to increase the performance of the get api
create index videos_published_at_idx on mydb.videos (published_at);