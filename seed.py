import database
import services
database.init_db()
services.add_event("Conférence IA 2026", "ENSA Fès", "2026-12-05", 100, 50)
services.add_event("Atelier Git et GitHub", "Salle B12", "2026-12-12", 30, 0)
services.add_event("Soirée de gala", "Hôtel de Fès", "2027-01-20", 50, 200)
services.add_reservation(1, "Sara Alaoui", "sara.alaoui@exemple.com", 2)
print("Données de démonstration ajoutées")
