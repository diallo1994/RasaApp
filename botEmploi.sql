-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.0-alpha1
-- PostgreSQL version: 9.6
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: new_database | type: DATABASE --
-- -- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE new_database
-- ;
-- -- ddl-end --
-- 

-- object: public."Metier" | type: TABLE --
-- DROP TABLE IF EXISTS public."Metier" CASCADE;
CREATE TABLE public."Metier"(
	"idMetier" smallint NOT NULL,
	"nomMetier" character varying(55) NOT NULL,
	"idSecteur_secteur" smallint NOT NULL,
	CONSTRAINT "idMetier" PRIMARY KEY ("idMetier")

);
-- ddl-end --
ALTER TABLE public."Metier" OWNER TO postgres;
-- ddl-end --

-- object: public.secteur | type: TABLE --
-- DROP TABLE IF EXISTS public.secteur CASCADE;
CREATE TABLE public.secteur(
	"idSecteur" smallint NOT NULL,
	"nomSecteur" character varying(55) NOT NULL,
	CONSTRAINT idsecteur PRIMARY KEY ("idSecteur")

);
-- ddl-end --
ALTER TABLE public.secteur OWNER TO postgres;
-- ddl-end --

-- object: secteur_fk | type: CONSTRAINT --
-- ALTER TABLE public."Metier" DROP CONSTRAINT IF EXISTS secteur_fk CASCADE;
ALTER TABLE public."Metier" ADD CONSTRAINT secteur_fk FOREIGN KEY ("idSecteur_secteur")
REFERENCES public.secteur ("idSecteur") MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.emplois | type: TABLE --
-- DROP TABLE IF EXISTS public.emplois CASCADE;
CREATE TABLE public.emplois(
	"idEmploi" smallint NOT NULL,
	"nomEmploi" character varying(55) NOT NULL,
	"idMetier_Metier" smallint NOT NULL,
	CONSTRAINT "idEmploi" PRIMARY KEY ("idEmploi")

);
-- ddl-end --
ALTER TABLE public.emplois OWNER TO postgres;
-- ddl-end --

-- object: "Metier_fk" | type: CONSTRAINT --
-- ALTER TABLE public.emplois DROP CONSTRAINT IF EXISTS "Metier_fk" CASCADE;
ALTER TABLE public.emplois ADD CONSTRAINT "Metier_fk" FOREIGN KEY ("idMetier_Metier")
REFERENCES public."Metier" ("idMetier") MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.offres | type: TABLE --
-- DROP TABLE IF EXISTS public.offres CASCADE;
CREATE TABLE public.offres(
	"idOffre" smallint NOT NULL,
	"nomEntreprise" character varying(250) NOT NULL,
	zone character varying(55),
	"dateExpiration" date NOT NULL,
	libelle character varying(250),
	"idEmploi_emplois" smallint NOT NULL,
	CONSTRAINT "idOffre" PRIMARY KEY ("idOffre")

);
-- ddl-end --
ALTER TABLE public.offres OWNER TO postgres;
-- ddl-end --

-- object: emplois_fk | type: CONSTRAINT --
-- ALTER TABLE public.offres DROP CONSTRAINT IF EXISTS emplois_fk CASCADE;
ALTER TABLE public.offres ADD CONSTRAINT emplois_fk FOREIGN KEY ("idEmploi_emplois")
REFERENCES public.emplois ("idEmploi") MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


