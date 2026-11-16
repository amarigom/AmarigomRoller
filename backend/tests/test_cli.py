from models import User


def test_create_admin_cli(app):
    runner = app.test_cli_runner()
    r = runner.invoke(args=["create-admin", "--email", "Root@Example.com", "--nombre", "Root"],
                      input="clave-muy-larga-123\nclave-muy-larga-123\n")
    assert r.exit_code == 0, r.output
    u = User.query.filter_by(email="root@example.com").first()
    assert u.rol == "admin"


def test_create_admin_cli_rechaza_clave_corta(app):
    runner = app.test_cli_runner()
    r = runner.invoke(args=["create-admin", "--email", "a@example.com", "--nombre", "A"], input="corta\ncorta\n")
    assert r.exit_code != 0
    assert User.query.count() == 0
