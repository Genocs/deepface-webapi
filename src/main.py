import io
from deepface import DeepFace
from PIL import Image
import os
from flask import Flask, request, jsonify
import base64
import logging

# from flask import render_template

# PRODUCTION
# from gevent.pywsgi import WSGIServer


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = Flask(__name__)

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace",
          "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
metrics = ["cosine", "euclidean", "euclidean_l2"]
backends = ['opencv', 'ssd', 'mtcnn', 'retinaface', 'mediapipe']

model = models[0]  # VGG-Face
metric = metrics[0]  # cosine
backend = backends[3]  # retinaface


def setup_logger(name='rabbitmq_client', log_file='app.log', level=logging.INFO):
    """
    Logger setup
    """
    # add logging to file
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(levelname)-8s %(message)s', level=level)

    # add logging to console
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
    console.setLevel(level)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    # logging.getLogger('').addHandler(logging.FileHandler(log_file))


def get_image_from_base64(base64_img: str):
    """
    Extract image from base64 string
    """

    try:
        # decode base64 string data
        imgdata = base64.b64decode(str(base64_img))
        image = Image.open(io.BytesIO(imgdata))
    except:
        image = None

    return image

def get_face_ambeddings(img: any, model, detector):
    """
    Return the embedding
    """

    try:
        embedding = DeepFace.represent(img_path=img, model_name=model, detector_backend=detector)
        return embedding
    except:
        logging.error()

    return ''

def face_verification(img1, img2, dist, model, detector):
    """
    Check the similarity of 2 images
    """

    try:
        result = DeepFace.verify(img1_path=img1, img2_path=img2,
                                 distance_metric=dist, model_name=model, detector_backend=detector)
    except:
        result = DeepFace.verify(img1_path=img1, img2_path=img2, distance_metric=dist, model_name=model, detector_backend=detector,
                                 enforce_detection=False)

    return result['verified'].astype(str), round(result['distance'], 4), result['threshold'], result['model'],


def facial_analysis(img1, detector):
    """
    Determine emotion, race, gender and age from models
    """

    try:
        # facial analysis
        obj = DeepFace.analyze(img_path=img1, actions=[
                               'age', 'gender', 'race', 'emotion'], detector_backend=detector)
    except:
        obj = DeepFace.analyze(img_path=img1, actions=['age', 'gender', 'race', 'emotion'], detector_backend=detector,
                               enforce_detection=False)

        print(obj)

    return obj[0]['age'], obj[0]['dominant_gender'], obj[0]['dominant_race'], obj[0]['dominant_emotion']


def face_recognition(img1, dir_loc, model, dist, detector):
    """
    Facial recognition given a database or folder location with images
    """

    # face recognition
    rec = DeepFace.find(img_path=img1, db_path=dir_loc,
                        distance_metric=dist, model_name=model, detector_backend=detector)
    return rec


@app.route('/')
def hello():
    return 'Genocs DeepFece WebApi built with Flask!'


@app.route('/hc', methods=['GET'])
def health_check():
    return 'healthy'


@app.route('/face_match', methods=['POST'])
def compare_json():
    """
    This API endpoint is used to compare 2 images and return the similarity score
    """

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json

        img_1 = data['first_image']
        img_2 = data['second_image']

        if img_1 is None or img_2 is None:
            return jsonify({'error': 'invalid image'}), 400

        verification_info = face_verification(
            img_1, img_2, metric, model, backend)
        return jsonify({'verified': verification_info[0],
                        'distance': verification_info[1],
                        'threshold': verification_info[2],
                        'model': verification_info[3]}), 200

    else:
        return "Content type is not supported."

def main():
    """
    The main function
    """
    setup_logger()

    logging.info('*************************************')
    logging.info('Deep Face Web API Warm up!')
    logging.info('*************************************')

    # read configuration from environment file
    dotenv_path = os.path.join(os.path.dirname(__file__), '../cloud.env')
    if os.path.exists(dotenv_path):
        logging.info('Reading configuration from environment file')
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)

    # Debug/Development
    # Run flash server 
    app.run(debug=True, host='0.0.0.0', port=5400)

    # Production
    # http_server = WSGIServer(('', 5400), app)
    # http_server.serve_forever()    


"""
The entry point
Warning: Use 0.0.0.0 instead of 127.0.0.1 to avoid issue when use docker container   
"""
if __name__ == '__main__':
    main()
