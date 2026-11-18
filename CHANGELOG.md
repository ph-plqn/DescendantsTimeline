# Historique public

## 1.0.0

Première version publique préparée à partir de la référence fonctionnelle DEP-01. Métadonnées publiques et documentation complétées. Code de calcul, rendu, zoom et navigation identique à DEP-01. Les identifiants internes de campagnes ne constituent pas des versions publiques. La publication distante reste à effectuer après levée des réserves du rapport PUB-01.

## 1.1.0

Ajout des règles BIRTH_BEFORE_PARTICIPATION_RULE et DEATH_AFTER_PARTICIPATION_RULE
Inference_parameters.py : création de liaisons entre les paramètres du greffon et les paramètres de configuration GRAMPS définis par l'Utilisateur (Préférences/Limites) :  MAX_LIFESPAN_YEARS = behavior.max-age-prob-alive, MIN_MARRIAGE_AGE_YEARS = behavior.min-generation-years. Merci à Gary Griffin 2026/11/11 19:06.

## 1.2.0

Ajout des règles BIRTH_BEFORE_CHILD_BIRTH_RULE et DEATH_AFTER_CHILD_BIRTH_RULE