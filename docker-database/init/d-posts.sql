\connect "docker-database";

CREATE TABLE public.posts (
  id serial primary key,
  author varchar NOT NULL,
  title varchar NOT NULL,
  content varchar NOT NULL,
  created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NULL
);

INSERT INTO public.posts
(id, author, title, "content", created_at, updated_at)
VALUES
(1, 'abcde@gmail.com', 'express server', 'express server ...', '2021-12-21 12:46:31.150', NULL),
(2, 'abcde@gmail.com', 'django server', 'django server ...', '2021-12-22 12:46:31.150', NULL),
(3, 'abcde@gmail.com', 'koa server', 'koa server ...', '2021-12-23 12:46:31.150', NULL),
(4, 'qwert@gmail.com', 'flask server', 'flask server ...', '2021-12-24 12:46:31.150', NULL),
(5, 'qwert@gmail.com', 'spring server', 'spring server ...', '2021-12-25 12:46:31.150', NULL),
(6, 'zxcvb@gmail.com', 'php server', 'php server ...', '2021-12-26 12:46:31.150', NULL),
(7, 'zxcvb@gmail.com', 'go server', 'go server ...', '2021-12-27 12:46:31.150', NULL);
