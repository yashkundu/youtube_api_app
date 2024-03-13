-- create tables
create table if not exists mydb.videos
(
    video_id varchar(50) primary key,
    title varchar(150) not null,
    description text,
    published_at timestamp not null,
    thumbnail_url varchar(50)
);