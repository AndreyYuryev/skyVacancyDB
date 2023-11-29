-- SQL-команды для создания таблиц
--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;
---
--- drop tables
---

DROP TABLE IF EXISTS VACANCIES;
DROP TABLE IF EXISTS COMPANIES;
DROP TABLE IF EXISTS CITIES;

--
-- Name: CITIES; Type: TABLE; Schema: public; Owner: -; Tablespace:
--
CREATE TABLE CITIES (
    CITY_ID int PRIMARY KEY,
    CITY_NAME VARCHAR(50) NOT NULL
);
--
-- Name: COMPANIES; Type: TABLE; Schema: public; Owner: -; Tablespace:
--
CREATE TABLE COMPANIES (
    COMPANY_ID int PRIMARY KEY,
    COMPANY_NAME VARCHAR(255) NOT NULL,
    CITY_ID int,
    OPEN_VACANCIES int,
    CONSTRAINT PK_COMPANIES_CITY_ID FOREIGN KEY(CITY_ID) REFERENCES CITIES(CITY_ID)
);
--
-- Name: VACANCIES; Type: TABLE; Schema: public; Owner: -; Tablespace:
--
CREATE TABLE VACANCIES (
    VACANCY_ID int PRIMARY KEY,
    VACANCY_TITLE VARCHAR(255) NOT NULL,
    COMPANY_ID int,
    CITY_ID int,
    SALARY real,
    CURRENCY varchar(5),
    URL varchar(255),
    CONSTRAINT PK_VACANCIES_CITY_ID FOREIGN KEY(CITY_ID) REFERENCES CITIES(CITY_ID),
    CONSTRAINT PK_VACANCIES_COMPANY_ID FOREIGN KEY(COMPANY_ID) REFERENCES COMPANIES(COMPANY_ID)
);

