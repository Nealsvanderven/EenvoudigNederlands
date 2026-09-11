## Verbinding verloopt

Bereikt de applicatie de Postgres-poort niet, dan stopt zij met `dial tcp: i/o timeout`. Die poort is standaard 5432.

1. Controleer of de host van de applicatie de Postgres-poort bereikt. Meestal blokkeert een firewall of een security group de verbinding.
2. Gebruik je een beheerde database (RDS, Cloud SQL)? Controleer dan of die verbindingen vanaf het IP-adres van de applicatie toestaat.

Je kunt de instellingen voor de verbinding op meerdere plaatsen vastleggen. Een verkeerde waarde blokkeert alle verbindingen.

## Incidentmelding

Tussen 14.02 en 14.31 uur mislukte 12 procent van de aanvragen. De oorzaak is nog onbekend. Wij onderzoeken het en melden de uitkomst vandaag.

## Releasenotitie

- De cachelaag is herbouwd. Pagina's laden nu sneller.
- De zoekfunctie is nieuw. Je zoekt nu door de hele catalogus.
