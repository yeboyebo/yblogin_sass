# @class_declaration interna_aqn_invitations #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_aqn_invitations(modelos.mtd_aqn_invitations, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_aqn_invitations #
class gesttare_aqn_invitations(interna_aqn_invitations, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration aqn_invitations #
class aqn_invitations(gesttare_aqn_invitations, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_invitations_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface

# # @class_declaration interna_aqn_invitations #
# import importlib

# from YBUTILS.viewREST import helpers

# from models.fllogin import models as modelos
# from YBLEGACY import baseraw


# class mtd_aqn_invitations(baseraw):
#     id = models.AutoField(db_column="id", verbose_name=FLUtil.translate(u"Identificador", u"MetaData"), primary_key=True, blank=False)._miextend(REQUIRED=True, visiblegrid=False, OLDTIPO="SERIAL")
#     email = models.CharField(max_length=254)._miextend(OLDTIPO="STRING")
#     hashcode = models.CharField(db_column="hashcode", verbose_name=FLUtil.translate(u"Hashcode", u"MetaData"), blank=True, null=True, max_length=200)._miextend(OLDTIPO="STRING")
#     idcompany = models.ForeignKey("mtd_aqn_companies", db_column="idcompany", verbose_name=FLUtil.translate(u"Compañia", u"MetaData"), blank=True, null=True, to_field="idcompany", on_delete=FLUtil.deleteCascade, related_name="aqn_invitations_idcompany__fk__aqn_companies_idcompany")._miextend(visiblegrid=False, OLDTIPO="UINT")
#     fecha = models.DateTimeField()._miextend(OLDTIPO="DATE")
#     activo = models.BooleanField()._miextend(OLDTIPO="BOOL")
#     # codproyecto = models.CharField(db_column="codproyecto", verbose_name=FLUtil.translate(u"Proyecto", u"MetaData"), blank=False, null=True, max_length=15)._miextend(REQUIRED=True, OLDTIPO="STRING")
#     codproyecto = models.ForeignKey("mtd_gt_proyectos", db_column="codproyecto", verbose_name=FLUtil.translate(u"Proyecto", u"MetaData"), blank=False, null=True, max_length=15, to_field="codproyecto", on_delete=FLUtil.deleteCascade, related_name="aqn_invitations_codproyecto__fk__gt_proyectos_codproyecto")._miextend(REQUIRED=True, OLDTIPO="STRING")
#     tipo = models.CharField(db_column="tipo", verbose_name=FLUtil.translate(u"Tipo", u"MetaData"), blank=True, null=True, max_length=50)._miextend(OLDTIPO="STRING")
#     caducidad = models.DateTimeField(blank=True, null=True)._miextend(OLDTIPO="DATE")

#     class Meta:
#         abstract = True


# class interna_aqn_user(mtd_aqn_invitations, helpers.MixinConAcciones):
#     pass

#     class Meta:
#         abstract = True

# # @class_declaration gesttare_aqn_invitations #
# class gesttare_aqn_invitations(interna_aqn_invitations, helpers.MixinConAcciones):
#     pass

#     class Meta:
#         proxy = True


# # @class_declaration aqn_invitations #
# class aqn_invitations(gesttare_aqn_invitations, helpers.MixinConAcciones):
#     pass

#     class Meta:
#         proxy = True

#     def getIface(self=None):
#         return form.iface


# definitions = importlib.import_module("models.fllogin.aqn_invitations_def")
# form = definitions.FormInternalObj()
# form._class_init()
# form.iface.ctx = form.iface
# form.iface.iface = form.iface
