import os

from flask import Flask, render_template, session, request, redirect, url_for, jsonify , make_response
from flask_session import Session
import time
app = Flask(__name__)



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")



@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

'''
@app.route("/project")
def project():
    return render_template("project.html")

@app.route("/achievements")
def achievements():
    return render_template("achievements.html")
@app.route("/current")
def current():
    return render_template("current.html")



from fastai.vision import *
import numpy as np
from PIL import Image



@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
  response = make_response(open('sitemap.xml').read())
  response.headers["Content-type"] = 'application/xml'
  return response

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/error.html', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('error.html')
    return Response(content, mimetype="text/html")

@app.route("/model", methods=["GET", "POST"])
def model():
    if request.method == "POST":
        try:
            if request.files:
                learn = load_learner("model0")

                #removing filess
                try:
                    for i in os.listdir("upload"):
                        try:
                            a = int(i[-10:-4])
                        except Exception as e:
                            print(99, e)
                            print(i)
                            continue
                        if time.time()%(10**6) - int(i[-10:-4]) > 10:
                            os.remove("upload/" + i)
                            print("69 removing " + "upload/" + i, time.time()%(10**6) , int(i[-10:-4]))
                        else:
                            print(time.time(), i)
                    for i in os.listdir("static/dump"):
                        try:
                            a = int(i[-10:-4])
                        except Exception as e:
                            print(111, e, i)
                            continue
                        if time.time()%(10**6) - int(i[-10:-4]) > 20:
                            os.remove("static/dump/" + i)
                            print("73 removing " + "static/dump/" + i ,time.time()%(10**6) ,  int(i[-10:-4]))
                except Exception as error:
                    print("78", error)
                    pass


                #removing files ended


                for i in os.listdir("static/dump"):
                    os.remove("static/dump/"+i)

                uniqe = uuid.uuid1()

                try:
                    image = request.files["image"]
                    savepath = "upload/" + str(uniqe)+ str(int(time.time()))[-6:] +  ".jpg"
                    image.save(savepath)
                    print("116: file saved at ", savepath)

                    path = savepath
                    print("120", image.filename,"upload/")
                    img = open_image(image)
                    print("122: file opened")
                    peeb = img.apply_tfms([crop_pad()], size=256, resize_method=ResizeMethod.SQUISH, padding_mode='zeros')
                    print(c)
                except Exception as error:
                    print(error, "okay")
                try:
                    model = learn.predict(peeb, return_x = True)
                except Exception as error:
                    print(error)
                pos = int(np.argmax(model[3]))


                th = 0.88
                temp = float(model[3][pos])
                if temp == th:
                     pred = 0.5
                elif temp < th:
                    pred = float(temp/th) * 0.5
                else:
                    pred = 0.5 + float((temp - th)/(1 - th))*0.5

                message = "Covid-19: " + str(round(100*pred,2)) + "%"


                try:
                    pathOutputImage = f'static/dump/{uniqe}' + str(int(time.time()))[-6:] +'.jpg'

                    h = HeatmapGenerator("disease/model_ones_3epoch_densenet.tar", nnClassCount, imgtransCrop)
                except Exception as error:
                    print("134",error)
                try:
                    q = h.generate(path, pathOutputImage, imgtransCrop)
                except Exception as error:
                    print("138",error)
                message1 = []

                for i in range(len(class_names)):
                    data = [class_names[i]]
                    temp = float(q[0][i])
                    #model change
                    th = class_threshold[i]/100
                    if temp == th:
                         pred = 0.5
                    elif temp < th:
                        pred = float(temp/th) * 0.5
                    else:
                        pred = 0.5 + float((temp - th)/(1 - th))*0.5

                    #pred = float(q[0][i])
                    try:
                        if pred > 0.5 and i == 7:  #pneumonia > 0.5 true
                            ans = "True"
                        elif pred > 0.55 and i != 0:  #any diseases > 0.55 true
                            ans = "True"
                        elif pred > 0.6:              #normal lung > 0.6 True, False for green
                            ans = "False"
                        elif pred < 0.45 and i != 0:              #if any
                            ans = "False"
                        elif pred < 0.45:
                            ans = "True"
                        elif i == 0:
                            ans = "False"
                        else:
                            ans = "Check up if possible"
                    except Exception as error:
                        print(error)
                    #message1.append(class_names[i] + ": " + str(round(100*pred,2)) )
                    #message1.append(class_names[i] + ": " + ans )
                    #message1.append()
                    data.append(ans)
                    data.append(str(round(pred*100,2))+"%")
                    message1.append(data)

                #removed prob display


                if message1[0][1] == "True":
                    for i in message1[1:]:
                        if "True" in i:
                            i[1] = "Check up highly recommended"




                file_handle = open(pathOutputImage, 'r')



                return render_template("model0.html", message = message, message1 = message1, source = pathOutputImage )


            else:
                return render_template("model0.html")
        except Exception as e:
            print(232,e)
            return render_template("model0.html")


    return render_template("model0.html")

def email_send(text, email="sambhav2003gupta@gmail.com"):

    sending given text to given email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("autofunproject@gmail.com", "sambhavgupta")
    message = """Subject: OTP for changing password

    Website: %s
    """ %(text)

    server.sendmail(
      "autofunproject@gmail.com",
      email,
      message)
    print("sent mail at ", email)
    server.quit()

if "__name__" == "__main__":
    learn = load_learner("model")

    learnai = load_learner('disease','export.pkl')



64626
<0,1,1,0,0,0,00,...,1>
model 1: model_zeroes_1epoch_densenet.pth.tar <1,0,1*,0,0,0,0,....1>
model2 : model_ones_3epoch_densenet.tar  <1,0*,1,0,,0,0,,0,1>


64556
<1,0,0,0,0,0,>
model1: <1,0,0,0,1**,0,0,0,0,0,0,1**,0)
model2: <1,1**,0,0,0,0,0,00,0,00,1**,0)

'''
