from flask_sqlalchemy import SQLAlchemy
import pendulum
import re #módulo re de Python para validar si un correo electrónico tiene un formato válido antes de que sea almacenado en la base de datos.
from sqlalchemy.orm import validates
from api.extensions import db, bcrypt
from sqlalchemy.engine import reflection

# Clase personalizada para errores de validación (opcional)
class ValidationError(Exception):
    pass

# Expresión regular para validar un email
def validate_email(email): 
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Acepta correos con cualquier dominio
    if not re.match(email_regex, email):
        raise ValidationError('Correo electrónico no válido.')


db = SQLAlchemy()

def lazy_utc_now():
    return pendulum.now("UTC")  # Función para manejar la fecha y hora en UTC
 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), unique=False, nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='role_enum'), default='user', nullable=False)
    status = db.Column(db.Enum('activo', 'en_revision', name='role_status'), default='en_revision', nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lazy_utc_now) 
    updated_at = db.Column(db.DateTime(timezone=True), default=lazy_utc_now, onupdate=lazy_utc_now)


  # Validación del correo electrónico antes de guardarlo
    @validates('email')
    def validate_email_field(self, key, email):
        validate_email(email)
        return email
    
    @staticmethod
    def create_default_admin():
        """Crea un administrador por defecto si no existe"""
        inspector = reflection.Inspector.from_engine(db.engine)
        if 'users' in inspector.get_table_names():
            admin_email = "admin@anda.com.uy"
            admin_password = "admin123"

            # Verificar si el administrador ya existe
            existing_admin = User.query.filter_by(email=admin_email).first()
            if not existing_admin:
                # Crear el administrador
                admin = User(
                    user_name="admin",
                    email=admin_email,
                    password_hash=bcrypt.generate_password_hash(admin_password).decode('utf-8'),
                    role="admin",
                    status="activo"
                )
                db.session.add(admin)
                db.session.commit()
                print(f"Administrador creado: {admin_email} / {admin_password}")
            else:
                print("El administrador ya existe en la base de datos.")
        else:
            print("La tabla 'users' no existe. Corre las migraciones primero.")

    # relacion con Reservations uno a muchos un usuario puede tener varias reservas
    reservations = db.relationship('Reservations', back_populates='user')

    #relacion con books_reservations uno a muchos Un usuario puede reservar múltiples libros.
    books_reservations = db.relationship('Books_reservations', back_populates='user')
    

    def __repr__(self):
        return f'<User {self.user_name}>'

    def serialize(self):
        return {
        "id": self.id,
        "username": self.user_name,
        "email": self.email,
        "role": self.role,
        "status": self.status,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }


class UserProfiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    identification = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    department = db.Column(db.String(50), nullable=True)
    sector = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lazy_utc_now)
    updated_at = db.Column(db.DateTime, default=lazy_utc_now, onupdate=lazy_utc_now)

    # establece una relación uno a uno entre el modelo User y UserProfiles (uselist=false indica que un perfil esta asociado a un solo usuario, relacion uno a uno)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))


    # Validación del correo electrónico en UserProfiles
    @validates('email')
    def validate_userprofile_email(self,key, email):
        validate_email(email)
        return email
    
    def __repr__(self):
        return f'<UserProfiles {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "identification": self.identification,
            "address": self.address,
            "phone_number": self.phone_number,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "department": self.department,
            "sector": self.sector,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lazy_utc_now)
    updated_at = db.Column(db.DateTime(timezone=True), default=lazy_utc_now, onupdate=lazy_utc_now)

    #Relacion inversa con User
    user = db.relationship('User', back_populates = 'reservations')

    def __repr__(self):
        return f'<Reservations {self.event_name}>'
    
    def serialize(self): #serialice
        return {
            "id": self.id, 
            "event_name": self.event_name,
            "user_id": self.user_id, 
            "user_email": self.user.email if self.user else None,
            "start_time": self.start_time, 
            "end_time": self.end_time, 
            "created_at": self.created_at.isoformat() if self.created_at else None, 
            "updated_at": self.updated_at.isoformat() if self.updated_at else None, 
        }



class Books(db.Model): 
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255), nullable=False)
    author= db.Column(db.String(255), nullable=False)
    book_gender = db.Column(db.Enum(
        'Novela', 'Cuento', 'Fantasía', 'Ciencia_Ficción', 'Romántico', 'Aventura', 
        'Histórico', 'Biografía', 'Documental', 'Poesía', 'Teatro', 'Terror', 
        name='book_gender_enum'), nullable=False)
    summary = db.Column(db.Text)
    # Campo availability como Boolean (True: Disponible, False: No disponible)
    availability= db.Column(db.Boolean, default=True, nullable=False)
    created_at= db.Column(db.DateTime(timezone=True), default=lazy_utc_now)
    updated_at= db.Column(db.DateTime(timezone=True), default=lazy_utc_now, onupdate=lazy_utc_now)
    
    #relacion Books con Books_reservations uno a muchos.  Un libro puede ser reservado muchas veces
    books_reservations = db.relationship('Books_reservations', back_populates='book')
 

    # Método de representación del objeto para facilitar la depuración
    def __repr__(self): 
        return f'<Books {self.title} by {self.author}'

    # Método para serializar convierte el objeto Books en un diccionario que se puede convertir a JSON
    def serialize(self): 
        return {
            "id": self.id, 
            "title": self.title, 
            "author": self.author, 
            "book_gender": self.book_gender,
            "summary": self.summary, 
            "availability": self.availability, 
            "created_at": self.created_at.isoformat() if self.created_at else None, 
            "updated_at": self.updated_at.isoformat() if self.updated_at else None

        }



class Books_reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    reserved_at = db.Column(db.DateTime(timezone=True), default=lazy_utc_now)
    returned_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    #relacion inversa con User. Cada reserva esta asociada a un unico usuario
    user = db.relationship('User', back_populates = 'books_reservations')
    #relacion inversa con books. Cada reserva esta asociada a un unico libro. 
    book = db.relationship('Books', back_populates='books_reservations')
    

    def __repr__(self):
        return f'<Books_reservations {self.book_id}>'

    def serialize(self): 
        return {
            "id": self.id,
            "book_id": self.book_id, 
            "user_id": self.user_id, 
            "reserved_at": self.reserved_at.isoformat() if self.reserved_at else None,
            "returned_at": self.returned_at.isoformat() if self.returned_at else None, 
        }
