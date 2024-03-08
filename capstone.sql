--
-- PostgreSQL database dump
--

-- Dumped from database version 13.14
-- Dumped by pg_dump version 13.14

-- Started on 2024-03-07 13:49:23

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 39538)
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying,
    age integer,
    gender character varying
);


ALTER TABLE public.actors OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 39536)
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO postgres;

--
-- TOC entry 3025 (class 0 OID 0)
-- Dependencies: 201
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- TOC entry 200 (class 1259 OID 39531)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 39560)
-- Name: casts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.casts (
    id integer NOT NULL,
    movie_id integer NOT NULL,
    actor_id integer NOT NULL
);


ALTER TABLE public.casts OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 39558)
-- Name: casts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.casts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.casts_id_seq OWNER TO postgres;

--
-- TOC entry 3026 (class 0 OID 0)
-- Dependencies: 205
-- Name: casts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.casts_id_seq OWNED BY public.casts.id;


--
-- TOC entry 204 (class 1259 OID 39549)
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying,
    release_date timestamp without time zone
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 39547)
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO postgres;

--
-- TOC entry 3027 (class 0 OID 0)
-- Dependencies: 203
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- TOC entry 2868 (class 2604 OID 39541)
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- TOC entry 2870 (class 2604 OID 39563)
-- Name: casts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casts ALTER COLUMN id SET DEFAULT nextval('public.casts_id_seq'::regclass);


--
-- TOC entry 2869 (class 2604 OID 39552)
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- TOC entry 3015 (class 0 OID 39538)
-- Dependencies: 202
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actors (id, name, age, gender) FROM stdin;
1	Lee Gleichner	41	n/a
2	Pat Gutmann	31	female
3	Karla Christiansen	53	female
4	Toby Christiansen II	43	male
5	Freda Hirthe	45	n/a
\.


--
-- TOC entry 3013 (class 0 OID 39531)
-- Dependencies: 200
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
feb35a2178a9
\.


--
-- TOC entry 3019 (class 0 OID 39560)
-- Dependencies: 206
-- Data for Name: casts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.casts (id, movie_id, actor_id) FROM stdin;
4	2	2
\.


--
-- TOC entry 3017 (class 0 OID 39549)
-- Dependencies: 204
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (id, title, release_date) FROM stdin;
1	Enim molestiae rerum et.	2024-03-26 07:16:58.125
2	Sed error consequuntur.	2024-03-23 07:17:59.671
\.


--
-- TOC entry 3028 (class 0 OID 0)
-- Dependencies: 201
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actors_id_seq', 6, true);


--
-- TOC entry 3029 (class 0 OID 0)
-- Dependencies: 205
-- Name: casts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.casts_id_seq', 4, true);


--
-- TOC entry 3030 (class 0 OID 0)
-- Dependencies: 203
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 2, true);


--
-- TOC entry 2878 (class 2606 OID 39567)
-- Name: casts _movie_actor_uc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT _movie_actor_uc UNIQUE (movie_id, actor_id);


--
-- TOC entry 2874 (class 2606 OID 39546)
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- TOC entry 2872 (class 2606 OID 39535)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 2880 (class 2606 OID 39565)
-- Name: casts casts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_pkey PRIMARY KEY (id);


--
-- TOC entry 2876 (class 2606 OID 39557)
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2881 (class 2606 OID 39568)
-- Name: casts casts_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id);


--
-- TOC entry 2882 (class 2606 OID 39573)
-- Name: casts casts_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


-- Completed on 2024-03-07 13:49:24

--
-- PostgreSQL database dump complete
--

