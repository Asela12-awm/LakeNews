import os
import sqlite3
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from werkzeug.utils import secure_filename
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

# Secret key
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "newswave-secret-key-change-this"
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE = os.path.join(
    BASE_DIR,
    "news.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
    "gif"
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_IMAGE_SIZE


# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    db = get_db()

    # -----------------------------------------------------
    # ADMIN TABLE
    # -----------------------------------------------------

    db.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # -----------------------------------------------------
    # NEWS TABLE
    # -----------------------------------------------------

    db.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------------------------------
    # ADMIN LOGIN
    #
    # Username: Maduz
    # Password: Maduz123
    # -----------------------------------------------------

    # Remove old admin accounts
    db.execute(
        """
        DELETE FROM admins
        WHERE username != ?
        """,
        ("Maduz",)
    )

    # Check Maduz account
    admin = db.execute(
        """
        SELECT id
        FROM admins
        WHERE username = ?
        """,
        ("Maduz",)
    ).fetchone()

    # Create password hash
    password_hash = generate_password_hash(
        "Maduz123"
    )

    if admin is None:

        # Create new admin
        db.execute(
            """
            INSERT INTO admins
            (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (
                "Maduz",
                password_hash
            )
        )

    else:

        # Update password
        db.execute(
            """
            UPDATE admins
            SET password = ?
            WHERE username = ?
            """,
            (
                password_hash,
                "Maduz"
            )
        )

    db.commit()

    db.close()


# =========================================================
# ADMIN LOGIN REQUIRED
# =========================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "admin_id" not in session:

            flash(
                "Please login as administrator.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        return function(
            *args,
            **kwargs
        )

    return decorated_function


# =========================================================
# FILE VALIDATION
# =========================================================

def allowed_file(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =========================================================
# SAVE UPLOADED IMAGE
# =========================================================

def save_uploaded_image(file):

    if not file:
        return None

    if not file.filename:
        return None

    if not allowed_file(
        file.filename
    ):
        return None

    filename = secure_filename(
        file.filename
    )

    if not filename:
        return None

    base, extension = os.path.splitext(
        filename
    )

    counter = 1

    final_filename = filename

    while os.path.exists(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            final_filename
        )
    ):

        final_filename = (
            f"{base}_{counter}{extension}"
        )

        counter += 1

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        final_filename
    )

    file.save(filepath)

    return final_filename


# =========================================================
# DELETE IMAGE
# =========================================================

def delete_image(filename):

    if not filename:
        return

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(filepath):

        try:
            os.remove(filepath)

        except OSError:
            pass


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    db = get_db()

    news = db.execute(
        """
        SELECT *
        FROM news
        ORDER BY id DESC
        """
    ).fetchall()

    db.close()

    # Convert sqlite rows to dictionaries
    news_list = [
        dict(item)
        for item in news
    ]

    return render_template(
        "index.html",
        news=news_list
    )


# =========================================================
# NEWS API
# =========================================================

@app.route("/api/news")
def api_news():

    db = get_db()

    news = db.execute(
        """
        SELECT *
        FROM news
        ORDER BY id DESC
        """
    ).fetchall()

    db.close()

    news_list = []

    for item in news:

        news_list.append({

            "id": item["id"],

            "title": item["title"],

            "category": item["category"],

            "description": item["description"],

            "content": item["content"],

            "image": (
                url_for(
                    "static",
                    filename=(
                        f"uploads/{item['image']}"
                    )
                )
                if item["image"]
                else ""
            ),

            "author": item["author"],

            "created_at": item["created_at"]
        })

    return jsonify(
        news_list
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def login():

    # Already logged in
    if "admin_id" in session:

        return redirect(
            url_for("dashboard")
        )

    # Login form submitted
    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # Empty fields
        if not username or not password:

            flash(
                "Please enter username and password.",
                "error"
            )

            return render_template(
                "login.html"
            )

        db = get_db()

        admin = db.execute(
            """
            SELECT *
            FROM admins
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        db.close()

        # Check login
        if admin and check_password_hash(
            admin["password"],
            password
        ):

            session.clear()

            session["admin_id"] = admin["id"]

            session["admin_username"] = (
                admin["username"]
            )

            flash(
                "Login successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        else:

            flash(
                "Invalid username or password.",
                "error"
            )

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/admin/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
@admin_required
def dashboard():

    db = get_db()

    news = db.execute(
        """
        SELECT *
        FROM news
        ORDER BY id DESC
        """
    ).fetchall()

    db.close()

    return render_template(
        "dashboard.html",
        news=news
    )


# =========================================================
# ADD NEWS
# =========================================================

@app.route(
    "/admin/news/add",
    methods=["GET", "POST"]
)
@admin_required
def add_news():

    if request.method == "POST":

        # Get form data
        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        author = request.form.get(
            "author",
            "NewsWave Team"
        ).strip()

        image_file = request.files.get(
            "image"
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not title:

            flash(
                "Title is required.",
                "error"
            )

            return redirect(
                url_for("add_news")
            )

        if not category:

            flash(
                "Category is required.",
                "error"
            )

            return redirect(
                url_for("add_news")
            )

        if not description:

            flash(
                "Description is required.",
                "error"
            )

            return redirect(
                url_for("add_news")
            )

        if not content:

            flash(
                "Content is required.",
                "error"
            )

            return redirect(
                url_for("add_news")
            )

        # -------------------------------------------------
        # IMAGE
        # -------------------------------------------------

        image_filename = None

        if image_file and image_file.filename:

            if not allowed_file(
                image_file.filename
            ):

                flash(
                    "Invalid image format. Use PNG, JPG, JPEG, WEBP or GIF.",
                    "error"
                )

                return redirect(
                    url_for("add_news")
                )

            image_filename = (
                save_uploaded_image(
                    image_file
                )
            )

        # -------------------------------------------------
        # DATABASE INSERT
        # -------------------------------------------------

        db = get_db()

        db.execute(
            """
            INSERT INTO news
            (
                title,
                category,
                description,
                content,
                image,
                author
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                category,
                description,
                content,
                image_filename,
                author
            )
        )

        db.commit()

        db.close()

        flash(
            "News published successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "edit_news.html",
        news=None
    )


# =========================================================
# EDIT NEWS
# =========================================================

@app.route(
    "/admin/news/edit/<int:news_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_news(news_id):

    db = get_db()

    news = db.execute(
        """
        SELECT *
        FROM news
        WHERE id = ?
        """,
        (news_id,)
    ).fetchone()

    # News not found
    if news is None:

        db.close()

        flash(
            "News article not found.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        author = request.form.get(
            "author",
            "NewsWave Team"
        ).strip()

        image_file = request.files.get(
            "image"
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not title:

            db.close()

            flash(
                "Title is required.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_news",
                    news_id=news_id
                )
            )

        if not category:

            db.close()

            flash(
                "Category is required.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_news",
                    news_id=news_id
                )
            )

        if not description:

            db.close()

            flash(
                "Description is required.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_news",
                    news_id=news_id
                )
            )

        if not content:

            db.close()

            flash(
                "Content is required.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_news",
                    news_id=news_id
                )
            )

        # -------------------------------------------------
        # OLD IMAGE
        # -------------------------------------------------

        new_image = news["image"]

        # -------------------------------------------------
        # NEW IMAGE
        # -------------------------------------------------

        if image_file and image_file.filename:

            if not allowed_file(
                image_file.filename
            ):

                db.close()

                flash(
                    "Invalid image format.",
                    "error"
                )

                return redirect(
                    url_for(
                        "edit_news",
                        news_id=news_id
                    )
                )

            uploaded_filename = (
                save_uploaded_image(
                    image_file
                )
            )

            if uploaded_filename:

                # Delete old image
                delete_image(
                    news["image"]
                )

                new_image = (
                    uploaded_filename
                )

        # -------------------------------------------------
        # UPDATE DATABASE
        # -------------------------------------------------

        db.execute(
            """
            UPDATE news
            SET
                title = ?,
                category = ?,
                description = ?,
                content = ?,
                image = ?,
                author = ?
            WHERE id = ?
            """,
            (
                title,
                category,
                description,
                content,
                new_image,
                author,
                news_id
            )
        )

        db.commit()

        db.close()

        flash(
            "News updated successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    db.close()

    return render_template(
        "edit_news.html",
        news=news
    )


# =========================================================
# DELETE NEWS
# =========================================================

@app.route(
    "/admin/news/delete/<int:news_id>",
    methods=["POST"]
)
@admin_required
def delete_news(news_id):

    db = get_db()

    news = db.execute(
        """
        SELECT *
        FROM news
        WHERE id = ?
        """,
        (news_id,)
    ).fetchone()

    if news:

        # Delete image
        delete_image(
            news["image"]
        )

        # Delete database record
        db.execute(
            """
            DELETE FROM news
            WHERE id = ?
            """,
            (news_id,)
        )

        db.commit()

        flash(
            "News deleted successfully.",
            "success"
        )

    else:

        flash(
            "News article not found.",
            "error"
        )

    db.close()

    return redirect(
        url_for("dashboard")
    )


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    flash(
        "Image is too large. Maximum size is 5 MB.",
        "error"
    )

    return redirect(
        url_for("add_news")
    )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    # Initialize database
    init_db()

    print("")
    print("========================================")
    print("          NEWSWAVE SERVER")
    print("========================================")
    print("")
    print("Website:")
    print("http://127.0.0.1:5000")
    print("")
    print("Admin Login:")
    print("http://127.0.0.1:5000/admin/login")
    print("")
    print("Username : Maduz")
    print("Password : Maduz123")
    print("")
    print("========================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )