
# @class_declaration yblogin_sass #
from YBLEGACY.constantes import *
from models.fllogin.aqn_user import aqn_user
import hashlib
import re
from YBUTILS import notifications


class yblogin_sass(yblogin):

    def yblogin_sass_account(self, request):
        url = "/system/aqn_user/" + str(qsatype.FLUtil.nameUser())
        return HttpResponseRedirect(url)
        # return render(request, "portal/account.html", {"error": error, "usuario": request.user})

    def yblogin_sass_changepassword(self, request, error):
        email = qsatype.FLUtil.sqlSelect(u"aqn_user", u"email", u"idusuario = '" + str(request.user) + u"'")
        return render(request, "portal/account.html", {"error": error, "usuario": email})

    def yblogin_sass_changepasswordparam(self, request, email, error):
        return render(request, "portal/changePassword.html", {"error": error, "usuario": email})

    def yblogin_sass_auth_login(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)

            if action == "login":
                if username == "admin":
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login_auth(request, user)
                        accessControl.accessControl.registraAC()
                    else:
                        return self.iface.login(request, 'Error de autentificación')
                    return HttpResponseRedirect("/")

                usuario = aqn_user.objects.filter(email__exact=username)
                if len(usuario) == 0:
                    return self.iface.login(request, 'No existe el usuario')
                if usuario[0].activo is False:
                    return self.iface.login(request, 'No existe el usuario')
                md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                print("falla por aqui??", md5passwd, usuario[0].password)
                if usuario[0].password != md5passwd:
                    return self.iface.login(request, 'Error de autentificación')
                idusuario = usuario[0].idusuario
                user = authenticate(username=idusuario, password="ybllogin")
                if user is not None:
                    login_auth(request, user)
                else:
                    return self.iface.login(request, "Error de autentificación")
                accessControl.accessControl.registraAC()
                return HttpResponseRedirect("/")
        return self.iface.login(request)

    def yblogin_sass_signup_request(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)

            if action == "signup":
                if password == password2:
                    try:
                        usuario = aqn_user.objects.filter(usuario__exact=username)
                        if len(usuario) >= 1:
                            return self.iface.signup(request, "El usuario ya existe")
                        md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                        # qsatype.FLSqlQuery().execSql("INSERT INTO aqn_user(password, usuario, nombre, email) VALUES ('" + md5passwd + "', '" + username + "', '" + username + ", '" + username + ")")
                        idusuario_activo = qsatype.FLUtil.nameUser()
                        idcompania = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", u"idusuario = '" + idusuario_activo + u"'")
                        cursor = qsatype.FLSqlCursor(u"aqn_user")
                        cursor.setModeAccess(cursor.Insert)
                        cursor.refreshBuffer()
                        cursor.setValueBuffer(u"password", md5passwd)
                        cursor.setValueBuffer(u"usuario", username)
                        cursor.setValueBuffer(u"nombre", username)
                        cursor.setValueBuffer(u"email", username)
                        cursor.setValueBuffer(u"idcompania", idcompania)
                        cursor.setValueBuffer(u"activo", True)
                        # cursor = qsatype.FLSqlCursor(u"usuarios")
                        # cursor.setModeAccess(cursor.Insert)
                        # cursor.refreshBuffer()
                        # cursor.setValueBuffer(u"password", md5passwd)
                        # cursor.setValueBuffer(u"idusuario", username)
                        # cursor.setValueBuffer(u"nombre", username)
                        # cursor.setValueBuffer(u"email", username)
                        # cursor.setValueBuffer(u"utilizarsmtp", True)
                        print("como que null", cursor.valueBuffer("utilizarsmtp"))
                        # cursor.setValueBuffer(u"idcompania", idcompania)
                        if not cursor.commitBuffer():
                            return self.iface.signup(request, "Error no se puede crear usuario")
                        user = User.objects.create_user(username=cursor.valueBuffer("idusuario"), password="ybllogin", first_name=username)
                        user.save()
                        return self.iface.signup(request, username + " Añadido")
                    except Exception as exc:
                        print(exc)
                        return self.iface.signup(request, "El usuario ya existe")
                else:
                    return self.iface.signup(request, "Las contraseñas no coinciden")
        return self.iface.signup(request, "")

    def yblogin_sass_changepassword_request(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            oldpassword = request.POST.get("oldpassword", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)

            if action == "account":
                currentpassword = qsatype.FLUtil.sqlSelect(u"aqn_user", u"password", u"idusuario = '" + str(request.user.username) + u"'")
                if hashlib.md5(oldpassword.encode('utf-8')).hexdigest() != currentpassword:
                    return self.iface.changepassword(request, "Contraseña actual incorrecta")
                if password == password2:
                    try:
                        usuario = str(request.user.username)
                        # user = User.objects.get(username=usuario)
                        # user.set_password(str(password))
                        # user.save()
                        md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                        # cursor = qsatype.FLSqlCursor(u"usuarios")
                        cursor = qsatype.FLSqlCursor(u"aqn_user")
                        cursor.select("idusuario = '{}'".format(usuario))
                        if not cursor.first():
                            return self.iface.changepassword(request, "Error no se puede modificar contraseña")
                        cursor.setModeAccess(cursor.Edit)
                        cursor.refreshBuffer()
                        cursor.setValueBuffer(u"password", md5passwd)
                        if not cursor.commitBuffer():
                            return self.iface.changepassword(request, "Error no se puede modificar contraseña")
                        return HttpResponseRedirect("/login")
                    except Exception as exc:
                        print(exc)
                        return self.iface.changepassword(request, "Error inesperado consulte administrador")
                else:
                    return self.iface.changepassword(request, "Las contraseñas no coinciden")
        return self.iface.changepassword(request, "")

    def yblogin_sass_changepassword_request_param(self, request, hashparam):
        curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
        curInvitacion.select("hashcode = '{}'".format(hashparam))
        if not curInvitacion.first():
            return HttpResponseRedirect("/403")
        curInvitacion.setModeAccess(curInvitacion.Browse)
        curInvitacion.refreshBuffer()
        email = curInvitacion.valueBuffer("email")
        # idinvitation = cursor.valueBuffer("id")
        if request.method == "POST":
            action = request.POST.get("action", None)
            # username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)

            if action == "account":
                if password == password2:
                    try:
                        # usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", u"email = '" + str(email) + u"'")
                        md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                        # cursor = qsatype.FLSqlCursor(u"usuarios")
                        cursor = qsatype.FLSqlCursor(u"aqn_user")
                        cursor.select("email = '{}'".format(email))
                        if not cursor.first():
                            return self.iface.changepasswordparam(request, email, "Error no se puede modificar contraseña")
                        cursor.setModeAccess(cursor.Edit)
                        cursor.refreshBuffer()
                        cursor.setValueBuffer(u"password", md5passwd)
                        if not cursor.commitBuffer():
                            return self.iface.changepasswordparam(request, email, "Error no se puede modificar contraseña")
                        if not qsatype.FLUtil.sqlUpdate(u"aqn_invitations", u"activo", False, ustr(u"email = ", email)):
                            return False
                        return HttpResponseRedirect("/login")
                    except Exception as exc:
                        print(exc)
                        return self.iface.changepasswordparam(request, email, "Error inesperado consulte administrador")
                else:
                    return self.iface.changepasswordparam(request, email, "Las contraseñas no coinciden")
        return self.iface.changepasswordparam(request, email, "")


    def yblogin_sass_join_request(self, request, hashparam):
        cursor = qsatype.FLSqlCursor(u"aqn_invitations")
        cursor.select("hashcode = '{}'".format(hashparam))
        if not cursor.first():
            return HttpResponseRedirect("/403")
        cursor.setModeAccess(cursor.Browse)
        cursor.refreshBuffer()
        email = cursor.valueBuffer("email")
        idcompany = cursor.valueBuffer("idcompany")
        idinvitation = cursor.valueBuffer("id")

        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None)
            nombre = request.POST.get("nombre", None)
            apellidos = request.POST.get("apellidos", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)

            if action == "join":
                # Despues de crear usuario marcamos invitacion a false o borramos?
                if password == password2:
                    try:
                        md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                        usuario = aqn_user.objects.filter(usuario__exact=username)
                        if len(usuario) >= 1:
                            print("o por aqui")
                            return self.iface.join(request, email, "El usuario " + username + " ya existe")

                        q = qsatype.FLSqlQuery()
                        q.setTablesList(u"aqn_user")
                        q.setSelect(u"activo, usuario")
                        q.setFrom(u"aqn_user")
                        q.setWhere(u"email = '" + email + "'")
                        if not q.exec_():
                            return self.iface.join(request, email, "Error contacte con soporte")

                        if q.size() > 0:
                            while q.next():
                                if q.value(0):
                                    return self.iface.join(request, email, "El usuario " + email + " ya existe")
                                else:
                                    cursor = qsatype.FLSqlCursor(u"aqn_user")
                                    cursor.select(ustr("email = '", email, "'"))
                                    if cursor.first():
                                        cursor.setModeAccess(cursor.Edit)
                                        cursor.refreshBuffer()
                                        cursor.setValueBuffer(u"password", md5passwd)
                                        cursor.setValueBuffer(u"usuario", username)
                                        cursor.setValueBuffer(u"idcompany", idcompany)
                                        cursor.setValueBuffer(u"activo", True)
                                        if not cursor.commitBuffer():
                                            return self.iface.join(request, email, "Error no se puede crear usuario")
                                        if not qsatype.FLUtil.sqlUpdate(u"aqn_invitations", u"activo", False, ustr(u"id = ", idinvitation)):
                                            return False
                                        return self.iface.login(request, None, "Bienvenido a dailyjob")
                                        # return HttpResponseRedirect("/")
                                    else:
                                        return self.iface.join(request, email, "Error no se puede crear usuario")

                        # idusuario_activo = qsatype.FLUtil.nameUser()
                        # idcompania = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", u"idusuario = '" + idusuario_activo + u"'")
                        if not email:
                            return self.iface.join(request, email, "Falta email")
                        cursor = qsatype.FLSqlCursor(u"aqn_user")
                        cursor.setModeAccess(cursor.Insert)
                        cursor.refreshBuffer()
                        cursor.setValueBuffer(u"password", md5passwd)
                        cursor.setValueBuffer(u"usuario", username)
                        cursor.setValueBuffer(u"nombre", nombre)
                        cursor.setValueBuffer(u"apellidos", apellidos)
                        cursor.setValueBuffer(u"email", email)
                        cursor.setValueBuffer(u"idcompany", idcompany)
                        cursor.setValueBuffer(u"activo", True)
                        if not cursor.commitBuffer():
                            return self.iface.join(request, email, "Error no se puede crear usuario")
                        user = User.objects.create_user(username=cursor.valueBuffer("idusuario"), password="ybllogin", first_name=username)
                        user.save()
                        if not qsatype.FLUtil.sqlUpdate(u"aqn_invitations", u"activo", False, ustr(u"id = ", idinvitation)):
                            return False
                        return HttpResponseRedirect("/")
                        # return self.iface.login(request, None, "Bienvenido a dailyjob")
                        # return self.iface.join(request, email, username + " Añadido")
                    except Exception as exc:
                        print(exc)
                        return self.iface.join(request, email, "El usuario ya existe")
                else:
                    return self.iface.join(request, email, "Las contraseñas no coinciden")
        return self.iface.join(request, email, "")

    def yblogin_sass_join(self, request, email, error):
        username = request.POST.get("username", None) or ""
        nombre = request.POST.get("nombre", None) or ""
        apellidos = request.POST.get("apellidos", None) or ""

        return render(request, "portal/join.html", {"error": error, "email": email, "nombre": nombre, "apellidos": apellidos, "username": username})

    def yblogin_sass_cooperate_request(self, request, hashparam):
        cursor = qsatype.FLSqlCursor(u"aqn_invitations")
        cursor.select("hashcode = '{}'".format(hashparam))
        if not cursor.first():
            return HttpResponseRedirect("/403")
        cursor.setModeAccess(cursor.Browse)
        cursor.refreshBuffer()
        # email = cursor.valueBuffer("email")
        idcompany = cursor.valueBuffer("idcompany")
        idproyecto = cursor.valueBuffer("idproyecto")

        if request.method == "POST":
            idusuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", u"email = '" + str(cursor.valueBuffer("email")) + u"'")
            curPartic = qsatype.FLSqlCursor("gt_particproyecto")
            curPartic.select("idusuario = '{}' AND idproyecto = '{}'".format(idusuario, str(idproyecto)))
            curPartic.refreshBuffer()
            if curPartic.first():
                return HttpResponseRedirect("/")
            curPartic.setModeAccess(curPartic.Insert)
            curPartic.refreshBuffer()
            curPartic.setValueBuffer("idusuario", idusuario)
            curPartic.setValueBuffer("idproyecto", idproyecto)
            if not curPartic.commitBuffer():
                return HttpResponseRedirect("/")

            if not qsatype.FLUtil.sqlUpdate(u"aqn_invitations", u"activo", False, ustr(u"id = '", str(cursor.valueBuffer("id")), "'")):
                return False
            return HttpResponseRedirect("/")
        return self.iface.cooperate(request, idproyecto, idcompany)

    def yblogin_sass_cooperate(self, request, idproyecto, idcompany):
        nombreEmpresa = qsatype.FLUtil.sqlSelect(u"aqn_companies", u"nombre", u"idcompany = '" + str(idcompany) + u"'")
        nombreProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", u"idproyecto = '" + str(idproyecto) + u"'")
        return render(request, "portal/cooperate.html", {"error": "", "nombreEmpresa": nombreEmpresa, "nombreProyecto": nombreProyecto})

    def yblogin_sass_forgetPassword_request(self, request):
        email = request.POST.get("email", None)
        if request.method == "POST":
            if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower()):
                return render(request, "portal/forgetPassword.html", {"error": "Formato email incorrecto"})
            username = qsatype.FLUtil.sqlSelect(u"aqn_user", u"usuario", u"email = '" + str(email) + u"'")
            hashcode = hashlib.md5(email.encode('utf-8')).hexdigest()
            curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
            curInvitacion.setModeAccess(curInvitacion.Insert)
            curInvitacion.refreshBuffer()
            curInvitacion.setValueBuffer(u"email", email)
            curInvitacion.setValueBuffer(u"hashcode", hashcode)
            curInvitacion.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
            curInvitacion.setValueBuffer(u"activo", True)
            curInvitacion.setValueBuffer(u"tipo", "cp")
            if not curInvitacion.commitBuffer():
                return False
            urlJoin = "https://app.dailyjob.io/changepassword/" + hashcode
            # urlJoin = "http://127.0.0.1:8000/changepassword/" + hashcode
            # cuerpo = "<img src='https://app.dailyjob.io/static/dist/img/logo/logo.png'/>"
            # cuerpo += "<br><a href='" + urlJoin + "''>Unirse DailyJob</a>"
            # cuerpo += "<br>"
            cuerpo = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" style="" class=" js flexbox flexboxlegacy canvas canvastext webgl no-touch geolocation postmessage websqldatabase indexeddb hashchange history draganddrop websockets rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface generatedcontent video audio localstorage sessionstorage webworkers no-applicationcache svg inlinesvg smil svgclippaths js csstransforms csstransforms3d csstransitions responsejs "><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Invitación Dailyjob</title><!-- Designed by https://github.com/kaytcat --><!-- Header image designed by Freepik.com --><style type="text/css">/* Take care of image borders and formatting */img { max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img { border: none; }table { border-collapse: collapse !important; }#outlook a { padding:0; }.ReadMsgBody { width: 100%; }.ExternalClass {width:100%;}.backgroundTable {margin:0 auto; padding:0; width:100% !important;}table td {border-collapse: collapse;}.ExternalClass * {line-height: 115%;}/* General styling */td {    font-family: Arial, sans-serif;}body {    -webkit-font-smoothing:antialiased;    -webkit-text-size-adjust:none;    width: 100%;    height: 100%;    color: #6f6f6f;    font-weight: 400;    font-size: 18px;}h1 {    margin: 10px 0;}a {    color: #27aa90;    text-decoration: none;}.force-full-width {    width: 100% !important;}.body-padding {    padding: 0 75px;}</style><style type="text/css" media="screen">        @media screen {            @import url(https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);            /* Thanks Outlook 2013! */            body {                font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;            }            .w280 {                width: 280px !important;            }        }</style><style type="text/css" media="only screen and (max-width: 480px)">    /* Mobile styles */    @media only screen and (max-width: 480px) {        table[class*="w320"] {            width: 320px !important;        }        td[class*="w320"] {            width: 280px !important;            padding-left: 20px !important;            padding-right: 20px !important;        }        img[class*="w320"] {            width: 250px !important;            height: 67px !important;        }        td[class*="mobile-spacing"] {            padding-top: 10px !important;            padding-bottom: 10px !important;        }        *[class*="mobile-hide"] {            display: none !important;        }        *[class*="mobile-br"] {            font-size: 12px !important;        }        td[class*="mobile-w20"] {            width: 20px !important;        }        img[class*="mobile-w20"] {            width: 20px !important;        }        td[class*="mobile-center"] {            text-align: center !important;        }        table[class*="w100p"] {            width: 100% !important;        }        td[class*="activate-now"] {            padding-right: 0 !important;            padding-top: 20px !important;        }        [class="mobile-block"] {            width: 100% !important;            display: block !important;        }    }</style>                                  </head><body offset="0" class="body ui-sortable" style="padding: 0px; margin: 0px; display: block; background: rgb(238, 235, 235); text-size-adjust: none; -webkit-font-smoothing: antialiased; width: 100%; height: 100%; color: rgb(111, 111, 111); font-weight: 400; font-size: 18px; cursor: auto; overflow: visible;" bgcolor="#eeebeb"><div data-section-wrapper="=" 1""="" align="center" valign="top" style="font-family: Arial, sans-serif;border-collapse: collapse;">    <center>        <table data-section="1" style="margin: 0px auto; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" cellspacing="0" cellpadding="0" width="600" class="w320" bgcolor="#ffffff">            <tbody><tr>                <td data-slot-container="1" style="text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                    <div data-slot="image" data-param-padding-top="50" data-param-padding-bottom="50" style="padding-top: 50px; padding-bottom: 25px;">                        <a href="http://dailyjob.io" target="_blank" rel="noopener noreferrer"><img class="w320 fr-view" width="311" height="83" src="http://dailyjob.io/img-mailing/color-horizontal.png" alt="company logo" style="max-width: 600px; outline: none; text-decoration: none; border: none; width: 394px; height: 96px;" /><br /></a>                    </div>                </td>            </tr>        </tbody></table>    </center></div><div data-section-wrapper="=" 1""="">    <center>        <table data-section="1" cellspacing="0" cellpadding="0" width="600" class="w320" style="background-color: rgb(255, 255, 255); border-collapse: collapse !important;" bgcolor="#ffffff">            <tbody><tr>                <td style="font-family: Arial, sans-serif;border-collapse: collapse;">                    <table cellspacing="0" cellpadding="0" width="100%" style="border-collapse: collapse !important;">                        <tbody><tr>                            <td data-slot-container="1" style="font-size: 18px;font-weight: 600;color: #ffffff;text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="mobile-spacing ui-sortable">                            <div data-slot="text" data-param-padding-top="" style="padding-top: 0px; padding-bottom: 20px;" data-param-padding-bottom=""><div style="padding: 20px 10%;"><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">¡Hola! <strong><span style="color: #2d95c1;">' + username + ' </span></strong></span></span></div><div style="text-align: justify;"><br /></div><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">Si has solicitado un cambio de contraseña, pulsa en el siguiente enlace o cópialo directamente en el navegador</span></strong></span></div><div style="text-align: justify;"><br /></div><div style="padding: 20px 10%;"><span style="font-size: 18px;"><span style="color: #2d95c1;"><a href="' + urlJoin + '">' + urlJoin + '</a></span></span></div><br/><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">En caso contrario, ignora este mensaje</span></span></div></div><br /></div><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;"></span></strong></span></div></td>                        </tr>                        <tr>                            <td data-slot-container="1" style="font-size: 24px;text-align: center;padding: 0 75px;color: #6f6f6f;font-family: Arial, sans-serif;border-collapse: collapse;" class="w320 mobile-spacing ui-sortable">                            </td>                        </tr>                    </tbody></table>                    <table cellspacing="0" cellpadding="0" width="100%" style="border-collapse: collapse !important;">                        <tbody><tr>                            <td data-slot-container="1" style="font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            </td>                        </tr>                    </tbody></table>                </td>            </tr>        </tbody></table>    </center></div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0px auto; width: 600px; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" class="w320" cellpadding="0" cellspacing="0" width="600" bgcolor="#ffffff">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column" bgcolor="#ffffff" style="background-color: rgb(255, 255, 255);">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0px auto; width: 600px; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" class="w320" cellpadding="0" cellspacing="0" width="600" bgcolor="#ffffff">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0 auto;border-collapse: collapse !important;width: 600px;" class="w320" cellpadding="0" cellspacing="0" width="600">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0 auto;border-collapse: collapse !important;width: 600px;" class="w320" cellpadding="0" cellspacing="0" width="600">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="=" 1""="">    <center>        <table data-section="1" cellspacing="0" cellpadding="0" width="600" class="w320" bgcolor="#2d95c1" style="background-color: #293333; border-collapse: collapse !important;">            <tbody><tr>                <td style="font-family: Arial, sans-serif;border-collapse: collapse;">                    <table cellspacing="0" cellpadding="0" class="force-full-width" style="border-collapse: collapse !important;width: 100% !important;">                        <tbody><tr>                            <td data-slot-container="1" style="text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            <div data-slot="image" data-param-padding-top="20" style="padding-top: 20px; padding-bottom: 30px;" data-param-padding-bottom="30"><a href="http://dailyjob.io" target="_blank" rel="noopener noreferrer"><img src="http://dailyjob.io/img-mailing/blanco-vertical.png" alt="An image" class="fr-view" style="width: 96px; height: 68.6377px;" /><br /></a><div style="clear:both"></div>                            </div>                            </td>                        </tr>                        <tr>                            <td data-slot-container="1" style="color: #f0f0f0;font-size: 14px;text-align: center;padding-bottom: 4px;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                                <div data-slot="text">© 2019 Todos los derechos reservados - <a data-bcup-haslogintext="no" href="mailto:soporte@dailyjob.io" style="color: #ffffff;">Contacto</a><br /><br /></div>                            </td>                        </tr>                        <tr>                            <td data-slot-container="1" style="color: #27aa90;font-size: 14px;text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            </td>                        </tr>                        <tr>                            <td style="font-size: 12px;font-family: Arial, sans-serif;border-collapse: collapse;">                            </td>                        </tr>                    </tbody></table>                </td>            </tr>        </tbody></table>    </center></div></body></html>'

            asunto = "[dailyjob] Reestablecer contraseña"

            # connection = notifications.get_connection("smtp.gmail.com", "todos.yeboyebo@gmail.com", "555zapato", "465", "SSL")Zv3-hZx4NB2eurm
            connection = notifications.get_connection("smtp.zoho.com", "soporte@dailyjob.io", "I7c5uXGnNuee", "465", "SSL")
            response = notifications.sendMail(connection, "Soporte dailyjob<soporte@dailyjob.io>", asunto, cuerpo, [email])
            if not response:
                return render(request, "portal/forgetPassword.html", {"error": "No se pudo enviar el email"})
            return HttpResponseRedirect("/")
            # return self.iface.login(request, None, "Correcto, revisa tu correo")
        return render(request, "portal/forgetPassword.html", {"error": ""})


    def __init__(self, context=None):
        super().__init__(context)

    @decoradores.check_authentication_iface
    def account(self, request):
        return self.iface.yblogin_sass_account(request)

    @decoradores.check_authentication_iface
    def changepassword(self, request, error):
        return self.iface.yblogin_sass_changepassword(request, error)

    def changepasswordparam(self, request, email, error):
        return self.iface.yblogin_sass_changepasswordparam(request, email, error)

    def auth_login(self, request):
        return self.iface.yblogin_sass_auth_login(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def signup_request(self, request):
        return self.iface.yblogin_sass_signup_request(request)

    @decoradores.check_authentication_iface
    def changepassword_request(self, request):
        return self.iface.yblogin_sass_changepassword_request(request)

    def changepassword_request_param(self, request, hashparam):
        return self.iface.yblogin_sass_changepassword_request_param(request, hashparam)

    def join_request(self, request, hashparam):
        return self.iface.yblogin_sass_join_request(request, hashparam)

    def cooperate_request(self, request, hashparam):
        return self.iface.yblogin_sass_cooperate_request(request, hashparam)

    def cooperate(self, request, idproyecto, idcompany):
        return self.iface.yblogin_sass_cooperate(request, idproyecto, idcompany)

    def join(self, request, email, error):
        return self.iface.yblogin_sass_join(request, email, error)

    def forgetPassword_request(self, request):
        return self.iface.yblogin_sass_forgetPassword_request(request)

