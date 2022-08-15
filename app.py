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
    st.sidebar.header('Chương trình phân tích ung thư da')
    st.sidebar.subheader('Chọn một trang để tiếp tục:')
    page = st.sidebar.selectbox("", ["Dữ liệu mẫu", "Tải lên hình ảnh của bạn"])

    if page == "Dữ liệu mẫu":
        st.header("Dự đoán dữ liệu mẫu về ung thư da")
        st.markdown("""
        **Bây giờ, đây có lẽ là lý do tại sao bạn đến đây. Hãy lấy cho bạn một số Dự đoán**

        Bạn cần chọn Dữ liệu mẫu
        """)

        mov_base = ['Dữ liệu mẫu 1']
        
        movies_chosen = st.multiselect('Chọn dữ liệu mẫu', mov_base)
        if len(movies_chosen) > 1:
            st.error('Vui lòng chọn Dữ liệu Mẫu')
        if len(movies_chosen) == 1:
            st.success("Bạn đã chọn Dữ liệu Mẫu")
        else:
            st.info('Vui lòng chọn Dữ liệu Mẫu')
        if len(movies_chosen) == 1:
            if st.checkbox('Hiển thị dữ liệu mẫu'):
                st.info("Hiển thị dữ liệu mẫu ---- >>>")
                image = load_mekd()
                st.image(image, caption='Sample Data', use_column_width=True)
                st.subheader("Chọn Thuật toán !")
                if st.checkbox('Keras'):
                    model = load_models()
                    st.success("Hoan hô !! Đã tải mô hình Keras!")
                    if st.checkbox('Hiển thị xác suất dự đoán của dữ liệu mẫu'):
                        x_test = data_gen(DATAPATH + '/ISIC_0024312.jpg')
                        y_new, Y_pred_classes = predict(x_test, model)
                        result = display_prediction(y_new)
                        st.write(result)
                        if st.checkbox('Biểu đồ xác suất hiển thị'):
                            fig = px.bar(result, x="Classes",
                                         y="Probability", color='Classes')
                            st.plotly_chart(fig, use_container_width=True)
        

       
     


    if page == "Tải lên hình ảnh của bạn":

        st.header("Tải lên hình ảnh của bạn")

        file_path = st.file_uploader('Tải lên một hình ảnh', type=['png', 'jpg'])

        if file_path is not None:
            x_test = data_gen(file_path)
            image = Image.open(file_path)
            img_array = np.array(image)

            st.success('Tải lên tệp thành công !!')
        else:
            st.info('Vui lòng tải lên tệp hình ảnh')

        if st.checkbox('Hiển thị hình ảnh đã tải lên'):
            st.info("Hiển thị hình ảnh đã tải lên ---- >>>")
            st.image(img_array, caption='Uploaded Image',
                     use_column_width=True)
            st.subheader("Chọn Thuật toán !")
            if st.checkbox('Keras'):
                model = load_models()
                st.success("Hoan hô !! Đã tải mô hình Keras!")
                if st.checkbox('Hiển thị xác suất dự đoán cho hình ảnh đã tải lên'):
                    y_new, Y_pred_classes = predict(x_test, model)
                    result = display_prediction(y_new)
                    st.write(result)
                    if st.checkbox('Biểu đồ xác suất hiển thị'):
                        fig = px.bar(result, x="Classes",
                                     y="Probability", color='Classes')
                        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
