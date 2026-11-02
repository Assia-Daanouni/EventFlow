from flask import Flask, flash, redirect, render_template, request, url_for

import database
import services

app = Flask(__name__)
app.secret_key = "eventflow-cle-de-test"   # nécessaire pour les messages flash


@app.route("/")
def index():
    return render_template("index.html", events=services.list_events())


@app.route("/events/new", methods=["GET", "POST"])
def new_event():
    if request.method == "POST":
        try:
            services.add_event(
                request.form["title"],
                request.form["location"],
                request.form["event_date"],
                request.form["capacity"],
                request.form["price"],
            )
            flash("Événement ajouté", "ok")
            return redirect(url_for("index"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("event_form.html", form=request.form)


@app.route("/events/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    try:
        services.delete_event(event_id)
        flash("Événement supprimé", "ok")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/events/<int:event_id>/reserve", methods=["GET", "POST"])
def reserve(event_id):
    event = services.get_event(event_id)
    if event is None:
        flash("Événement introuvable", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        try:
            total = services.add_reservation(
                event_id,
                request.form["full_name"],
                request.form["email"],
                request.form["places"],
            )
            flash(f"Réservation enregistrée. Montant à payer : {total:.2f} DH", "ok")
            return redirect(url_for("reservations"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("reserve.html", event=event, form=request.form)


@app.route("/reservations")
def reservations():
    return render_template("reservations.html", reservations=services.list_reservations())


@app.route("/reservations/<int:reservation_id>/cancel", methods=["POST"])
def cancel(reservation_id):
    try:
        services.cancel_reservation(reservation_id)
        flash("Réservation annulée, places libérées", "ok")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("reservations"))


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)