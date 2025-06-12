import sqlalchemy
from sqlalchemy.orm import relationship

def create_admin_user_table(metadata):
    return sqlalchemy.Table(
        "admin_users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("email", sqlalchemy.String(255), unique=True),
        sqlalchemy.Column("password", sqlalchemy.String(255)),

        # relationship("Projects", back_populates="author"),
        # relationship("Blogs", back_populates="author")
    )