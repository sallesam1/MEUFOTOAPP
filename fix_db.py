from app import app, db, Watermark
app.app_context().push()
wms = Watermark.query.all()
for w in wms:
    w.position = 'diagonal'
db.session.commit()
print('BD: ' + str(len(wms)) + ' registro(s) atualizado(s) para diagonal')
