import smtplib
import sys
import email
import importlib
from flask_cors import CORS
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
importlib.reload(sys)
sys.stdout.encoding

app = Flask(__name__)

# Cors:
CORS(app)

SENDER_EMAIL = 'danycarrillodeveloper@gmail.com'
SENDER_PASSWORD = 'Analista2455'

def create_success_data(data,code=None):
    response = {
    'data': data,
    'success': True,
    'code': code
    }
    return response

def create_error_data(data,code=None):
    response = {
    'data':data,
    'success':False,
    'code':code
    }
    return response

@app.route('/')
@app.route('/test', methods=['GET'])
def test():
    return jsonify(create_success_data({'msg':'Bienvenido API'},200))


def util_sendEmail_template(data):
    """
    Parametros: {"subject":"Consulta","to":"cliente@hotmail.com","sender_email":"danydeveloper@outlook.com","msg":"<html>","name":"Dany"}
    Descripcion: Funcion envia correo con template en html
    """
    try:
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = data['subject']
        mensaje['From'] = data['sender_email']
        mensaje['To'] = data['to']
        mensaje.attach(MIMEText(data['msg'],'html'))

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.ehlo()
        s.starttls()

        # Login Credentials for sending the mail
        s.login(SENDER_EMAIL, SENDER_PASSWORD)

        s.sendmail(data['sender_email'], data['to'], mensaje.as_string())
        s.close()
        return create_success_data({'msg':'Envio de correo exitoso'},200)
    except Exception as e:
        #return create_error_data({'msg':'Error en: '+str(e)},500)
        raise e

def util_sendEmail(data):
    """
    Parametros: {"subject":"Consulta","to":["dany_188_10@hotmail.com","danydeveloper@outlook.com"],"sender_email":"cliente@hotmail.com","msg":"texto","name":"Dany"}
    Descripcion: Funcion envia correo de texto plano
    """
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo() #identify computer
        mail.starttls() #transport layer security
        mail.login(SENDER_EMAIL, SENDER_PASSWORD)

        mensaje = MIMEText(data['msg_all'])
        mensaje["Subject"] = data['subject']

        mail.sendmail(
            data['sender_email'],
            data['to'],
            mensaje.as_string()
             )
        mail.close()

        return create_success_data({'msg':'Envio de correo exitoso'},200)

    except Exception as e:
        return create_error_data({'msg':'Error en: '+str(e)},500)

@app.route('/send',methods=['POST'])
def send():
    try:
        if not request.is_json:
            return jsonify(create_error_data({'msg':'Revisar los parametros'},400))
        data = request.get_json()
        print("data: ",data)
        data['msg_all'] = str(data['msg']) + '\n \n'+ str(data['name'])+'\n'+str(data['email'])
        print("msg: ",data['msg'])
        data['sender_email'] = data['msg_all']
        data['to'] = ['dany_188_10@hotmail.com','danydeveloper@outlook.com']
        send_to = util_sendEmail(data)
        if not send_to['success']:
            return jsonify(create_error_data(
                {'msg':'No se pudo enviar el correo, intente nuevamente.'},send_to['code'])
            )

        # Respuesta automatica con html
        datos = {
        'msg':"""
        <html>
        <body>
        <table id="all" style="font-family:sans-serif; margin:auto; width:850px">
            <tbody>
            <tr>
                <td>
                    <table id="company" style="width:850px">
                        <tbody>
                        <tr>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <p style="text-align: right;"><a style="text-decoration: none;" href="https://danycarrillo.herokuapp.com"><span
                                    style="color: #00657E;">danycarrillo.herokuapp.com</span></a>
                        </p>
                            </td>
                        </tr>
                        </tbody>
                    </table>

                    <!-- cabecera-->

                    <table id="m_3934484554991843377body" style="border-top:#25ABB9 3px solid; margin:auto; width:850px; padding-top: 15px; padding-bottom: 15px;">
                        <tbody>
                        <tr>
                            <td colspan="2" style="padding-top:30px; padding-bottom:30px;">
                                <p><span style="font-size:32px; color:#25ABB9"><strong>Envío de correo exitoso</strong></span></p>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="3" style="padding-left:15px; border-radius: 15px; padding-right:15px; background:#e9ecef; padding-bottom: 25px; padding-top: 20px; width: 850px;">
                                <p><img style="padding-right:15px;"alt="email" src="https://danycarrillo.herokuapp.com/img/redes/Email.svg" width="25" height="25"><span style="font-size:18px; color:#25ABB9; font-weight:600;">Hola:</span></p>
                                <p><span style="font-size:18px; padding-left:40px; color:#00657E;font-weight:bold;">"""+str(data['name'])+"""</span></p>
                            </td>
                        </tr>
                        <tr>
                            <td> &nbsp;</td>
                            <td> &nbsp;</td>
                        </tr>
                        <tr>
                     <!--informacion-BD-->
                            <td align="center">
                                <table>
                                    <tbody>
                                    <tr>
                                    </tr>
                                    <tr>
                                        <td> &nbsp;</td>
                                        <td> &nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td style="color:#3e3e3e; "><label>Esto es una respuesta automática para confirmarte que tu correo se envió correctamente. Dany Carrillo te respondará en cuanto revise tu correo.</label>
                                        </td>

                                    </tr>
                                   <tr>
                                    <td style=" color:#3e3e3e; "><label></label>
                                    </td>
                                   </tr>
                                   <tr>
                                    <td style=" color:#3e3e3e;"><label></label>
                                    </td>
                                   </tr>
                                    <tr>
                                    <td style="text-align:center; color:#3e3e3e;"><label><strong>Saludos,</strong></label>
                                    </td>
                                   </tr>
                                    <tr>
                                    <td style="text-align:center; color:#3e3e3e;"><label><strong>Dany Carrillo</strong></label>
                                    </td>
                                   </tr>
                                    </tbody>
                            </table>
                        </tr>
                    </table>
                </td>
                </td>
            </tr>
            <tr>
            </tbody>
        </table>


        <!-- redes-sociales -->
        <table style="background:#e9ecef; color:#00657E; margin:auto; width:850px;">
            <tbody>
            <tr id="links" style="font-family:sans-serif; padding-bottom: 20px; padding-top: 30px; padding-right: 50px; padding-left: 50px; background: #e9ecef; width:850px;">
                <td style="text-align: left; color: #00657E; font-size:14px; margin: auto; padding-right: 10px; padding-left: 20px; padding-top: 20px; padding-bottom: 20px;">Redes sociales:
                    <a href="#" style=" margin-left:30px; margin-right: 20px; text-decoration: none;" target="_blank">                      <img height="25" width="25"  alt="Facebook" src="https://danycarrillo.herokuapp.com/img/network/facebook-64px.png"></a>
                    <a href="#" style="margin-right: 20px; text-decoration: none;" target="_blank">                      <img height="25" width="25" alt="twitter" src="https://danycarrillo.herokuapp.com/img/network/twitter-64px.png"></a>
                    <a href="#" style="margin-right: 20px; text-decoration: none;" target="_blank">                           <img height="25" width="25"alt="instagram" src="https://danycarrillo.herokuapp.com/img/redes/instagram-mail.png"></a>
                    <a href="#" style="margin-right: 20px; text-decoration: none;" target="_blank">                      <img height="25" width="25" alt="youtube" src="https://danycarrillo.herokuapp.com/img/redes/youtube.png"></a>
                    <a href="#" style="margin-right: 40px; text-decoration: none;" target="_blank">                     <img height="25" width="25" alt="linkedin" src="https://danycarrillo.herokuapp.com/img/network/linkedin-64px.png"></a>
                    <a href="https://danycarrillo.herokuapp.com" style="text-decoration: none; color: #00657E;"><span style="border-left: #00657E solid 1px; padding-left: 40px; padding-top: 10px; padding-bottom: 10px;">danycarrillo.herokuapp.com</span></a>
                </td>
            </tr>
            </tbody>
        </table>


        <table id="RRSS" style="font-family:sans-serif;  border-botto: ;m-right-radius: 15px;  border-bottom-left-radius: 15px; padding-bottom: 30px; padding-top: 20px; padding-right: 65px; padding-left: 65px; background: #e9ecef; margin:auto; font-size:10px; width:850px;">
            <tbody>
            <tr>
            <tr>
                <td style="text-align: center; color: #00657E; padding-top:40px;">&#169; 2019 Dany Carrillo Todos los derechos reservados</td>
            </tr>

            </tbody>

        </table>
        </body>
        </html>
        """
        }
        datos['to'] = data['email']
        datos['sender_email'] = 'danydeveloper@outlook.com'
        datos['subject'] = 'Confirmación de envío de correo'
        resend_to = util_sendEmail_template(datos)
        if not resend_to['success']:
            return jsonify(create_error_data(
                {'msg':'No se pudo enviar el correo, intente nuevamente.'},resend_to['code'])
            )
        return jsonify(create_success_data({'msg':'Se envió el correo satisfactoriamente!'},200))
    except Exception as e:
        return jsonify(create_error_data({'msg':'[Error]: No se logro enviar el correo'+str(e)},500))


if __name__ == '__main__':
    app.run()