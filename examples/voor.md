## Verbindingsproblemen oplossen

Indien de applicatie blijft hangen of faalt met de foutmelding `dial tcp: i/o timeout`, dient u allereerst te controleren of de host waarop de applicatie draait de Postgres-poort (doorgaans 5432) daadwerkelijk kan bereiken — dit wordt in de praktijk veelal veroorzaakt door een firewallregel of een security group die de betreffende verbinding blokkeert. Bij het gebruikmaken van een beheerde database (zoals RDS, Cloud SQL, etc.) verdient het bovendien aanbeveling te verifiëren dat de instantie verbindingen vanaf het IP-adres van de applicatie toestaat.

Het is belangrijk om te vermelden dat de configuratie van de verbinding op meerdere plaatsen kan worden vastgelegd. Het wijzigen van de instellingen dient derhalve zorgvuldig te geschieden, aangezien een onjuiste waarde ertoe zou kunnen leiden dat de applicatie in het geheel geen verbinding meer kan maken.

## Incidentmelding

Wij hebben geconstateerd dat er mogelijk sprake is geweest van een verstoring die impact kan hebben gehad op het vermogen van een deel van onze gebruikers om toegang te verkrijgen tot de dienstverlening. Uiteraard wordt er momenteel door ons team met de hoogste prioriteit aan een structurele oplossing gewerkt en wij verontschuldigen ons voor het eventuele ongemak dat dit met zich mee heeft kunnen brengen.

## Releasenotitie

In deze release is er een aantal verbeteringen doorgevoerd welke de algehele performance van het systeem naar een hoger niveau tillen. Zo is onder andere de caching-laag volledig herzien, hetgeen ertoe leidt dat pagina's aanzienlijk sneller geladen worden. Tevens is de robuuste nieuwe zoekfunctionaliteit beschikbaar gekomen, die het voor gebruikers eenvoudigweg mogelijk maakt om naadloos door de catalogus te navigeren.
