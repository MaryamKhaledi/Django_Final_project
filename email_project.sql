--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

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
-- Name: accounts_otpcode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_otpcode (
    id bigint NOT NULL,
    phone_number character varying(11) NOT NULL,
    code smallint NOT NULL,
    created timestamp with time zone NOT NULL,
    CONSTRAINT accounts_otpcode_code_check CHECK ((code >= 0))
);


ALTER TABLE public.accounts_otpcode OWNER TO postgres;

--
-- Name: accounts_otpcode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_otpcode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_otpcode_id_seq OWNER TO postgres;

--
-- Name: accounts_otpcode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_otpcode_id_seq OWNED BY public.accounts_otpcode.id;


--
-- Name: accounts_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    is_staff boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    username character varying(50) NOT NULL,
    first_name character varying(30),
    last_name character varying(30),
    recovery character varying(15) NOT NULL,
    email character varying(50),
    phone_number character varying(13),
    birth_date timestamp with time zone,
    gender character varying(10),
    country character varying(40),
    is_active boolean NOT NULL
);


ALTER TABLE public.accounts_user OWNER TO postgres;

--
-- Name: accounts_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.accounts_user_groups OWNER TO postgres;

--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_user_groups_id_seq OWNER TO postgres;

--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_user_groups_id_seq OWNED BY public.accounts_user_groups.id;


--
-- Name: accounts_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_user_id_seq OWNER TO postgres;

--
-- Name: accounts_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_user_id_seq OWNED BY public.accounts_user.id;


--
-- Name: accounts_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.accounts_user_user_permissions OWNER TO postgres;

--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_user_user_permissions_id_seq OWNED BY public.accounts_user_user_permissions.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: mail_page_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_contacts (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    email character varying(60) NOT NULL,
    phone_number character varying(13),
    other_email character varying(60),
    birth_date timestamp with time zone,
    owner_id bigint NOT NULL
);


ALTER TABLE public.mail_page_contacts OWNER TO postgres;

--
-- Name: mail_page_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_contacts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_contacts_id_seq OWNER TO postgres;

--
-- Name: mail_page_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_contacts_id_seq OWNED BY public.mail_page_contacts.id;


--
-- Name: mail_page_email; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_email (
    id bigint NOT NULL,
    receiver character varying(50),
    cc character varying(800),
    bcc character varying(800),
    subject character varying(100),
    body text,
    file character varying(100),
    "timestamp" timestamp with time zone,
    is_draft boolean NOT NULL,
    is_read boolean NOT NULL,
    is_reply boolean NOT NULL,
    is_archived boolean,
    is_trash boolean,
    status character varying(20) NOT NULL,
    reply_id bigint,
    signature_id bigint,
    user_id bigint NOT NULL
);


ALTER TABLE public.mail_page_email OWNER TO postgres;

--
-- Name: mail_page_email_filter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_email_filter (
    id bigint NOT NULL,
    email_id bigint NOT NULL,
    filter_id bigint NOT NULL
);


ALTER TABLE public.mail_page_email_filter OWNER TO postgres;

--
-- Name: mail_page_email_filter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_email_filter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_email_filter_id_seq OWNER TO postgres;

--
-- Name: mail_page_email_filter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_email_filter_id_seq OWNED BY public.mail_page_email_filter.id;


--
-- Name: mail_page_email_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_email_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_email_id_seq OWNER TO postgres;

--
-- Name: mail_page_email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_email_id_seq OWNED BY public.mail_page_email.id;


--
-- Name: mail_page_email_label; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_email_label (
    id bigint NOT NULL,
    email_id bigint NOT NULL,
    label_id bigint NOT NULL
);


ALTER TABLE public.mail_page_email_label OWNER TO postgres;

--
-- Name: mail_page_email_label_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_email_label_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_email_label_id_seq OWNER TO postgres;

--
-- Name: mail_page_email_label_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_email_label_id_seq OWNED BY public.mail_page_email_label.id;


--
-- Name: mail_page_filter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_filter (
    id bigint NOT NULL,
    sender character varying(50),
    subject character varying(500),
    body text,
    file boolean,
    action character varying(20) NOT NULL
);


ALTER TABLE public.mail_page_filter OWNER TO postgres;

--
-- Name: mail_page_filter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_filter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_filter_id_seq OWNER TO postgres;

--
-- Name: mail_page_filter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_filter_id_seq OWNED BY public.mail_page_filter.id;


--
-- Name: mail_page_label; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_label (
    id bigint NOT NULL,
    title character varying(50) NOT NULL,
    owner_id bigint NOT NULL
);


ALTER TABLE public.mail_page_label OWNER TO postgres;

--
-- Name: mail_page_label_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_label_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_label_id_seq OWNER TO postgres;

--
-- Name: mail_page_label_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_label_id_seq OWNED BY public.mail_page_label.id;


--
-- Name: mail_page_signature; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mail_page_signature (
    id bigint NOT NULL,
    title character varying(300) NOT NULL,
    owner_id bigint NOT NULL
);


ALTER TABLE public.mail_page_signature OWNER TO postgres;

--
-- Name: mail_page_signature_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mail_page_signature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_page_signature_id_seq OWNER TO postgres;

--
-- Name: mail_page_signature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mail_page_signature_id_seq OWNED BY public.mail_page_signature.id;


--
-- Name: taggit_tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taggit_tag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE public.taggit_tag OWNER TO postgres;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taggit_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taggit_tag_id_seq OWNER TO postgres;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taggit_tag_id_seq OWNED BY public.taggit_tag.id;


--
-- Name: taggit_taggeditem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taggit_taggeditem (
    id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.taggit_taggeditem OWNER TO postgres;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taggit_taggeditem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taggit_taggeditem_id_seq OWNER TO postgres;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taggit_taggeditem_id_seq OWNED BY public.taggit_taggeditem.id;


--
-- Name: accounts_otpcode id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_otpcode ALTER COLUMN id SET DEFAULT nextval('public.accounts_otpcode_id_seq'::regclass);


--
-- Name: accounts_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user ALTER COLUMN id SET DEFAULT nextval('public.accounts_user_id_seq'::regclass);


--
-- Name: accounts_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups ALTER COLUMN id SET DEFAULT nextval('public.accounts_user_groups_id_seq'::regclass);


--
-- Name: accounts_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.accounts_user_user_permissions_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: mail_page_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_contacts ALTER COLUMN id SET DEFAULT nextval('public.mail_page_contacts_id_seq'::regclass);


--
-- Name: mail_page_email id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email ALTER COLUMN id SET DEFAULT nextval('public.mail_page_email_id_seq'::regclass);


--
-- Name: mail_page_email_filter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_filter ALTER COLUMN id SET DEFAULT nextval('public.mail_page_email_filter_id_seq'::regclass);


--
-- Name: mail_page_email_label id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_label ALTER COLUMN id SET DEFAULT nextval('public.mail_page_email_label_id_seq'::regclass);


--
-- Name: mail_page_filter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_filter ALTER COLUMN id SET DEFAULT nextval('public.mail_page_filter_id_seq'::regclass);


--
-- Name: mail_page_label id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_label ALTER COLUMN id SET DEFAULT nextval('public.mail_page_label_id_seq'::regclass);


--
-- Name: mail_page_signature id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_signature ALTER COLUMN id SET DEFAULT nextval('public.mail_page_signature_id_seq'::regclass);


--
-- Name: taggit_tag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_tag ALTER COLUMN id SET DEFAULT nextval('public.taggit_tag_id_seq'::regclass);


--
-- Name: taggit_taggeditem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_taggeditem ALTER COLUMN id SET DEFAULT nextval('public.taggit_taggeditem_id_seq'::regclass);


--
-- Data for Name: accounts_otpcode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_otpcode (id, phone_number, code, created) FROM stdin;
\.


--
-- Data for Name: accounts_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user (id, password, last_login, is_superuser, is_staff, date_joined, username, first_name, last_name, recovery, email, phone_number, birth_date, gender, country, is_active) FROM stdin;
1	pbkdf2_sha256$260000$TlwiWWFCx5SDR2oLgPkqPB$5pcZ+qwa9UdTX/Xc8Vb4E2j0REimbbLqb4u0tlARZpI=	2022-03-17 20:57:51.049583+03	f	f	2022-03-16 18:22:58.977125+03	maryam@eml.com	\N	\N	email_address	khaledi.maryam74@gmail.com	\N	\N	\N	\N	t
3	pbkdf2_sha256$260000$tsBg1nor4b19lKHjTkKiSX$WMzMeKe3sSAZKhxkPc5SiV9ljLsg+5w6NbCnPjhGVQY=	2022-03-17 20:59:18.403505+03	f	f	2022-03-16 18:26:22.4986+03	mohammad@eml.com	\N	\N	email_address	marytst1may@gmail.com	\N	\N	\N	\N	t
2	pbkdf2_sha256$260000$xnMhBTqymuMWutpU1w5zYM$HfONtrywEo19cOBsJfbMVLoDHSrD0HTpdklp0Dk88XM=	2022-03-17 21:06:15.205997+03	f	f	2022-03-16 18:24:27.145097+03	ali@eml.com	\N	\N	email_address	math.khaledi74@gmail.com	\N	\N	\N	\N	t
\.


--
-- Data for Name: accounts_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: accounts_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add filter	6	add_filter
22	Can change filter	6	change_filter
23	Can delete filter	6	delete_filter
24	Can view filter	6	view_filter
25	Can add signature	7	add_signature
26	Can change signature	7	change_signature
27	Can delete signature	7	delete_signature
28	Can view signature	7	view_signature
29	Can add label	8	add_label
30	Can change label	8	change_label
31	Can delete label	8	delete_label
32	Can view label	8	view_label
33	Can add email	9	add_email
34	Can change email	9	change_email
35	Can delete email	9	delete_email
36	Can view email	9	view_email
37	Can add contacts	10	add_contacts
38	Can change contacts	10	change_contacts
39	Can delete contacts	10	delete_contacts
40	Can view contacts	10	view_contacts
41	Can add otp code	11	add_otpcode
42	Can change otp code	11	change_otpcode
43	Can delete otp code	11	delete_otpcode
44	Can view otp code	11	view_otpcode
45	Can add user	12	add_user
46	Can change user	12	change_user
47	Can delete user	12	delete_user
48	Can view user	12	view_user
49	Can add tag	13	add_tag
50	Can change tag	13	change_tag
51	Can delete tag	13	delete_tag
52	Can view tag	13	view_tag
53	Can add tagged item	14	add_taggeditem
54	Can change tagged item	14	change_taggeditem
55	Can delete tagged item	14	delete_taggeditem
56	Can view tagged item	14	view_taggeditem
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	mail_page	filter
7	mail_page	signature
8	mail_page	label
9	mail_page	email
10	mail_page	contacts
11	accounts	otpcode
12	accounts	user
13	taggit	tag
14	taggit	taggeditem
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-03-16 18:20:45.752619+03
2	contenttypes	0002_remove_content_type_name	2022-03-16 18:20:45.878627+03
3	auth	0001_initial	2022-03-16 18:20:46.469659+03
4	auth	0002_alter_permission_name_max_length	2022-03-16 18:20:46.48866+03
5	auth	0003_alter_user_email_max_length	2022-03-16 18:20:46.49766+03
6	auth	0004_alter_user_username_opts	2022-03-16 18:20:46.514663+03
7	auth	0005_alter_user_last_login_null	2022-03-16 18:20:46.526662+03
8	auth	0006_require_contenttypes_0002	2022-03-16 18:20:46.533662+03
9	auth	0007_alter_validators_add_error_messages	2022-03-16 18:20:46.544665+03
10	auth	0008_alter_user_username_max_length	2022-03-16 18:20:46.557664+03
11	auth	0009_alter_user_last_name_max_length	2022-03-16 18:20:46.571667+03
12	auth	0010_alter_group_name_max_length	2022-03-16 18:20:46.617667+03
13	auth	0011_update_proxy_permissions	2022-03-16 18:20:46.630668+03
14	auth	0012_alter_user_first_name_max_length	2022-03-16 18:20:46.648668+03
15	accounts	0001_initial	2022-03-16 18:20:47.2147+03
16	admin	0001_initial	2022-03-16 18:20:47.38671+03
17	admin	0002_logentry_remove_auto_add	2022-03-16 18:20:47.411711+03
18	admin	0003_logentry_add_action_flag_choices	2022-03-16 18:20:47.441715+03
19	mail_page	0001_initial	2022-03-16 18:20:48.137753+03
20	sessions	0001_initial	2022-03-16 18:20:48.231759+03
21	taggit	0001_initial	2022-03-16 18:20:48.509773+03
22	taggit	0002_auto_20150616_2121	2022-03-16 18:20:48.559777+03
23	taggit	0003_taggeditem_add_unique_index	2022-03-16 18:20:48.601785+03
24	taggit	0004_alter_taggeditem_content_type_alter_taggeditem_tag	2022-03-16 18:20:48.655782+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
s1qlp0im1h8ai4yj81gx9dfsgpw9nmyl	.eJxVjEsOwjAMBe-SNYocJySFJfueoXJshxZQI_WzQtydVuoCtjPz3tt0tC59t846dYOYq_Hm9Msy8VPHXciDxnu1XMdlGrLdE3vY2bZV9HU72r-DnuZ-WwMVgHNyAQKikyQhOizBoQcunlEyM6XYEGnQJouqJNK4gQsgAZvPF9IbODw:1nUVXx:-kv3KWajPEBBpi5nqXNqaeUtg176L5eGICXr_2oxEAs	2022-03-30 18:26:45.091871+03
i6mr0761a7gpviktbv4bcasm5ahuxypf	.eJxVjDsOwyAQBe9CHSFYzGdTpvcZELA4OIlAMnYV5e6xJRdJ-2bmvZkP21r81vPiZ2JXJtnld4shPXM9AD1CvTeeWl2XOfJD4SftfGyUX7fT_TsooZe9dhacQIoqxIxZCCIZANOUyDgtrQEYnAJtlcYExoJKAk3ESQ4Gd27Z5wvOojaY:1nUuCT:Yt017z3uMkLmBXUgoeSJKvAvN9Vs0TWOYhQQPL6CoEI	2022-03-31 20:46:13.765285+03
n3shsj8f0fzk68caahvrka9glnhcuxd4	.eJxVjEEOgjAQRe_StWmkhSl16Z4zNDPMjEUNTSisjHdXEha6_e-9_zIJtzWnrcqSJjYX48zpdyMcHzLvgO8434ody7wuE9ldsQetdigsz-vh_h1krPlbk_N9aCNpdKTBMxO7qMAYzw5IPTBDHzqClkUgcKfSSBMYgDyoonl_AP2zOOU:1nUuVr:o8esWteVwLqeTHNhVtah1GGtxCxxQyfHnNGuwqBPGjs	2022-03-31 21:06:15.249002+03
\.


--
-- Data for Name: mail_page_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_contacts (id, name, email, phone_number, other_email, birth_date, owner_id) FROM stdin;
\.


--
-- Data for Name: mail_page_email; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_email (id, receiver, cc, bcc, subject, body, file, "timestamp", is_draft, is_read, is_reply, is_archived, is_trash, status, reply_id, signature_id, user_id) FROM stdin;
4	\N	\N	\N	test 4	where are you?		2022-03-17 18:39:48.828788+03	t	f	f	f	f	none	\N	\N	1
6	ali@eml.com	\N	\N	test 5	hi rafigh\n sent to: mohammad@eml.com		2022-03-17 20:59:51.656381+03	f	f	f	f	f	none	\N	\N	3
5	mohammad@eml.com	\N	\N	test 5	hi rafigh\n sent to: mohammad@eml.com		2022-03-17 20:59:51.536379+03	f	f	f	t	f	none	\N	\N	3
2	mohammad@eml.com	\N	\N	test 2	happy berth day\n sent to: mohammad@eml.com	documents/2022/03/17/╪ش┘╪│┘ç-3-╪ز┘╪»-╪«┘ê╪د┘█î.pdf	2022-03-17 18:38:21.692874+03	f	f	f	t	f	none	\N	\N	1
8	maryam@eml.com	\N	\N	test 6	maraym montazeretone\n sent to: ali@eml.com\n sent to: maryam@eml.com	documents/2022/03/17/╪ش┘╪│┘ç-┘╛┘╪ش┘à-╪ز┘╪»╪«┘ê╪د┘█î-┘ê-╪ز┘é┘ê█î╪ز-╪ص╪د┘╪╕┘ç-╪د╪│╪▒╪د_s7f0dGv.pdf	2022-03-17 21:05:49.747563+03	f	f	f	f	f	none	\N	\N	3
9	ali@eml.com	\N	\N	test 7	\n sent to: ali@eml.com		2022-03-17 21:07:54.373588+03	f	f	f	t	f	none	\N	\N	2
7	ali@eml.com	\N	\N	test 6	maraym montazeretone\n sent to: ali@eml.com	documents/2022/03/17/╪ش┘╪│┘ç-┘╛┘╪ش┘à-╪ز┘╪»╪«┘ê╪د┘█î-┘ê-╪ز┘é┘ê█î╪ز-╪ص╪د┘╪╕┘ç-╪د╪│╪▒╪د.pdf	2022-03-17 21:05:49.332539+03	f	f	f	t	f	none	\N	\N	3
11	maryam@eml.com	\N	\N	test 8	do you noww?		2022-03-17 23:58:05.79337+03	f	f	f	f	f	none	\N	\N	2
3	ali@eml.com	\N	\N	test 2	happy berth day\n sent to: mohammad@eml.com	documents/2022/03/17/╪ش┘╪│┘ç-3-╪ز┘╪»-╪«┘ê╪د┘█î_zMF3wXB.pdf	2022-03-17 18:38:21.715877+03	f	f	f	t	t	none	\N	\N	1
1	ali@eml.com	\N	\N	tset 1	hi maryam	documents/2022/03/17/╪ش┘╪│┘ç-1-2.pdf	2022-03-17 18:36:50.328724+03	f	f	f	t	t	none	\N	\N	1
10	maryam@eml.com	\N	\N	test 7	\n sent to: ali@eml.com\n sent to: maryam@eml.com		2022-03-17 21:07:54.38659+03	f	f	f	f	f	none	\N	\N	2
\.


--
-- Data for Name: mail_page_email_filter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_email_filter (id, email_id, filter_id) FROM stdin;
\.


--
-- Data for Name: mail_page_email_label; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_email_label (id, email_id, label_id) FROM stdin;
1	7	2
2	11	1
\.


--
-- Data for Name: mail_page_filter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_filter (id, sender, subject, body, file, action) FROM stdin;
\.


--
-- Data for Name: mail_page_label; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_label (id, title, owner_id) FROM stdin;
1	class	2
2	hapy	2
3	sprint	2
\.


--
-- Data for Name: mail_page_signature; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mail_page_signature (id, title, owner_id) FROM stdin;
\.


--
-- Data for Name: taggit_tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taggit_tag (id, name, slug) FROM stdin;
\.


--
-- Data for Name: taggit_taggeditem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taggit_taggeditem (id, object_id, content_type_id, tag_id) FROM stdin;
\.


--
-- Name: accounts_otpcode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_otpcode_id_seq', 1, false);


--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_groups_id_seq', 1, false);


--
-- Name: accounts_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_id_seq', 3, true);


--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_user_permissions_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 56, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 14, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 24, true);


--
-- Name: mail_page_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_contacts_id_seq', 1, false);


--
-- Name: mail_page_email_filter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_email_filter_id_seq', 1, false);


--
-- Name: mail_page_email_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_email_id_seq', 11, true);


--
-- Name: mail_page_email_label_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_email_label_id_seq', 2, true);


--
-- Name: mail_page_filter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_filter_id_seq', 1, false);


--
-- Name: mail_page_label_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_label_id_seq', 3, true);


--
-- Name: mail_page_signature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mail_page_signature_id_seq', 1, false);


--
-- Name: taggit_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taggit_tag_id_seq', 1, false);


--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taggit_taggeditem_id_seq', 1, false);


--
-- Name: accounts_otpcode accounts_otpcode_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_otpcode
    ADD CONSTRAINT accounts_otpcode_phone_number_key UNIQUE (phone_number);


--
-- Name: accounts_otpcode accounts_otpcode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_otpcode
    ADD CONSTRAINT accounts_otpcode_pkey PRIMARY KEY (id);


--
-- Name: accounts_user accounts_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_email_key UNIQUE (email);


--
-- Name: accounts_user_groups accounts_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_pkey PRIMARY KEY (id);


--
-- Name: accounts_user_groups accounts_user_groups_user_id_group_id_59c0b32f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_user_id_group_id_59c0b32f_uniq UNIQUE (user_id, group_id);


--
-- Name: accounts_user accounts_user_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_phone_number_key UNIQUE (phone_number);


--
-- Name: accounts_user accounts_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_pkey PRIMARY KEY (id);


--
-- Name: accounts_user_user_permissions accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq UNIQUE (user_id, permission_id);


--
-- Name: accounts_user_user_permissions accounts_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: accounts_user accounts_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_username_key UNIQUE (username);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: mail_page_contacts mail_page_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_contacts
    ADD CONSTRAINT mail_page_contacts_pkey PRIMARY KEY (id);


--
-- Name: mail_page_email_filter mail_page_email_filter_email_id_filter_id_4dcbe4b8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_filter
    ADD CONSTRAINT mail_page_email_filter_email_id_filter_id_4dcbe4b8_uniq UNIQUE (email_id, filter_id);


--
-- Name: mail_page_email_filter mail_page_email_filter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_filter
    ADD CONSTRAINT mail_page_email_filter_pkey PRIMARY KEY (id);


--
-- Name: mail_page_email_label mail_page_email_label_email_id_label_id_e901a235_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_label
    ADD CONSTRAINT mail_page_email_label_email_id_label_id_e901a235_uniq UNIQUE (email_id, label_id);


--
-- Name: mail_page_email_label mail_page_email_label_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_label
    ADD CONSTRAINT mail_page_email_label_pkey PRIMARY KEY (id);


--
-- Name: mail_page_email mail_page_email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email
    ADD CONSTRAINT mail_page_email_pkey PRIMARY KEY (id);


--
-- Name: mail_page_filter mail_page_filter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_filter
    ADD CONSTRAINT mail_page_filter_pkey PRIMARY KEY (id);


--
-- Name: mail_page_label mail_page_label_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_label
    ADD CONSTRAINT mail_page_label_pkey PRIMARY KEY (id);


--
-- Name: mail_page_label mail_page_label_title_owner_id_7e21acab_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_label
    ADD CONSTRAINT mail_page_label_title_owner_id_7e21acab_uniq UNIQUE (title, owner_id);


--
-- Name: mail_page_signature mail_page_signature_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_signature
    ADD CONSTRAINT mail_page_signature_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag taggit_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_tag
    ADD CONSTRAINT taggit_tag_name_key UNIQUE (name);


--
-- Name: taggit_tag taggit_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_tag
    ADD CONSTRAINT taggit_tag_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag taggit_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_tag
    ADD CONSTRAINT taggit_tag_slug_key UNIQUE (slug);


--
-- Name: taggit_taggeditem taggit_taggeditem_content_type_id_object_i_4bb97a8e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_content_type_id_object_i_4bb97a8e_uniq UNIQUE (content_type_id, object_id, tag_id);


--
-- Name: taggit_taggeditem taggit_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_pkey PRIMARY KEY (id);


--
-- Name: accounts_otpcode_phone_number_da335c33_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_otpcode_phone_number_da335c33_like ON public.accounts_otpcode USING btree (phone_number varchar_pattern_ops);


--
-- Name: accounts_user_email_b2644a56_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_email_b2644a56_like ON public.accounts_user USING btree (email varchar_pattern_ops);


--
-- Name: accounts_user_groups_group_id_bd11a704; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_groups_group_id_bd11a704 ON public.accounts_user_groups USING btree (group_id);


--
-- Name: accounts_user_groups_user_id_52b62117; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_groups_user_id_52b62117 ON public.accounts_user_groups USING btree (user_id);


--
-- Name: accounts_user_phone_number_af3e1068_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_phone_number_af3e1068_like ON public.accounts_user USING btree (phone_number varchar_pattern_ops);


--
-- Name: accounts_user_user_permissions_permission_id_113bb443; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_user_permissions_permission_id_113bb443 ON public.accounts_user_user_permissions USING btree (permission_id);


--
-- Name: accounts_user_user_permissions_user_id_e4f0a161; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_user_permissions_user_id_e4f0a161 ON public.accounts_user_user_permissions USING btree (user_id);


--
-- Name: accounts_user_username_6088629e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_user_username_6088629e_like ON public.accounts_user USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: mail_page_contacts_owner_id_94a0f644; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_contacts_owner_id_94a0f644 ON public.mail_page_contacts USING btree (owner_id);


--
-- Name: mail_page_email_filter_email_id_a74ddca9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_filter_email_id_a74ddca9 ON public.mail_page_email_filter USING btree (email_id);


--
-- Name: mail_page_email_filter_filter_id_fa4514c0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_filter_filter_id_fa4514c0 ON public.mail_page_email_filter USING btree (filter_id);


--
-- Name: mail_page_email_label_email_id_664bc686; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_label_email_id_664bc686 ON public.mail_page_email_label USING btree (email_id);


--
-- Name: mail_page_email_label_label_id_4ec2d445; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_label_label_id_4ec2d445 ON public.mail_page_email_label USING btree (label_id);


--
-- Name: mail_page_email_reply_id_3be89f01; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_reply_id_3be89f01 ON public.mail_page_email USING btree (reply_id);


--
-- Name: mail_page_email_signature_id_c36fd73a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_signature_id_c36fd73a ON public.mail_page_email USING btree (signature_id);


--
-- Name: mail_page_email_user_id_8fa7b63f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_email_user_id_8fa7b63f ON public.mail_page_email USING btree (user_id);


--
-- Name: mail_page_label_owner_id_4911c1dc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_label_owner_id_4911c1dc ON public.mail_page_label USING btree (owner_id);


--
-- Name: mail_page_signature_owner_id_96497f38; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mail_page_signature_owner_id_96497f38 ON public.mail_page_signature USING btree (owner_id);


--
-- Name: taggit_tag_name_58eb2ed9_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taggit_tag_name_58eb2ed9_like ON public.taggit_tag USING btree (name varchar_pattern_ops);


--
-- Name: taggit_tag_slug_6be58b2c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taggit_tag_slug_6be58b2c_like ON public.taggit_tag USING btree (slug varchar_pattern_ops);


--
-- Name: taggit_taggeditem_content_type_id_9957a03c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taggit_taggeditem_content_type_id_9957a03c ON public.taggit_taggeditem USING btree (content_type_id);


--
-- Name: taggit_taggeditem_content_type_id_object_id_196cc965_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taggit_taggeditem_content_type_id_object_id_196cc965_idx ON public.taggit_taggeditem USING btree (content_type_id, object_id);


--
-- Name: taggit_taggeditem_object_id_e2d7d1df; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taggit_taggeditem_object_id_e2d7d1df ON public.taggit_taggeditem USING btree (object_id);


--
-- Name: taggit_taggeditem_tag_id_f4f5b767; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX taggit_taggeditem_tag_id_f4f5b767 ON public.taggit_taggeditem USING btree (tag_id);


--
-- Name: accounts_user_groups accounts_user_groups_group_id_bd11a704_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_group_id_bd11a704_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_groups accounts_user_groups_user_id_52b62117_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_user_id_52b62117_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_user_permissions accounts_user_user_p_permission_id_113bb443_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_p_permission_id_113bb443_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_user_permissions accounts_user_user_p_user_id_e4f0a161_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_p_user_id_e4f0a161_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_contacts mail_page_contacts_owner_id_94a0f644_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_contacts
    ADD CONSTRAINT mail_page_contacts_owner_id_94a0f644_fk_accounts_user_id FOREIGN KEY (owner_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email_filter mail_page_email_filt_filter_id_fa4514c0_fk_mail_page; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_filter
    ADD CONSTRAINT mail_page_email_filt_filter_id_fa4514c0_fk_mail_page FOREIGN KEY (filter_id) REFERENCES public.mail_page_filter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email_filter mail_page_email_filter_email_id_a74ddca9_fk_mail_page_email_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_filter
    ADD CONSTRAINT mail_page_email_filter_email_id_a74ddca9_fk_mail_page_email_id FOREIGN KEY (email_id) REFERENCES public.mail_page_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email_label mail_page_email_label_email_id_664bc686_fk_mail_page_email_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_label
    ADD CONSTRAINT mail_page_email_label_email_id_664bc686_fk_mail_page_email_id FOREIGN KEY (email_id) REFERENCES public.mail_page_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email_label mail_page_email_label_label_id_4ec2d445_fk_mail_page_label_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email_label
    ADD CONSTRAINT mail_page_email_label_label_id_4ec2d445_fk_mail_page_label_id FOREIGN KEY (label_id) REFERENCES public.mail_page_label(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email mail_page_email_reply_id_3be89f01_fk_mail_page_email_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email
    ADD CONSTRAINT mail_page_email_reply_id_3be89f01_fk_mail_page_email_id FOREIGN KEY (reply_id) REFERENCES public.mail_page_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email mail_page_email_signature_id_c36fd73a_fk_mail_page_signature_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email
    ADD CONSTRAINT mail_page_email_signature_id_c36fd73a_fk_mail_page_signature_id FOREIGN KEY (signature_id) REFERENCES public.mail_page_signature(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_email mail_page_email_user_id_8fa7b63f_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_email
    ADD CONSTRAINT mail_page_email_user_id_8fa7b63f_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_label mail_page_label_owner_id_4911c1dc_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_label
    ADD CONSTRAINT mail_page_label_owner_id_4911c1dc_fk_accounts_user_id FOREIGN KEY (owner_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_page_signature mail_page_signature_owner_id_96497f38_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mail_page_signature
    ADD CONSTRAINT mail_page_signature_owner_id_96497f38_fk_accounts_user_id FOREIGN KEY (owner_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem taggit_taggeditem_content_type_id_9957a03c_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_content_type_id_9957a03c_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES public.taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

