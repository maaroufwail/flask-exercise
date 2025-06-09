# schemas.py

from marshmallow import fields, validate, post_load
from flask_marshmallow import Marshmallow
from models import (
    Artist,
    Album,
    Track,
    Genre,
    MediaType,
    # Customer,
    # Invoice,
    # InvoiceItem,
    # Playlist,
    # PlaylistTrack,
    # Employee
)
from app import ma, db

# ---------------------------------------------------------
# 1. Schema per Artist
# ---------------------------------------------------------
class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        load_instance = True         # se si vuole ottenere un'istanza SQLAlchemy
        sqla_session = db.session    # sessione per eventuale post_load
        include_relationships = True  # includi relazioni (se definite)
        load_only = ("albums",)       # in input possiamo ignorare albums
        dump_only = ("ArtistId",)     # l'ID lo restituiamo solo in output

    # Se vuoi validare la lunghezza del nome
    Name = fields.String(required=True, validate=validate.Length(max=200))


# ---------------------------------------------------------
# 2. Schema per Album
# ---------------------------------------------------------
class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album
        load_instance = True
        sqla_session = db.session
        include_fk = True            # include le chiavi esterne (ArtistId)
        include_relationships = True  # se vuoi includere l'oggetto "artist" annidato
    
    # Di solito l'album ha:
    # AlbumId (dump only),
    # Title (obbligatorio),
    # ArtistId (obbligatorio, FK verso Artist)
    AlbumId = fields.Int(dump_only=True)
    Title = fields.String(required=True, validate=validate.Length(max=160))
    ArtistId = fields.Int(required=True)

    # Se vuoi nidificare i dati dell'artista quando fai dump:
    artist = fields.Nested(ArtistSchema, dump_only=True)


# ---------------------------------------------------------
# 3. Schema per Genre
# ---------------------------------------------------------
class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        sqla_session = db.session

    GenreId = fields.Int(dump_only=True)
    Name = fields.String(required=True, validate=validate.Length(max=120))


# ---------------------------------------------------------
# 4. Schema per MediaType
# ---------------------------------------------------------
class MediaTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MediaType
        load_instance = True
        sqla_session = db.session

    MediaTypeId = fields.Int(dump_only=True)
    Name = fields.String(required=True, validate=validate.Length(max=120))


# ---------------------------------------------------------
# 5. Schema per Track
# ---------------------------------------------------------
class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track
        load_instance = True
        sqla_session = db.session
        include_fk = True            # includi AlbumId, GenreId, MediaTypeId
        include_relationships = True  # includi oggetti nidificati se definiti

    TrackId    = fields.Int(dump_only=True)
    Name       = fields.String(required=True, validate=validate.Length(max=200))
    AlbumId    = fields.Int(required=False, allow_none=True)
    MediaTypeId= fields.Int(required=True)
    GenreId    = fields.Int(required=False, allow_none=True)
    Composer   = fields.String(validate=validate.Length(max=220), allow_none=True)
    Milliseconds = fields.Int(required=True)
    Bytes      = fields.Int(required=False, allow_none=True)
    UnitPrice  = fields.Decimal(as_string=True, required=True)

    # Se voglio nidificare l'album, il genere e il media type nel dump:
    album      = fields.Nested(AlbumSchema, dump_only=True)
    genre      = fields.Nested(GenreSchema, dump_only=True)
    media_type = fields.Nested(MediaTypeSchema, dump_only=True)


# # ---------------------------------------------------------
# # 6. Schema per Customer
# # ---------------------------------------------------------
# class CustomerSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Customer
#         load_instance = True
#         sqla_session = db.session
#         include_relationships = False  # di default non includo relazioni complesse

#     CustomerId   = fields.Int(dump_only=True)
#     FirstName    = fields.String(required=True, validate=validate.Length(max=40))
#     LastName     = fields.String(required=True, validate=validate.Length(max=20))
#     Company      = fields.String(validate=validate.Length(max=80), allow_none=True)
#     Address      = fields.String(validate=validate.Length(max=70), allow_none=True)
#     City         = fields.String(validate=validate.Length(max=40), allow_none=True)
#     State        = fields.String(validate=validate.Length(max=40), allow_none=True)
#     Country      = fields.String(validate=validate.Length(max=40), allow_none=True)
#     PostalCode   = fields.String(validate=validate.Length(max=10), allow_none=True)
#     Phone        = fields.String(validate=validate.Length(max=24), allow_none=True)
#     Email        = fields.Email(required=True, validate=validate.Length(max=60))

#     # campi load_only/dump_only per gestire, ad es., la password:
#     PasswordHash = fields.String(load_only=True) 
#     # (non includo la password in dump; se voglio salvarla, gestirò il campo Hash dal backend)


# # ---------------------------------------------------------
# # 7. Schema per InvoiceItem (riga di fattura)
# # ---------------------------------------------------------
# class InvoiceItemSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = InvoiceItem
#         load_instance = True
#         sqla_session = db.session
#         include_fk = True

#     InvoiceLineId = fields.Int(dump_only=True)
#     InvoiceId     = fields.Int(required=True)
#     TrackId       = fields.Int(required=True)
#     UnitPrice     = fields.Decimal(as_string=True, required=True)
#     Quantity      = fields.Int(required=True)

#     # Se voglio nidificare i dettagli della traccia nella riga fattura (dump_only)
#     track = fields.Nested(TrackSchema, dump_only=True)


# # ---------------------------------------------------------
# # 8. Schema per Invoice (fattura)
# # ---------------------------------------------------------
# class InvoiceSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Invoice
#         load_instance = True
#         sqla_session = db.session
#         include_fk = True
#         include_relationships = True

#     InvoiceId     = fields.Int(dump_only=True)
#     CustomerId    = fields.Int(required=True)
#     InvoiceDate   = fields.DateTime(dump_only=True)
#     BillingAddress    = fields.String(validate=validate.Length(max=70), allow_none=True)
#     BillingCity       = fields.String(validate=validate.Length(max=40), allow_none=True)
#     BillingState      = fields.String(validate=validate.Length(max=40), allow_none=True)
#     BillingCountry    = fields.String(validate=validate.Length(max=40), allow_none=True)
#     BillingPostalCode = fields.String(validate=validate.Length(max=10), allow_none=True)
#     Total         = fields.Decimal(as_string=True, dump_only=True)

#     # Nidifico le righe di fattura (InvoiceItems) in un array
#     invoice_items = fields.List(fields.Nested(InvoiceItemSchema), dump_only=True)

#     # Per deserializzare (caricare) le righe di fattura passate in POST:
#     InvoiceItems = fields.List(fields.Nested(InvoiceItemSchema), load_only=True)

#     @post_load
#     def make_invoice(self, data, **kwargs):
#         """
#         Facciamo in modo che, quando chiedo di 'load' un JSON in un oggetto Invoice,
#         gli InvoiceItems passati in input diventino vere istanze SQLAlchemy.
#         In genere, però, preferisco gestire manualmente la creazione nel mio modulo
#         routes/invoices.py, ma questo è un esempio di come farlo via post_load.
#         """
#         items_data = data.pop("InvoiceItems", [])
#         invoice = Invoice(**data)
#         for item_data in items_data:
#             invoice.invoice_items.append(InvoiceItem(**item_data))
#         return invoice


# # ---------------------------------------------------------
# # 9. Schema per PlaylistTrack (tabella di join)
# # ---------------------------------------------------------
# class PlaylistTrackSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = PlaylistTrack
#         load_instance = True
#         sqla_session = db.session
#         include_fk = True

#     PlaylistId = fields.Int(required=True)
#     TrackId    = fields.Int(required=True)


# # ---------------------------------------------------------
# # 10. Schema per Playlist
# # ---------------------------------------------------------
# class PlaylistSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Playlist
#         load_instance = True
#         sqla_session = db.session
#         include_fk = True
#         include_relationships = True

#     PlaylistId  = fields.Int(dump_only=True)
#     Name        = fields.String(required=True, validate=validate.Length(max=120))
#     CustomerId  = fields.Int(required=True)

#     # Nidifico i brani all'interno della playlist (dump_only)
#     tracks = fields.List(fields.Nested(TrackSchema), dump_only=True)

#     # Se arriva un body JSON con { TrackId: X }, potrei caricarlo tramite PlaylistTrackSchema
#     @post_load
#     def make_playlist(self, data, **kwargs):
#         """
#         Es. se in POST invio { Name: 'My Playlist', CustomerId: 5 },
#         restituisco già un'istanza Playlist pronta per inserimento in DB.
#         Eventuale aggiunta di tracce di solito gestita in un endpoint separato.
#         """
#         return Playlist(**data)


# # ---------------------------------------------------------
# # 11. Schema per Employee (dipendente)
# # ---------------------------------------------------------
# class EmployeeSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Employee
#         load_instance = True
#         sqla_session = db.session
#         include_relationships = False

#     EmployeeId = fields.Int(dump_only=True)
#     LastName   = fields.String(required=True, validate=validate.Length(max=20))
#     FirstName  = fields.String(required=True, validate=validate.Length(max=20))
#     Title      = fields.String(validate=validate.Length(max=30), allow_none=True)
#     ReportsTo  = fields.Int(allow_none=True)
#     BirthDate  = fields.Date(allow_none=True)
#     HireDate   = fields.Date(allow_none=True)
#     Address    = fields.String(validate=validate.Length(max=70), allow_none=True)
#     City       = fields.String(validate=validate.Length(max=40), allow_none=True)
#     State      = fields.String(validate=validate.Length(max=40), allow_none=True)
#     Country    = fields.String(validate=validate.Length(max=40), allow_none=True)
#     PostalCode = fields.String(validate=validate.Length(max=10), allow_none=True)
#     Phone      = fields.String(validate=validate.Length(max=24), allow_none=True)
#     Email      = fields.Email(validate=validate.Length(max=60), allow_none=True)
#     # Se hai un campo PasswordHash, inseriscilo con load_only=True
#     PasswordHash = fields.String(load_only=True)
