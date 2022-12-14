import streamlit as st
import numpy as np
import pandas as pd
import keras
from keras.utils.np_utils import to_categorical
from keras.models import Sequential, load_model
from keras import backend as K
import os
import time
import io
from PIL import Image
import plotly.express as px
from tensorflow import keras
model = keras.models.load_model('path/to/location')

MODELSPATH = './models/'
DATAPATH = './data/'


def render_header():
    st.write("""
        <p align="center"> 
            <H1> Skin cancer Analyzer 
        </p>

    """, unsafe_allow_html=True)


@st.cache
def load_mekd():
    img = Image.open(DATAPATH + '/ISIC_0024312.jpg')
    
    return img


@st.cache
def data_gen(x):
    img = np.asarray(Image.open(x).resize((100, 75)))
    x_test = np.asarray(img.tolist())
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    x_validate = x_test.reshape(1, 75, 100, 3)

    return x_validate


@st.cache
def data_gen_(img):
    img = img.reshape(100, 75)
    x_test = np.asarray(img.tolist())
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    x_validate = x_test.reshape(136,415,664)

    return x_validate


def load_models():

    model = load_model(MODELSPATH + 'model.h5')
    return model


@st.cache
def predict(x_test, model):
    Y_pred = model.predict(x_test)
    ynew = model.predict(x_test)
    K.clear_session()
    ynew = np.round(ynew, 2)
    ynew = ynew*100
    y_new = ynew[0].tolist()
    Y_pred_classes = np.argmax(Y_pred, axis=1)
    K.clear_session()
    return y_new, Y_pred_classes


@st.cache
def display_prediction(y_new):
    """Display image and preditions from model"""

    result = pd.DataFrame({'Probability': y_new}, index=np.arange(7))
    result = result.reset_index()
    result.columns = ['Classes', 'Probability']
    lesion_type_dict = {2: 'Benign keratosis-like lesions', 4: 'Melanocytic nevi', 3: 'Dermatofibroma',
                        5: 'Melanoma', 6: 'Vascular lesions', 1: 'Basal cell carcinoma', 0: 'Actinic keratoses'}
    result["Classes"] = result["Classes"].map(lesion_type_dict)
    return result


def main():
    st.sidebar.header('Ch????ng tr??nh ph??n t??ch ung th?? da')
    st.sidebar.subheader('Ch???n m???t trang ????? ti???p t???c:')
    page = st.sidebar.selectbox("", ["D??? li???u m???u", "T???i l??n h??nh ???nh c???a b???n"])

    if page == "D??? li???u m???u":
        st.header("D??? ??o??n d??? li???u m???u v??? ung th?? da")
        st.markdown("""
        **B??y gi???, ????y c?? l??? l?? l?? do t???i sao b???n ?????n ????y. H??y l???y cho b???n m???t s??? D??? ??o??n**

        B???n c???n ch???n D??? li???u m???u
        """)

        mov_base = ['D??? li???u m???u 1']
        
        movies_chosen = st.multiselect('Ch???n d??? li???u m???u', mov_base)
        if len(movies_chosen) > 1:
            st.error('Vui l??ng ch???n D??? li???u M???u')
        if len(movies_chosen) == 1:
            st.success("B???n ???? ch???n D??? li???u M???u")
        else:
            st.info('Vui l??ng ch???n D??? li???u M???u')
        if len(movies_chosen) == 1:
            if st.checkbox('Hi???n th??? d??? li???u m???u'):
                st.info("Hi???n th??? d??? li???u m???u ---- >>>")
                image = load_mekd()
                st.image(image, caption='Sample Data', use_column_width=True)
                st.subheader("Ch???n Thu???t to??n !")
                if st.checkbox('Keras'):
                    model = load_models()
                    st.success("Hoan h?? !! ???? t???i m?? h??nh Keras!")
                    if st.checkbox('Hi???n th??? x??c su???t d??? ??o??n c???a d??? li???u m???u'):
                        x_test = data_gen(DATAPATH + '/ISIC_0024312.jpg')
                        y_new, Y_pred_classes = predict(x_test, model)
                        result = display_prediction(y_new)
                        st.write(result)
                        if st.checkbox('Bi???u ????? x??c su???t hi???n th???'):
                            fig = px.bar(result, x="Classes",
                                         y="Probability", color='Classes')
                            st.plotly_chart(fig, use_container_width=True)
        

       
     


    if page == "T???i l??n h??nh ???nh c???a b???n":

        st.header("T???i l??n h??nh ???nh c???a b???n")

        file_path = st.file_uploader('T???i l??n m???t h??nh ???nh', type=['png', 'jpg'])

        if file_path is not None:
            x_test = data_gen(file_path)
            image = Image.open(file_path)
            img_array = np.array(image)

            st.success('T???i l??n t???p th??nh c??ng !!')
        else:
            st.info('Vui l??ng t???i l??n t???p h??nh ???nh')

        if st.checkbox('Hi???n th??? h??nh ???nh ???? t???i l??n'):
            st.info("Hi???n th??? h??nh ???nh ???? t???i l??n ---- >>>")
            st.image(img_array, caption='Uploaded Image',
                     use_column_width=True)
            st.subheader("Ch???n Thu???t to??n !")
            if st.checkbox('Keras'):
                model = load_models()
                st.success("Hoan h?? !! ???? t???i m?? h??nh Keras!")
                if st.checkbox('Hi???n th??? x??c su???t d??? ??o??n cho h??nh ???nh ???? t???i l??n'):
                    y_new, Y_pred_classes = predict(x_test, model)
                    result = display_prediction(y_new)
                    st.write(result)
                    if st.checkbox('Bi???u ????? x??c su???t hi???n th???'):
                        fig = px.bar(result, x="Classes",
                                     y="Probability", color='Classes')
                        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
