\connect "docker-database";

CREATE TABLE public.users (
  id serial primary key,
  email varchar NOT NULL,
	"password" varchar NOT NULL,
  created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NULL
);

INSERT INTO public.users
(id, email, "password", created_at, updated_at)
VALUES
(1, 'abcde@gmail.com', '$2b$10$0dqgeGWLUHI74Ezua6vNL.uZCEef9qDFnO7cjZpoEJ2vd97tFxU56', '2021-12-21 12:42:43.633', NULL),
(2, 'qwert@gmail.com', '$2b$10$0dqgeGWLUHI74Ezua6vNL.uZCEef9qDFnO7cjZpoEJ2vd97tFxU56', '2021-12-21 13:42:43.633', NULL),
(3, 'asdfg@gmail.com', '$2b$10$0dqgeGWLUHI74Ezua6vNL.uZCEef9qDFnO7cjZpoEJ2vd97tFxU56', '2021-12-21 14:42:43.633', NULL);
