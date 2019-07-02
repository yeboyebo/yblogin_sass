# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration yblogin_sass #
from YBLEGACY.constantes import *


class yblogin_sass(interna):

    def yblogin_getDesc(self):
        return None

    def yblogin_sass_nueva_invitacion(self, oParam):
        response = {}
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', oParam["email"].lower()):
            print("Correo incorrecto")
            response["status"] = 1
            response["msg"] = "Formato correo intorrecto"
            return response
        # Comprobamos que no existe usuario con ese email para esa compañia
        usuario = qsatype.FLUtil.nameUser()
        if usuario != "admin":
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
        else:
            idcompany = 1
        codifica = oParam["email"] + str(idcompany)
        hashcode = hashlib.md5(codifica.encode('utf-8')).hexdigest()
        cursor = qsatype.FLSqlCursor(u"aqn_invitations")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"email", oParam["email"])
        cursor.setValueBuffer(u"hashcode", hashcode)
        cursor.setValueBuffer(u"idcompany", idcompany)
        cursor.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
        cursor.setValueBuffer(u"activo", True)
        cursor.setValueBuffer(u"tipo", "ni")
        if not cursor.commitBuffer():
            return False
        # enviomailinvitacion
        _i = self.iface
        if not _i.envioMailInvitacion(cursor.valueBuffer("email"), cursor.valueBuffer("hashcode")):
            return False
        response["resul"] = True
        response["msg"] = "Invitacion enviada con éxito"
        return response

    def yblogin_sass_envioMailInvitacion(self, email, hashcode):
        usuario = qsatype.FLUtil.nameUser()
        if usuario != "admin":
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            nombreCompania = qsatype.FLUtil.sqlSelect(u"aqn_companies", u"nombre", ustr(u"idcompany = '", str(idcompany), u"'"))
        else:
            nombreCompania = ""
        urlJoin = "https://demo.dailyjob.io/join/" + hashcode
        # urlJoin = "http://127.0.0.1:8000/join/" + hashcode
        # cuerpo = "<img src='https://app.dailyjob.io/static/dist/img/logo/logo.png'/>"
        # cuerpo += "<br><a href='" + urlJoin + "''>Unirse DailyJob</a>"
        # cuerpo += "<br>"

        cuerpo = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" style="" class=" js flexbox flexboxlegacy canvas canvastext webgl no-touch geolocation postmessage websqldatabase indexeddb hashchange history draganddrop websockets rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface generatedcontent video audio localstorage sessionstorage webworkers no-applicationcache svg inlinesvg smil svgclippaths js csstransforms csstransforms3d csstransitions responsejs "><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Invitación Dailyjob</title><!-- Designed by https://github.com/kaytcat --><!-- Header image designed by Freepik.com --><style type="text/css">/* Take care of image borders and formatting */img { max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img { border: none; }table { border-collapse: collapse !important; }#outlook a { padding:0; }.ReadMsgBody { width: 100%; }.ExternalClass {width:100%;}.backgroundTable {margin:0 auto; padding:0; width:100% !important;}table td {border-collapse: collapse;}.ExternalClass * {line-height: 115%;}/* General styling */td {    font-family: Arial, sans-serif;}body {    -webkit-font-smoothing:antialiased;    -webkit-text-size-adjust:none;    width: 100%;    height: 100%;    color: #6f6f6f;    font-weight: 400;    font-size: 18px;}h1 {    margin: 10px 0;}a {    color: #27aa90;    text-decoration: none;}.force-full-width {    width: 100% !important;}.body-padding {    padding: 0 75px;}</style><style type="text/css" media="screen">        @media screen {            @import url(https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);            /* Thanks Outlook 2013! */            body {                font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;            }            .w280 {                width: 280px !important;            }        }</style><style type="text/css" media="only screen and (max-width: 480px)">    /* Mobile styles */    @media only screen and (max-width: 480px) {        table[class*="w320"] {            width: 320px !important;        }        td[class*="w320"] {            width: 280px !important;            padding-left: 20px !important;            padding-right: 20px !important;        }        img[class*="w320"] {            width: 250px !important;            height: 67px !important;        }        td[class*="mobile-spacing"] {            padding-top: 10px !important;            padding-bottom: 10px !important;        }        *[class*="mobile-hide"] {            display: none !important;        }        *[class*="mobile-br"] {            font-size: 12px !important;        }        td[class*="mobile-w20"] {            width: 20px !important;        }        img[class*="mobile-w20"] {            width: 20px !important;        }        td[class*="mobile-center"] {            text-align: center !important;        }        table[class*="w100p"] {            width: 100% !important;        }        td[class*="activate-now"] {            padding-right: 0 !important;            padding-top: 20px !important;        }        [class="mobile-block"] {            width: 100% !important;            display: block !important;        }    }</style>                                  </head><body offset="0" class="body ui-sortable" style="padding: 0px; margin: 0px; display: block; background: rgb(238, 235, 235); text-size-adjust: none; -webkit-font-smoothing: antialiased; width: 100%; height: 100%; color: rgb(111, 111, 111); font-weight: 400; font-size: 18px; cursor: auto; overflow: visible;" bgcolor="#eeebeb"><div data-section-wrapper="=" 1""="" align="center" valign="top" style="font-family: Arial, sans-serif;border-collapse: collapse;">    <center>        <table data-section="1" style="margin: 0px auto; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" cellspacing="0" cellpadding="0" width="600" class="w320" bgcolor="#ffffff">            <tbody><tr>                <td data-slot-container="1" style="text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                    <div data-slot="image" data-param-padding-top="50" data-param-padding-bottom="50" style="padding-top: 50px; padding-bottom: 25px;">                        <a href="http://dailyjob.io" target="_blank" rel="noopener noreferrer"><img class="w320 fr-view" width="311" height="83" src="http://dailyjob.io/img-mailing/color-horizontal.png" alt="company logo" style="max-width: 600px; outline: none; text-decoration: none; border: none; width: 394px; height: 96px;" /><br /></a>                    </div>                </td>            </tr>        </tbody></table>    </center></div><div data-section-wrapper="=" 1""="">    <center>        <table data-section="1" cellspacing="0" cellpadding="0" width="600" class="w320" style="background-color: rgb(255, 255, 255); border-collapse: collapse !important;" bgcolor="#ffffff">            <tbody><tr>                <td style="font-family: Arial, sans-serif;border-collapse: collapse;">                    <table cellspacing="0" cellpadding="0" width="100%" style="border-collapse: collapse !important;">                        <tbody><tr>                            <td data-slot-container="1" style="font-size: 18px;font-weight: 600;color: #ffffff;text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="mobile-spacing ui-sortable">                            <div data-slot="text" data-param-padding-top="" style="padding-top: 0px; padding-bottom: 20px;" data-param-padding-bottom=""><div style="padding: 20px 10%;"><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">¡Hola! </span></span></div><div style="text-align: justify;"><br /></div><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;"><strong><span style="color: #2d95c1;">' + nombreCompania + '</span></strong> te ha ha enviado una invitación para unirte a <strong><span style="color: #2d95c1;">dailyjob</span></strong>, una plataforma que tiene como principal objetivo facilitar tu actividad diaria a través del método <strong><span style="color: #2d95c1;">Productive Moments</span></strong>.</span> </span></div><div style="text-align: justify;"><br /></div><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">Para crear y configurar tu cuenta de usuario, haz clic en el siguiente enlace:</span></span></div></div><div style="padding: 20px 10%;"><span style="font-size: 18px;"><span style="color: #2d95c1;"><a href="' + urlJoin + '">' + urlJoin + '</a></span></span></div></div></td>                        </tr>                        <tr>                            <td data-slot-container="1" style="font-size: 24px;text-align: center;padding: 0 75px;color: #6f6f6f;font-family: Arial, sans-serif;border-collapse: collapse;" class="w320 mobile-spacing ui-sortable">                            </td>                        </tr>                    </tbody></table>                    <table cellspacing="0" cellpadding="0" width="100%" style="border-collapse: collapse !important;">                        <tbody><tr>                            <td data-slot-container="1" style="font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            </td>                        </tr>                    </tbody></table>                </td>            </tr>        </tbody></table>    </center></div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0px auto; width: 600px; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" class="w320" cellpadding="0" cellspacing="0" width="600" bgcolor="#ffffff">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column" bgcolor="#ffffff" style="background-color: rgb(255, 255, 255);">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0px auto; width: 600px; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" class="w320" cellpadding="0" cellspacing="0" width="600" bgcolor="#ffffff">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0 auto;border-collapse: collapse !important;width: 600px;" class="w320" cellpadding="0" cellspacing="0" width="600">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0 auto;border-collapse: collapse !important;width: 600px;" class="w320" cellpadding="0" cellspacing="0" width="600">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="=" 1""="">    <center>        <table data-section="1" cellspacing="0" cellpadding="0" width="600" class="w320" bgcolor="#2d95c1" style="background-color: #293333; border-collapse: collapse !important;">            <tbody><tr>                <td style="font-family: Arial, sans-serif;border-collapse: collapse;">                    <table cellspacing="0" cellpadding="0" class="force-full-width" style="border-collapse: collapse !important;width: 100% !important;">                        <tbody><tr>                            <td data-slot-container="1" style="text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            <div data-slot="image" data-param-padding-top="20" style="padding-top: 20px; padding-bottom: 30px;" data-param-padding-bottom="30"><a href="http://dailyjob.io" target="_blank" rel="noopener noreferrer"><img src="http://dailyjob.io/img-mailing/blanco-vertical.png" alt="An image" class="fr-view" style="width: 96px; height: 68.6377px;" /><br /></a><div style="clear:both"></div>                            </div>                            </td>                        </tr>                        <tr>                            <td data-slot-container="1" style="color: #f0f0f0;font-size: 14px;text-align: center;padding-bottom: 4px;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                                <div data-slot="text">© 2019 Todos los derechos reservados - <a data-bcup-haslogintext="no" href="mailto:soporte@dailyjob.io" style="color: #ffffff;">Contacto</a><br /><br /></div>                            </td>                        </tr>                        <tr>                            <td data-slot-container="1" style="color: #27aa90;font-size: 14px;text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            </td>                        </tr>                        <tr>                            <td style="font-size: 12px;font-family: Arial, sans-serif;border-collapse: collapse;">                            </td>                        </tr>                    </tbody></table>                </td>            </tr>        </tbody></table>    </center></div></body></html>'

        asunto = "[dailyjob] Has recibido una invitación para crear una cuenta"

        # connection = notifications.get_connection("smtp.gmail.com", "todos.yeboyebo@gmail.com", "555zapato", "465", "SSL")Zv3-hZx4NB2eurm
        connection = notifications.get_connection("smtp.zoho.com", "soporte@dailyjob.io", "060Sh8FLrYvs", "465", "SSL")
        response = notifications.sendMail(connection, "Soporte dailyjob<soporte@dailyjob.io>", asunto, cuerpo, [email])
        if not response:
            return False

        return True

    def yblogin_sass_getFilters(self, model, name, template=None):
        filters = []
        usuario = qsatype.FLUtil.nameUser()
        if name == 'usuariosCompania' and usuario != "admin":
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            return [{'criterio': 'idcompany__exact', 'valor': idcompany}]
        return filters


    def yblogin_sass_reenviar_invitacion(self, model, oParam):
        _i = self.iface
        response = {}
        if not _i.envioMailInvitacion(model.email, model.hashcode):
            return False
        response["resul"] = True
        response["msg"] = "Invitacion enviada con éxito"
        return response

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.yblogin_getDesc()

    def nueva_invitacion(self, oParam):
        return self.ctx.yblogin_sass_nueva_invitacion(oParam)

    def reenviar_invitacion(self, model, oParam):
        return self.ctx.yblogin_sass_reenviar_invitacion(model, oParam)

    def getFilters(self, model, name, template=None):
        return self.ctx.yblogin_sass_getFilters(model, name, template)

    def envioMailInvitacion(self, email, hashcode):
        return self.ctx.yblogin_sass_envioMailInvitacion(email, hashcode)


# @class_declaration head #
class head(yblogin_sass):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
